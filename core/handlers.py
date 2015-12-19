import bpy
from bpy.app.handlers import persistent
from . import loadscript


@persistent
def load_handler(scene):
    # load scripts
    for text in bpy.data.texts:
        if "@node_script" in text.as_string():
            loadscript.load_script(text.name)


def register():
    bpy.app.handlers.load_post.append(load_handler)


def unregister():
    bpy.app.handlers.load_post.remove(load_handler)
