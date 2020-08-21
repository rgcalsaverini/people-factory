from person_gen.descriptors import Gradient

templates = {
    'portrait': './templates/portrait.svg',
    'straight_fringe': './templates/fhair_1.svg',
    'straight_fringe2': './templates/fhair_3.svg',
    'straight_fringe3': './templates/fhair_5.svg',
    'tied_fringe': './templates/fhair_2.svg',
    'spiky_fringe': './templates/fhair_4.svg',
    'buzz_cut': './templates/fhair_6.svg',
    'army': './templates/fhair_7.svg',
    'short_sides': './templates/fhair_8.svg',
    'pompadour': './templates/fhair_9.svg',
    'curly_fringe': './templates/fhair_10.svg',
    'short_square': './templates/fhair_12.svg',
    'tied_braids': './templates/fhair_13.svg',
    'dread_locks': './templates/fhair_14.svg',
    'loose_straight': './templates/bhair_1.svg',
    'short_straight': './templates/bhair_4.svg',
    'bun': './templates/bhair_2.svg',
    'spiky_back': './templates/bhair_3.svg',
    'curly_back': './templates/bhair_5.svg',
    'afro_back_1': './templates/bhair_6.svg',
    'afro_back_2': './templates/bhair_7.svg',
    'small_dlocks_back': './templates/bhair_8.svg',

    'moustache1': './templates/fac_hair_1.svg',
    'light_beard1': './templates/fac_hair_2.svg',
    'under_lip_1': './templates/fac_hair_3.svg',
    'under_lip_2': './templates/fac_hair_4.svg',
    'goatee_1': './templates/fac_hair_5.svg',
    'goatee_2': './templates/fac_hair_6.svg',
    'corporate_beard': './templates/fac_hair_7.svg',
    'full_beard': './templates/fac_hair_8.svg',
    'moustache2': './templates/fac_hair_9.svg',
    'lampshade_moustache': './templates/fac_hair_10.svg',
    'goatee_3': './templates/fac_hair_11.svg',

    'mal_pull_shirt_1': './templates/clothing/male_pro_1.svg',
    'mal_pull_shirt_2': './templates/clothing/male_pro_4.svg',
    'mal_shirt_1': './templates/clothing/male_pro_2.svg',
    'mal_shirt_2': './templates/clothing/male_pro_3.svg',
    'mal_shirt_no_tie_1': './templates/clothing/male_pro_5.svg',
    'mal_t_shirt_1': './templates/clothing/male_inf_1.svg',

    'fem_pull_shirt_1': './templates/clothing/fem_pro_1.svg',
    'fem_shirt_1': './templates/clothing/fem_pro_2.svg',
    'fem_t_shirt_1': './templates/clothing/fem_inf_1.svg',

    'fem_earrings_1': './templates/clothing/fem_earrings_1.svg',
    'glasses_1': './templates/clothing/glasses_1.svg',
    'glasses_2': './templates/clothing/glasses_2.svg',
}

bright_colors = ['#4d4d4d', '#0044aa', '#c83737', '#a05a2c', '#d4aa00',
                 '#44aa00', '#37abc8']
light_colors = {0.5: '#FFFFFF', 0.66: '#d5f6ff', 0.83: '#ffd5d5',
                1.0: '#f4e3d7'}

tshirt = {
    0.00: '#000000',
    0.40: '#FFFFFF',
    0.46: '#c83737',
    0.52: '#ff8080',
    0.58: '#ff6600',
    0.64: '#ffcc00',
    0.70: '#55d400',
    0.76: '#165016',
    0.82: '#00ccff',
    0.88: '#0066ff',
    0.94: '#002255',
    1.00: '#002255',

}

default_descriptors = {
    'cheek': (0.3, 0.18),
    'cheek_low': lambda d: d['cheek'] * 2 if d['cheek'] < 0.5 else 0,
    'cheek_high': lambda d: (d['cheek'] - 0.5) * 2 if d['cheek'] > 0.5 else 0,
    'chin': (0.5, 0.15),
    'ear_size': (0.0, 0.3),
    'eye_size': (0.25, 0.12),
    'eye_height': (0.5, 0.2),
    'eye_distance': (0.5, 0.2),
}

jewell_colors = {
    0.3: '#FFFFFF',
    0.5: '#ffcc00',
    0.79: '#ffcc00',
    0.8: '#d40000',
    0.9: '#5aa02c',
    1.0: '#0066ff',
}

clothing = [
    [100, {
        'tid': 'mal_pull_shirt_1',
        'labels': ['male', 'basic'],
        'colors': [
            Gradient(light_colors),
            Gradient(bright_colors),
            Gradient(bright_colors),
        ]
    }],
    [100, {
        'tid': 'mal_pull_shirt_2',
        'labels': ['male', 'basic'],
        'colors': [
            Gradient(light_colors),
            Gradient(bright_colors),
            Gradient(bright_colors),
        ]
    }],
    [100, {
        'tid': 'mal_shirt_1',
        'labels': ['male', 'basic'],
        'colors': [Gradient(light_colors)]
    }],
    [100, {
        'tid': 'mal_shirt_no_tie_1',
        'labels': ['male', 'basic'],
        'colors': [Gradient(light_colors)]
    }],
    [100, {
        'tid': 'mal_shirt_no_tie_1',
        'labels': ['male', 'basic'],
        'colors': [Gradient(bright_colors)]
    }],
    [100, {
        'tid': 'mal_shirt_1',
        'labels': ['male', 'basic'],
        'colors': [Gradient(bright_colors)]
    }],
    [200, {
        'tid': 'mal_shirt_2',
        'labels': ['male', 'basic'],
        'colors': [Gradient(light_colors), Gradient(bright_colors)]
    }],
    [100, {
        'tid': 'fem_pull_shirt_1',
        'labels': ['female', 'basic'],
        'colors': [
            Gradient(light_colors),
            Gradient(bright_colors),
            Gradient(jewell_colors)
        ]
    }],
    [150, {
        'tid': 'mal_t_shirt_1',
        'labels': ['male', 'basic'],
        'colors': [Gradient(tshirt), Gradient(tshirt)]
    }],

    [150, {
        'tid': 'fem_t_shirt_1',
        'labels': ['female', 'basic'],
        'colors': [Gradient(tshirt), Gradient(tshirt)]
    }],
    [100, {
        'tid': 'fem_shirt_1',
        'labels': ['female', 'basic'],
        'colors': [Gradient(light_colors)]
    }],
    [100, {
        'tid': 'fem_shirt_1',
        'labels': ['female', 'basic'],
        'colors': [Gradient(bright_colors)]
    }],

    [100, {
        'tid': 'fem_earrings_1',
        'labels': ['female', 'ear'],
        'colors': [Gradient(jewell_colors)]
    }],
    [20, {
        'tid': 'glasses_1',
        'labels': ['female', 'male', 'eye'],
        'colors': []
    }],
    [100, {
        'tid': 'glasses_2',
        'labels': ['female', 'male', 'eye'],
        'colors': []
    }],
]
