from bpy.types import NodeTree


def get_link(link):
    return (link.from_node.name, link.from_socket.name,
            link.to_node.name, link.to_socket.name)

def get_sockets(link_data, names_remap):

    from_socket = self.nodes[link_data[0]].outputs[link_data[1]]
    to_socket = self.nodes[link_data[2]].inputs[link_data[3]]


class SverchCustomTree(NodeTree):
    '''Sverchok -  node programming system for blender'''
    bl_idname = 'SvRxTreeType'
    bl_label = 'SverchokRedux Node Tree'
    bl_icon = 'GHOST_ENABLED'

    def update(self):
        pass

    def get_sockets(self, link_data, names_remap):
        from_node = self.nodes[names_remap.get(link_data[0], link_data[0])]
        from_socket = from_node.outputs[link_data[1]]
        to_node = self.nodes[names_remap.get(link_data[2], link_data[2])]
        to_socket = to_node.inputs[link_data[3]]
        return from_socket, to_socket


    def serialize(self):
        layout_dict = {}
        layout_dict["nodes"] = [node.serialize() for node in self.nodes]
        layout_dict["links"] = [get_link(l) for l in self.links]
        return layout_dict

    def load(self, layout_dict):
        # this is simplified and needs to be a bit more complicated
        # 2) dynamic sockets, behaving like Sverchok are not supported
        # 3) many other things I think
        names_remap = {}

        for node_data in layout_dict["nodes"]:
            node = self.nodes.new(node_data["bl_idname"])
            name = node_data["name"]
            node.name = name
            if node.name != name:
                names_remap[name] = node.name
            node.load(node_data)

        for link_data in layout_dict["links"]:
            self.links.new(self.get_sockets(link_data))
