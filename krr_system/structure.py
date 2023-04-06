from copy import deepcopy
from typing import List

from krr_system.domain import Fluent, DomainDescription


class Statement:
    def __init__(self, fluents: List[Fluent], actions: List[str]):
        self.fluents = fluents
        self.actions = actions


class Structure:

    def __init__(self, model: DomainDescription):
        self.model = deepcopy(model)

    def is_statement_true(self, statement: Statement):
        m = deepcopy(self.model)

        for action in statement.actions:
            m.do_action(action)

        return m._check(statement.fluents)