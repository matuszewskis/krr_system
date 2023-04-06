def fuzzy_not(o):
    if o is None:
        return o
    return not o


def fuzzy_or(o1, o2):
    if o1 is None or o2 is None:
        return None
    return o1 or o2


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
