import bpy
from bpy.utils import previews

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
        path='icons/' + icon + '.png',
        path_type='IMAGE'
    )
