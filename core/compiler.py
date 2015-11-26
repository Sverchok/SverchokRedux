from .execute import GraphNode
from . import preprocess


def compile(layout_dict):
    preprocess.proprocess(layout_dict)
    # get nodes without any outputs
    root_nodes = layout_dict["nodes"].keys() - {l[0] for l in layout_dict["links"]}
    graph_dict = {}
    out = [GraphNode.from_layout(root_node, layout_dict, graph_dict) for root_node in root_nodes]
    return out
