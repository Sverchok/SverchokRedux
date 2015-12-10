from SverchokRedux.core.factory import node_factory_from_func
import bpy
import collections
import traceback

# a common lookup table for all nodes
# bl_idname -> NodeData, see core/factory.py

_node_dict = {}


def load_nodes(imported_modules):
    _node_dict.clear()
    nodes = {name: module for name, module in imported_modules.items() if name.startswith("SverchokRedux.nodes.")}
    for name, module in nodes.items():
        if hasattr(module, "SvRxFunc"):
            for func in module.SvRxFunc:
                print("loading{}".format(func.__name__))
                try:
                    node_data = node_factory_from_func(func)
                    _node_dict[node_data.cls.bl_idname] = node_data
                except Exception as err:
                    print("Error: failed to load {}".format(func.__name__))
                    traceback.print_tb(err.__traceback__)


def get_node_data(bl_idname):
    return _node_dict[bl_idname]


def register():
    for node_data in _node_dict.values():
        bpy.utils.register_class(node_data.cls)


def unregister():
    for node_data in _node_dict.values():
        bpy.utils.unregister_class(node_data.cls)
