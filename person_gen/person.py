from numpy import random
from svgpathtools import wsvg

from .color import from_gradient, hex2rgb, rgb2hex, change_value
from .miscutils import roulette_random
from .svg import TemplateFile


class PersonCategory(object):
    def __init__(self,
                 categ_id,
                 pretty_name=None,
                 skin_gradient=None,
                 hair_gradient=None,
                 physical_descriptors=None,
                 templates=None,
                 hairstyle=None):
        self.categ_id = categ_id
        self.pretty_name = pretty_name or categ_id.title()
        self.skin_gradient = skin_gradient
        self.hair_gradient = hair_gradient
        self.physical_descriptors = {
            'chin': (0.3, 0.18),
            'cheek': (0.5, 0.15),
            'ear_size': (0.0, 0.3),

        }
        self.physical_descriptors.update(physical_descriptors)
        self.hairstyle = hairstyle
        self.templates = templates

    @staticmethod
    def from_dict(categ_id, templates, data_dict):
        return PersonCategory(
            categ_id=categ_id,
            pretty_name=data_dict.get('pretty_name', categ_id.title()),
            skin_gradient=json_to_gradient(data_dict.get('skin_gradient')),
            hair_gradient=json_to_gradient(data_dict.get('hair_gradient')),
            physical_descriptors=data_dict.get('physical_descriptors'),
            templates=templates,
            hairstyle=data_dict.get('hairstyle'),
        )

    def new_person(self, gender, portrait):
        descriptors = dict()
        for key, info in self.physical_descriptors.items():
            if isinstance(info, float) or isinstance(info, int):
                value = random.uniform() < info
            elif isinstance(info, tuple) or isinstance(info, set) or isinstance(info, list):
                value = random.normal(*info)
            else:
                continue
            descriptors[key] = value

        hairstyle = roulette_random(self.hairstyle[gender])
        front_hair_id = hairstyle[0]
        back_hair_id = roulette_random(hairstyle[1])
        descriptors['front_hair'] = self.templates[front_hair_id]['file'] if front_hair_id else None
        descriptors['back_hair'] = self.templates[back_hair_id]['file'] if back_hair_id else None

        print(self.categ_id, self.skin_gradient)

        return Person(
            descriptors=descriptors,
            gender=gender,
            skin_color=from_gradient(self.skin_gradient),
            hair_color=from_gradient(self.hair_gradient),
            portrait=portrait,
        )


def json_to_gradient(json_gradient):
    if isinstance(json_gradient, list):
        return [hex2rgb(c) for c in json_gradient]
    elif isinstance(json_gradient, dict):
        return {float(v): hex2rgb(c) for v, c in json_gradient.items()}
    raise ValueError('Unknown color gradient format')


def get_template_and_inlay(target, position, template_name, descriptors, fills):
    template = TemplateFile(template_name)
    template.load()
    template.apply_transitions(descriptors)
    target.inlay(position, template.get_paths(), template.get_attributes(fills))


class Person(object):
    def __init__(self, descriptors, gender, skin_color, hair_color, portrait):
        self.descriptors = descriptors
        self.gender = gender
        self.skin_color = skin_color
        self.hair_color = hair_color
        self.portrait = portrait

    def make_portrait(self):
        descriptors = self.descriptors
        descriptors['cheek_low'] = descriptors['cheek'] * 2 if descriptors['cheek'] < 0.5 else 0
        descriptors['cheek_high'] = (descriptors['cheek'] - 0.5) * 2 if descriptors['cheek'] > 0.5 else 0
        self.portrait.apply_transitions(descriptors)
        fill = {'hair': rgb2hex(self.hair_color)}

        if descriptors['front_hair']:
            get_template_and_inlay(self.portrait, 8, descriptors['front_hair'], descriptors, fill)

        if descriptors['back_hair']:
            get_template_and_inlay(self.portrait, 1, descriptors['back_hair'], descriptors, fill)

    def export_portrait(self, filename):
        wsvg(self.portrait.get_paths(),
             attributes=self.portrait.get_attributes({
                 'skin': rgb2hex(self.skin_color),
                 'body': rgb2hex(change_value(self.skin_color, -0.1))}),
             filename=filename)
