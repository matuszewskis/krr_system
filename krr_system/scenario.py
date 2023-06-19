from copy import deepcopy
from typing import List, Tuple, Union

from sympy.logic.boolalg import BooleanFunction

from krr_system.domain import TimeDomainDescription, Formula


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
        """
        This function returns three values.
            True - corresponds to conditions being met in all models meaning that they are met necessarily
            None - conditions were met in some models, corresponding to possibly
            False - conditions were not met in any of the model
        """
        if self.is_consistent() is False:
            raise Exception("Model is inconsistent, cannot check conditions")

        conditions = Formula(conditions)

        domain = deepcopy(self.domain)
        for time in range(after_time + 1):
            if time in self.observations:
                # set fluents so they satisfy observations
                domain._set(self.observations[time].get_fluents())

            if time == after_time:
                return domain._check(conditions.conditions)

            if time in self.action_occurrences:
                domain.do_action(self.action_occurrences[time], time)
            domain.step()

        raise ValueError(f"Time of observation: {after_time} was never reached")

    def is_consistent(self, return_possibly=False, verbose=False) -> bool:
        """
        This function returns information about existence of model defined wrt provided domain and scenario.
        It returns only true or false. False is returned if one of the observation or action occurrence is unobtainable,
        true is returned if all observations and actions are achievable in some model.
        """

        domain = deepcopy(self.domain)
        result = True
        max_time = max(max(self.observations.keys()), max(self.action_occurrences.keys()))
        for time in range(max_time + 1):
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

                # set fluents so they satisfy observations
                domain._set(self.observations[time].get_fluents())

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

        if return_possibly:
            return result
        return result is not False