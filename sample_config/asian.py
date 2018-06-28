from person_gen.descriptors import PersonCategory, Gradient, \
    PhysicalDescriptors
from sample_config.base import templates, default_descriptors, clothing

asian_hair = {
    0: '#000000',
    0.6: '#28170b',
    0.85: '#3c2210',
    0.97: '#784421',
}
iris = {
    0.7: '#2b1100',
    0.9: '#2b1100',
    1.0: '#845531',
}

asian = PersonCategory(
    'asian',
    skin_col=Gradient(['#f4dcc4', '#edd8ae', '#edd8ae', '#dac8a8']),
    hair_col=Gradient(asian_hair),
    iris_col=Gradient(asian_hair),
    physical=PhysicalDescriptors(
        default_descriptors,
        chin=0,
        eye_size=(0.9, 0.2),
    ),
    templates=templates,
    clothing=clothing,
)

basic_back = [
    [100, 'loose_straight'],
    [50, 'bun'],
    [50, 'spiky_back']
]

asian.hair.female.add(150, 'tied_fringe', basic_back)
asian.hair.female.add(150, 'straight_fringe', basic_back)
asian.hair.female.add(150, 'straight_fringe2', basic_back)
asian.hair.female.add(150, 'straight_fringe3', basic_back)
asian.hair.female.add(150, 'spiky_fringe', [
    [20, 'loose_straight'],
    [100, 'spiky_back'],
])
asian.hair.female.add(150, 'curly_fringe', [
    [50, 'loose_straight'],
    [50, 'bun'],
    [50, 'spiky_back'],
])

asian.hair.male.add(100, 'straight_fringe3', [[100, 'short_straight']])
asian.hair.male.add(100, 'buzz_cut')
asian.hair.male.add(100, 'army')
asian.hair.male.add(100, 'short_sides')
asian.hair.male.add(100, 'pompadour')
