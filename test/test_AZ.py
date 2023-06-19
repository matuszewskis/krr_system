import unittest

from sympy import Symbol

from krr_system import TimeDomainDescription, Scenario


class TestQueryAZ(unittest.TestCase):
    def expectEqual(self, v1, v2, msg=None):
        with self.subTest():
            self.assertEqual(v1, v2, msg)

    def test_is_consistent(self):
        is_read = Symbol('is_read')
        borrowed = Symbol('borrowed')
        closed = Symbol('closed')  # Library

        d = TimeDomainDescription()
        d.initially(closed=True, read=False, borrowed=False)

        d.causes('read', is_read, borrowed)
        d.causes('borrow', borrowed, ~borrowed & ~closed)
        d.causes('return', ~is_read & ~borrowed, is_read & borrowed & ~closed)
        d.causes('open', ~closed)
        d.causes('close', closed)

        d.duration('read', 2)
        d.duration('borrow', 1)
        d.duration('return', 1)
        d.duration('open', 3)
        d.duration('close', 3)

        d.terminate_time(10)

        obs = [(~closed, 4), (borrowed, 5), (is_read, 7)]
        acs = [('open', 1)]
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        res = s.is_consistent(verbose=True)
        print(f"Is consistent? -", res)
        self.expectEqual(res, True)


        obs = [(~closed, 4), (borrowed, 5), (is_read, 7)]
        acs = [('borrow', 4)]
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        res = s.is_consistent(verbose=True)
        print(f"Is consistent? -", res)
        self.expectEqual(res, True)


        obs = [(~closed, 4), (borrowed, 5), (is_read, 7)]
        acs = [('close', 4)]
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        print(f"Is consistent? -", res)
        self.expectEqual(res, False)


        obs = [(~closed, 4), (borrowed, 5), (is_read, 7)]
        acs = [('open', 1), ('borrow', 4)]
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        res = s.is_consistent()
        print(f"Is consistent? -", res)
        self.expectEqual(res, True)


    def test_action_performs(self):
        is_read = Symbol('is_read')
        borrowed = Symbol('borrowed')
        closed = Symbol('closed')  # Library

        d = TimeDomainDescription()
        d.initially(closed=True, read=False, borrowed=False)

        d.causes('read', is_read, borrowed)
        d.causes('borrow', borrowed, ~borrowed & ~closed)
        d.causes('return', ~is_read & ~borrowed, is_read & borrowed & ~closed)
        d.causes('open', ~closed)
        d.causes('close', closed)

        d.duration('read', 2)
        d.duration('borrow', 1)
        d.duration('return', 1)
        d.duration('open', 3)
        d.duration('close', 3)

        d.terminate_time(10)

        obs = [(~closed, 4), (borrowed, 5), (is_read, 7)]
        acs = [('open', 1), ('borrow', 4), ('read', 5)]
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        res = s.is_consistent(verbose=True)
        print(f"Is consistent? -", res)
        self.expectEqual(res, True)

        print(f"Does action borrow perform at timepoint 4? -", res)
        res = s.does_action_perform('borrow', 4)
        self.expectEqual(res, True)

        print(f"Does action open hold at timepoint 1? -", res)
        res = s.does_action_perform('open', 1)
        self.expectEqual(res, True)

    def test_action_performs_2(self):
        is_read = Symbol('is_read')
        borrowed = Symbol('borrowed')
        closed = Symbol('closed')  # Library

        d = TimeDomainDescription()
        d.initially(closed=True, read=False, borrowed=False)

        d.causes('read', is_read, borrowed)
        d.causes('borrow', borrowed, ~borrowed & ~closed)
        d.causes('return', ~is_read & ~borrowed, is_read & borrowed & ~closed)
        d.causes('open', ~closed)
        d.causes('close', closed)

        d.duration('read', 2)
        d.duration('borrow', 1)
        d.duration('return', 1)
        d.duration('open', 3)
        d.duration('close', 3)

        d.terminate_time(10)

        obs = [(~closed, 4), (borrowed, 5), (is_read, 7)]
        acs = [('open', 1), ('read', 5)]
        s = Scenario(domain=d, observations=obs, action_occurrences=acs)

        res = s.is_consistent(verbose=True)
        print(f"Is consistent? -", res)
        self.expectEqual(res, True)

        print(f"Does action borrow perform at timepoint 4? -", res)
        res = s.does_action_perform('borrow', 4)
        self.expectEqual(res, True)

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
        self.expectEqual(res, False)

        res = s.check_if_condition_hold(loaded, 3)
        print(f"Does loaded hold at timepoint 3? -", res)
        self.expectEqual(res, True)

        res = s.check_if_condition_hold(loaded, 5)
        print(f"Does loaded hold at timepoint 4? -", res)
        self.expectEqual(res, False)


if __name__ == '__main__':
    unittest.main()