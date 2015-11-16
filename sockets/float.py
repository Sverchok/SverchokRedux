import bpy


class SvRxFloatSocket(bpy.types.NodeSocket):
    default_value = bpy.props.FloatProperty()

    def draw(self, context, layout, node, text):
        if not self.is_linked and not self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 1.0, 0.6, 1.0)
