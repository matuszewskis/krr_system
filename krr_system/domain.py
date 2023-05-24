from __future__ import annotations

from copy import copy, deepcopy
from typing import List, Tuple, Dict

from sympy import Symbol, satisfiable
from sympy.logic.boolalg import BooleanFunction

from krr_system.utils import fuzzy_eq, fuzzy_and, PartiallyMutableDict, ImmutableDict


class Fluent:
    def __init__(self, **fluents):
        for name, value in fluents.items():
            assert (isinstance(name, str))
            self.name = name
            self.value = value
            break  # only the first value is processed

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


class Formula:

    def __init__(self, formula: BooleanFunction | Symbol):
        self.formula = formula
        if not self.is_satisfiable():
            raise ValueError(f"Provided formula is never true. Formula: {formula}")
        self.vals_dict: dict[str, bool] = self.satisfied_values()
        self.fluents: List[Fluent] = self.get_fluents()
        self.conditions: List[dict] = self.satisfied_conditions()

    def is_satisfiable(self) -> bool:
        return bool(satisfiable(self.formula))

    def satisfied_values(self) -> dict:
        if self.formula is None:
            return {}
        models = satisfiable(self.formula, all_models=True)
        conditions = PartiallyMutableDict()
        for d in models:
            for k, v in d.items():  # has to be done this way instead e.g. via update method
                conditions[k.name] = v
        return conditions

    def get_fluents(self) -> List[Fluent]:
        return [Fluent(**{k: v}) for k, v in self.vals_dict.items()]

    def satisfied_conditions(self):
        if self.formula is None:
            return None
        models = satisfiable(self.formula, all_models=True)
        return [dict((k.name, v) for k, v in d.items()) for d in models]


class DomainDescription:

    def __init__(self):

        self.fluents: Dict[str, Fluent] = dict()
        self._causes: Dict[str, List[Tuple[List[Fluent], List[dict]]]] = dict()
        self.impossibles: Dict[str, List[List[dict]]] = dict()
        self._step_diff: Dict[str, bool | None] = ImmutableDict()

    def __repr__(self):
        return self.description()

    def description(self):
        repr = f"State\n{self.fluents}\n"
        if len(self._causes):
            repr += "\nACTIONS"
            for cause, changes in self._causes.items():
                repr += f"\nAction: {cause}"
                for to_set, conditions in self._causes[cause]:
                    repr += f"\n     to set: {to_set}"
                    if conditions:
                        repr += f"\n          under conditions: {conditions}"

        if len(self.impossibles):
            repr += "\nImpossibilities"
            for cause, conditions in self.impossibles.items():
                repr += f"\n     Action: {cause}"
                if conditions:
                    repr += f"\n          under conditions: {conditions}"
        return repr

    def state(self):
        return [(f.name, f.value) for f in self.fluents.values()]

    def copy(self):
        return deepcopy(self)

    def _check_if_known(self, fluents: List[Fluent], default_value=None):
        if isinstance(fluents, Fluent):
            fluents = [fluents]
        for fluent in fluents:
            if fluent.name not in self.fluents:
                assumed_fluent = Fluent(**{fluent.name: default_value})
                self.fluents[fluent.name] = assumed_fluent

    def _set(self, fluents: List[Fluent] | Fluent):
        if isinstance(fluents, Fluent):
            fluents = [fluents]
        for fluent in fluents:
            self.fluents[fluent.name] = fluent

    def _check(self, conditions: List[dict]) -> bool | None:
        """Checks a single list of fluent requirements"""
        if conditions is None:
            return True

        def _fuzzy_dict_include(d1: dict, d2: dict) -> bool | None:
            result = True
            for k, v in d1.items():
                if k not in d2:
                    return False  # possible error
                r = fuzzy_eq(v, d2[k])
                if r is False:
                    return False
                if r is None:
                    result = None
            return result

        result = False
        for d in conditions:
            r = _fuzzy_dict_include(d, self.fluents)
            if r:
                return True
            if r is None:
                result = None
        return result

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
        diff = [copy(f) for f in fluents]
        if conditions_met is None or possible is None:
            for fluent in diff:
                fluent.value = None

        for fluent in diff:
            self._step_diff[fluent.name] = fluent.value

        self._set(diff)

    def do_action(self, action_name: str, *args, **kwargs):
        # reset the step diff
        self._step_diff = ImmutableDict()
        possible = self._possible(action_name)
        if possible is False:
            return False
        for to_set, conditions in self._causes[action_name]:
            try:
                self._do(to_set, self._check(conditions), possible)
            except ValueError:
                return False
        return True

    def _add_action(self, action_name: str, fluents: List[Fluent] | Fluent, conditions: List[dict] | Fluent | None):
        if action_name not in self._causes:
            self._causes[action_name] = []
            setattr(self.__class__, action_name, lambda x: x.do_action(action_name, ))

        self._causes[action_name].append((fluents, conditions))

    def initially(self, **kwargs):
        for key, value in kwargs.items():
            self.fluents[key] = Fluent(**{key: value})

    def impossible(self, action: str, conditions: BooleanFunction | Symbol | None = None):
        conditions = Formula(conditions)
        if action not in self.impossibles:
            self.impossibles[action] = []

        self.impossibles[action].append(conditions.conditions)

    def causes(self, action: str, formula: BooleanFunction | Symbol,
               conditions: BooleanFunction | Symbol | None = None):
        formula = Formula(formula)

        conditions = Formula(conditions)

        self._check_if_known(formula.fluents)
        self._add_action(action, formula.fluents, conditions.conditions)

    def releases(self, action: str, formula: BooleanFunction | Fluent,
                 conditions: BooleanFunction | Symbol | None = None):
        formula = Formula(formula)
        conditions = Formula(conditions)

        for fluent in formula.fluents:
            fluent.value = None

        self._check_if_known(formula.fluents)
        self._add_action(action, formula.fluents, conditions.conditions)


