import bpy
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector

from sverchok_redux.node_tree import SvRxTreeNode


class SvRxMathTrig(bpy.types.Node, SvRxTreeNode):
    ''' Scalar Trig '''

    bl_idname = 'SvRxMathTrig'
    bl_label = 'Trig'

    dummy = IntProperty(default=3)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(SvRxMathTrig)


def unregister():
    bpy.utils.unregister_class(SvRxMathTrig)
