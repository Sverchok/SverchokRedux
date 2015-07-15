# -*- coding: utf-8 -*-
# ##### BEGIN GPL LICENSE BLOCK #####
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
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

from collections import OrderedDict

from nodeitems_utils import NodeCategory, NodeItem
import nodeitems_utils


class SvReduxNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'SvRxTree'


def make_node_cats():

    node_cats = OrderedDict()
    '''  bl_idname, shortname, <icon> (optional) '''

    #   bl_idname,             shortname,       <icon> (optional)

    node_cats["Generators"] = [
        ["SvRxLine",            "Line",                  "GRIP"],
        ["SvRxPlane",           "Plane",           "MESH_PLANE"],
        # leave this line commented as last line

    ]

    node_cats["Array Math"] = [
        ["SvRxMathVector",      "Vector",                "GRIP"],
        ["SvRxMathScalar",      "Scalar"],
        ["SvRxMathTrig",        "Trig"],
        # leave this line commented as last line

    ]

    return node_cats


def juggle_and_join(node_cats):
    '''
    this step post processes the extended catagorization used
    by ctrl+space dynamic menu, and attempts to merge previously
    joined catagories. Why? Because the default menu gets very
    long if there are too many catagories.

    The only real alternative to this approach is to write a
    replacement for nodeitems_utils which respects catagories
    and submenus.

    '''
    node_cats = node_cats.copy()
    return node_cats


def make_categories():
    original_categories = make_node_cats()
    node_cats = juggle_and_join(original_categories)

    node_categories = []
    node_count = 0
    for category, nodes in node_cats.items():
        name_big = "SVRDX_" + category.replace(' ', '_')
        node_categories.append(SvReduxNodeCategory(
            name_big, category,
            # -----NodeItem(bl_idname, name   )
            items=[NodeItem(props[0], props[1]) for props in nodes]))
        node_count += len(nodes)

    return node_categories, node_count


def reload_menu():
    menu, node_count = make_categories()
    if 'SVRDX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRDX")
    nodeitems_utils.register_node_categories("SVRDX", menu)


def register():
    menu, node_count = make_categories()
    if 'SVRDX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRDX")
    nodeitems_utils.register_node_categories("SVRDX", menu)

    print("\n** Sverchok REDUX loaded with {i} nodes **".format(i=node_count))


def unregister():
    if 'SVRDX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRDX")
