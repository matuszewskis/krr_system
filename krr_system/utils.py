def fuzzy_not(o):
    if o is None:
        return o
    return not o


def fuzzy_or(o1, o2):
    if o1 or o2:
        return True
    if o1 is None or o2 is None:
        return None
    return False


def fuzzy_and(o1, o2):
    if o1 is False or o2 is False:
        return False
    if o1 is None or o2 is None:
        return None
    return True


def fuzzy_eq(o1, o2):
    if o1 is None or o2 is None:
        return None
    return o1 == o2


def fuzzy_imply(o1, o2):
    return fuzzy_or(fuzzy_not(o1), o2)


def fuzzy_iff(o1, o2):
    return fuzzy_eq(o1, o2)


class ImmutableDict(dict):
    def __setitem__(self, item, value):
        if item in self and self[item] != value:
            super(ImmutableDict, self).__setitem__(item, None)
            return
        super(ImmutableDict, self).__setitem__(item, value)