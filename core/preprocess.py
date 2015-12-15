

def proprocess(layout_dict):
    remove_reroutes(layout_dict)


def remove_reroutes(layout_dict):
    """
    Clean up layout before compling

    """
    reroutes = {name for name, node in layout_dict["nodes"].items() if node["bl_idname"] == 'NodeReroute'}
    links = layout_dict["links"]
    for reroute in reroutes:
        from_node = [(f_n, f_s) for f_n, f_s, t_n, t_s in links if t_n == reroute]
        to_nodes = [(t_n, t_s) for f_n, f_s, t_n, t_s in links if f_n == reroute]
        if len(from_node) == 1:
            from_node = from_node[0]
            for to_node in to_nodes:
                links.append(tuple(from_node + to_node))
            layout_dict["nodes"].pop(reroute)

    layout_dict["links"] = [(f_n, f_s, t_n, t_s) for f_n, f_s, t_n, t_s in links
                            if set((f_n, t_n)).isdisjoint(reroutes)]
