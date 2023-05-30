import unittest

from sympy import Symbol

from krr_system import TimeDomainDescription, Scenario


class MyTestCase(unittest.TestCase):
    def test_Q1_PS(self):
        """This scenario is consistent"""
        f = Symbol("flying")
        r = Symbol('refuelled')
        c = Symbol('crash')

        d = TimeDomainDescription()
        d.initially(f=False, r=True, c=False)
        d.causes('refuel', r, conditions= ~f & ~c)
        d.causes("takeoff", f, conditions= r & ~c)
        d.causes("land", ~f & ~r, conditions=f)
        d.releases("takeoff", c & ~f)
        d.duration("refuel", 1)
        d.duration("takeoff", 2)
        d.duration("land", 1)

        d.terminate_time(8)

        OBS = ((~f & ~r & ~c, 0),)
        ACS = (("refuel", 1),("takeoff", 2))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("S is consistent? - ", s.is_consistent())
        self.assertEqual(s.is_consistent(verbose=True), True)


if __name__ == '__main__':
    unittest.main()
