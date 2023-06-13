
from copy import deepcopy
from typing import List, Tuple, Union

from sympy.logic.boolalg import BooleanFunction

from krr_system.domain import TimeDomainDescription, Fluent, Formula


class Scenario:

    def __init__(self, domain: TimeDomainDescription, observations: List[Tuple[BooleanFunction, int]],
                 action_occurrences: List[Tuple[str, int]]):
        self._raw_observations = dict((time, formula) for formula, time in observations)
        self.observations = dict((time, Formula(formula)) for formula, time in observations)
        self.action_occurrences = dict((time, name) for name, time in action_occurrences)
        self.domain = deepcopy(domain)

    def does_action_perform(self, action: str, time: int) -> bool:
        """
        All things happening should be defined in action occurrences,
        thus to check if action is performed it is enough to check scenario
        consistency and existence in action occurrences
        """
        return self.is_consistent() and (self.action_occurrences.get(time) == action)

    def check_if_condition_hold(self, conditions: BooleanFunction, after_time: int) -> Union[bool, None]:

        conditions = Formula(conditions)
        domain = deepcopy(self.domain)

        # follow scenario to the specified point
        for time in range(after_time):
            if time in self.action_occurrences:
                r = domain.do_action(self.action_occurrences[time], time)
                assert r is not False
            domain.step()

        # domain frozen at time after after_time
        return domain._check(conditions.conditions)

    def is_consistent(self, verbose=False) -> bool:

        domain = deepcopy(self.domain)
        result = True
        max_time = max(max(self.observations.keys()), max(self.action_occurrences.keys()))
        for time in range(max_time+1):
            if time in self.observations:
                r = domain._check(self.observations[time].conditions)
                if r is False:
                    if verbose:
                        print(f"Observation {self._raw_observations[time]} at time {time} breaks consistency")
                    return False
                if r is None:
                    if verbose:
                        print(f"Observation {self._raw_observations[time]} at time {time} caused None")
                    result = None

            if time in self.action_occurrences:
                r = domain.do_action(self.action_occurrences[time], time)
                if r is False:
                    if verbose:
                        print(f"Action {self.action_occurrences[time]} at time {time} breaks consistency")
                    return False
                if r is None:
                    if verbose:
                        print(f"Action {self.action_occurrences[time]} at time {time} caused None")
                    result = None

            domain.step()

        return result
