import bpy
from .base import SvRxSocketBase


class SvRxIntSocket(bpy.types.NodeSocket, SvRxSocketBase):

    default_value = bpy.props.IntProperty(default=0)

    def draw(self, context, layout, node, text):
        if not self.is_linked and not self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 1.0, 0.6, 1.0)
