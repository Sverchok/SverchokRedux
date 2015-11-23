import bpy
import inspect
import numpy as np
from ..ui.node import SvRxNode


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
    for name, parameter in sig.parameters.items():
        s = (annotations[name], name, default_value=parameter.default)
        inputs_template.append(s)

    if not inputs_template:
        inputs_template = None

    ret_values = annotations.get("return")
    if ret_values:
        outputs_template = [(socket_type, name) for name, socket_type in ret_values]
        node_dict["outputs_template"] = outputs_template
    else:
        node_dict["outputs_template"] = None


def node_factory_from_func(func):
    # classes are named SvRxNodeModuleName
    class_name = "SvRxNode{}{}".format(func.__module__.split(".")[2].title(), func.__name__.title())
    bases = (SvRxNode, bpy.types.Node)

    inputs_template, outputs_template = get_signature(func)

    node_dict = {}

    node_dict["bl_idname"] = class_name
    node_dict["bl_label"] = getattr(func, "label", func.__name__).topic()
    node_dict["bl_icon"] = 'OUTLINER_OB_EMPTY'

    node_dict["inputs_template"] = [Socket(*data) for data in inputs] if inputs_template else None
    node_dict["outputs_template"] = [Socket(*data) for data in outputs] if outputs_template else None

    node_class = type(class_name, bases, node_dict)
    return node_class
