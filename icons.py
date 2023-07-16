import bpy
from bpy.utils import previews
from pathlib import Path
from os import path

icons_dir = str(Path(__file__).parent / 'icons')

icons = previews.new()

icons_files = ['IGNORE',
               'TYPE_IGNORE',
               'HIERARCHY_IGNORE',
               'COLLECTION_IGNORE',
               'MATERIAL_IGNORE',
               'MODIFIER_IGNORE',
               'VERTEX_GROUP_IGNORE',
               'SHAPE_KEY_IGNORE',
               'CONSTRAINT_IGNORE']

for icon in icons_files:
    icons.load(
        name=icon,
        path=path.join(icons_dir, icon + '.png'),
        path_type='IMAGE'
    )
