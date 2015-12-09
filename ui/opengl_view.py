import bgl
import bmesh
import bpy

SpaceView3D = bpy.types.SpaceView3D

_callback_dict = {}


def tag_redraw_all_view3d():
    context = bpy.context
    # Py cant access notifers
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()


def callback_enable(n_id=0, cached_view=None, options=None):
    global _callback_dict
    if n_id in _callback_dict:
        return

    config = triangulate_bm()

    handle_view = SpaceView3D.draw_handler_add(
        draw_callback_view, config, 'WINDOW', 'POST_VIEW')
    _callback_dict[n_id] = handle_view
    tag_redraw_all_view3d()


def callback_disable(n_id):
    global _callback_dict
    handle_view = _callback_dict.get(n_id, None)
    if not handle_view:
        return
    SpaceView3D.draw_handler_remove(handle_view, 'WINDOW')
    del _callback_dict[n_id]
    tag_redraw_all_view3d()


def callback_disable_all():
    global _callback_dict
    temp_list = list(_callback_dict.keys())
    for name in temp_list:
        if name:
            callback_disable(name)


def triangulate_bm(bm=None):
    if bm is None:
        bm = bmesh.new()
        bmesh.ops.create_monkey(bm)
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bm.faces.ensure_lookup_table()
    bm.verts.ensure_lookup_table()
    verts = bgl.Buffer(bgl.GL_FLOAT, [len(bm.verts), 3])
    faces = bgl.Buffer(bgl.GL_INT, [len(bm.faces), 3])
    for i in range(len(bm.faces)):
        for j in range(3):
            faces[i][j] = bm.faces[i].verts[j].index
    for i in range(len(bm.verts)):
        verts[i] = bm.verts[i].co
    return verts, faces

vertex_shader = """
in vec4 vPosition;
in vec4 vColor;

out vec4 color;
uniform mat4 ModelViewProjectionMatrix;
void
main() {
     color = vColor;
     gl_Position = ModelViewProjectionMatrix * vPosition;
 }
"""



def draw_callback_view(verts, faces):

    VERT = 0
    FACES = 1

    buffers = bgl.Buffer(bgl.GL_INT, [2])
    bgl.glGenBuffers(2, buffers)

    bgl.glBindBuffer(bgl.GL_ARRAY_BUFFER, buffers[VERT])
    bgl.glBufferData(bgl.GL_ARRAY_BUFFER, 4 * 3 * len(verts), verts, bgl.GL_STATIC_DRAW)
    bgl.glVertexPointer(3, bgl.GL_FLOAT, 0, verts)
    bgl.glColor3f(1.0,0,0)
    bgl.glEnableClientState(bgl.GL_VERTEX_ARRAY)
    bgl.glDrawArrays(bgl.GL_POINTS, 0, len(verts))
    bgl.glDisableClientState(bgl.GL_VERTEX_ARRAY)
    #bgl.glBindBuffer(bgl.GL_ELEMENT_ARRAY_BUFFER, buffers[FACES])
    #bgl.glBufferData(bgl.GL_ELEMENT_ARRAY_BUFFER, 4*3*len(faces), faces, bgl.GL_STATIC_DRAW)

    #bgl.glDrawElements(bgl.GL_TRIANGLES, len(faces), bgl.GL_INT, bgl.Buffer(bgl.GL_INT,[1]))
