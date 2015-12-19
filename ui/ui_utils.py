def swap_node(node, bl_idname):
    """Hotswap a node and replace it with new node of bl_idname,
    reconnecting as far as possible.
    """
    ng = node.id_data
    in_links = []
    out_links = []
    for socket in node.inputs:
        if socket.is_linked:
            in_links.append((socket.link[0].from_node.name, socket.link[0].from_socket.name))
    for socket in node.outputs:
        socket_links = []
        for link in socket.links:
            socket_links.append((link.to_node.name, link.to_node.socket.name))
