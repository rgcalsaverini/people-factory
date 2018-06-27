from person_gen.utils import bounded


def hex2rgb(color):
    """
    Return (red, green, blue) for the color given as #rrggbb.
    """
    if isinstance(color, tuple) and len(color) == 3:
        return color
    if not isinstance(color, str) or color[0] != '#':
        raise ValueError("Invalid hex color '%s'" % str(color))
    color = color.lstrip('#')
    lv = len(color)
    if lv != 6:
        raise ValueError("Invalid hex color '%s'" % str(color))
    return tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb2hex(color):
    """
    Return color as #rrggbb for the given color values.
    """
    if isinstance(color, str) and len(color) == 7 and color[0] == '#':
        return color
    if not isinstance(color, tuple) or len(color) != 3:
        raise ValueError("Invalid rgb color '%s'" % str(color))
    cols = [bounded_col(round(c)) for c in color]
    return '#%02x%02x%02x' % (cols[0], cols[1], cols[2])


def transform_color(inpt_color, hue=None, sat=None, val=None):
    if hue or sat:
        raise NotImplementedError('Not yet implemented')
    if isinstance(inpt_color, str):
        color = hex2rgb(inpt_color)
        was_hex = True
    else:
        color = inpt_color
        was_hex = False
    new_col = bounded_col(tuple([c * (1 + val) for c in color]))

    if was_hex:
        return rgb2hex(new_col)
    return new_col


# def get_value(color):
#     return sum(color) / 765.0
#
#
# def get_hue(color):
#     return (max(color) - min(color)) / 255.0
#
#
# def get_saturation(color):
#     color_value = get_value(color)
#
#     if color_value == 1:
#         return 0
#     color_hue = get_hue(color)
#     return color_hue / (1 - abs(2 * color_value - 1))
def bounded_col(val):
    return bounded(val, 255, 0, int)


def mix_colors(color_a, color_b, offset):
    """
    Mix two colors given an offset.
    0 offset means 100% color a and 1 means 100% color b
    """
    col = [color_a[i] * (1 - offset) + color_b[i] * offset for i in range(3)]
    return bounded_col(tuple(col))
