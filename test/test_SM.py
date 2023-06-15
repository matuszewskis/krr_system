import unittest
from sympy import Symbol
from krr_system import TimeDomainDescription, Scenario

class MyTestCase(unittest.TestCase):
    def expectEqual(self, v1, v2, msg=None):
        with self.subTest():
            self.assertEqual(v1, v2, msg)

    def test_Q3_SM(self):
        """This scenario is consistent"""
        money = Symbol("money")
        ticket = Symbol('ticket')

        d = TimeDomainDescription()
        d.initially(money=False, ticket=False)
        d.causes('buy cinema ticket', ticket & ~money, conditions=money)
        d.causes("deposit money", money)
        d.causes("sell cinema ticket", money & ~ticket, conditions=ticket)
        d.duration("buy cinema ticket", 1)
        d.duration("sell cinema ticket", 2)
        d.duration("deposit money", 1)

        d.terminate_time(8)

        obs = [(~money & ~ticket, 0)]
        acs = [('deposit money', 1), ('buy cinema ticket', 2), ('sell cinema ticket', 3)]
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        res1 = s.check_if_condition_hold(ticket, 6)
        print(f"Does ticket hold at timepoint 6? -", res1)
        self.expectEqual(res1, False)

        res2 = s.check_if_condition_hold(money, 6)
        print(f"Does money hold at timepoint 6? -", res2)
        self.expectEqual(res2, True)


if __name__ == '__main__':
    unittest.main()
