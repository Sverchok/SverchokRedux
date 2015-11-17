import bpy
import inspect
import numpy as np
from bpy.types import EnumProperty

"""
From sverchok, by zeffi
"""

def find_enumerators(node):
    ignored_enums = ['bl_icon', 'bl_static_type', 'type']
    node_props = node.bl_rna.properties[:]
    f = filter(lambda p: isinstance(p, EnumProperty), node_props)
    return [p.identifier for p in f if not p.identifier in ignored_enums]

class SvRxNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in {'SvRxTreeType'}

    def init(self, context):
        if self.inputs_template:
            for socket_type, name, args in self.inputs_template:
                s = self.inputs.new(socket_type, name)
                if "default_value" in args:
                    s.default_value = args["default_value"]

        if self.outputs_template:
            for socket_type, name, args in self.outputs_template:
                self.outputs.new(socket_type, name)

    def update(self):
        pass

    def serialize(self):
        node_dict = {}
        node_items = {}
        node_enums = find_enumerators(self)

        for k, v in self.items():
            if isinstance(v, (float, int, str)):
                node_items[k] = v
            else:
                node_items[k] = v[:]
            if k in node_enums:
                v = getattr(self, k)
                node_items[k] = v

        node_dict['params'] = node_items
        node_dict['location'] = self.location[:]
        node_dict['bl_idname'] = self.bl_idname
        node_dict['height'] = self.height
        node_dict['width'] = self.width
        node_dict['label'] = self.label
        node_dict['hide'] = self.hide
        node_dict['color'] = self.color[:]

        node_dict['inputs'] = [s.serialize() for s in self.inputs]
        node_dict['outputs'] = [s.serialize() for s in self.outputs]

        return node_dict

    def load(self, node_data):
        # needs more details
        self.location = node_data["location"]

def Socket(s_type, name, **kwargs):
    #  1 should match s_type to socket,
    #  2 match to specific subtype
    type_dict = {int: "SvRxIntSocket",
                 float: "SvRxFloatSocket",
                 np.array: "SvRxFloatSocket",
                 list: "SvRxGenericSocket",
                 }
    return type_dict[s_type], name, kwargs


def node_factory_from_func(func):
    annotations = func.__annotations__
    if not annotations:
        return None
    class_name = "SvRxNode{}".format(func.__name__)
    bases = (SvRxNode, bpy.types.Node)

    sig = inspect.signature(func)
    inputs_template = []
    for name, parameter in sig.parameters.items():
        s = Socket(annotations[name], name, default_value=parameter.default)
        inputs_template.append(s)

    node_dict = {}

    ret_values = annotations["return"]
    if ret_values:
        outputs_template = [Socket(socket_type, name) for name, socket_type in ret_values]
        node_dict["outputs_template"] = outputs_template
    else:
        node_dict["outputs_template"] = None

    node_dict["bl_idname"] = class_name
    node_dict["bl_label"] = getattr(func, "label", func.__name__)
    node_dict["bl_icon"] = 'OUTLINER_OB_EMPTY'
    node_dict["inputs_template"] = inputs_template

    node_class = type(class_name, bases, node_dict)
    return node_class
