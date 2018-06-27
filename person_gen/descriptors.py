from numpy.random import normal as normal_random, uniform as uniform_random
from svgpathtools import wsvg

from person_gen.color import hex2rgb, rgb2hex, transform_color, mix_colors
from person_gen.utils import roulette_random, upper_bound_value, bounded_pct, \
    apply_map
from .svg import TemplateFile


def list_to_gradient(source):
    if len(source) == 1:
        return {0: hex2rgb(source[0])}
    step = 1.0 / (len(source) - 1.0)
    gradient = {(step * i): hex2rgb(s) for i, s in enumerate(source[:-1])}
    gradient[1] = hex2rgb(source[-1])
    return gradient


class Gradient(object):
    def __init__(self, colors, random_func=None):
        self.random_func = random_func or (lambda: uniform_random(0, 1))
        if isinstance(colors, list):
            self.colors = list_to_gradient(colors)
        elif isinstance(colors, dict):
            self.colors = {float(k): hex2rgb(v) for k, v in colors.items()}
        else:
            raise TypeError('Invalid gradient of type %s' % type(colors))

    def random(self, as_hex=True):
        offset = self.random_func()
        offset_list = sorted(self.colors.keys())

        if len(offset_list) == 0:
            raise ValueError('Empty gradient')
        if len(offset_list) == 1:
            color = self.colors[offset_list[0]]
        else:
            if len(offset_list) == 2:
                idx_a = offset_list[0]
                idx_b = offset_list[1]

            else:
                idx_b = upper_bound_value(offset_list, offset)
                idx_a = offset_list[offset_list.index(idx_b) - 1]
            offset = bounded_pct((offset - idx_a) / (idx_b - idx_a))
            color_a = self.colors[idx_a]
            color_b = self.colors[idx_b]
            color = mix_colors(color_a, color_b, offset)
        if as_hex:
            return rgb2hex(color)
        return color


class PhysicalDescriptors(object):
    def __init__(self, base, **extra):
        combined = base.copy()
        for key, value in extra.items():
            combined.update({key: value})
        self.static = {k: v for k, v in combined.items() if not callable(v)}
        self.dynamic = {k: v for k, v in combined.items() if callable(v)}

    def random(self):
        values = {}
        for key, val in self.static.items():
            values[key] = self._gen_static_value(val)
        for key, val in self.dynamic.items():
            values[key] = val(values)
        return values

    @staticmethod
    def _gen_static_value(descriptor):
        if isinstance(descriptor, (list, tuple)):
            value = normal_random(*descriptor)
        else:
            value = int(uniform_random(0, 1) < descriptor)
        return value


class GenderGroup(object):
    def __init__(self, container_class):
        self.male = container_class()
        self.female = container_class()


class Hairstyles(object):
    def __init__(self):
        self.values = []

    def add(self, weight, front=None, backs=None):
        self.values.append([weight, [front, backs]])

    def random(self):
        if not self.values:
            return None, None
        front = roulette_random(self.values)
        front_id = front[0]
        back_id = roulette_random(front[1]) if front[1] else None
        return front_id, back_id if back_id else None


class PersonCategory(object):
    def __init__(self, category_name, skin_col=None, hair_col=None,
                 physical=None, templates=None, gender_ratio=None):
        self.category_name = category_name
        self.skin_col = skin_col
        self.hair_col = hair_col
        self.physical = physical
        self.hair = GenderGroup(Hairstyles)
        self.templates = templates
        self.gender_ratio = gender_ratio or 0.5

    def _random_gender(self):
        if uniform_random(0, 1) < self.gender_ratio:
            return 'male'
        return 'female'

    def random(self):
        gender = self._random_gender()
        skin_col = self.skin_col.random()
        hair_col = self.hair_col.random()
        hair_ids = getattr(self.hair, gender).random()
        hair = apply_map(hair_ids, self.templates)
        physical = self.physical.random()
        portrait = self.templates['portrait']
        return Person(gender, skin_col, hair_col, hair, physical, portrait)


class Person(object):
    def __init__(self, gender, skin_col, hair_col, hair, physical, portrait):
        self.gender = gender
        self.skin_col = skin_col
        self.hair_col = hair_col
        self.hair_templates = hair
        self.physical = physical
        self._portrait = TemplateFile(portrait)

    def make_portrait(self):
        self._portrait.apply_transitions(self.physical)
        self._inlay_template(self.hair_templates[0], 8)
        self._inlay_template(self.hair_templates[1], 1)

    def _inlay_template(self, template, position):
        if template is None:
            return
        template = TemplateFile(template)
        template.load()
        template.apply_transitions(self.physical)
        paths = template.get_paths()
        fills = template.get_attributes({'hair': self.hair_col})
        self._portrait.inlay(position, paths, fills)

    def export_svg(self, filename):
        paths = self._portrait.get_paths()
        attributes = self._portrait.get_attributes({
            'skin': self.skin_col,
            'dark_skin': transform_color(self.skin_col, val=-0.2),
            'body': transform_color(self.skin_col, val=-0.1),
        })
        wsvg(paths, attributes=attributes, filename=filename, margin_size=0)
