from ..nodes import _node_dict
from SverchokRedux.core.factory import node_factory_from_func
import bpy
import traceback

def register_node(func):
    try:
        node_data = node_factory_from_func(func)
        _node_dict[node_data.cls.bl_idname] = node_data
    except Exception as err:
        print("Error: failed to load {}".format(func.__name__))
        traceback.print_tb(err.__traceback__)


def node_func(*args, **values):
    def real_node_func(func):
        def annotate(func):
            for key, value in values.items():
                setattr(func, key, value)
            return func
        annotate(func)
        register_node(func)
        return func
    if args and callable(args[0]):
        return real_node_func(args[0])
    else:
        return real_node_func
