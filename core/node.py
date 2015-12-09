import bpy
import inspect
import numpy as np
import collections

from ..ui.node import SvRxNode


def execute_tree(self, context):
    self.id_data.execute()

NodeData = collections.namedtuple("NodeData", ['cls', 'func', 'category', 'inputs', 'outputs'])


def Socket(s_type, name, **kwargs):
    #  1 should match s_type to socket,
    #  2 match to specific subtype
    type_dict = {int: "SvRxIntSocket",
                 float: "SvRxFloatSocket",
                 np.ndarray: "SvRxFloatSocket",
                 list: "SvRxGenericSocket",
                 }
    return type_dict[s_type], name, kwargs


def get_signature(func):
    """
    Return two lists of tuple value with (type, name, dict_of_parameters)
    inputs, outputs
    """
    annotations = func.__annotations__
    sig = inspect.signature(func)
    inputs_template = []
    properties = {}
    items = list(sig.parameters.items())
    for name, parameter in items:
        if isinstance(annotations[name], tuple):  # and annotations[name][0].__name__.endswith("Propery"):
            break
        s = (annotations[name], name, {"default_value": parameter.default})
        inputs_template.append(s)
    for name, parameter in items:
        print(name, parameter, annotations[name])
        if not isinstance(annotations[name], tuple):
            continue
        prop = annotations[name]
        prop[1].update({"name": name,
                        "default": parameter.default,
                        "update": execute_tree})
        properties["svrx_{}".format(name)] = prop
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
