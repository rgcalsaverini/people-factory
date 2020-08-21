from person_gen.descriptors import PersonCategory, Gradient, \
    PhysicalDescriptors
from sample_config.base import templates, default_descriptors, clothing

eye_colors = {
    0.0: '#2b1100',
    0.25: '#2b1100',
    0.4: '#845531',
    0.55: '#845531',
    0.58: '#a06c2c',
    0.6: '#6581b9',
    0.8: '#6f918a',
    1.0: '#65b98c',

}

european = PersonCategory(
    'asian',
    skin_col=Gradient(["#e8c9c9", "#f4d7ce", "#ffc8ce", "#ffe2db"]),
    hair_col=Gradient(["#28170b", "#784421", "#926a45", "#ffdd55"]),
    iris_col=Gradient(eye_colors),
    physical=PhysicalDescriptors(default_descriptors),
    templates=templates,
    clothing=clothing,
)

european.hair.female.add(100, 'curly_fringe', [
    [100, "curly_back"],
    [50, "bun"],
    [50, "loose_straight"],
    [50, "spiky_back"],
])

european.hair.female.add(50, 'spiky_fringe', [
    [100, "loose_straight"],
    [100, "spiky_back"],
    [100, "curly_back"],
    [10, "bun"],
])

european.hair.female.add(50, 'straight_fringe', [
    [100, "loose_straight"],
    [50, "bun"],
    [50, "spiky_back"],
])

european.hair.male.add(100, 'buzz_cut', None)
european.hair.male.add(100, 'short_sides')
european.hair.male.add(100, 'pompadour')
european.hair.male.add(70, 'army', None)
european.hair.male.add(70, 'short_square')

european.facial_hair.add(50, 'moustache1')
european.facial_hair.add(100, 'light_beard1')
european.facial_hair.add(50, 'under_lip_1')
european.facial_hair.add(50, 'under_lip_2')
european.facial_hair.add(20, 'goatee_1')
european.facial_hair.add(50, 'goatee_2')
european.facial_hair.add(150, 'corporate_beard')
european.facial_hair.add(50, 'full_beard')
european.facial_hair.add(150, 'moustache2')
european.facial_hair.add(80, 'lampshade_moustache')
european.facial_hair.add(50, 'goatee_3')
