import bpy
from .base import SvRxSocketBase


class SvRxMeshSocket(bpy.types.NodeSocket):

    default_value = bpy.props.StringProperty()

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 1.0, 0.6, 1.0)
