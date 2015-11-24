import bpy

def serialize(socket):
    # _index is only used internally, not in relation to blender
    socket_dict = {"name": socket.name,
                   "bl_idname": socket.bl_idname,
                   "default_value": getattr(socket, "default_value", None),
                   "is_linked": socket.is_linked,
                   }
    return socket_dict

class SvRxSocketBase(object):
    """base class for sockets """
    def serialize(self):
        return serialize(self)

    def load(self, socket_dict):
        value = socket_dict["default_value"]
        if value is not None:
            socket.default_value = value

class SvRxFloatSocket(bpy.types.NodeSocket, SvRxSocketBase):
    default_value = bpy.props.FloatProperty()

    def draw(self, context, layout, node, text):
        if not self.is_linked and not self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 1.0, 0.6, 1.0)

class SvRxGenericSocket(bpy.types.NodeSocket, SvRxSocketBase):
    default_value = None

    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 0.0, 0.6, 1.0)

class SvRxIntSocket(bpy.types.NodeSocket, SvRxSocketBase):

    default_value = bpy.props.IntProperty(default=0)

    def draw(self, context, layout, node, text):
        if not self.is_linked and not self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 1.0, 0.6, 1.0)

class SvRxMeshSocket(bpy.types.NodeSocket):

    default_value = bpy.props.StringProperty()

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return(0.6, 1.0, 0.6, 1.0)
