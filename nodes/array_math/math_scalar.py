import bpy
from bpy.props import IntProperty, FloatProperty
from mathutils import Vector

from sverchok_redux.node_tree import SvRxTreeNode


class SvRxMathScalar(bpy.types.Node, SvRxTreeNode):
    ''' Scalar Math '''

    bl_idname = 'SvRxMathScalar'
    bl_label = 'Scalar'

    dummy = IntProperty(default=3)

    def draw_buttons(self, context, layout):
        pass


def register():
    bpy.utils.register_class(SvRxMathScalar)


def unregister():
    bpy.utils.unregister_class(SvRxMathScalar)
