from bpy.types import NodeTree


def compile_socket(socket):
    if hasattr(socket, "svrx_value"):
        return (socket.name, socket.bl_idname, socket.node.name, socket.svrx_value)
    else:
        return (socket.name, socket.bl_idname, socket.node.name)


def compile_link(link):
    return compile_socket(link.to_socket), compile_socket(link.from_socket)


class SverchCustomTree(NodeTree):
    '''Sverchok -  node programming system for blender'''
    bl_idname = 'SvRxTreeType'
    bl_label = 'SverchokRedux Node Tree'
    bl_icon = 'GHOST_ENABLED'

    def update(self):
        pass

    def as_json(self):
        nodes = [node.as_json() for node in self.nodes]
        links = [(l.from_node.name, l.from_socket.name, l.from_socket)]
