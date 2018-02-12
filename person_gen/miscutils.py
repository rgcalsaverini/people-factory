import random

def roulette_random(pairs):
    """
    Return a random item from a weighted pair list
    :param pairs: A list of (weight, item) pairs, where weight is an integer and item is anything
    :return: A random item
    """
    total = sum(pair[0] for pair in pairs)
    random_pick = random.randrange(total)
    for (weight, item) in pairs:
        random_pick -= weight
        if random_pick <= 0:
            return item
    raise ValueError('Failed to pick an item')
