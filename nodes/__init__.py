import bpy
import collections
import traceback

# the dict is populated from the decorator @node_func
_node_dict = {}


def get_node_data(bl_idname):
    return _node_dict[bl_idname]


def register():
    for node_data in _node_dict.values():
        bpy.utils.register_class(node_data.cls)


def unregister():
    for node_data in _node_dict.values():
        bpy.utils.unregister_class(node_data.cls)
