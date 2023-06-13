import unittest

from sympy import Symbol
from krr_system import TimeDomainDescription, Scenario


class MyTestCase(unittest.TestCase):
    def test_Q1_Q3_PS(self):
        """This scenario is consistent"""
        f = Symbol("flying")
        r = Symbol('refuelled')

        d = TimeDomainDescription()
        d.initially(flying=False, refuelled=True, crash=False)
        d.causes('refuel', r, conditions= ~f )
        d.causes("takeoff", f, conditions= r )
        d.causes("land", ~f & ~r, conditions=f)
        d.duration("refuel", 1)
        d.duration("takeoff", 2)
        d.duration("land", 1)

        d.terminate_time(8)

        OBS = [(~f & r, 0)]
        ACS = [("refuel", 1), ("takeoff", 2)]
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        # Q1
        print("S is consistent? - ", s.is_consistent())
        self.assertEqual(s.is_consistent(verbose=True), True)
        # Q3
        print("does in flight hold at timepoint 4 - ", s.check_if_condition_hold(f, 3))
        self.assertEqual(s.check_if_condition_hold(f, 3), None)
        # Q3
        print("does in flight hold at timepoint 4 - ", s.check_if_condition_hold(f, 4))
        self.assertEqual(s.check_if_condition_hold(f, 4), True)


if __name__ == '__main__':
    unittest.main()
