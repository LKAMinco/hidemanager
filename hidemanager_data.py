import logging

import bpy
from bpy.props import EnumProperty, StringProperty, BoolProperty, PointerProperty
from bpy.types import PropertyGroup, Modifier, GpencilModifier, Constraint


# TODO implement not implemented filters
class HIDEMANAGER_PG_CustomCollection(PropertyGroup):
    line_type: EnumProperty(default='CONTAINS', name='Filter type', items=[
        ('', 'Basic Filters', '', '', 0),
        ('CONTAINS', 'Contains', 'Filter will be applied to all objects with filled string in name', 'ALIGN_LEFT', 1),
        ('IGNORE', 'Contains Ignore', 'Filter will ignore all objects with filled string in name', 'ALIGN_LEFT', 2),
        ('TYPE', 'Type', 'Filter will be applied to selected type of objects', 'SCENE_DATA', 3),
        ('TYPE_IGNORE', 'Type Ignore', 'Filter will ignore selected type of objects', 'SCENE_DATA', 4),
        ('HIERARCHY', 'Hierarchy', 'Filter will be applied to object and all its children of this object', 'EMPTY_DATA',
         5),
        ('HIERARCHY_IGNORE', 'Hierarchy Ignore', 'Filter will ignore object and all its children of this object',
         'EMPTY_DATA', 6),
        ('COLLECTION', 'Collection', 'Filter will be applied to all objects in selected collection',
         'OUTLINER_COLLECTION', 7),
        ('COLLECTION_IGNORE', 'Collection Ignore', 'Filter will ignore all objects in selected collection',
         'OUTLINER_COLLECTION', 8),
        ('', 'Materials / Modifiers Filters', '', '', 0),
        ('MATERIAL', 'Material', 'Filter will be applied to all objects with selected material', 'MATERIAL_DATA', 9),
        ('MATERIAL_CONTAINS', 'Material Contains',
         'Filter will be applied to all objects with material that contains selected string', 'MATERIAL_DATA', 10),
        ('MATERIAL_IGNORE', 'Material Ignore', 'Filter will ignore all objects with selected material', 'MATERIAL_DATA',
         11),
        ('MODIFIER', 'Modifier', 'Filter will be applied to all objects which contains selected modifier',
         'MODIFIER_DATA', 12),
        ('MODIFIER_CONTAINS', 'Modifier Contains',
         'Filter will be applied to all objects which contains string in one of object modifiers', 'MODIFIER_DATA', 13),
        ('MODIFIER_IGNORE', 'Modifier Ignore', 'Filter will ignore all objects which contains selected modifier',
         'MODIFIER_DATA', 14),
        ('', 'Object Data Filters', '', '', 0),
        ('VERTEX_GROUP_CONTAINS', 'Vertex Group Contains',
         'Filter will be applied to all objects with vertex group which contains filled string',
         'GROUP_VERTEX', 15),
        ('VERTEX_GROUP_IGNORE', 'Vertex Group Ignore',
         'Filter will ignore all objects with vertex group which contains filled string', 'GROUP_VERTEX', 16),
        ('SHAPE_KEY_CONTAINS', 'Shape Key',
         'Filter will be applied to all objects with shape key which contains filled string',
         'SHAPEKEY_DATA', 17),
        ('SHAPE_KEY_IGNORE', 'Shape Key Ignore',
         'Filter will ignore all objects with shape key which contains filled string',
         'SHAPEKEY_DATA', 18),
        ('CONSTRAINT', 'Constraint', 'Filter will be applied to all objects which contains selected constraint',
         'CONSTRAINT', 19),
        ('CONSTRAINT_IGNORE', 'Constraint Ignore', 'Filter will ignore all objects which contains selected constraint',
         'CONSTRAINT', 20),
    ])

    object_type: EnumProperty(default='MESH', name='Object Type', description='Type of objects', items=[
        ('MESH', 'Mesh', 'Mesh', 'MESH_DATA', 1),
        ('CURVE', 'Curve', 'Curve', 'CURVE_DATA', 2),
        ('EMPTY', 'Empty', 'Empty', 'EMPTY_DATA', 3),
        ('LIGHT', 'Light', 'Light', 'LIGHT_DATA', 4),
        ('ARMATURE', 'Armature', 'Armature', 'ARMATURE_DATA', 5),
        ('CAMERA', 'Camera', 'Camera', 'CAMERA_DATA', 6),
        ('SURFACE', 'Surface', 'Surface', 'SURFACE_DATA', 7),
        ('META', 'Meta', 'Meta', 'META_DATA', 8),
        ('FONT', 'Font', 'Font', 'FONT_DATA', 9),
        ('CURVES', 'Hair Curves', 'Hair Curves', 'CURVE_DATA', 10),
        ('POINTCLOUD', 'Point Cloud', 'Point Cloud', 'POINTCLOUD_DATA', 11),
        ('VOLUME', 'Volume', 'Volume', 'VOLUME_DATA', 12),
        ('GPENCIL', 'Grease Pencil (legacy)', 'Grease Pencil (legacy)', 'GREASEPENCIL', 13),
        ('GREASEPENCIL', 'Grease Pencil', 'Grease Pencil', 'GREASEPENCIL', 14),
        ('LATTICE', 'Lattice', 'Lattice', 'LATTICE_DATA', 15),
        ('LIGHT_PROBE', 'Light Probe', 'Light Probe', 'OUTLINER_DATA_LIGHTPROBE', 16),
        ('SPEAKER', 'Speaker', 'Speaker', 'SPEAKER', 17),
    ])

    mod_items = []
    idx = 0
    for mod in Modifier.bl_rna.properties['type'].enum_items:
        if len(mod_items) == 0:
            mod_items.append(('', 'Modify', '', '', 0))
        elif len(mod_items) == 11:
            mod_items.append(('', 'Generate', '', '', 0))
            idx = -1
        elif len(mod_items) == 32:
            mod_items.append(('', 'Deform', '', '', 0))
            idx = -2
        elif len(mod_items) == 49:
            mod_items.append(('', 'Phisics', '', '', 0))
            idx = -3
        mod_items.append((mod.identifier, mod.name, mod.description, mod.icon, len(mod_items) + idx))

    for mod in GpencilModifier.bl_rna.properties['type'].enum_items:
        if len(mod_items) == 61:
            mod_items.append(('', 'Grease Pencil', '', '', 0))
            idx = -4
        mod_items.append((mod.identifier, mod.name, mod.description, mod.icon, len(mod_items) + idx))

    modifier_type: EnumProperty(default='MIRROR', name='Modifier', items=mod_items)

    contains: StringProperty(default='', name='String in name', )

    # contains_ignore: StringProperty(default='', name='String in name',
    #                                 description='Filter will ignore all objects with this string in name')

    line_enable: BoolProperty(default=True, name='Filter active state',
                              description='Enable / Disable filter. In case of disable, filter will be skipped')

    material: PointerProperty(type=bpy.types.Material, name='Material', )

    # material_ignore: PointerProperty(type=bpy.types.Material, name='Material',
    #                                  description='Filter will ignore all objects with this material')
    #
    # material_contains: StringProperty(default='', name='String in material name',
    #                                   description='Filter will be applied to all objects with this string in material name')

    object: PointerProperty(type=bpy.types.Object, name='Hierarchy of objects')

    collection: PointerProperty(type=bpy.types.Collection, name='Collection')

    group: StringProperty(default='', name='Group filters',
                          description='To make a group, fill this line with numbers (ids of filters from Hide Manager Filters) separated with comma or use range first - id-last id. Example: 1,3-5,7,8-10,12'
                                      '\nGroup filters uses both active and inactive filters from Hide Manager Filters')

    group_name: StringProperty(default='Name', name='Group name', description='Name of group')

    constraint_items = []
    idx = 0
    for con in Constraint.bl_rna.properties['type'].enum_items:
        if len(constraint_items) == 0:
            constraint_items.append(('', 'Motion Tracking', '', '', 0))
        elif len(constraint_items) == 4:
            constraint_items.append(('', 'Transform', '', '', 0))
            idx = -1
        elif len(constraint_items) == 16:
            constraint_items.append(('', 'Tracking', '', '', 0))
            idx = -2
        elif len(constraint_items) == 24:
            constraint_items.append(('', 'Relationship', '', '', 0))
            idx = -3
        constraint_items.append((con.identifier, con.name, con.description, con.icon, len(constraint_items) + 1))

    constraint_type: EnumProperty(default='COPY_LOCATION', name='Constraint Type', description='Type of constraint',
                                  items=constraint_items)