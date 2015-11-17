from bpy.types import NodeTree


def get_link(link):
    return (link.from_node.name, link.from_socket.name,
            link.to_node.name, link.to_socket.name)


class SverchCustomTree(NodeTree):
    '''Sverchok -  node programming system for blender'''
    bl_idname = 'SvRxTreeType'
    bl_label = 'SverchokRedux Node Tree'
    bl_icon = 'GHOST_ENABLED'

    def update(self):
        pass

    def serialize(self):
        layout_dict = {}
        layout_dict["nodes"] = [node.serialize() for node in self.nodes]
        layout_dict["links"] = [get_link(l) for l in self.links]
        return layout_dict

    def load(self, layout_dict):
        # this is simplified and needs to be a bit more complicated
        # 1) none empty layout and node name collisions
        # 2) dynamic sockets, behaving like Sverchok are not supported
        # 3) many other things I think
         
        for node_data in layout_dict["nodes"]:
            node = self.nodes.new(node_data["bl_idname"])
            node.load(node_data)

        for link_data in layout_dict["links"]:
            from_socket = self.nodes[link_data[0]].outputs[link_data[1]]
            to_socket = self.nodes[link_data[2]].inputs[link_data[3]]
            self.links.new(from_socket, to_socket)
