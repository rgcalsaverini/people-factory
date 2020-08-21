import unittest

from person_gen.utils import roulette_random, upper_bound_value, bounded, \
    apply_map


def almost_equal(a, b):
    tolerance = (a + b) * 0.05
    assert abs(a - b) < tolerance, '{} != {} +- {}'.format(a, b, tolerance)


def distribution(num):
    val = [0] * num
    pairs = [[1, i] for i in range(num)]
    total = 50000
    for i in range(total):
        res = roulette_random(pairs)
        val[res] += 1
    for v in val:
        almost_equal(v, total / len(val))


class TestRoulette(unittest.TestCase):
    def test_none(self):
        self.assertIsNone(roulette_random(None))
        self.assertIsNone(roulette_random([]))
        self.assertIsNone(roulette_random([[0, 1], [0, 2]]))

    def test_one(self):
        for i in range(100):
            self.assertEqual(roulette_random([[1, 1]]), 1)
            self.assertEqual(roulette_random([[1, 1], [0, 2]]), 1)
            self.assertEqual(roulette_random([[0, 2], [1, 1]]), 1)
            self.assertEqual(roulette_random([[0, 2], [1, 1], [0, 3]]), 1)

    def test_two(self):
        distribution(2)

    def test_three(self):
        distribution(3)

    def test_ten(self):
        distribution(10)


class TestUpperValue(unittest.TestCase):
    def test_none(self):
        self.assertEqual(upper_bound_value([], 0), None)
        self.assertEqual(upper_bound_value(None, 0), None)

    def test_one(self):
        self.assertEqual(upper_bound_value([1], 1), 1)
        self.assertEqual(upper_bound_value([1], 0), 1)
        self.assertEqual(upper_bound_value([1], 2), 1)

    def test_two(self):
        self.assertEqual(upper_bound_value([0, 1], 1), 1)
        self.assertEqual(upper_bound_value([0, 1], 0), 1)
        self.assertEqual(upper_bound_value([2, 3], 1), 2)

    def test_three(self):
        self.assertEqual(upper_bound_value([0, 1, 2], -1), 0)
        self.assertEqual(upper_bound_value([0, 1, 2], 0), 1)
        self.assertEqual(upper_bound_value([0, 1, 2], 1), 2)
        self.assertEqual(upper_bound_value([0, 1, 2], 2), 2)


class TestMisc(unittest.TestCase):
    def test_bounded(self):
        values = [-10, -5.1, -0, 0, 0.1, -0.1, 1, 1.2]

        for v in values:
            self.assertEqual(type(bounded(v, 100, -100, int)), int)
            self.assertEqual(type(bounded(v, 100, -100, float)), float)
            self.assertGreaterEqual(bounded(v, 100, 0, float), 0)
            self.assertGreaterEqual(bounded(v, 100, -1, float), -1)
            self.assertLessEqual(bounded(v, 0, -100, float), 0)
            self.assertLessEqual(bounded(v, 1, -100, float), 1)
            self.assertLessEqual(bounded(v, -1, -100, float), -1)

    def test_apply_map(self):
        self.assertEqual(apply_map(['test'], {'test': 1}), [1])
        self.assertEqual(apply_map(['test1', 'test2'], {'test1': 1, 'test2': 2}), [1, 2])
        self.assertEqual(apply_map(['test1', None], {'test1': 1, 'test2': 2}), [1, None])
        self.assertEqual(apply_map([None], {'test1': 1}), [None])


if __name__ == '__main__':
    unittest.main()
