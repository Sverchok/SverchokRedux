import bpy
from bpy.types import EnumProperty
from bpy.props import StringProperty, BoolProperty
from . import socket as SvRxSocket


def serialize(node):
    node_dict = {}
    node_items = {}
    node_enums = find_enumerators(node)

    for k, v in node.items():
        if isinstance(v, (float, int, str)):
            node_items[k] = v
        else:
            node_items[k] = v[:]
        if k in node_enums:
            v = getattr(node, k)
            node_items[k] = v

    node_dict['params'] = node_items
    node_dict['location'] = node.location[:]
    node_dict['bl_idname'] = node.bl_idname
    node_dict['height'] = node.height
    node_dict['width'] = node.width
    node_dict['label'] = node.label
    node_dict['hide'] = node.hide
    node_dict['color'] = node.color[:]
    node_dict['use_custom_color'] = node.use_custom_color

    def get_sockets(socket_list):
        out = []
        for socket in socket_list:
            if hasattr(socket, "serialize"):
                out.append(socket.serialize())
            else:
                out.append(SvRxSocket.serialize(socket))
        return out

    node_dict['inputs'] = get_sockets(node.inputs)
    node_dict['outputs'] = get_sockets(node.outputs)

    return node_dict


def find_enumerators(node):
    """
    From sverchok, by zeffi
    """
    ignored_enums = ['bl_icon', 'bl_static_type', 'type']
    node_props = node.bl_rna.properties[:]
    f = filter(lambda p: isinstance(p, EnumProperty), node_props)
    return [p.identifier for p in f if p.identifier not in ignored_enums]


class SvRxNode:
    """Base class for SverchokRedux classes
    """
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in {'SvRxTreeType'}

    def init(self, context):
        if self.inputs_template:
            for socket_type, name, args in self.inputs_template:
                s = self.inputs.new(socket_type, name)
                if "default_value" in args:
                    s.default_value = args["default_value"]

        if self.outputs_template:
            for socket_type, name, args in self.outputs_template:
                self.outputs.new(socket_type, name)
                if "default_value" in args:
                    s.default_value = args["default_value"]

    def draw_buttons(self, context, layout):
        for prop in self.svrx_props:
            layout.prop(self, prop)

    def draw_buttons_ext(self, context, layout):
        self.draw_buttons(context, layout)
        for prop in self.svrx_props_ext:
            layout.prop(self, prop)


    def update(self):
        pass

    def serialize(self):
        return serialize(self)

    def load(self, node_data):
        # needs more details
        params = node_data["params"]
        for p in params.keys():
            val = params[p]
            setattr(self, p, val)

        self.location = node_data['location']
        self.height = node_data['height']
        self.width = node_data['width']
        self.label = node_data['label']
        self.hide = node_data['hide']
        self.color = node_data['color']
        self.use_custom_color = node_data['use_custom_color']

        # for now no output sockets
        for socket_data in node_data["inputs"]:
            name = socket_data["name"]
            self.inputs[name].load(socket_data)


class SvRxScriptNode(SvRxNode):

    text_file = StringProperty()

    def draw_buttons(self, context, layout):
        if not self.text_file:
            row = layout.row()
            row.prop_search(self, 'text_file', bpy.data, 'texts', text='', icon='TEXT')
            #row.operator("node.SVRX_load_script")
        else:
            layout.label("Script node")
            super().draw_buttons(context, layout)


class SvRxLoadSript(bpy.types.Operator):

    bl_idname = "node.svrxloadscript"
    bl_label = "SvRx scriptnode callback"
    bl_options = {'REGISTER', 'UNDO'}

    relink_node = BoolProperty(default=False)

    def execute(self, context):
        n = context.node
        text_file = n.text_file
        if text_file in bpy.data.texts:
            new_nodes = loadscript.load_script(text_file)
            if new_nodes:
                if not relink_node:
                    bl_idname = new_nodes[0]
                    node = n.id_data.nodes.new(bl_idname)
                    node.location = n.location
                    node.text_file = text_file
                    node.id_data.nodes.remove(n)
                    return {'FINISHED'}

        return {'CANCELLED'}
