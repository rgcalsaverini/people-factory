from numpy import random
import math


def upper_bound_value(value_list, value):
    """
    Given a list of increasing weights, return the one that is immediately superior to value
    """
    for i in value_list:
        if value - i < 0:
            return i
    return value_list[-1]


def constrain_pct(pct):
    """
    Return a constrained floating point number between 0 and 1
    """
    if pct < 0:
        return 0.0
    if pct > 1:
        return 1.0
    return float(pct)


def constrain_col(col_tuple):
    """
    Return a constrained 3-number tuple between 0 and 255
    """
    res = []
    for col in col_tuple:
        if col < 0:
            res.append(0)
        elif col > 255:
            res.append(255)
        else:
            res.append(int(col))
    return tuple(res)


def from_gradient(gradient, offset=None, random_function=None, mixer=None):
    """
    Pick an intermediary color from a gradient.

    :param gradient:        The color gradient. It can be a list of RGB color tuples, on which case all colors will be
                            treated as equidistant on the gradient, or a dictionary where the offsets are on the keys.
    :param offset:          Optional position inside the gradient. If not provided will pick a random one.
    :param random_function: The function that generates the random offset between 0 and 1.
    :param mixer            The function that will mix two colors given the said two plus an offset
    :return:                a RGB color tuple
    """
    random_function = random_function or random.uniform
    offset = offset if offset is not None else random_function()

    if isinstance(gradient, list):
        if len(gradient) == 1:
            return constrain_col(gradient[0])
        if len(gradient) == 2:
            idx_a, idx_b = 0, 1
        else:
            color_length = 1 / (len(gradient) - 1)
            offset_by_length = offset / color_length
            idx_b = math.ceil(offset_by_length) or 1
            idx_a = idx_b - 1
            offset = offset_by_length - idx_a
    elif isinstance(gradient, dict):
        offset_list = sorted(gradient.keys())

        if len(offset_list) == 1:
            return constrain_col(gradient[0])
        if len(gradient) == 2:
            idx_a, idx_b = offset_list[0], offset_list[-1]
            offset = constrain_pct((offset - offset_list[0]) / (offset_list[1] - offset_list[0]))
        else:
            idx_b = upper_bound_value(offset_list, offset)
            idx_a = offset_list[offset_list.index(idx_b) - 1]
            offset = constrain_pct((offset - idx_a) / (idx_b - idx_a))
    else:
        raise ('Invalid type {} for gradient'.format(type(gradient)))

    return mix_colors(gradient[idx_a], gradient[idx_b], offset)


def mix_colors(color_a, color_b, offset):
    """Mix two colors given an offset. 0 offset means 100% color a and 1 means 100% color b"""
    return constrain_col([color_a[i] * (1 - offset) + color_b[i] * offset for i in range(3)])


def hex2rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb.
    Extracted from :https://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
    """
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb2hex(color):
    """Return color as #rrggbb for the given color values.
    Extracted from :https://stackoverflow.com/questions/214359/converting-hex-color-to-rgb-and-vice-versa
    """
    return '#%02x%02x%02x' % (color[0], color[1], color[2])


def get_value(color):
    return sum(color) / 765.0


def get_hue(color):
    return (max(color) - min(color)) / 255.0


def get_saturation(color):
    color_value = get_value(color)

    if color_value == 1:
        return 0
    color_hue = get_hue(color)
    return color_hue / (1 - abs(2 * color_value - 1))


def change_value(color, pct):
    return constrain_col([(int(c * (1 + pct))) for c in color])

# "0": "#ebb8af", "0.2": "#e8c9c9", "0.4": "#f4d7ce", "0.6": "#ffe2db", "0.8": "#ffd5e1", "1": "#ffc8ce"
