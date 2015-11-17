#  ***** BEGIN GPL LICENSE BLOCK *****
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, see <http://www.gnu.org/licenses/>
#  and write to the Free Software Foundation, Inc., 51 Franklin Street,
#  Fifth Floor, Boston, MA  02110-1301, USA..
#
#  The Original Code is Copyright (C) 2015 by Gorodetskiy Nikita  ###
#  All rights reserved.
#
#  Contact:      linusyng@live.com    ###
#
#  The Original Code is: all of this file.
#
#  Contributor(s):
#     Linus Yng (aka Ly29)
#
#  ***** END GPL LICENSE BLOCK *****
#
# -*- coding: utf-8 -*-

bl_info = {
    "name": "SverchokRedux",
    "author":
        "ly29",
    "version": (0, 6, 0, 1),
    "blender": (2, 7, 6),
    "location": "Nodes > Ghost > Add user nodes",
    "description": "Parametric node-based geometry programming",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "https://github.com/nortikin/sverchok/issues/688",
    "category": "Node"}

import importlib
import sys

imported_modules = []

# ugly hack, should make respective dict in __init__ like nodes
# or parse it
root_modules = ["core", "util", "ui", "nodes", "sockets"]
core_modules = ["compiler", "node", "nodetree", "socket"]
ui_modules = ["menu"]
util_modules = ["lib"]
nodes_mods = ["math", "debug"]
math_mods = ["linspace", "arange", "add"]
debug_nodes = ["debugprint"]
socket_mods = ["float", "int", "generic", "base"]

# modules and pkg path, nodes are done separately.
mods_bases = [(root_modules, "SverchokRedux"),
              (core_modules, "SverchokRedux.core"),
              (util_modules, "SverchokRedux.util"),
              (ui_modules, "SverchokRedux.ui"),
              (nodes_mods, "SverchokRedux.nodes"),
              (math_mods, "SverchokRedux.nodes.math"),
              (socket_mods, "SverchokRedux.sockets"),
              (debug_nodes, "SverchokRedux.nodes.debug")
              ]


def import_modules(modules, base, im_list):
    for m in modules:
        im = importlib.import_module('.{}'.format(m), base)
        im_list.append(im)

for mods, base in mods_bases:
    import_modules(mods, base, imported_modules)

nodes.load_nodes()

reload_event = bool("bpy" in locals())

if reload_event:
    for im in imported_modules:
        importlib.reload(im)
    nodes.load_nodes()
    ui.menu.reload_menu()

import bpy


def register():

    for m in imported_modules:
        if hasattr(m, "register"):
            m.register()
    bpy.utils.register_module(__name__)
    if reload_event:
        print("SvRx is reloaded, press update")


def unregister():
    bpy.utils.unregister_module(__name__)
    # still needed, see register()
    for m in reversed(imported_modules):
        if hasattr(m, "unregister"):
            m.unregister()
