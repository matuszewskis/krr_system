import unittest
from sympy import Symbol
from krr_system import TimeDomainDescription, Scenario

class DP_tests(unittest.TestCase):
    def test_1(self):

        print("\n-------------")
        print("Test 1")
        print("Expected result: inconsistency due to performing an action leading nonexisting state")
        
        
	# fluent declaration
        f = Symbol("f")
        g = Symbol("g")

	# domain description declaration
        d = TimeDomainDescription()
        d.initially(f=True, g=False)
        d.causes("A", ~f, f)
        d.causes("A", f, ~g)
        d.duration("A", 1)
        d.terminate_time(10)

        # scenario declaration
        OBS = ((f & ~g, 1),)
        ACS = (("A", 3),)
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("Expected scenario consistency: False")
        print("Obtained scenario consistency:", s.is_consistent(verbose=True), )
        self.assertEqual(s.is_consistent(verbose=False), False)

    def test_2(self):

        print("\n-------------")
        print("Test 2")
        print("Expected result: inconsistency due to overlapping actions")
        
        
	# fluent declaration
        f = Symbol("f")
        g = Symbol("g")

	# domain description declaration
        d = TimeDomainDescription()
        d.initially(f=True, g=True)
        d.causes("A", ~g, f)
        d.causes("B", f, ~g)
        d.duration("A", 2)
        d.duration("B", 3)
        d.terminate_time(10)

        # scenario declaration
        OBS = ((f & g, 0),)
        ACS = (("B", 3),("A", 5))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("Expected scenario consistency: False")
        print("Obtained scenario consistency:", s.is_consistent(verbose=True))
        self.assertEqual(s.is_consistent(verbose=False), False)

    def test_3(self):

        print("\n-------------")
        print("Test 3")
        print("Expected result: inconsistency due to exceeding termination time")
        
        
	# fluent declaration
        f = Symbol("f")
        g = Symbol("g")

	# domain description declaration
        d = TimeDomainDescription()
        d.initially(f=True, g=False)
        d.causes("A", g, f)
        d.duration("A", 5)
        d.terminate_time(10)

        # scenario declaration
        OBS = ((f & ~g, 0),)
        ACS = (("A", 2),("A", 8))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("Expected scenario consistency: False")
        print("Obtained scenario consistency:", s.is_consistent(verbose=True))
        self.assertEqual(s.is_consistent(verbose=False), False)

    def test_4(self):

        print("\n-------------")
        print("Test 4")
        print("Expected result: consistent scenario, correct answers to queries")
        
        
	# fluent declaration
        f = Symbol("f")
        g = Symbol("g")
        h = Symbol("h")

	# domain description declaration
        d = TimeDomainDescription()
        d.initially(f=True, g=True, h=True)

        d.releases("A", f)
        d.causes("A", ~g, h)
        d.causes("A", g, ~h)
        d.impossible("A", conditions=~f)
	
        d.causes("B", ~h, h)
        d.impossible("B", conditions=g|~h)
 
        d.duration("A", 2)
        d.duration("B", 1)
        d.terminate_time(10)

        # scenario declaration
        OBS = ((f & g & h, 0),)
        ACS = (("A", 1), ("B", 3), ("A", 4))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        print("Expected scenario consistency: True")
        print("Obtained scenario consistency:", s.is_consistent(verbose=True))
        self.assertEqual(s.is_consistent(verbose=False), True)

        print("f at 3")
        print("expected: None, obtained: ", s.check_if_condition_hold(f, 3))
        print("g at 6")
        print("expected: True, obtained: ", s.check_if_condition_hold(g, 6))
        print("h at 7")
        print("expected: False, obtained: ", s.check_if_condition_hold(h, 7)) 
        print("f at 7")
        print("expected: None, obtained: ", s.check_if_condition_hold(f, 7)) 
        print("f | h at 3")
        print("expected: True, obtained: ", s.check_if_condition_hold(f | h, 3))        


if __name__ == '__main__':
    unittest.main()