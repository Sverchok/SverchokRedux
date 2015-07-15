import bpy
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector

from sverchok_redux.node_tree import SvRxTreeNode


class SvRxLine(bpy.types.Node, SvRxTreeNode):
    ''' Line '''

    bl_idname = 'SvRxLine'
    bl_label = 'Line'

    dummy = IntProperty(default=3)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(SvRxLine)


def unregister():
    bpy.utils.unregister_class(SvRxLine)
