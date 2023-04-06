from __future__ import annotations

from copy import copy, deepcopy
from typing import List, Tuple, Dict

from krr_system.utils import fuzzy_eq, fuzzy_and


class Fluent:
    def __init__(self, **fluents):
        for name, value in fluents.items():
            assert (isinstance(name, str))
            self.name = name
            self.value = value
            break  # only the first value is processed

    # for if statements
    def __bool__(self):
        return self.value

    # for ==, != comparisons
    def __eq__(self, other):
        if isinstance(other, bool) or other is None:
            return fuzzy_eq(self.value, other)
        elif isinstance(other, Fluent):
            return fuzzy_and(fuzzy_eq(self.value, other.value), self.name == other.name)
        else:
            return False

    def __repr__(self):
        return f"{self.name}={self.value}"


class DomainDescription:

    def __init__(self):

        self.fluents: Dict[str, Fluent] = dict()
        self._causes: Dict[str, List[Tuple[List[Fluent], List[Fluent]]]] = dict()
        self.impossibles: Dict[str, List[List[Fluent]]] = dict()

    def state(self):
        return [(f.name, f.value) for f in self.fluents.values()]

    def copy(self):
        return deepcopy(self)

    def _check_if_known(self, fluents: List[Fluent], default_value=None):
        if isinstance(fluents, Fluent):
            fluents = [fluents]
        for fluent in fluents:
            if fluent.name not in self.fluents:
                assumed_fluent = copy(fluent)
                assumed_fluent.value = default_value
                self.fluents[fluent.name] = assumed_fluent

    def _set(self, fluents: List[Fluent] | Fluent):
        if isinstance(fluents, Fluent):
            fluents = [fluents]
        for fluent in fluents:
            self.fluents[fluent.name] = fluent

    def _check(self, conditions: List[Fluent]) -> bool | None:
        """Checks a single list of fluent requirements"""
        if conditions is None:
            return True

        conditions_met = []
        for f in conditions:
            if f.name not in self.fluents:
                return False  # maybe should be None

            conditions_met.append(f == self.fluents[f.name])

        if False in conditions_met:
            return False
        if None in conditions_met:
            return None
        return True

    def _possible(self, action: str) -> bool | None:
        """Checks a list of lists of fluent requirements"""
        if action not in self.impossibles:
            return True

        conditions_met = [self._check(conditions) for conditions in self.impossibles[action]]

        if True in conditions_met:
            return False
        if None in conditions_met:
            return None
        return True

    def _do(self, fluents: List[Fluent], conditions_met: bool | None, possible: bool | None) -> bool | None:
        """
        Sets fluents to values specified in fluents variable if action possible and conditions_met
        if conditions met is None, set the difference between current fluents and new ones to None
        """

        if conditions_met is False:
            return False

        # at this stage both possible and conditions_met are either None or True
        diff: List[Fluent] = []
        for fluent in fluents:
            # check the possible changes in fluents
            if (self.fluents[fluent.name] == fluent) is not True:  # so if any change happens
                diff.append(fluent)

        if conditions_met is None or possible is None:
            diff = [copy(f) for f in diff]
            for fluent in diff:
                fluent.value = None
        self._set(diff)

    def do_action(self, action_name: str, *args, **kwargs):
        possible = self._possible(action_name)
        if possible is False:
            return False

        for to_set, conditions in self._causes[action_name]:
            self._do(to_set, self._check(conditions), possible)
        return True

    def _add_action(self, action_name: str, fluents: List[Fluent] | Fluent, conditions: List[Fluent] | Fluent | None):
        if action_name not in self._causes:
            self._causes[action_name] = []
            setattr(self.__class__, action_name, lambda x: x.do_action(action_name))

        self._causes[action_name].append((fluents, conditions))

    def initially(self, **kwargs):
        for key, value in kwargs.items():
            self.fluents[key] = Fluent(**{key: value})

    def impossible(self, action: str, conditions: List[Fluent] | Fluent):
        if isinstance(conditions, Fluent):
            conditions = [conditions]
        if action not in self.impossibles:
            self.impossibles[action] = []

        self.impossibles[action].append(conditions)

    def causes(self, action: str, fluents: List[Fluent] | Fluent, conditions: List[Fluent] | Fluent | None = None):
        if isinstance(fluents, Fluent):
            fluents = [fluents]
        if isinstance(conditions, Fluent):
            conditions = [conditions]

        self._check_if_known(fluents)
        self._add_action(action, fluents, conditions)

    def releases(self, action: str, fluents: List[Fluent] | Fluent):
        if isinstance(fluents, Fluent):
            fluents = [fluents]

        for fluent in fluents:
            fluent.value = None

        self._check_if_known(fluents)
        self._add_action(action, fluents, None)


class TimeDomainDescription(DomainDescription):

    def __init__(self):
        super().__init__()
        self.durations: Dict[str, int] = dict()
        self.time = 1
        self.termination_time = float('inf')

    def duration(self, action, time):
        self.durations[action] = time

    def terminate_time(self, time):
        self.termination_time = time

    def make_time_step(self, action):
        if action not in self.durations:
            # maybe should raise exception
            self.time += 1
            return

        self.time += self.durations[action]

    def _add_action(self, action_name: str, fluents: List[Fluent], conditions: List[Fluent]):
        if action_name not in self._causes:
            self._causes[action_name] = []
            setattr(self.__class__, action_name,
                    lambda x, time: x.do_action(action_name, time))  # added time to action execution

        self._causes[action_name].append((fluents, conditions))

    def do_action(self, action_name: str, time_start: int) -> bool:
        if time_start < self.time:
            # maybe an exception?
            return False

        possible = self._possible(action_name)
        # print(f"{action_name=} {possible=}")
        if possible is False:
            return False

        self.make_time_step(action_name)
        for to_set, conditions in self._causes[action_name]:
            self._do(to_set, self._check(conditions), possible)
        return True
