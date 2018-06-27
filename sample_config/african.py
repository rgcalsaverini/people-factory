from person_gen.descriptors import PersonCategory, Gradient, \
    PhysicalDescriptors
from sample_config.base import templates, default_descriptors

african = PersonCategory(
    'african',
    skin_col=Gradient(["#605143", "#775537", "#8f5a2c", "#bb8555"]),
    hair_col=Gradient(["#000000", "#28170b"]),
    physical=PhysicalDescriptors(default_descriptors),
    templates=templates,
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
# african.hair.male.add(100, 'dread_locks', [
#     [100, 'small_dlocks_back'],
# ])
# african.hair.female.add(100, 'dread_locks', [
#     [100, 'small_dlocks_back'],
# ])
