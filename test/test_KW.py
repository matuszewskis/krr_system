import unittest

from sympy import Symbol

from krr_system import TimeDomainDescription, Scenario


class MyTestCase(unittest.TestCase):
    def test_Q1_KW(self):
        """This scenario is not consistent due to invalid observation"""
        dr = Symbol("driving")
        sl = Symbol("sleeping")
        fu = Symbol("fuelled")

        d = TimeDomainDescription()
        d.initially(driving=False, sleeping=False, fuelled=False)
        d.causes("drive", dr & ~fu, conditions=~sl & fu & ~dr)
        d.causes("stop", ~dr & ~fu, conditions=dr)
        d.causes("refuel", fu, conditions=~sl)
        d.duration("refuel", 1)
        d.duration("drive", 3)
        d.duration("stop", 1)

        d.terminate_time(6)

        OBS = [(~dr & ~sl & fu, 1)]
        ACS = (("refuel", 2), ("drive", 3))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("S is consistent? - ", s.is_consistent())
        self.assertEqual(s.is_consistent(verbose=True), False)

    def test_Q2_KW(self):
        """This scenario is consistent and in the middle of refueling it is not fuelled"""
        dr = Symbol("driving")
        sl = Symbol("sleeping")
        fu = Symbol("fuelled")

        d = TimeDomainDescription()
        d.initially(driving=False, sleeping=False, fuelled=False)
        d.causes("drive", dr & ~fu, conditions=~sl & fu & ~dr)
        d.causes("stop", ~dr & ~fu, conditions=dr)
        d.causes("refuel", fu, conditions=~sl)
        d.duration("refuel", 2)
        d.duration("drive", 3)
        d.duration("stop", 1)

        d.terminate_time(8)

        OBS = [(~dr & ~sl & ~fu, 1)]
        ACS = (("refuel", 2), ("drive", 4))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("S is consistent? - ", s.is_consistent())
        self.assertEqual(s.is_consistent(verbose=True), True)

        print("Does fuelled hold at timepoint 3? - ", s.check_if_condition_hold(fu, 3))
        self.assertEqual(s.check_if_condition_hold(fu, 3), None)

    def test_Q3_KW(self):
        """This scenario is not consistent because drive cannot be performed when it is not fuelled"""
        dr = Symbol("driving")
        sl = Symbol("sleeping")
        fu = Symbol("fuelled")

        d = TimeDomainDescription()
        d.initially(driving=False, sleeping=False, fuelled=False)
        d.causes("drive", dr & ~fu, conditions=~sl & fu & ~dr)
        d.causes("stop", ~dr & ~fu, conditions=dr)
        d.causes("refuel", fu, conditions=~sl)
        d.duration("refuel", 2)
        d.duration("drive", 3)
        d.duration("stop", 1)

        d.terminate_time(8)

        OBS = [(~dr & ~sl & ~fu, 1)]
        ACS = (("drive", 2),)
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("Does DRIVE perform at 2? - ", s.does_action_perform("drive", 2))
        self.assertEqual(s.does_action_perform("drive", 2), False)


if __name__ == "__main__":
    unittest.main()