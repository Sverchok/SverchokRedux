import SverchokRedux.nodes as nodes
import numpy as np
from itertools import repeat


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
    # get nodes without any outputs
    root_nodes = layout_dict["nodes"].keys() - {l[0] for l in layout_dict["links"]}
    graph_dict = {}
    out = [GraphNode.from_layout(root_node, layout_dict, graph_dict) for root_node in root_nodes]
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

type_table = {
    (float, int): int,
    (float, np.ndarray): lambda n: np.array([n]),
    (int, np.ndarray): lambda n: np.array([n]),
}


def expand_types(t):
    return {float: (float, np.float64, int, np.int64, np.int32),
            int: (int, np.int64, np.int32),
            list: (list, tuple),
            }.get(t, (t,))


def convert_type(value, to_type):
    value_type = type(value)
    for f, t in type_table.keys():
        print(f, t)
    value_type = type(value)
    for t_t in to_type:
        f = type_table.get((value_type, t_t))
        if f:
            print("found type", t_t)
            return f(value)

    return value

# f(a0, a1, ..., aN) -> x


def recursive_map(func, args, inputs_types, level=0):

    if level == 0 and isinstance(args, inputs_types[0]):
        return func(*args)
    # print(args)
    # args = [convert_type(arg, inputs_types) for arg in args]
    checked = [isinstance(arg, types) for arg, types in zip(args, inputs_types)]
    # print(checked, args, inputs_types, level, [type(a) for a in args])

    if all(checked):
        return func(*args)
    if any(checked):
        new_args = [repeat(arg) if check else arg for check, arg in zip(checked, args)]
    else:
        new_args = args

    return [recursive_map(func, arg, inputs_types, level + 1) for arg in zip(*new_args)]


def get_graph_cls(bl_idname):
    """
    return the node class from corressponding bl_idname
    """
    cls_table = {
        "SvRxNodeif_node": IfNode,
    }
    return cls_table.get(bl_idname, ExecNode)


class GraphNode():
    def __init__(self, name, layout_dict={}):
        self.name = name
        self.children = []
        self.value = None
        self.offsets = []

    def __iter__(self):
        for child in self.children:
            for node in child:
                yield node
        yield self

    def __hash__(self):
        return hash(self.name)

    @classmethod
    def from_layout(cls, start_node, layout_dict, graph_dict):
        nodes = layout_dict["nodes"]
        node = nodes[start_node]
        bl_idname = node["bl_idname"]
        new_cls = get_graph_cls(bl_idname)
        node = new_cls(start_node, layout_dict)
        create_graph(node, layout_dict, graph_dict)
        return node

    def get_value(self, offset=None):
        return self.value if offset is None else self.value[offset]

    def print_tree(self, level=0, visited=set()):
        visited.add(self)
        print('\t' * level + repr(self.name) + str(type(self)))
        for child in self.children:
            if child not in visited:
                child.print_tree(level + 1, visited)

    def add_child(self, child, offset=None):
        self.children.append(child)
        self.offsets.append(offset)

    def execute(self, visited=set()):
        pass
        # print(self.name)


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
        node_data = nodes.get_node_data(bl_idname)
        self.func = node_data.func
        self.inputs_types = [expand_types(i[0]) for i in node_data.inputs]

    def execute(self, visited=set()):
        visited.add(self)
        gen = (child for child in self.children if child not in visited)
        for child in gen:
            child.execute(visited)
        if all(isinstance(t, list) for t in self.inputs_types):
            self.value = self.func(*args)
        else:
            args = [child.get_value(offset) for child, offset in zip(self.children, self.offsets)]
            self.value = recursive_map(self.func, args, self.inputs_types)
            # print(self.value)


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
