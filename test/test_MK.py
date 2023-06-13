import unittest

from sympy import Symbol

from krr_system import TimeDomainDescription, Scenario


class MyTestCase(unittest.TestCase):
    def test_Q1_inconsistent_MK(self):
        inspired = Symbol("inspired")
        painted = Symbol("painted")

        d = TimeDomainDescription()
        d.initially(inspired=True, painted=False)
        d.causes("paint", painted & ~inspired)
        d.impossible("paint", conditions=~inspired)
        d.causes("pay", ~painted)
        d.impossible("pay", conditions=~painted)
        d.releases("pay", inspired)
        d.duration("paint", 2)
        d.duration("pay", 1)

        d.terminate_time(6)

        OBS = ((inspired & ~painted, 1),)
        ACS = (("paint", 1), ("pay", 3), ("pay", 4), ("paint", 5))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("Is scenario consistent? - ", s.is_consistent(verbose=True))
        self.assertEqual(s.is_consistent(), False)
        
    def test_Q1_consistent_MK(self):
        inspired = Symbol("inspired")
        painted = Symbol("painted")

        d = TimeDomainDescription()
        d.initially(inspired=True, painted=False)
        d.causes("paint", painted & ~inspired)
        d.impossible("paint", conditions=~inspired)
        d.causes("pay", ~painted)
        d.impossible("pay", conditions=~painted)
        d.releases("pay", inspired)
        d.duration("paint", 2)
        d.duration("pay", 1)

        d.terminate_time(6)

        OBS = ((inspired & ~painted, 1),)
        ACS = (("paint", 1), ("pay", 3))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("Is scenario consistent? - ", s.is_consistent(verbose=True))
        self.assertEqual(s.is_consistent(), True)

    def test_Q2_MK(self):
        inspired = Symbol("inspired")
        painted = Symbol("painted")

        d = TimeDomainDescription()
        d.initially(inspired=True, painted=False)
        d.causes("paint", painted & ~inspired)
        d.impossible("paint", conditions=~inspired)
        d.causes("pay", ~painted)
        d.impossible("pay", conditions=~painted)
        d.releases("pay", inspired)
        d.duration("paint", 2)
        d.duration("pay", 1)

        d.terminate_time(6)

        OBS = ((inspired & ~painted, 1),)
        ACS = (("paint", 1), ("pay", 3))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("Does PAINT perform at 1? - ", s.does_action_perform("paint", 1))
        self.assertEqual(s.does_action_perform("paint", 1), True)

        print("Does PAINT perform at 1? - ", s.does_action_perform("paint", 1))
        self.assertEqual(s.does_action_perform("paint", 3), False)
        
        print("Does PAY perform at 3? - ", s.does_action_perform("pay", 3))
        self.assertEqual(s.does_action_perform("pay", 3), True)


if __name__ == '__main__':
    unittest.main()