class TimeDomainDescription(DomainDescription):

    def __init__(self):
        super().__init__()
        self.durations: Dict[str, int] = dict()
        self.time = 1
        self.termination_time = float('inf')

    def __repr__(self):
        return self.description()

    def description(self):

        repr = f"State\n{self.fluents}\n"
        if len(self._causes):
            repr += "\nACTIONS"
            for cause, changes in self._causes.items():
                repr += f"\nAction: {cause}"
                repr += f"\nduration: {self.durations[cause]}"
                for to_set, conditions in self._causes[cause]:
                    repr += f"\n     to set: {to_set}"
                    if conditions:
                        repr += f"\n          under conditions: {conditions}"

        if len(self.impossibles):
            repr += "\nImpossibilities"
            for cause, conditions in self.impossibles.items():
                repr += f"\n     Action: {cause}"
                if conditions:
                    repr += f"\n          under conditions: {conditions}"
        return repr

    def duration(self, action, time):
        self.durations[action] = time

    def terminate_time(self, time):
        self.termination_time = time

    def time_step_possible(self, action_name: str) -> bool:
        if action_name not in self.durations:
            return False

        self.time += self.durations[action_name]
        if self.time > self.termination_time:
            return False
        return True

    def _add_action(self, action_name: str, fluents: List[Fluent] | Fluent, conditions: List[dict] | Fluent | None):
        if action_name not in self._causes:
            self._causes[action_name] = []
            setattr(self.__class__, action_name,
                    lambda x, time: x.do_action(action_name, time))  # added time to action execution

        self._causes[action_name].append((fluents, conditions))

    def do_action(self, action_name: str, time_start: int, *args, **kwargs) -> bool:
        if time_start < self.time:
            # maybe an exception?
            return False

        if not self.time_step_possible(action_name):
            return False

        return super().do_action(action_name, time_start, *args, **kwargs)
