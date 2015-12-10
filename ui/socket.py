import bpy
from bpy.props import (FloatProperty,
                       IntProperty,
                       StringProperty,
                       FloatVectorProperty,)

# Default color definitions for sockets, the values in this module can be changed
# from a

NUMBER_SOCKET = (0.6, 1.0, 0.6, 1.0)
VERT_SOCKET = (0.9, 0.6, 0.2, 1.0)
TOPOLOGY_SOCKET = (0.1, .8, .8, 1.0)
DICT_SOCKET = (0.1, 0.1, 0.1, 1.0)
STRING_SOCKET = (0.1, .3, .3, 1.0)
COLOR_SOCKET = (0.1, .3, .3, 1.0)
OBJECT_SOCKET = (0.4, .3, .8, 1.0)
MESH_SOCKET = (0.4, .3, .8, 1.0)
MATRIX_SOCKET = (.2, .8, .8, 1.0)
GENERIC_SOCKET = (0.6, 0.0, 0.6, 1.0)


def serialize(socket):
    socket_dict = {"name": socket.name,
                   "bl_idname": socket.bl_idname,
                   "default_value": getattr(socket, "default_value", None),
                   "is_linked": socket.is_linked,
                   }
    return socket_dict


def execute_tree(self, context):
    self.id_data.execute()


class SvRxSocketBase(object):
    """base class for sockets """
    default_value = None

    def draw(self, context, layout, node, text):
        layout.label(text)

    def serialize(self):
        return serialize(self)

    def load(self, socket_dict):
        value = socket_dict["default_value"]
        if value is not None:
            socket.default_value = value


class SvRxVerticesSocket(bpy.types.NodeSocket, SvRxSocketBase):

    def draw_color(self, context, node):
        return VERT_SOCKET


class SvRxVectorSocket(bpy.types.NodeSocket, SvRxSocketBase):
    default_value = FloatVectorProperty(default=(0, 0, 0),
                                        size=3,
                                        update=execute_tree)

    def draw(self, context, layout, node, text):
        if not self.is_linked and not self.is_output:
            layout.template_component_menu(self, "prop", name=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return VERT_SOCKET


class SvRxColorSocket(bpy.types.NodeSocket, SvRxSocketBase):
    default_value = FloatVectorProperty(default=(0.0, 0.0, 1.0, 1.0),
                                        size=4,
                                        update=execute_tree,
                                        subtype='COLOR')

    def draw(self, context, layout, node, text):
        if not self.is_linked and not self.is_output:
            layout.prop(self, "prop", name=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return COLOR_SOCKET


class SvRxFloatSocket(bpy.types.NodeSocket, SvRxSocketBase):
    default_value = FloatProperty(update=execute_tree)

    def draw(self, context, layout, node, text):
        if not self.is_linked and not self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return NUMBER_SOCKET


class SvRxGenericSocket(bpy.types.NodeSocket, SvRxSocketBase):

    def draw_color(self, context, node):
        return GENERIC_SOCKET


class SvRxDictSocket(bpy.types.NodeSocket, SvRxSocketBase):

    def draw_color(self, context, node):
        return DICT_SOCKET


class SvRxIntSocket(bpy.types.NodeSocket, SvRxSocketBase):

    default_value = IntProperty(default=0, update=execute_tree)

    def draw(self, context, layout, node, text):
        if not self.is_linked and not self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return NUMBER_SOCKET


class SvRxMeshSocket(bpy.types.NodeSocket, SvRxSocketBase):

    default_value = StringProperty()

    def draw(self, context, layout, node, text):
        if not self.is_linked:
            # okay so this could be prop_search, todo
            layout.prop(self, "default_value", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return MESH_SOCKET

#
# Valuesockets below
#


class ValueSocketBase(SvRxSocketBase):
    def draw(self, context, layout, node, text):
        if self.is_output:
            layout.prop(self, "default_value", text=text)
        else:
            pass


class SvRxIntValueSocket(bpy.types.NodeSocket, ValueSocketBase):
    """ For use with input nodes"""

    default_value = IntProperty(update=execute_tree)

    def draw_color(self, context, node):
        return NUMBER_SOCKET


class SvRxFloatValueSocket(bpy.types.NodeSocket, ValueSocketBase):
    """For use with input nodes"""

    default_value = FloatProperty(update=execute_tree)

    def draw_color(self, context, node):
        return NUMBER_SOCKET
