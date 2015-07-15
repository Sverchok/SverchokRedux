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

import time


import bpy
from bpy.props import StringProperty, BoolProperty, FloatVectorProperty, IntProperty
from bpy.types import NodeTree, NodeSocket, NodeSocketStandard

sentinel = None


class SvRxArraySocket(NodeSocketStandard):

    ''' temp details '''

    bl_idname = "SvRxArraySocket"
    bl_label = "Array Socket"

    prop_name = StringProperty(default='')
    prop_type = StringProperty(default='')
    prop_index = IntProperty()

    def sv_get(self, default=sentinel, deepcopy=True):
        ...

    def sv_set(self, data):
        ...

    def draw(self, context, layout, node, text):
        ...

    def draw_color(self, context, node):
        return(0.6, 1.0, 0.6, 1.0)


class SvRxTree(NodeTree):

    ''' Parametric node based geometry programming '''

    bl_idname = 'SvRxTree'
    bl_label = 'SverchokRedux Node Tree'
    bl_icon = 'RADIO'

    def update(self):
        '''
        Rebuild and update the Sverchok node tree, used at editor changes
        '''

        # this prevents execution when the node_group isn't ready
        try:
            l = bpy.data.node_groups[self.id_data.name]
        except:
            return

        ...


class SvRxTreeNode:

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in ['SvRxTree']


def register():
    bpy.utils.register_class(SvRxTree)
    bpy.utils.register_class(SvRxArraySocket)


def unregister():
    bpy.utils.unregister_class(SvRxArraySocket)
    bpy.utils.unregister_class(SvRxTree)
