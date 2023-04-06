
from copy import deepcopy
from typing import List, Tuple

from krr_system.domain import TimeDomainDescription, Fluent


class Scenario:

    def __init__(self, domain: TimeDomainDescription, observations: List[Tuple[Fluent, int]],
                 action_occurances: List[Tuple[str, int]]):
        self.observations = observations
        self.action_occurances = action_occurances
        self.domain = deepcopy(domain)

    def set_observations_as_true(self):
        pass

    def does_action_perform(self, action: str, time: int):
        """
        All things happening should be defined in action occurances,
        thus to check if action is performed it is neough to check scenario
        consistency and existence is action occurances
        """
        return self.is_consistent() and ((action, time) in self.action_occurances)

    def check_if_condition_hold(self, conditions: List[Fluent], after_time: int, verbose=False):
        if isinstance(conditions, Fluent):
            conditions = [conditions]

        domain = deepcopy(self.domain)
        for action, time in self.action_occurances:

            # follow scenario to the specified point
            if time > after_time:
                break
            if domain.do_action(action, time) is False:
                if verbose:
                    print(f"Action {action} at time {time} breaks consistency")
                return False

        # domain frozen at time after after_time
        return domain._check(conditions)

    def is_consistent(self, verbose=False):
        domain = deepcopy(self.domain)
        for action, time in self.action_occurances:
            if domain.do_action(action, time) is False:
                if verbose:
                    print(f"Action {action} at time {time} breaks consistency")
                return False
        return True