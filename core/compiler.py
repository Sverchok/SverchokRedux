from .execute import GraphNode
from . import preprocess


def create_graph(node, layout_dict, graph_dict={}):
    def get_socket_index(name, socket_list):
        for i, s in enumerate(socket_list):
            if s["name"] == name:
                return i
        raise(ValueError("{} isn't a socket in {}".format(name, repr(socket_list))))

    nodes = layout_dict["nodes"]
    node_data = nodes[node.name]
    links = {to_socket: (from_node, from_socket) for from_node, from_socket, to_node, to_socket in layout_dict["links"]
             if to_node == node.name}
    for socket_data in node_data["inputs"]:
        socket_name = socket_data["name"]
        if socket_data["is_linked"]:
            from_node_name, from_socket_name = links[socket_name]
            from_node = graph_dict.get(from_node_name)
            if not from_node:
                cls = get_graph_cls(nodes[from_node_name]["bl_idname"])
                from_node = cls(from_node_name, layout_dict)
                graph_dict[from_node.name] = from_node
                create_graph(from_node, layout_dict, graph_dict)

            if len(nodes[from_node_name]["outputs"]) > 1:
                offset = get_socket_index(from_socket_name, nodes[from_node_name]["outputs"])
            else:
                offset = None
            node.add_child(from_node, offset)
        else:
            node.add_child(ValueNode(node.name + "." + socket_name, socket_data["default_value"]))


def compile(layout_dict):
    preprocess.proprocess(layout_dict)
    # get nodes without any outputs
    root_nodes = layout_dict["nodes"].keys() - {l[0] for l in layout_dict["links"]}
    graph_dict = {}
    out = [GraphNode.from_layout(root_node, layout_dict, graph_dict) for root_node in root_nodes]
    return out
