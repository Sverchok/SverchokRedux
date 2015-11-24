from bpy.types import NodeTree
from SverchokRedux.core import compiler
from . import node as SvRxNode


def get_link(link):
    return (link.from_node.name, link.from_socket.name,
            link.to_node.name, link.to_socket.name)


def get_sockets(ng, link_data, names_remap):
    from_node = ng.nodes[names_remap.get(link_data[0], link_data[0])]
    from_socket = from_node.outputs[link_data[1]]
    to_node = ng.nodes[names_remap.get(link_data[2], link_data[2])]
    to_socket = to_node.inputs[link_data[3]]
    return from_socket, to_socket


class SverchCustomTree(NodeTree):
    '''Sverchok -  node programming system for blender'''
    bl_idname = 'SvRxTreeType'
    bl_label = 'SverchokRedux Node Tree'
    bl_icon = 'GHOST_ENABLED'

    def update(self):
        self.execute()

    def execute(self):
        roots = self.compile()
        for root_node in roots:
            root_node.execute(set())

    def compile(self):
        return compiler.compile(self.serialize())

    def serialize(self):
        layout_dict = {"name": self.name}
        nodes = []
        for node in self.nodes:
            if hasattr(node, "serialize"): # SvRx Nodes
                nodes.append((node.name, node.serialize()))
            else:
                nodes.append((node.name , SvRxNode.serialize(node)))

        layout_dict["nodes"] = dict(nodes)
        layout_dict["links"] = [get_link(l) for l in self.links]
        return layout_dict

    def load(self, layout_dict):
        # this is simplified and needs to be a bit more complicated
        # 2) dynamic sockets, behaving like Sverchok are not supported
        # 3) many other things I think
        names_remap = {}

        for name, node_data in layout_dict["nodes"].items():
            node = self.nodes.new(node_data["bl_idname"])
            node.name = name
            if node.name != name:
                names_remap[name] = node.name
            if hasattr(node, 'load'):
                node.load(node_data)
            else:  # frames, reroutes etc.
                pass

        for link_data in layout_dict["links"]:
            self.links.new(*get_sockets(self, link_data, names_remap))
