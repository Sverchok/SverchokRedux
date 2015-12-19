import bpy
from ..core.factory import node_factory_from_func
import bpy.types
import traceback

# the dict is populated from the register_node called via @node_func
# decorator

_node_dict = {}

# collect new nodes during import
_new_nodes = []


def register_node(func, register_new=False):
    try:
        node_data = node_factory_from_func(func)

        if register_new:
            cls = node_data.cls
            bl_idname = cls.bl_idname
            if bl_idname in _node_dict:
                bpy.utils.unregister_class(_node_dict[bl_idname].cls)
                del _node_dict[bl_idname]
            bpy.utils.register_class(node_data.cls)
            _node_dict[node_data.cls.bl_idname] = node_data
            _new_nodes.append(bl_idname)
        else:
            _node_dict[node_data.cls.bl_idname] = node_data

    except Exception as err:
        print("Error: failed to load {}".format(func.__name__))
        traceback.print_tb(err.__traceback__)
        raise err


def get_node_data(bl_idname):
    return _node_dict[bl_idname]


def get_new_nodes():
    tmp = _new_nodes[:]
    _new_nodes.clear()
    return tmp


def register():
    for node_data in _node_dict.values():
        bpy.utils.register_class(node_data.cls)


def unregister():
    for node_data in _node_dict.values():
        bpy.utils.unregister_class(node_data.cls)
