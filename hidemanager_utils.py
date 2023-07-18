import bpy

context = bpy.context

has_material = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL']
has_modifier = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL', 'LATTICE']
has_vertex_group = ['MESH', 'LATTICE']
has_shape_key = ['MESH', 'CURVE', 'SURFACE', 'LATTICE']

def objectAction(operation: str, obj: bpy.types.Object) -> None:
    """Performs the action selected in the enum

    :param bpy.types.Object obj: Object to be affected by operation
    :return: None
    """

    if operation == 'SELECT':
        obj.select_set(True)
    elif operation == 'DESELECT':
        obj.select_set(False)
    elif operation == 'HIDE':
        obj.hide_set(True)
    elif operation == 'SHOW':
        obj.hide_set(False)
    elif operation == 'ENABLE_RENDER':
        obj.hide_render = False
    elif operation == 'DISABLE_RENDER':
        obj.hide_render = True
    elif operation == 'ENABLE_VIEWPORT':
        obj.hide_viewport = False
    elif operation == 'DISABLE_VIEWPORT':
        obj.hide_viewport = True