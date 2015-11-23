import SverchokRedux.nodes
import numpy as np


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
                    if 'SvRxNodeif_node' == nodes[from_node_name]["bl_idname"]:
                        from_node = IfNode(from_node_name)
                    else:
                        from_node = ExecNode(from_node_name, layout_dict)
                    graph_dict[from_node.name] = from_node
                    create_graph(from_node, layout_dict, graph_dict)
                node.add_child(from_node)
            else:
                node.add_child(ValueNode(node.name + "." + socket_name, socket_data["default_value"]))

    # get nodes without any outputs
    root_nodes = layout_dict["nodes"].keys() - {l[0] for l in layout_dict["links"]}

    out = [ExecNode(root_node, layout_dict) for root_node in root_nodes]
    for node in out:
        create_graph(node, layout_dict)
    return out

# this should be moved to an execute module I guess...


def match_length(args):
    lengths = [len(arg) for arg in args]
    if lengths.count(lengths[0]) == len(lengths):
        return args
    max_len = max(lengths)
    out = []
    for arg, length in zip(args, lengths):
        if length < max_len:
            new_arg = np.zeros(max_len)
            new_arg[:length] = arg
            new_arg[length:] = arg[-1]
            out.append(new_arg)
        else:
            out.append(arg)
    return out


class GraphNode():
    def __init__(self, name):
        self.name = name
        self.children = []
        self.value = None

    def __iter__(self):
        for child in self.children:
            for node in child:
                yield node
        yield self

    def __hash__(self):
        return hash(self.name)

    def print_tree(self, level=0, visited=set()):
        visited.add(node)
        print('\t' * level + repr(node.name) + str(type(node)))
        for child in node.children:
            if child not in visited:
                other_name(child, level + 1, visited)

    def add_child(self, child):
        self.children.append(child)

    def execute(self, visited=set()):
        print(self.name)


class ValueNode(GraphNode):
    def __init__(self, name, value):
        # socket name
        self.name = name
        self.value = np.array([value])
        self.children = []


class ExecNode(GraphNode):
    def __init__(self, name, layout_dict):
        super().__init__(name)
        bl_idname = layout_dict["nodes"][name]["bl_idname"]
        self.func = SverchokRedux.nodes.node_dict[bl_idname].func

    def execute(self, visited=set()):
        visited.add(self)
        gen = (child for child in self.children if child not in visited)
        for child in gen:
            child.execute(visited)
        # this is to simplistic
        args = match_length([child.value for child in self.children])
        self.value = self.func(*args)


class IfNode(GraphNode):

    def execute(self, visited=set()):
        visited.add(self)

        def get_value(val):
            if isinstance(val, (list, type(np.array([0])))) and val:
                return get_value(val[0])
            return val

        self.children[0].execute(visited)
        # needs to be more clever

        if get_value(self.children[0].value):
            self.children[1].execute(visited)
            self.value = self.children[1].value
        else:
            self.children[2].execute(visited)
            self.value = self.children[2].value

class GroupInNode(GraphNode):
    pass

class GroupOutNode(GraphNode):
    pass

class ForNode(GraphNode):
    pass

class WhileNode(GraphNode):
    pass
