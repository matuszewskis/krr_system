import unittest

from sympy import Symbol

from krr_system import TimeDomainDescription, Scenario


class TestQuery3(unittest.TestCase):
    def expectEqual(self, v1, v2, msg=None):
        with self.subTest():
            self.assertEqual(v1, v2, msg)

    def test_condition_holds(self):
        alive = Symbol('alive')
        hidden = Symbol('hidden')
        loaded = Symbol('loaded')

        d = TimeDomainDescription()
        d.initially(alive=True)
        d.causes('load', loaded)
        d.causes('shoot', ~loaded)
        d.causes('shoot', ~alive, ~hidden & loaded)
        d.releases('shoot', hidden)
        d.causes('hide', hidden)
        d.duration('load', 2)
        d.duration('shoot', 1)
        d.duration('hide', 1)
        d.terminate_time(10)

        obs = [(alive & ~loaded & hidden, 1), (alive & loaded & hidden, 3)]
        acs = [('load', 1), ('shoot', 4), ('load', 5)]
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        res = s.check_if_condition_hold(loaded, 1)
        print(f"Does loaded hold at timepoint 1? -", res)
        self.expectEqual(res, True)

        res = s.check_if_condition_hold(loaded, 3)
        print(f"Does loaded hold at timepoint 3? -", res)
        self.expectEqual(res, True)

        res = s.check_if_condition_hold(loaded, 4)
        print(f"Does loaded hold at timepoint 4? -", res)
        self.expectEqual(res, False)


if __name__ == '__main__':
    unittest.main()
