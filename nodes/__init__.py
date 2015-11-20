from SverchokRedux.core.node import node_factory_from_func
import bpy
import collections

NodeData = collections.namedtuple("NodeData", ['cls', 'func'])

node_dict = {}


def load_nodes():
    # this should really be either automatic or more organized
    funcs = [math.linspace.linspace, math.arange.arange, math.add.add, debug.debugprint.debug_print]

    for func in funcs:
        cls = node_factory_from_func(func)
        node_dict[cls.bl_idname] = NodeData(cls, func)


def register():
    for cls, func in node_dict.values():
        bpy.utils.register_class(cls)


def unregister():
    for cls, func in node_dict.values():
        bpy.utils.unregister_class(cls)
