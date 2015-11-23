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

import bpy
from ..core.node import SvRxNode
from ..nodes import _node_dict as node_dict

from collections import OrderedDict, defaultdict

from nodeitems_utils import NodeCategory, NodeItem
import nodeitems_utils


class SvRxNodeCategory(NodeCategory):

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'SvRxTreeType'


def make_node_cats():

    # category information should be created here
    node_cats = OrderedDict()
    cats = set(node_data.category for node_data in node_dict.values())

    for cat in sorted(cats):
        nodes = [nd for nd in node_dict.values() if nd.category == cat]
        node_cat = sorted([(nd.cls.bl_idname, nd.cls.bl_label) for nd in nodes], key=lambda x: x[1])
        node_cats[cat.title()] = node_cat

    return node_cats


def make_categories():
    node_cats = make_node_cats()

    node_categories = []
    node_count = 0
    print(node_cats)
    for category, nodes in node_cats.items():
        name_big = "SVRX_" + category
        print(nodes)
        node_categories.append(SvRxNodeCategory(
            name_big, category,
            # bl_idname, name
            items=[NodeItem(*data) for data in nodes]))
        node_count += len(nodes)

    return node_categories, node_count


def reload_menu():
    menu, node_count = make_categories()
    if 'SVRX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRX")
    nodeitems_utils.register_node_categories("SVRX", menu)


def register():
    menu, node_count = make_categories()
    if 'SVRX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRX")
    nodeitems_utils.register_node_categories("SVRX", menu)

    print("\n** SVRX loaded with {i} nodes **".format(i=node_count))


def unregister():
    if 'SVRX' in nodeitems_utils._node_categories:
        nodeitems_utils.unregister_node_categories("SVRX")
