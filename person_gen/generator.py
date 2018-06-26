from person_gen.person import PersonCategory
import json
from numpy import random
from copy import deepcopy

from .miscutils import roulette_random
from .svg import TemplateFile


class ResourcePool(object):
    def __init__(self, config):
        self.config = config


class Generator(object):
    def __init__(self, male_to_female=None, category_frequency=None, categories=None):
        self.male_to_female = male_to_female
        self.category_frequency = category_frequency
        self.categories = categories or dict()
        self.portrait = None

    @staticmethod
    def from_file(filename):
        with open(filename, 'r') as conf_file:
            json_data = json.loads(conf_file.read())
        new_generator = Generator(json_data.get('male_to_female'), json_data.get('category_frequency'))

        for categ_id, categ_info in json_data.get('categories').items():
            templates = json_data.get('templates')
            new_generator.categories[categ_id] = PersonCategory.from_dict(categ_id, templates, categ_info)

        new_generator.portrait = TemplateFile(json_data.get('templates').get('portrait'))
        new_generator.portrait.load()
        return new_generator

    def random_person(self):
        gender = 'male' if random.uniform(0, 1) < self.male_to_female else 'female'
        category_id = roulette_random(self.category_frequency)
        portrait = deepcopy(self.portrait)
        return self.categories[category_id].new_person(gender, portrait)
