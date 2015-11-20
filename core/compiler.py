import collections
import itertools
import SverchokRedux.nodes

"""
def compile(layout_dict):
    nodes = layout_dict["nodes"]
    links = layout_dict["links"]
    dependencies = {"{}.{}".format(t_n,t_s): f_n for f_n,f_s,t_n,t_s in links}

    node_stack = collections.deque()

    node = next(iter(nodes))

    node_stack.push(node)

    order = []

    while node_stack:
        node_data = nodes[node]
        for socket_data in inputs:
            socket = socket_data["name"]
            node_socket = "{}.{}".format(node, socket)
            up_node = dependencies.get(node_socket, None)
            if up_node and up_node not in order:
                node_stack.push(up_node)
                node = up_node
                break
        else:
"""

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

    root_nodes = layout_dict["nodes"].keys() - {l[0] for l in layout_dict["links"]}
    for root_node in root_nodes:
        node = ExecNode(root_node, layout_dict)
        create_graph(node, layout_dict)
        return node


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

class ExecNode(GraphNode):
    def __init__(self, name, layout_dict):
        super().__init__(name)
        bl_idname = layout_dict["nodes"][name]["bl_idname"]
        self.func = SverchokRedux.nodes.node_dict[bl_idname].func


    def execute(self):
        print("Entering {}".format(self.name))
        for child in self.children:
            child.execute()
        self._process()


class IfNode(GraphNode):

    def execute(self):
        self.children[0].execute()
        if self.children[0].eval():
            for child in self.children[1]:
                child.execute()
        else:
            for child in self.children[2]:
                child.execute()
