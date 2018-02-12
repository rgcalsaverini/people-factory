from numpy.random import normal

func = lambda: round(min(1, abs(normal(0.5, 0.15))), 1)


def pct(f_val):
    val = f_val * 100
    if val >= 10:
        digits = None
    elif val >= 1:
        digits = 1
    elif val >= 0.1:
        digits = 2
    else:
        digits = 3
    return '{}%'.format(round(val, digits))


size = 500000
all = [func() for _ in range(size)]

for i in range(11):
    v = i / 10
    print('{}: {}'.format(v, pct(all.count(v) / size)))
