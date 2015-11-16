
import collections

#  nothing in this file does anything right now, this the next step,
#  lower parts can be seen as notes or a old sketch.

def collect_links(ng):
    dependencies = collections.defaultdict(set)

    for link in ng.links:
        if not link.is_valid:
            return {}

        key, value = (link.from_node.name, link.to_node.name)
        dependencies[key].add(value)

    return dependencies


def pre_process(nodes):

    nodes = filter(nodes, lambda n: n.bl_idname in svrx_nodes)


def compile(ng):
    """Compile the layout ng.
    """
    if not ng.bl_idname == "SvRxTreeType":
        return

    dependencies = collect_links(ng)

    nodes = pre_process(ng.nodes)
