import bpy
import bmesh
import numpy as np
from ..svtyping import Vertices, Topology


def to_mesh(vertices: Vertices, edges: Topology) -> None:
    make_bmesh_geometry(vertices, edges)

to_mesh.label = "To mesh"
to_mesh.match = lambda x: x


# the below taken from bmesh/utils viewer in sverchok


def default_mesh(name):
    verts, faces = [(1, 1, -1), (1, -1, -1), (-1, -1, -1)], [(0, 1, 2)]
    mesh_data = bpy.data.meshes.new(name)
    mesh_data.from_pydata(verts, [], faces)
    mesh_data.update()
    return mesh_data


def make_bmesh_geometry(verts, edges=None):
    scene = bpy.context.scene
    meshes = bpy.data.meshes
    objects = bpy.data.objects
    name = "svrx.to_mesh"
    vert_count = len(verts)
    if edges is None:
        edges = list(zip(range(vert_count), range(1, vert_count)))

    if name in objects:
        sv_object = objects[name]
    else:
        temp_mesh = default_mesh(name)
        sv_object = objects.new(name, temp_mesh)
        scene.objects.link(sv_object)

    mesh = sv_object.data

    ''' get bmesh, write bmesh to obj, free bmesh'''
    bm = bmesh_from_pydata(verts, edges, [])
    bm.to_mesh(sv_object.data)
    bm.free()

    sv_object.hide_select = False


def bmesh_from_pydata(verts=None, edges=None, faces=None):
    ''' verts is necessary, edges/faces are optional '''

    bm = bmesh.new()
    add_vert = bm.verts.new
    [add_vert(co) for co in verts]
    bm.verts.index_update()

    if hasattr(bm.verts, "ensure_lookup_table"):
        bm.verts.ensure_lookup_table()

    if faces is not None:
        add_face = bm.faces.new
        for face in faces:
            add_face(tuple(bm.verts[i] for i in face))
        bm.faces.index_update()

    if edges is not None:
        add_edge = bm.edges.new
        for edge in edges:
            edge_seq = tuple(bm.verts[i] for i in edge)
            try:
                add_edge(edge_seq)
            except ValueError:
                # edge exists!
                pass

        bm.edges.index_update()

    return bm

SvRxFunc = [to_mesh]
