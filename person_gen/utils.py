import random


def roulette_random(pairs):
    if not pairs:
        return None
    total = sum(pair[0] for pair in pairs)
    if not total:
        return None
    random_pick = random.randrange(total)
    for (weight, item) in pairs:
        random_pick -= weight
        if random_pick < 0:
            return item
    raise ValueError('Failed to pick an item')


def upper_bound_value(value_list, value):
    if not value_list:
        return None
    for i in value_list:
        if i > value:
            return i
    return value_list[-1]


def bounded(val, max_v, min_v, v_type):
    if isinstance(val, (list, tuple, set)):
        return type(val)([bounded(v, max_v, min_v, v_type) for v in val])
    return max(min_v, min(max_v, v_type(val)))


def bounded_pct(val):
    return bounded(val, 1, 0, float)


def apply_map(source, templates):
    return [templates[s] if s else None for s in source]
