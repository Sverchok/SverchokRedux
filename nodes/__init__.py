from SverchokRedux.core.node import node_factory_from_func
import bpy

my_nodes = []

def load_nodes():
    # this should really be either automatic or more organized
    funcs = [math.linspace.linspace, math.arange.arange, math.add.add, debug.debugprint.debug_print]
    for func in funcs:
        res = node_factory_from_func(func)
        my_nodes.append(res)

def register():
    for cls in my_nodes:
        bpy.utils.register_class(cls)
    # load_nodes()

def unregister():
    for cls in my_nodes:
        bpy.utils.unregister_class(cls)
