from ..nodes import _node_dict
from ..core.factory import node_factory_from_func
from ..ui import menu
import bpy
import bpy.types
import traceback


def register_node(func, register_new=False):
    try:
        node_data = node_factory_from_func(func)
        if register_new:
            if hasattr(bpy.types, node_data.cls.bl_idname):
                bpy.utils.unregister_class(node_data.cls)
            bpy.utils.register_class(node_data.cls)
            _node_dict[node_data.cls.bl_idname] = node_data
            menu.reload_menu()
        else:
            _node_dict[node_data.cls.bl_idname] = node_data

    except Exception as err:
        print("Error: failed to load {}".format(func.__name__))
        traceback.print_tb(err.__traceback__)
        raise err


def node_script(*args, **values):
    def real_node_func(func):
        def annotate(func):
            for key, value in values.items():
                setattr(func, key, value)
            return func
        annotate(func)
        register_node(func, register_new=True)
        return func
    if args and callable(args[0]):
        return real_node_func(args[0])
    else:
        return real_node_func


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
