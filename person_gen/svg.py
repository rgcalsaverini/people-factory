import random
from collections import OrderedDict
from copy import deepcopy
from os import path
from uuid import uuid4
from xml.dom.minidom import parseString as xml_parse

from svgpathtools import CubicBezier, Line, Arc
from svgpathtools.parser import parse_path


def random_id():
    return str(uuid4().hex)


def _resolve_path(filename):
    """Try to guess template path if not found"""
    if path.isfile(filename):
        return filename
    guess = path.join(path.dirname(path.abspath(__file__)), filename)
    if path.isfile(guess):
        return guess

    raise IOError('%s not found.' % filename)


def get_svg_root(node):
    """Get the SVG root from a minidom root node or throws if it is not found"""
    for child in node.childNodes:
        if getattr(child, 'nodeName', None) == 'svg':
            return child
    raise ValueError('No svg found on file')


def get_groups(node):
    """ Get the groups on the SVG or throws if none is found """
    groups = [c for c in node.childNodes if
              getattr(c, 'nodeName', None) == 'g']
    if not groups:
        raise ValueError(
            'No groups found on the svg file. Templates should have at least one.')
    return groups


def attributes_to_dict(attributes):
    return {k: getattr(v, 'value', 'None') for k, v in
            dict(attributes).items()}


def recursively_parse_paths(group):
    paths = OrderedDict()
    attributes = OrderedDict()
    for node in group.childNodes:
        if getattr(node, 'nodeName', None) == 'g':
            child_paths, child_attrs = recursively_parse_paths(node)
            paths.update(child_paths)
            attributes.update(child_attrs)
        elif getattr(node, 'nodeName', None) == 'path':
            node_attrs = attributes_to_dict(node.attributes)
            if 'transform' in node_attrs.keys():
                msg = 'Transform found on %s. Cannot handle transforms'
                raise NotImplementedError(msg)
            if 'inkscape:label' not in node_attrs.keys():
                path_id = random_id()
            else:
                path_id = node_attrs['inkscape:label']
            attributes[path_id] = node_attrs
            paths[path_id] = parse_path(node_attrs.get('d'))
    return paths, attributes


def path_differences(base_path, comp_path):
    differences = dict()

    if len(base_path) != len(comp_path):
        msg = "Paths must have same number of segments, got {} (base) and {}"
        raise ValueError(
            msg.format(len(base_path), len(comp_path))
        )

    for idx in range(len(base_path)):
        segment_1 = base_path[idx]
        segment_2 = comp_path[idx]
        if not isinstance(segment_1, type(segment_2)):
            raise ValueError(
                "Segments of index %d do not have the same type on both paths." % idx)
        if segment_1 == segment_2:
            continue
        if isinstance(segment_1, CubicBezier):
            keys = ['start', 'control1', 'control2', 'end']
        elif isinstance(segment_1, Line):
            keys = ['start', 'end']
        elif isinstance(segment_1, Arc):
            keys = ['start', 'end', 'radius', 'rotation', 'large_arc', 'sweep']
        else:
            raise NotImplementedError(type(segment_1))
        seg_differences = {k: getattr(segment_2, k) - getattr(segment_1, k) for
                           k in keys}
        differences[idx] = seg_differences
    return differences


def apply_transition_to_path(target, transition, amount):
    for seg_idx, changes in transition.items():
        values = {k: getattr(target[seg_idx], k) + amount * changes[k] for k in
                  changes.keys()}
        target[seg_idx] = type(target[seg_idx])(**values)


def split_css(styles):
    return {s.split(':')[0].strip(): s.split(':')[1].strip() for s in
            styles.split(';') if len(s) > 1}


def split_classes(class_str):
    return set([c.strip() for c in class_str.split(' ')])


class TemplateFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.path_attributes = OrderedDict()
        self.default = dict()
        self.layers = dict()
        self.alt_layers = dict()
        self.must_provide = list()
        self._loaded = False
        self.transition_map = dict()
        self.inlays = list()

    def __copy__(self):
        new_one = type(self)(self.filename)
        new_one.__dict__.update(self.__dict__)
        return new_one

    def __deepcopy__(self, memodict={}):
        new_one = type(self)(self.filename)
        new_one.path_attributes = deepcopy(self.path_attributes)
        new_one.default = deepcopy(self.default)
        new_one.layers = deepcopy(self.layers)
        new_one.must_provide = deepcopy(self.must_provide)
        new_one.transition_map = deepcopy(self.transition_map)
        new_one._loaded = self._loaded
        return new_one

    def get_paths(self):
        values = list(self.default.values())

        for inlay in self.inlays:
            position, paths, _ = inlay
            values[position:position] = paths

        return values

    def get_attributes(self, fills=None):
        attributes = list()
        for path_attrs in self.path_attributes.get('default').values():
            new_attr = dict()
            classes = split_classes(path_attrs.get('class', ''))
            fills_in_class = classes.intersection(fills.keys())
            styles = split_css(path_attrs.get('style', ''))

            if fills_in_class:
                new_attr['fill'] = fills[fills_in_class.pop()]
            else:
                new_attr['fill'] = path_attrs.get('fill', None) or styles.get(
                    'fill', '#FF0000')
            new_attr['opacity'] = path_attrs.get('opacity',
                                                 None) or styles.get('opacity',
                                                                     '1')

            attributes.append(new_attr)

        for inlay in self.inlays:
            position, _, inlay_attrs = inlay
            attributes[position:position] = inlay_attrs

        return attributes

    def inlay(self, position, paths, attributes):
        self.inlays.append((position, paths, attributes))

    def load(self):
        print(self.filename)
        file_path = _resolve_path(self.filename)

        with open(file_path, 'r') as svg_in:
            svg_node = get_svg_root(xml_parse(svg_in.read()))

        groups = get_groups(svg_node)
        self._parse_layers(groups)
        if 'default' not in self.layers.keys():
            raise ValueError('Missing \'default\' layer')
        self.default = self.layers['default']
        del self.layers['default']
        self._create_transition_map()
        self._loaded = True

    def _parse_layers(self, groups):
        for group in groups:
            attributes = attributes_to_dict(group.attributes)
            if not attributes.get('inkscape:groupmode', None) == 'layer':
                msg = 'Top-level groups should be layers on templates.'
                raise ValueError(msg)
            layer_name = attributes.get('inkscape:label')
            if layer_name == 'ignore':
                continue
            paths, attributes = recursively_parse_paths(group)
            if not paths:
                raise ValueError('No paths found on the layer.')
            if layer_name[0] == '_':
                layer_name = layer_name.lstrip('_')
                self.must_provide.append(layer_name)
            if layer_name[0] == '%':
                name_bits = layer_name[1:].split(' ')
                if len(name_bits) < 2:
                    msg = "Alternative layer name invalid for '%s' ."
                    raise ValueError(msg % layer_name)
                pct = float(name_bits[0])
                layer_name = name_bits[1]
                self.alt_layers[layer_name] = (pct, paths, name_bits[2:])
                self.path_attributes[layer_name] = attributes
                continue

            self.layers[layer_name] = paths
            self.path_attributes[layer_name] = attributes

    def _create_transition_map(self):
        default_paths = self.default.keys()
        for layer_id, layer_paths in self.layers.items():
            layer_transitions = dict()
            for path_id in set(layer_paths.keys()).intersection(default_paths):
                diff = path_differences(self.default[path_id],
                                        layer_paths[path_id])
                if diff:
                    layer_transitions[path_id] = diff
            if layer_transitions:
                self.transition_map[layer_id] = layer_transitions

    def apply_transitions(self, descriptors=None):
        if not self._loaded:
            self.load()

        descriptors = descriptors or {}

        for transition_id, transition_elements in self.transition_map.items():
            if transition_id in self.must_provide:
                if transition_id not in descriptors.keys():
                    raise KeyError(
                        'Descriptor \'%s\' should be provided' % transition_id)
                amount = descriptors[transition_id]
            else:
                amount = random.uniform(0, 1)
            for element_id, element_paths in transition_elements.items():
                apply_transition_to_path(self.default[element_id],
                                         element_paths, amount)

        selected_alt = []
        alt_layers = list(self.alt_layers.keys())
        random.shuffle(alt_layers)
        for key in alt_layers:
            alt = self.alt_layers[key]
            print(alt[2], key, selected_alt)
            if any([k in selected_alt for k in alt[2]]) or ('*' in alt[2] and len(selected_alt) > 0):
                continue
            if random.uniform(0, 1) < alt[0]:
                selected_alt.append(key)
                self.default.update(alt[1])
                self.path_attributes['default'].update(
                    self.path_attributes[key])
