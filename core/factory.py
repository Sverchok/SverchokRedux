import bpy
import inspect
import numpy as np
import collections

from ..ui.node import SvRxNode, SvRxScriptNode
from ..nodes import svtyping


def execute_tree(self, context):
    #  print(dir(context))
    self.id_data.execute()

NodeData = collections.namedtuple("NodeData", ['cls', 'func', 'category', 'inputs', 'outputs'])


def Socket(s_type, name, **kwargs):
    return svtyping.socket_type(s_type), name, kwargs


def get_signature(func):
    """
    Return two lists of tuple value with (type, name, dict_of_parameters)
    inputs, outputs
    """
    annotations = func.__annotations__
    sig = inspect.signature(func)
    inputs_template = []
    properties = collections.OrderedDict()
    items = list(sig.parameters.items())
    offset = 0
    for name, parameter in items:
        if isinstance(annotations[name], tuple):  # and annotations[name][0].__name__.endswith("Property"):
            break
        s = (annotations[name], name, {"default_value": parameter.default})
        inputs_template.append(s)
        offset += 1

    for name, parameter in items[offset:]:
        func, kwargs = annotations[name]
        defaults = {"name": name,
                    "default": parameter.default,
                    "update": execute_tree}
        for key, value in defaults.items():
            if key not in kwargs:
                kwargs[key] = value
        properties["svrx_{}".format(name)] = (func, kwargs)

    if not inputs_template:
        inputs_template = None
    ret_values = annotations.get("return")
    if ret_values:
        outputs_template = [(socket_type, name) for name, socket_type in ret_values]
    else:
        outputs_template = None
    return inputs_template, outputs_template, properties


def node_factory_from_func(func):
    # classes are named SvRxNodeModuleName
    module_name = func.__module__.split(".")[2].title()
    func_name = func.__name__.title()
    class_name = "SvRxNode{}{}".format(module_name, func_name)

    if module_name == "script":
        bases = (SvRxScriptNode, bpy.types.Node)
    else:
        bases = (SvRxNode, bpy.types.Node)

    inputs, outputs, properties = get_signature(func)
    func.inputs = inputs
    func.outputs = outputs
    node_dict = properties.copy()

    node_dict["bl_idname"] = class_name
    node_dict["bl_label"] = getattr(func, "label", func.__name__).title()
    node_dict["bl_icon"] = 'OUTLINER_OB_EMPTY'

    node_dict["inputs_template"] = [Socket(*data[:2], **data[-1]) for data in inputs] if inputs else None
    node_dict["outputs_template"] = [Socket(*data) for data in outputs] if outputs else None
    node_dict["svrx_props"] = list(properties.keys())

    node_class = type(class_name, bases, node_dict)
    return NodeData(node_class, func, module_name, inputs, outputs)
