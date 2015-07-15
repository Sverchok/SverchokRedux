# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you may redistribute it, and/or
# modify it, under the terms of the GNU General Public License
# as published by the Free Software Foundation - either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, write to:
#
#   the Free Software Foundation Inc.
#   51 Franklin Street, Fifth Floor
#   Boston, MA 02110-1301, USA
#
# or go online at: http://www.gnu.org/licenses/ to view license options.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Sverchok Redux",
    "author": "Team Sverchok",
    "version": (0, 0, 0, 1),
    "blender": (2, 7, 5),
    "location": "Nodes > CustomNodesTree",
    "description": "Parametric node-based geometry programming",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/Sverchok/SverchokRedux/issues",
    "category": "Node"
}


import sys
import os
import importlib
import imp

if __name__ != "sverchok_redux":
    sys.modules["sverchok_redux"] = sys.modules[__name__]

# to store imported modules
imported_modules = []

# ugly hack, should make respective dict in __init__ like nodes
# or parse it
root_modules = [
    "node_indexing", "node_tree",
    "core", "utils", "ui", "nodes"
]

core_modules = []
utils_modules = []
ui_modules = []

# modules and pkg path, nodes are done separately.
mods_bases = [
    (root_modules, "sverchok_redux"),
    (core_modules, "sverchok_redux.core"),
    (utils_modules, "sverchok_redux.utils"),
    (ui_modules, "sverchok_redux.ui")
]


def import_modules(modules, base, im_list):
    for m in modules:
        im = importlib.import_module('.{}'.format(m), base)
        im_list.append(im)


# parse the nodes/__init__.py dictionary and load all nodes
def make_node_list():
    node_list = []
    base_name = "sverchok_redux.nodes"
    for category, names in nodes.nodes_dict.items():
        importlib.import_module('.{}'.format(category), base_name)
        import_modules(names, '{}.{}'.format(base_name, category), node_list)
    return node_list

for mods, base in mods_bases:
    import_modules(mods, base, imported_modules)

node_list = make_node_list()


reload_event = bool("bpy" in locals())
if reload_event:
    print('reload event!')
    import nodeitems_utils
    #  reload the base modules
    #  then reload nodes after the node module as been reloaded
    for im in imported_modules:
        importlib.reload(im)
    node_list = make_node_list()
    for node in node_list:
        importlib.reload(node)
    node_indexing.reload_menu()

import bpy


def register():
    print('starting register function')
    for m in imported_modules + node_list:
        if hasattr(m, "register"):
            m.register()
    if reload_event:
        print('handling reload event..')

    #  add_keymaps()


def unregister():
    print('starting unregister function')
    for m in reversed(imported_modules + node_list):
        if hasattr(m, "unregister"):
            m.unregister()

    #  remove_keymaps()
