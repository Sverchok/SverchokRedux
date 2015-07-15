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


# ...

import bpy


def register():
    bpy.utils.register_module(__name__)
    #  add_keymaps()


def unregister():
    bpy.utils.unregister_module(__name__)
    #  remove_keymaps()
