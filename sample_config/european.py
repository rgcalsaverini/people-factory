from person_gen.descriptors import PersonCategory, Gradient, \
    PhysicalDescriptors
from sample_config.base import templates, default_descriptors

european = PersonCategory(
    'asian',
    skin_col=Gradient(["#e8c9c9", "#f4d7ce", "#ffc8ce", "#ffe2db"]),
    hair_col=Gradient(["#28170b", "#784421", "#926a45", "#ffdd55"]),
    physical=PhysicalDescriptors(default_descriptors),
    templates=templates,
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
