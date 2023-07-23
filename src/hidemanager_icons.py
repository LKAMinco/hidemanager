import bpy
from bpy.utils import previews
from os import path


def regIcons():
    icons_dir = path.join(path.dirname(__file__), '../icons')
    icons = previews.new()

    icons_files = ['IGNORE',
                   'TYPE_IGNORE',
                   'EXACT_OBJECT_IGNORE',
                   'HIERARCHY_IGNORE',
                   'COLLECTION_IGNORE',
                   'MATERIAL_IGNORE',
                   'MODIFIER_IGNORE',
                   'VERTEX_GROUP_IGNORE',
                   'SHAPE_KEY_IGNORE',
                   'CONSTRAINT_IGNORE',
                   'ID']

    for icon in icons_files:
        icons.load(
            name=icon,
            path=path.join(icons_dir, icon + '.png'),
            path_type='IMAGE'
        )

    return icons


def unregIcons(icons):
    previews.remove(icons)
