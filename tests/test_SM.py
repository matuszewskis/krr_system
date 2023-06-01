import unittest
from sympy import Symbol
from krr_system import TimeDomainDescription, Scenario

class MyTestCase(unittest.TestCase):
    def expectEqual(self, v1, v2, msg=None):
        with self.subTest():
            self.assertEqual(v1, v2, msg)

    def test_Q3_SM(self):
        """This scenario is consistent"""
        money = Symbol("has money on a card")
        ticket = Symbol('has a cinema ticket')

        d = TimeDomainDescription()
        d.initially(m=False, ticket=False)
        d.causes('buy cinema ticket', ticket, conditions=money)
        d.causes("deposit money", money)
        d.causes("sell cinema ticket", money & ~ticket, conditions=ticket)
        d.duration("buy cinema ticket", 1)
        d.duration("sell cinema ticket", 2)
        d.duration("deposit money", 1)

        d.terminate_time(8)

        obs = [(~money & ~ticket, 0)]
        acs = [(1, 'deposit money'),(2,'buy cinema ticket'),(3,'sell cinema ticket')]  
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        res1 = s.check_if_condition_hold(ticket, 6, verbose=False)
        print(f"Does ticket is hold at timepoint 6? -", res1)
        self.expectEqual(res1, False)

        res2 = s.check_if_condition_hold(money, 6, verbose=True)
        print(f"Does money is hold at timepoint 6? -", res2)
        self.expectEqual(res2, True)


if __name__ == '__main__':
    unittest.main()
