import unittest
from person_gen.color import from_gradient, mix_colors

_black = (0, 0, 0)
_white = (255, 255, 255)


def assert_col_eq(col_a, col_b):
    for i in range(3):
        assert abs(col_a[i] - col_b[i]) < 2, "{} != {}".format(col_a, col_b)


class TestMixer(unittest.TestCase):
    def test_black(self):
        for i in range(11):
            offset = i / 10.0
            should_be = tuple([int(255 * offset)] * 3)
            color = mix_colors(_black, _white, offset)
            assert_col_eq(color, should_be)

    def test_rgb(self):
        assert_col_eq(mix_colors((255, 0, 0), (0, 0, 0), 0.5), (127, 0, 0))
        assert_col_eq(mix_colors((0, 255, 0), (0, 0, 0), 0.5), (0, 127, 0))
        assert_col_eq(mix_colors((0, 0, 255), (0, 0, 0), 0.5), (0, 0, 127))
        assert_col_eq(mix_colors((255, 0, 0), (0, 255, 128), 0.5), (127, 127, 64))


class TestGradientPick(unittest.TestCase):
    def test_list_1col(self):
        for i in range(11):
            assert_col_eq(from_gradient([(1, 2, 3)], i / 10.0), (1, 2, 3))

    def test_list_2col(self):
        gradient = [(100, 0, 255), (50, 137, 1)]
        for i in range(11):
            pct = i / 10.0
            assert_col_eq(from_gradient(gradient, pct), mix_colors(*gradient, pct))

    def test_list_3col(self):
        gradient = [(100, 50, 25), (255, 0, 0), (0, 200, 137)]
        for i in range(11):
            pct = i / 10.0
            color = from_gradient(gradient, pct)

            if pct == 0:
                assert_col_eq(color, gradient[0])
            elif pct < 0.5:
                assert_col_eq(from_gradient(gradient, pct), mix_colors(gradient[0], gradient[1], pct * 2))
            elif pct == 0.5:
                assert_col_eq(from_gradient(gradient, pct), gradient[1])
            elif pct < 1:
                assert_col_eq(from_gradient(gradient, pct), mix_colors(gradient[1], gradient[2], (pct - 0.5) * 2))
            elif pct == 1:
                assert_col_eq(from_gradient(gradient, pct), gradient[2])

    def test_dict_1col(self):
        for i in range(11):
            assert_col_eq(from_gradient({0: (1, 2, 3)}, i / 10.0), (1, 2, 3))

    def test_dict_2col_extremes(self):
        gradient = {0: (100, 0, 255), 1: (50, 137, 1)}
        for i in range(11):
            pct = i / 10.0
            assert_col_eq(from_gradient(gradient, pct), mix_colors(gradient[0], gradient[1], pct))

    def test_dict_2col_non_extremes(self):
        gradient = {0.25: (100, 0, 255), 0.75: (50, 137, 1)}
        assert_col_eq(from_gradient(gradient, 0.0), gradient[0.25])
        assert_col_eq(from_gradient(gradient, 0.1), gradient[0.25])
        assert_col_eq(from_gradient(gradient, 0.2), gradient[0.25])

        for i in range(25, 80, 5):
            offset = i / 100.0
            assert_col_eq(from_gradient(gradient, offset), mix_colors(gradient[0.25], gradient[0.75], (offset - 0.25) * 2))

        assert_col_eq(from_gradient(gradient, 0.8), gradient[0.75])
        assert_col_eq(from_gradient(gradient, 0.9), gradient[0.75])
        assert_col_eq(from_gradient(gradient, 1), gradient[0.75])

    def test_dict_3col(self):
        gradient = {0.1: (100, 50, 25), 0.6: (255, 0, 0), 1: (0, 200, 137)}
        assert_col_eq(from_gradient(gradient, 0.0), gradient[0.1])
        assert_col_eq(from_gradient(gradient, 0.05), gradient[0.1])
        assert_col_eq(from_gradient(gradient, 0.1), gradient[0.1])
        assert_col_eq(from_gradient(gradient, 0.2), mix_colors(gradient[0.1], gradient[0.6], 0.2))
        assert_col_eq(from_gradient(gradient, 0.3), mix_colors(gradient[0.1], gradient[0.6], 0.4))
        assert_col_eq(from_gradient(gradient, 0.4), mix_colors(gradient[0.1], gradient[0.6], 0.6))
        assert_col_eq(from_gradient(gradient, 0.5), mix_colors(gradient[0.1], gradient[0.6], 0.8))
        assert_col_eq(from_gradient(gradient, 0.6), gradient[0.6])
        assert_col_eq(from_gradient(gradient, 0.7), mix_colors(gradient[0.6], gradient[1], 0.25))
        assert_col_eq(from_gradient(gradient, 0.8), mix_colors(gradient[0.6], gradient[1], 0.5))
        assert_col_eq(from_gradient(gradient, 0.9), mix_colors(gradient[0.6], gradient[1], 0.75))
        assert_col_eq(from_gradient(gradient, 1.0), gradient[1])


if __name__ == '__main__':
    unittest.main()
