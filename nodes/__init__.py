from SverchokRedux.core.node import node_factory_from_func
import bpy
import collections

NodeData = collections.namedtuple("NodeData", ['cls', 'func', 'category'])

node_dict = {}


def load_nodes(imported_modules):
    nodes = {name: module for name, module in imported_modules.items() if name.startswith("SverchokRedux.nodes.")}
    for name, module in nodes.items():
        if hasattr(module, "SvRxFunc"):
            for func in module.SvRxFunc:
                cls = node_factory_from_func(func)
                cat = module.__name__.split(".")[-2]
                node_dict[cls.bl_idname] = NodeData(cls, func, cat)


def register():
    for node_data in node_dict.values():
        bpy.utils.register_class(node_data.cls)


def unregister():
    for node_data in node_dict.values():
        bpy.utils.unregister_class(node_data.cls)
