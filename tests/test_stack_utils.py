import inspect

from abyss.stack_utils import diff_stacks, format_frames, remove_common


def b(fn, val):
    if val > 3:
        if val % 2 == 0:
            return b(fn, val - 1)
        else:
            return a(fn, val / 2)
    else:
        fn()


def a(fn, val):
    return b(fn, val)


def test_get_stack():
    def test():
        funcs = [f.func for f in format_frames(inspect.currentframe(), 1)[:10]]
        assert funcs == ["b", "a", "b", "a", "b", "a", "b", "b", "a", "test_get_stack"]

    a(test, 16)


def c(stacks):
    stacks.append(format_frames(inspect.currentframe()))


def d(stacks):
    stacks.append(format_frames(inspect.currentframe()))
    c(stacks)
    stacks.append(format_frames(inspect.currentframe()))


def test_diff_stacks():
    stacks = []
    stacks.append(format_frames(inspect.currentframe()))
    c(stacks)
    stacks.append(format_frames(inspect.currentframe()))
    d(stacks)
    stacks.append(format_frames(inspect.currentframe()))
    stacks = [s[::-1] for s in stacks]
    stacks = remove_common(stacks)
    assert list(map(len, stacks)) == [0, 1, 0, 1, 2, 1, 0]
    assert len(stacks) == 7

    events = list(diff_stacks(stacks[1], stacks[3]))
    assert get_event_and_func(events) == [("exit", "c"), ("enter", "d")]

    events = list(diff_stacks(stacks[1], stacks[4]))
    assert get_event_and_func(events) == [("exit", "c"), ("enter", "d"), ("enter", "c")]

    events = list(diff_stacks(stacks[0], stacks[1]))
    assert get_event_and_func(events) == [("enter", "c")]

    assert not list(diff_stacks(stacks[0], stacks[-1]))


def get_event_and_func(events):
    return [(e[0], e[1].func) for e in events]
