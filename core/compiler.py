import SverchokRedux.nodes


def compile(layout_dict):
    def create_graph(node, layout_dict, graph_dict={}):
        nodes = layout_dict["nodes"]
        node_data = nodes[node.name]
        links = {to_socket: from_node for from_node, from_socket, to_node, to_socket in layout_dict["links"]
                 if to_node == node.name}
        for socket_data in node_data["inputs"]:
            socket_name = socket_data["name"]
            if socket_data["is_linked"]:
                from_node_name = links[socket_name]
                from_node = graph_dict.get(from_node_name)
                if not from_node:
                    from_node = ExecNode(from_node_name, layout_dict)
                    graph_dict[from_node.name] = from_node
                    create_graph(from_node, layout_dict, graph_dict)
                node.add_child(from_node)
            else:
                node.add_child(ValueNode(node.name + "." + socket_name, socket_data["default_value"]))

    # get nodes without any outputs
    root_nodes = layout_dict["nodes"].keys() - {l[0] for l in layout_dict["links"]}

    out = [ExecNode(root_node, layout_dict) in root_nodes]
    for node in out:
        create_graph(node, layout_dict)


class GraphNode():
    def __init__(self, name):
        self.name = name
        self.children = []

    def __iter__(self):

        for child in self.children:
            for node in child:
                yield node
        yield self

    def add_child(self, child):
        self.children.append(child)


class ValueNode(GraphNode):
    def __init__(self, name, value):
        # socket name
        self.name = name
        self.value = value
        self.children = []

    def add_child(self, child):
        pass

    def execute(self):
        pass


class ExecNode(GraphNode):
    def __init__(self, name, layout_dict):
        super().__init__(name)
        bl_idname = layout_dict["nodes"][name]["bl_idname"]
        self.func = SverchokRedux.nodes.node_dict[bl_idname].func

    def execute(self):
        for child in self.children:
            child.execute()
        args = [child.value for child in self.children]
        self.value = self.func(*args)


class IfNode(GraphNode):

    def execute(self):
        self.children[0].execute()
        if self.children[0].eval():
            for child in self.children[1]:
                child.execute()
        else:
            for child in self.children[2]:
                child.execute()
