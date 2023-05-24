import unittest

from sympy import Symbol

from krr_system import TimeDomainDescription, Scenario


class MyTestCase(unittest.TestCase):
    def test_contradiction_in_action(self):
        """Expects consistency fail when fluent is ment to be set to two different states at the exact same moment."""
        f = Symbol("f")
        a = Symbol('a')
        b = Symbol('b')

        d = TimeDomainDescription()
        d.initially(a=True, b=False)
        d.causes('set_b_true', b)
        d.causes("action", f, conditions=a)
        d.causes("action", ~f, conditions=b)
        d.duration("action", 1)
        d.duration("set_b_true", 1)
        d.terminate_time(7)

        self.assertEqual(d.do_action('action', 1), True)
        self.assertEqual(d.do_action('set_b_true', 2), True)
        self.assertEqual(d.do_action('action', 3), False)


    def test_observations(self):
        loaded = Symbol("loaded")
        hidden = Symbol("hidden")
        jammed = Symbol("jammed")
        alive = Symbol("alive")

        d = TimeDomainDescription()
        d.initially(alive=True)
        d.causes("load", loaded & ~ jammed)
        d.releases("load", hidden)
        d.causes("jam", jammed, conditions=loaded)
        d.causes("shoot", ~alive, conditions=loaded & ~ hidden & ~ jammed)
        d.causes("shoot", ~loaded & ~jammed)
        d.duration("load", 2)
        d.duration("jam", 1)
        d.duration("shoot", 1)
        d.terminate_time(7)

        OBS = ((alive & ~ loaded & jammed & ~ hidden, 1), (alive & loaded & jammed, 5))
        ACS = (('load', 1), ("jam", 3), ("shoot", 4))
        s = Scenario(domain=d, observations=OBS, action_occurrences=ACS)

        self.assertEqual(s.is_consistent(), None)


if __name__ == '__main__':
    unittest.main()
