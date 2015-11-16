import bpy


class SvRxGenericSocket(bpy.types.NodeSocket):
    default_value = None

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 0.0, 0.6, 1.0)
