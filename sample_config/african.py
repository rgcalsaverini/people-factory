from person_gen.descriptors import PersonCategory, Gradient, \
    PhysicalDescriptors
from sample_config.base import templates, default_descriptors, clothing

eye_colors = {
    0.60: '#000000',
    0.80: '#2b1100',
    0.95: '#845531',
    0.98: '#a06c2c',
    1.0: '#65b98c',
}

african = PersonCategory(
    'african',
    skin_col=Gradient(["#605143", "#775537", "#8f5a2c", "#bb8555"]),
    hair_col=Gradient(["#000000", "#28170b"]),
    iris_col=Gradient(eye_colors),
    physical=PhysicalDescriptors(default_descriptors),
    templates=templates,
    clothing=clothing
)

african.hair.female.add(100, 'curly_fringe', [
    [100, 'afro_back_1'],
    [100, "curly_back"],
    [20, "spiky_back"],
    [20, "small_dlocks_back"],
])

african.hair.female.add(100, 'tied_fringe', [
    [100, 'afro_back_1'],
    [100, "curly_back"],
    [20, "spiky_back"],

])
african.hair.female.add(30, 'spiky_fringe', [
    [100, 'afro_back_1'],
    [100, "curly_back"],
    [20, "spiky_back"],
])
african.hair.female.add(20, 'tied_braids', [
    [100, 'small_dlocks_back'],
])

african.hair.female.add(20, 'straight_fringe3', [
    [100, 'small_dlocks_back'],
])

african.hair.female.add(20, 'dread_locks', [
    [100, 'small_dlocks_back'],
])


african.hair.male.add(100, 'buzz_cut', None)
african.hair.male.add(100, 'army', None)
african.hair.male.add(100, 'short_square', [
    [100, None],
    [100, 'afro_back_2'],
])

african.facial_hair.add(50, 'moustache1')
african.facial_hair.add(100, 'light_beard1')
african.facial_hair.add(50, 'under_lip_1')
african.facial_hair.add(50, 'under_lip_2')
african.facial_hair.add(100, 'goatee_2')
african.facial_hair.add(150, 'corporate_beard')
african.facial_hair.add(80, 'full_beard')
african.facial_hair.add(150, 'moustache2')
african.facial_hair.add(50, 'lampshade_moustache')
african.facial_hair.add(100, 'goatee_3')

