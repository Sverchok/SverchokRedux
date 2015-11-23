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
