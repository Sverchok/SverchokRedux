import importlib
import importlib.abc
import importlib.util
import keyword
import sys
from ..ui import menu

import bpy
import bpy.types
from .. import nodes as svrx_nodes

_script_modules = {}


def load_script(text):
    """
    Will load the blender text file as a module in nodes.script
    """
    if text.endswith("py"):
        name = text.rstrip(".py")
    else:
        name = text
    if not name.isidentifier() or keyword.iskeyword(name):
        print("bad text name: {}".format(text))
        return

    # we could introduce simple auto renamning or name mangling system
    if name in _script_modules:
        mod = _script_modules[name]
        importlib.reload(mod)
    else:
        mod = importlib.import_module("SverchokRedux.nodes.script.{}".format(name))
        _script_modules[name] = mod

    new_nodes = svrx_nodes.get_new_nodes()

    if new_nodes:
        print("Load {} new nodes from {}".format(len(new_nodes), mod))
    else:
        print("No new nodes loaded")

    return new_nodes


class SvRxFinder(importlib.abc.MetaPathFinder):

    def find_spec(self, fullname, path, target=None):
        if fullname.startswith("SverchokRedux.nodes.script."):
            name = fullname.split(".")[-1]
            name_py = "{}.py".format(name)
            if name in bpy.data.texts:
                return importlib.util.spec_from_loader(fullname, SvRxLoader(name))
            elif name_py in bpy.data.texts:
                return importlib.util.spec_from_loader(fullname, SvRxLoader(name_py))

        elif fullname == "SverchokRedux.nodes.script":
            # load Module, right now uses real but empty module, will perhaps change
            pass

        return None


class SvRxLoader(importlib.abc.SourceLoader):

    def __init__(self, text):
        self._text = text

    def get_data(self, path):
        return bpy.data.texts[self._text].as_string()

    def get_filename(self, fullname):
        return "<bpy.data.texts[{}]>".format(self._text)


sys.meta_path.append(SvRxFinder())
