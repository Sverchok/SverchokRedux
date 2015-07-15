import bpy
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector

from sverchok_redux.node_tree import SvRxTreeNode


class SvRxPlane(bpy.types.Node, SvRxTreeNode):
    ''' Plane '''

    bl_idname = 'SvRxPlane'
    bl_label = 'Plane'

    dummy = IntProperty(default=3)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(SvRxPlane)


def unregister():
    bpy.utils.unregister_class(SvRxPlane)
