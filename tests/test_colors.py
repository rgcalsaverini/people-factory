import unittest

from person_gen.color import mix_colors, hex2rgb, rgb2hex
from person_gen.descriptors import Gradient, list_to_gradient

_black = (0, 0, 0)
_white = (255, 255, 255)


class TestMixer(unittest.TestCase):
    def test_black(self):
        for i in range(11):
            offset = i / 10.0
            should_be = tuple([int(255 * offset)] * 3)
            color = mix_colors(_black, _white, offset)
            self.assertTupleEqual(color, should_be)

    def test_rgb(self):
        self.assertTupleEqual(mix_colors((255, 0, 0), (0, 0, 0), 0.5), (127, 0, 0))
        self.assertTupleEqual(mix_colors((0, 255, 0), (0, 0, 0), 0.5), (0, 127, 0))
        self.assertTupleEqual(mix_colors((0, 0, 255), (0, 0, 0), 0.5), (0, 0, 127))
        self.assertTupleEqual(mix_colors((255, 0, 0), (0, 255, 128), 0.5), (127, 127, 64))


class TestConversions(unittest.TestCase):
    def test_list_to_gradient(self):
        conversions = [
            [['#000000', '#FFFFFF'], [0.0, 1.0]],
            [['#000000', '#111111', '#222222'], [0.0, 0.5, 1.0]],
            [
                ['#000000', '#111111', '#222222', '#333333'],
                [0.0, 0.33, 0.67, 1.0]
            ],
            [
                ['#000000', '#111111', '#222222', '#333333', '#444444'],
                [0.0, 0.25, 0.5, 0.75, 1.0]
            ],
            [
                ['#000000', '#111111', '#222222', '#333333', '#444444', '#555555'],
                [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
            ],

        ]
        for c in conversions:
            self.assertListEqual(
                [round(p, 2) for p in sorted(list_to_gradient(c[0]).keys())],
                c[1]
            )

    def test_no_conversion_needed(self):
            self.assertEqual(rgb2hex('#FF8800'), '#FF8800')
            self.assertTupleEqual(hex2rgb((123, 233, 0)), (123, 233, 0))

    def test_valid(self):
        colors = {
            '#000000': (0, 0, 0),
            '#FF0000': (255, 0, 0),
            '#00FF00': (0, 255, 0),
            '#0000FF': (0, 0, 255),
            '#FFFFFF': (255, 255, 255),
            '#888888': (136, 136, 136),
            '#102030': (16, 32, 48),
            '#00B5C1': (0, 181, 193),
            '#72C1F4': (114, 193, 244),
            '#88FF00': (136, 255, 0),
        }

        for hex_col, rgb_col in colors.items():
            self.assertTupleEqual(hex2rgb(hex_col), rgb_col)
            self.assertEqual(rgb2hex(rgb_col).lower(), hex_col.lower())

    def test_color_bad_formatted(self):
        colors = {
            '#000000': [(-1, 0, 0), (0, -1, 0), (0, 0, -1), (-45, -9999999, 0)],
            '#FF0000': [(256, 0, 0), (300, 0, 0), (9999999, 0, 0), (255.1, 0, 0)],
            '#880000': [(135.9999999, 0, 0), (136.2, 0, 0)],
        }

        for hex_col, rgb_colors in colors.items():
            for rgb in rgb_colors:
                self.assertEqual(rgb2hex(rgb).lower(), hex_col.lower())

    def test_color_rgb_invalid(self):
        colors = [(1, 2), 'not a color', None, 1, 1.2]

        for rgb_col in colors:
            with self.assertRaises(ValueError):
                rgb2hex(rgb_col)

    def test_color_hex_invalid(self):
        colors = ['123456', '#12345', 'white', '#FFF', 12.0, 7]

        for hex_col in colors:
            with self.assertRaises(ValueError):
                hex2rgb(hex_col)


class TestGradient(unittest.TestCase):
    def test_1col(self):
        gradient = Gradient(['#88FF00'])
        for i in range(11):
            gradient.random_func = lambda: i / 10.0
            self.assertTupleEqual(gradient.random(False), (136, 255, 0))

    def test_2col(self):
        colors = [(100, 0, 255), (50, 137, 1)]
        gradient = Gradient(colors)
        for i in range(11):
            pct = i / 10.0
            gradient.random_func = lambda: pct
            self.assertTupleEqual(gradient.random(False), mix_colors(*colors, offset=pct))

    def test_3col(self):
        colors = [(100, 50, 25), (255, 0, 0), (0, 200, 137)]
        gradient = Gradient(colors)

        for i in range(11):
            pct = i / 10.0
            gradient.random_func = lambda: pct
            col = gradient.random(False)
            if pct == 0:
                self.assertTupleEqual(col, colors[0])
            elif pct < 0.5:
                self.assertTupleEqual(col, mix_colors(colors[0], colors[1], pct * 2))
            elif pct == 0.5:
                self.assertTupleEqual(col, colors[1])
            elif pct < 1:
                self.assertTupleEqual(col, mix_colors(colors[1], colors[2], (pct - 0.5) * 2))
            elif pct == 1:
                self.assertTupleEqual(col, colors[2])

    def test_2shifted(self):
        colors = {0.25: (100, 0, 255), 0.75: (50, 137, 1)}
        gradient = Gradient(colors)
        gradient.random_func = lambda: 0.0
        self.assertTupleEqual(gradient.random(False), colors[0.25])
        gradient.random_func = lambda: 0.1
        self.assertTupleEqual(gradient.random(False), colors[0.25])
        gradient.random_func = lambda: 0.2
        self.assertTupleEqual(gradient.random(False), colors[0.25])
        for i in range(25, 80, 5):
            pct = i / 100.0
            gradient.random_func = lambda: pct
            self.assertTupleEqual(gradient.random(False), mix_colors(colors[0.25], colors[0.75], (pct - 0.25) * 2))
        gradient.random_func = lambda: 0.8
        self.assertTupleEqual(gradient.random(False), colors[0.75])
        gradient.random_func = lambda: 0.9
        self.assertTupleEqual(gradient.random(False), colors[0.75])
        gradient.random_func = lambda: 1.0
        self.assertTupleEqual(gradient.random(False), colors[0.75])


#     def test_dict_3col(self):
#         gradient = {0.1: (100, 50, 25), 0.6: (255, 0, 0), 1: (0, 200, 137)}
#         assert_col_eq(from_gradient(gradient, 0.0), gradient[0.1])
#         assert_col_eq(from_gradient(gradient, 0.05), gradient[0.1])
#         assert_col_eq(from_gradient(gradient, 0.1), gradient[0.1])
#         assert_col_eq(from_gradient(gradient, 0.2), mix_colors(gradient[0.1], gradient[0.6], 0.2))
#         assert_col_eq(from_gradient(gradient, 0.3), mix_colors(gradient[0.1], gradient[0.6], 0.4))
#         assert_col_eq(from_gradient(gradient, 0.4), mix_colors(gradient[0.1], gradient[0.6], 0.6))
#         assert_col_eq(from_gradient(gradient, 0.5), mix_colors(gradient[0.1], gradient[0.6], 0.8))
#         assert_col_eq(from_gradient(gradient, 0.6), gradient[0.6])
#         assert_col_eq(from_gradient(gradient, 0.7), mix_colors(gradient[0.6], gradient[1], 0.25))
#         assert_col_eq(from_gradient(gradient, 0.8), mix_colors(gradient[0.6], gradient[1], 0.5))
#         assert_col_eq(from_gradient(gradient, 0.9), mix_colors(gradient[0.6], gradient[1], 0.75))
#         assert_col_eq(from_gradient(gradient, 1.0), gradient[1])
#
#
if __name__ == '__main__':
    unittest.main()
