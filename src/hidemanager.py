import logging

import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty
from bpy.types import Operator
from .hidemanager_utils import objectAction, has_material, has_modifier, has_vertex_group, has_shape_key
from bpy.ops import object


class HIDEMANAGER_OT_Force(Operator):
    bl_idname = 'hidemanager.force'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    action: EnumProperty(default='MARK', items=[
        ('MARK', 'Mark', 'Mark objects'),
        ('UNMARK', 'Unmark', 'Unmark objects'),
        ('MARK_IGNORE', 'Mark Ignore', 'Mark objects as ignore'),
    ])

    @classmethod
    def description(cls, context, properties):
        if context.mode != 'EDIT_MESH':
            if properties.action == 'MARK':
                return 'Force action to be performed on selected objects'
            elif properties.action == 'UNMARK':
                return 'Remove force from selected objects'
            elif properties.action == 'MARK_IGNORE':
                return 'Force ignore selected objects'
        else:
            obj = context.active_object
            index = obj.hidemanager_edit_index
            try:
                item = obj.hidemanager_edit[index]
            except IndexError:
                pass
            else:
                if properties.action == 'MARK':
                    if item.line_type == 'MATERIAL':
                        return 'Add selected material on selection'
                    elif item.line_type == 'MATERIAL_CONTAINS':
                        return 'Add first material that contains selected string on selection'
                    elif item.line_type == 'VERTEX_GROUP_CONTAINS':
                        return 'Add selection to selected vertex groups containing selected string'
                elif properties.action == 'MARK_IGNORE':
                    if item.line_type == 'MATERIAL':
                        return 'Set default (first) material on selection where selected material is used'
                    elif item.line_type == 'MATERIAL_CONTAINS':
                        return 'Set default (first) material on selection where first material that contains selected string is used'
                    elif item.line_type == 'VERTEX_GROUP_CONTAINS':
                        return 'Remove selection from selected vertex groups containing selected string'

    def getMark(self):
        return self['force_state']

    bpy.types.Object.force_state = StringProperty(get=getMark)

    def execute(self, context):
        scene = context.scene
        if context.mode != 'EDIT_MESH':
            for obj in context.selected_objects:
                if self.action == 'MARK':
                    obj['force_state'] = 'MARK'
                elif self.action == 'MARK_IGNORE':
                    obj['force_state'] = 'MARK_IGNORE'
                elif self.action == 'UNMARK':
                    if 'force_state' in obj.keys():
                        del obj['force_state']
        else:
            obj = context.active_object
            index = obj.hidemanager_edit_index
            try:
                item = obj.hidemanager_edit[index]
            except IndexError:
                pass
            else:
                if item.line_type == 'MATERIAL':
                    if item.material.name in obj.data.materials:
                        material_index = obj.data.materials.find(item.material.name)
                        obj.active_material_index = material_index
                        if self.action == 'MARK':
                            object.material_slot_assign()
                        elif self.action == 'MARK_IGNORE':
                            object.mode_set(mode='OBJECT')
                            object.material_slot_remove()
                            object.mode_set(mode='EDIT')
                    else:
                        if self.action == 'MARK':
                            object.material_slot_add()
                            obj.active_material = item.material
                            object.material_slot_assign()
                elif item.line_type == 'MATERIAL_CONTAINS':
                    for material in obj.data.materials:
                        if item.contains in material.name:
                            material_index = obj.data.materials.find(material.name)
                            obj.active_material_index = material_index
                            if self.action == 'MARK':
                                object.material_slot_assign()
                            elif self.action == 'MARK_IGNORE':
                                object.mode_set(mode='OBJECT')
                                object.material_slot_remove()
                                object.mode_set(mode='EDIT')
                            break
                elif item.line_type == 'VERTEX_GROUP_CONTAINS':
                    for vertex_group in obj.vertex_groups:
                        if item.contains in vertex_group.name:
                            vertex_group_index = obj.vertex_groups.find(vertex_group.name)
                            obj.vertex_groups.active_index = vertex_group_index
                            if self.action == 'MARK':
                                object.vertex_group_assign()
                            elif self.action == 'MARK_IGNORE':
                                object.vertex_group_remove_from()

        return {'FINISHED'}


class HIDEMANAGER_OT_Actions(Operator):
    bl_idname = 'hidemanager.actions'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    action: EnumProperty(default='ADD', items=[
        ('ADD', 'Add', 'Create new filter'),
        ('REMOVE', 'Remove', 'Remove selected filter'),
        ('DOWN', 'Down', 'Move selected filter down'),
        ('UP', 'Up', 'Move selected filter up')
    ])

    @classmethod
    def description(cls, context, properties):
        if properties.action == 'ADD':
            return 'Create new filter'
        elif properties.action == 'REMOVE':
            return 'Remove selected filter'
        elif properties.action == 'DOWN':
            return 'Move selected filter down'
        elif properties.action == 'UP':
            return 'Move selected filter up'

    def invoke(self, context, event):
        scene = context.scene
        index = scene.hidemanager_index

        try:
            item = scene.hidemanager[index]
        except IndexError:
            pass
        else:
            if self.action == 'REMOVE':
                scene.hidemanager_index -= 1
                scene.hidemanager.remove(index)
            elif self.action == 'DOWN' and index < len(scene.hidemanager) - 1:
                item_next = scene.hidemanager[index + 1].name
                scene.hidemanager.move(index, index + 1)
                scene.hidemanager_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.hidemanager_index + 1)
            elif self.action == 'UP' and index >= 1:
                item_prev = scene.hidemanager[index - 1].name
                scene.hidemanager.move(index, index - 1)
                scene.hidemanager_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.hidemanager_index + 1)
        if self.action == 'ADD':
            item = scene.hidemanager.add()
            item.line_type = 'CONTAINS'
            item.object_type = 'MESH'
        return {'FINISHED'}


class HIDEMANAGER_OT_GroupActions(Operator):
    bl_idname = 'hidemanager_group.actions'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    action: EnumProperty(default='ADD', items=[
        ('ADD', 'Add', 'Create new group of filters'),
        ('REMOVE', 'Remove', 'Remove selected groups'),
        ('DOWN', 'Down', 'Move selected group down'),
        ('UP', 'Up', 'Move selected group up')
    ])

    @classmethod
    def description(cls, context, properties):
        if properties.action == 'ADD':
            return 'Create new group of filters'
        elif properties.action == 'REMOVE':
            return 'Remove selected groups'
        elif properties.action == 'DOWN':
            return 'Move selected group down'
        elif properties.action == 'UP':
            return 'Move selected group up'

    def invoke(self, context, event):
        scene = context.scene
        index = scene.hidemanager_group_index

        try:
            item = scene.hidemanager_group[index]
        except IndexError:
            pass
        else:
            if self.action == 'REMOVE':
                scene.hidemanager_group_index -= 1
                scene.hidemanager_group.remove(index)
            elif self.action == 'DOWN' and index < len(scene.hidemanager_group) - 1:
                item_next = scene.hidemanager_group[index + 1].name
                scene.hidemanager_group.move(index, index + 1)
                scene.hidemanager_group_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.hidemanager_group_index + 1)
            elif self.action == 'UP' and index >= 1:
                item_prev = scene.hidemanager_group[index - 1].name
                scene.hidemanager_group.move(index, index - 1)
                scene.hidemanager_group_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, scene.hidemanager_group_index + 1)
        if self.action == 'ADD':
            item = scene.hidemanager_group.add()
        return {'FINISHED'}


class HIDEMANAGER_OT_EditActions(Operator):
    bl_idname = 'hidemanager_edit.actions'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    action: EnumProperty(default='ADD', items=[
        ('ADD', 'Add', 'Create new group of filters'),
        ('REMOVE', 'Remove', 'Remove selected groups'),
        ('DOWN', 'Down', 'Move selected group down'),
        ('UP', 'Up', 'Move selected group up')
    ])

    @classmethod
    def description(cls, context, properties):
        if properties.action == 'ADD':
            return 'Create new filter'
        elif properties.action == 'REMOVE':
            return 'Remove selected filter'
        elif properties.action == 'DOWN':
            return 'Move selected filter down'
        elif properties.action == 'UP':
            return 'Move selected filter up'

    def invoke(self, context, event):
        scene = context.scene
        obj = context.active_object
        index = obj.hidemanager_edit_index
        try:
            item = obj.hidemanager_edit[index]
        except IndexError:
            pass
        else:
            if self.action == 'REMOVE':
                obj.hidemanager_edit_index -= 1
                obj.hidemanager_edit.remove(index)
            elif self.action == 'DOWN' and index < len(obj.hidemanager_edit) - 1:
                item_next = obj.hidemanager_edit[index + 1].name
                obj.hidemanager_edit.move(index, index + 1)
                obj.hidemanager_edit_index += 1
                info = 'Item "%s" moved to position %d' % (item.name, obj.hidemanager_edit_index + 1)
            elif self.action == 'UP' and index >= 1:
                item_prev = obj.hidemanager_edit[index - 1].name
                obj.hidemanager_edit.move(index, index - 1)
                obj.hidemanager_edit_index -= 1
                info = 'Item "%s" moved to position %d' % (item.name, obj.hidemanager_edit_index + 1)
        if self.action == 'ADD':
            item = obj.hidemanager_edit.add()
        return {'FINISHED'}


class HIDEMANAGER_OT_State(Operator):
    bl_idname = 'hidemanager.state'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    action: EnumProperty(default='ENABLE', items=[
        ('ENABLE', 'Enable', 'Enable'),
        ('DISABLE', 'Disable', 'Disable'),
        ('INVERT', 'Invert', 'Invert')
    ])

    group: BoolProperty(default=False)
    edit_mode: BoolProperty(default=False)

    @classmethod
    def description(cls, context, properties):
        if properties.group:
            hdmng_context = 'groups'
        else:
            hdmng_context = 'filters'

        if properties.action == 'ENABLE':
            return 'Enable all %s' % hdmng_context
        elif properties.action == 'DISABLE':
            return 'Disable all %s' % hdmng_context
        elif properties.action == 'INVERT':
            return 'Invert all %s active state' % hdmng_context

    def execute(self, context):
        if self.group:
            hdmng_context = context.scene.hidemanager_group
        elif self.edit_mode:
            hdmng_context = context.scene.hidemanager_edit
        else:
            hdmng_context = context.scene.hidemanager

        for item in hdmng_context:
            if self.action == 'ENABLE':
                item.line_enable = True
            elif self.action == 'DISABLE':
                item.line_enable = False
            elif self.action == 'INVERT':
                item.line_enable = not item.line_enable
        self.group = False
        self.edit_mode = False
        return {'FINISHED'}


class HIDEMANAGER_OT_Selected(Operator):
    bl_idname = 'hidemanager.selected'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    operation: EnumProperty(default='SELECT', items=[
        ('SELECT', 'Select', 'Select objects by selected filter'),
        ('DESELECT', 'Deselect', 'Deselect objects by selected filter'),
        ('SELECT_INVERT', 'Select Invert', 'Select inverse objects by selected filter'),
        ('HIDE', 'Hide', 'Hide objects by selected filter'),
        ('SHOW', 'Show', 'Show objects by selected filter'),
        ('ENABLE_RENDER', 'Enable Render', 'Enable objects in render by selected filter'),
        ('DISABLE_RENDER', 'Disable Render', 'Disable objects in render by selected filter'),
        ('ENABLE_VIEWPORT', 'Enable Viewport', 'Enable objects in viewport by selected filter'),
        ('DISABLE_VIEWPORT', 'Disable Viewport', 'Disable objects in viewport by selected filter'),
    ])

    @classmethod
    def description(cls, context, properties):
        if properties.operation == 'SELECT':
            return 'Select objects by selected filter'
        elif properties.operation == 'DESELECT':
            return 'Deselect objects by selected filter'
        elif properties.operation == 'SELECT_INVERT':
            return 'Select inverse objects by selected filter'
        elif properties.operation == 'HIDE':
            return 'Hide objects by selected filter'
        elif properties.operation == 'SHOW':
            return 'Show objects by selected filter'
        elif properties.operation == 'ENABLE_RENDER':
            return 'Enable objects in render by selected filter'
        elif properties.operation == 'DISABLE_RENDER':
            return 'Disable objects in render by selected filter'
        elif properties.operation == 'ENABLE_VIEWPORT':
            return 'Enable objects in viewport by selected filter'
        elif properties.operation == 'DISABLE_VIEWPORT':
            return 'Disable objects in viewport by selected filter'

    def execute(self, context):
        scene = context.scene
        index = scene.hidemanager_index
        try:
            item = scene.hidemanager[index]
        except IndexError:
            self.forceOperation(scene)

            if context.mode == 'OBJECT':
                if self.operation == 'SELECT_INVERT':
                    bpy.ops.object.select_all(action='INVERT')
            else:
                self.report({'WARNING'}, 'This operation is not available in edit mode')
        else:
            already_checked = []

            for obj in scene.view_layers[0].objects:
                skip = False

                if obj in already_checked:
                    continue

                if 'force_state' in obj.keys():
                    self.report({'INFO'}, 'Force used in execution')
                    if obj['force_state'] == 'MARK':
                        objectAction(self.operation, obj)
                        already_checked.append(obj)
                        continue
                    elif obj['force_state'] == 'MARK_IGNORE':
                        already_checked.append(obj)
                        continue

                if item.line_type == 'CONTAINS':
                    if item.contains == '':
                        break
                    if item.contains in obj.name:
                        objectAction(self.operation, obj)

                elif item.line_type == "IGNORE":
                    if item.contains == '':
                        break
                    if item.contains not in obj.name:
                        objectAction(self.operation, obj)

                elif item.line_type == 'TYPE':
                    if obj.type == item.object_type:
                        objectAction(self.operation, obj)

                elif item.line_type == 'TYPE_IGNORE':
                    if obj.type != item.object_type:
                        objectAction(self.operation, obj)

                elif item.line_type == 'EXACT_OBJECT':
                    if item.object is None:
                        break
                    objectAction(self.operation, item.object)

                elif item.line_type == 'EXACT_OBJECT_IGNORE':
                    if item.object is None:
                        break
                    if obj is not item.object:
                        objectAction(self.operation, obj)

                elif item.line_type == 'HIERARCHY':
                    if item.object is None:
                        break
                    if obj is item.object:
                        objectAction(self.operation, obj)
                        already_checked.append(obj)
                        for child in obj.children_recursive:
                            objectAction(self.operation, child)
                            already_checked.append(child)

                elif item.line_type == 'HIERARCHY_IGNORE':
                    if item.object is None:
                        break
                    if obj is not item.object:
                        objectAction(self.operation, obj)
                    else:
                        for child in obj.children_recursive:
                            already_checked.append(child)

                elif item.line_type == 'COLLECTION':
                    if item.collection is None:
                        break
                    if item.collection in obj.users_collection:
                        objectAction(self.operation, obj)

                elif item.line_type == 'COLLECTION_IGNORE':
                    if item.collection is None:
                        break
                    if item.collection not in obj.users_collection:
                        objectAction(self.operation, obj)

                elif item.line_type == 'MATERIAL':
                    if obj.type in has_material:
                        if item.material is None:
                            break
                        if item.material.name in obj.data.materials:
                            objectAction(self.operation, obj)

                elif item.line_type == 'MATERIAL_CONTAINS':
                    if obj.type in has_material:
                        if item.contains == '':
                            break
                        for mat in obj.data.materials:
                            if item.contains in mat.name:
                                objectAction(self.operation, obj)

                elif item.line_type == 'MATERIAL_IGNORE':
                    if obj.type in has_material:
                        if item.material is None:
                            break
                        if item.material.name not in obj.data.materials:
                            objectAction(self.operation, obj)

                elif item.line_type == 'MODIFIER':
                    if obj.type in has_modifier:
                        for mod in obj.modifiers:
                            if mod.type == item.modifier_type:
                                objectAction(self.operation, obj)

                elif item.line_type == 'MODIFIER_CONTAINS':
                    if item.contains == '':
                        break
                    if obj.type in has_modifier:
                        for mod in obj.modifiers:
                            if item.contains in mod.name:
                                objectAction(self.operation, obj)

                elif item.line_type == 'MODIFIER_IGNORE':
                    if obj.type in has_modifier:
                        mod_types = [mod.type for mod in obj.modifiers]
                        if item.modifier_type not in mod_types:
                            objectAction(self.operation, obj)

                elif item.line_type == 'VERTEX_GROUP_CONTAINS':
                    if item.contains == '':
                        break
                    if obj.type in has_vertex_group:
                        for vg in obj.vertex_groups:
                            if item.contains in vg.name:
                                objectAction(self.operation, obj)

                elif item.line_type == 'VERTEX_GROUP_IGNORE':
                    if item.contains == '':
                        break
                    if obj.type in has_vertex_group:
                        for vg in obj.vertex_groups:
                            if item.contains in vg.name:
                                skip = True
                        if not skip:
                            objectAction(self.operation, obj)

                elif item.line_type == 'SHAPE_KEY_CONTAINS':
                    if item.contains == '':
                        break
                    if obj.type in has_shape_key:
                        if obj.data.shape_keys is not None:
                            for sk in obj.data.shape_keys.key_blocks:
                                if item.contains in sk.name:
                                    objectAction(self.operation, obj)

                elif item.line_type == 'SHAPE_KEY_IGNORE':
                    if item.contains == '':
                        break
                    if obj.type in has_shape_key:
                        if obj.data.shape_keys is not None:
                            for sk in obj.data.shape_keys.key_blocks:
                                if item.contains in sk.name:
                                    skip = True
                            if not skip:
                                objectAction(self.operation, obj)
                        else:
                            objectAction(self.operation, obj)

                elif item.line_type == 'CONSTRAINT':
                    for con in obj.constraints:
                        if con.type == item.constraint_type:
                            objectAction(self.operation, obj)

                elif item.line_type == 'CONSTRAINT_IGNORE':
                    con_types = [con.type for con in obj.constraints]
                    if item.constraint_type not in con_types:
                        objectAction(self.operation, obj)

        if context.mode == 'OBJECT':
            if self.operation == 'SELECT_INVERT':
                bpy.ops.object.select_all(action='INVERT')
        else:
            self.report({'WARNING'}, 'This operation is not available in edit mode')
        return {'FINISHED'}

    def forceOperation(self, scene):
        for obj in scene.view_layers[0].objects:
            if 'force_state' in obj.keys():
                self.report({'INFO'}, 'Force used in execution')
                if obj['force_state'] == 'MARK':
                    objectAction(self.operation, obj)


class Filter:
    type = ''
    value = None

    def __init__(self, type='', value=None):
        self.type = type
        self.value = value


class Filters:
    filters = []
    use_priority = False
    filter_count = 0
    non_ignorable_count = 0
    priority = ['EXACT_OBJECT', 'HIERARCHY', 'TYPE', 'CONTAINS', 'CONSTRAINT', 'COLLECTION', 'MODIFIER', 'MODIFIER_CONTAINS',
                'MATERIAL', 'MATERIAL_CONTAINS', 'VERTEX_GROUP_CONTAINS', 'SHAPE_KEY_CONTAINS']
    operation = ''
    already_checked = None

    def execFilters(self, obj):
        if 'force_state' in obj.keys():
            self.report({'INFO'}, 'Force used in execution')
            if obj['force_state'] == 'MARK':
                objectAction(self.operation, obj)
                self.already_checked.append(obj)
            elif obj['force_state'] == 'MARK_IGNORE':
                self.already_checked.append(obj)
            return

        for filter in self.filters:
            filter_exec = getattr(self, filter.type)
            res = filter_exec(obj, filter.value)
            if res:
                self.already_checked.append(obj.name)
                return
        if self.non_ignorable_count == 0:
            objectAction(self.operation, obj)

        self.already_checked.append(obj.name)

    def clear(self):
        self.filters.clear()
        self.use_priority = False
        self.filter_count = 0
        self.non_ignorable_count = 0

    def append(self, type='', value='', ignore=False):
        if ignore:
            self.use_priority = True
        else:
            self.non_ignorable_count += 1
        filter = Filter(type, value)
        self.filters.append(filter)
        self.filter_count += 1

    def sortByFastestPriority(self):
        self.filters.sort(key=lambda x: self.priority.index(x.type))

    def CONTAINS(self, obj, value):
        if value in obj.name:
            objectAction(self.operation, obj)
            return True
        return False

    def CONTAINS_IGNORE(self, obj, value):
        if value in obj.name:
            return True
        return False

    def IGNORE(self, obj, value):
        if value in obj.name:
            return True
        return False

    def TYPE(self, obj, value):
        if obj.type == value:
            objectAction(self.operation, obj)
            return True
        return False

    def TYPE_IGNORE(self, obj, value):
        if obj.type == value:
            return True
        return False

    def EXACT_OBJECT(self, obj, value):
        if obj == value:
            objectAction(self.operation, obj)
            return True
        return False

    def EXACT_OBJECT_IGNORE(self, obj, value):
        if obj == value:
            return True
        return False

    def HIERARCHY_CHECK(self, obj, value):
        if obj == value:
            return True
        else:
            if obj.parent is not None:
                return self.HIERARCHY_CHECK(obj.parent, value)
            else:
                return False

    def HIERARCHY(self, obj, value):
        if self.HIERARCHY_CHECK(obj, value):
            objectAction(self.operation, obj)
            return True
        return False

    def HIERARCHY_IGNORE(self, obj, value):
        if obj == value:
            return True
        else:
            if obj.parent is not None:
                return self.HIERARCHY_IGNORE(obj.parent, value)
            else:
                return False
        return False

    def COLLECTION(self, obj, value):
        if value in obj.users_collection:
            objectAction(self.operation, obj)
            return True
        return False

    def COLLECTION_IGNORE(self, obj, value):
        if value in obj.users_collection:
            return True
        return False

    def MATERIAL(self, obj, value):
        if obj.type in has_material:
            if value in obj.data.materials:
                objectAction(self.operation, obj)
                return True
        return False

    def MATERIAL_CONTAINS(self, obj, value):
        if obj.type in has_material:
            for mat in obj.data.materials:
                if value in mat.name:
                    objectAction(self.operation, obj)
                    return True
        return False

    def MATERIAL_IGNORE(self, obj, value):
        if obj.type in has_material:
            if value in obj.data.materials:
                return True
        return False

    def MODIFIER(self, obj, value):
        if obj.type in has_modifier:
            for mod in obj.modifiers:
                if value == mod.type:
                    objectAction(self.operation, obj)
                    return True
        return False

    def MODIFIER_CONTAINS(self, obj, value):
        if obj.type in has_modifier:
            for mod in obj.modifiers:
                if value in mod.name:
                    objectAction(self.operation, obj)
                    return True
        return False

    def MODIFIER_IGNORE(self, obj, value):
        if obj.type in has_modifier:
            for mod in obj.modifiers:
                if value == mod.type:
                    return True
        return False

    def VERTEX_GROUP_CONTAINS(self, obj, value):
        if obj.type in has_vertex_group:
            for vg in obj.vertex_groups:
                if value in vg.name:
                    objectAction(self.operation, obj)
                    return True
        return False

    def VERTEX_GROUP_IGNORE(self, obj, value):
        if obj.type in has_vertex_group:
            for vg in obj.vertex_groups:
                if value in vg.name:
                    return True
        return False

    def SHAPE_KEY_CONTAINS(self, obj, value):
        if obj.type in has_shape_key:
            if obj.data.shape_keys is not None:
                for sk in obj.data.shape_keys.key_blocks:
                    if value in sk.name:
                        objectAction(self.operation, obj)
                        return True
        return False

    def SHAPE_KEY_IGNORE(self, obj, value):
        if obj.type in has_shape_key:
            if obj.data.shape_keys is not None:
                for sk in obj.data.shape_keys.key_blocks:
                    if value in sk.name:
                        return True
        return False

    def CONSTRAINT(self, obj, value):
        for con in obj.constraints:
            if value == con.type:
                objectAction(self.operation, obj)
                return True
        return False

    def CONSTRAINT_IGNORE(self, obj, value):
        for con in obj.constraints:
            if value == con.type:
                return True
        return False


class FiltersIgnore(Filters):
    filters = []
    priority = ['HIERARCHY_IGNORE', 'TYPE_IGNORE', 'IGNORE', 'CONSTRAINT_IGNORE', 'COLLECTION_IGNORE',
                'MODIFIER_IGNORE', 'MATERIAL_IGNORE', 'VERTEX_GROUP_IGNORE', 'SHAPE_KEY_IGNORE']
    already_checked = None
    operation = ''
    non_ignorable_count = 0

    def execFilters(self, obj):
        if 'force_state' in obj.keys():
            self.report({'INFO'}, 'Force used in execution')
            if obj['force_state'] == 'MARK':
                objectAction(self.operation, obj)
                self.already_checked.append(obj)
            elif obj['force_state'] == 'MARK_IGNORE':
                self.already_checked.append(obj)
            return

        for filter in self.filters:
            filter_exec = getattr(self, filter.type)
            res = filter_exec(obj, filter.value)
            if res:
                self.already_checked.append(obj.name)
                return

        if self.non_ignorable_count == 0:
            objectAction(self.operation, obj)

    def sortByFastestPriority(self):
        self.filters.sort(key=lambda x: self.priority.index(x.type))

    def HIERARCHY_IGNORE(self, obj, value):
        if obj == value:
            self.already_checked.append(obj.name)
            for child in obj.children_recursive:
                if child not in self.already_checked:
                    self.already_checked.append(child.name)


# TODO maybe add filter for greasepencil layers
class HIDEMANAGER_OT_All(Operator):
    bl_idname = 'hidemanager.all'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    filters = Filters()
    filters_ignore = FiltersIgnore()

    groups = []
    already_checked = []

    group: BoolProperty(default=False)

    operation: EnumProperty(default='SELECT', items=[
        ('SELECT', 'Select', 'Select objects by selected filter'),
        ('DESELECT', 'Deselect', 'Deselect objects by selected filter'),
        ('SELECT_INVERT', 'Select Invert', 'Select inverse objects by selected filter'),
        ('HIDE', 'Hide', 'Hide objects by selected filter'),
        ('SHOW', 'Show', 'Show objects by selected filter'),
        ('ENABLE_RENDER', 'Enable Render', 'Enable objects in render by selected filter'),
        ('DISABLE_RENDER', 'Disable Render', 'Disable objects in render by selected filter'),
        ('ENABLE_VIEWPORT', 'Enable Viewport', 'Enable objects in viewport by selected filter'),
        ('DISABLE_VIEWPORT', 'Disable Viewport', 'Disable objects in viewport by selected filter'),
    ])

    @classmethod
    def description(cls, context, properties):
        if properties.group:
            if context.scene.hidemanager_group_only_active:
                hdmg_context = 'selected group'
            else:
                hdmg_context = 'all enabled groups'
        else:
            hdmg_context = 'all enabled filters'

        if properties.operation == 'SELECT':
            return 'Select objects by %s' % hdmg_context
        elif properties.operation == 'DESELECT':
            return 'Deselect objects by %s' % hdmg_context
        elif properties.operation == 'SELECT_INVERT':
            return 'Select inverse objects by %s' % hdmg_context
        elif properties.operation == 'HIDE':
            return 'Hide objects by %s' % hdmg_context
        elif properties.operation == 'SHOW':
            return 'Show objects by %s' % hdmg_context
        elif properties.operation == 'ENABLE_RENDER':
            return 'Enable objects in render by %s' % hdmg_context
        elif properties.operation == 'DISABLE_RENDER':
            return 'Disable objects in render by %s' % hdmg_context
        elif properties.operation == 'ENABLE_VIEWPORT':
            return 'Enable objects in viewport by %s' % hdmg_context
        elif properties.operation == 'DISABLE_VIEWPORT':
            return 'Disable objects in viewport by %s' % hdmg_context

    # TODO add option disable order
    def execute(self, context):
        scene = context.scene
        if len(scene.hidemanager) == 0:
            for obj in scene.view_layers[0].objects:
                if 'force_state' in obj.keys():
                    self.report({'INFO'}, 'Force used in execution')
                    if obj['force_state'] == 'MARK':
                        objectAction(self.operation, obj)

            if context.mode == 'OBJECT':
                if self.operation == 'SELECT_INVERT':
                    bpy.ops.object.select_all(action='INVERT')
            else:
                self.report({'WARNING'}, 'This operation is not available in edit mode')
            return {'FINISHED'}

        self.clear()
        self.getConfig(context)

        self.filters.already_checked = self.already_checked
        self.filters.operation = self.operation

        if not self.filters.use_priority:
            self.filters_ignore.already_checked = self.already_checked
            self.filters_ignore.operation = self.operation
            self.filters_ignore.non_ignorable_count = self.filters.non_ignorable_count

        if not self.filters.use_priority:
            self.filters.sortByFastestPriority()

        if not self.filters.use_priority:
            self.filters_ignore.sortByFastestPriority()

            if self.filters_ignore.filter_count > 0:
                for obj in scene.view_layers[0].objects:
                    if obj.name in self.already_checked:
                        continue
                    self.filters_ignore.execFilters(obj)

        if self.filters.filter_count > 0:
            for obj in scene.view_layers[0].objects:
                if obj.name in self.already_checked:
                    continue
                self.filters.execFilters(obj)

        if context.mode == 'OBJECT':
            if self.operation == 'SELECT_INVERT':
                bpy.ops.object.select_all(action='INVERT')
        else:
            self.report({'WARNING'}, 'This operation is not available in edit mode')
        return {'FINISHED'}

    def getConfig(self, context):
        scene = context.scene
        if self.group:
            self.getGroups(context)

        if self.group:
            if not scene.hidemanager_group_order:
                self.groups = (list(set(self.groups)))
                idx = 0
                for item in scene.hidemanager:
                    idx += 1

                    if idx not in self.groups:
                        continue

                    self.getLines(item, False)
            else:
                for idx in self.groups:
                    try:
                        self.getLines(scene.hidemanager[idx - 1], True)
                    except IndexError:
                        pass
        else:
            for item in scene.hidemanager:
                if not item.line_enable:
                    continue

                self.getLines(item, scene.hidemanager_priority)

        self.group = False

    def getLines(self, item, priority):
        if item.line_type == 'CONTAINS':
            if item.contains == '':
                return
            # self.contains.append(item.contains)
            self.filters.append('CONTAINS', item.contains)

        elif item.line_type == 'IGNORE':
            if item.contains == '':
                return
            # self.ignore.append(item.contains)
            if not priority:
                self.filters_ignore.append('IGNORE', item.contains, True)
            else:
                self.filters.append('IGNORE', item.contains, True)

        elif item.line_type == 'TYPE':
            # self.types.append(item.object_type)
            self.filters.append('TYPE', item.object_type)

        elif item.line_type == 'TYPE_IGNORE':
            # self.types_ignore.append(item.object_type)
            if not priority:
                self.filters_ignore.append('TYPE_IGNORE', item.object_type, True)
            else:
                self.filters.append('TYPE_IGNORE', item.object_type, True)

        elif item.line_type == 'EXACT_OBJECT':
            if item.object is None:
                return
            self.filters.append('EXACT_OBJECT', item.object)

        elif item.line_type == 'EXACT_OBJECT_IGNORE':
            if item.object is None:
                return
            if not priority:
                self.filters_ignore.append('EXACT_OBJECT_IGNORE', item.object, True)
            else:
                self.filters.append('EXACT_OBJECT_IGNORE', item.object, True)

        elif item.line_type == 'HIERARCHY':
            if item.object is None:
                return
            # self.hierarchy.append(item.object)
            self.filters.append('HIERARCHY', item.object)

        elif item.line_type == 'HIERARCHY_IGNORE':
            if item.object is None:
                return
            # self.hierarchy_ignore.append(item.object)
            if not priority:
                self.filters_ignore.append('HIERARCHY_IGNORE', item.object, True)
            else:
                self.filters.append('HIERARCHY_IGNORE', item.object, True)

        elif item.line_type == 'COLLECTION':
            if item.collection is None:
                return
            # self.collection.append(item.collection)
            self.filters.append('COLLECTION', item.collection)

        elif item.line_type == 'COLLECTION_IGNORE':
            if item.collection is None:
                return
            # self.collection_ignore.append(item.collection)
            if not priority:
                self.filters_ignore.append('COLLECTION_IGNORE', item.collection, True)
            else:
                self.filters.append('COLLECTION_IGNORE', item.collection, True)

        elif item.line_type == 'MATERIAL':
            if item.material is None:
                return
            # self.material.append(item.material.name)
            self.filters.append('MATERIAL', item.material.name)

        elif item.line_type == 'MATERIAL_CONTAINS':
            if item.contains == '':
                return
            # self.material_contains.append(item.contains)
            self.filters.append('MATERIAL_CONTAINS', item.contains)

        elif item.line_type == 'MATERIAL_IGNORE':
            if item.material is None:
                return
            # self.material_ignore.append(item.material.name)
            if not priority:
                self.filters_ignore.append('MATERIAL_IGNORE', item.material.name, True)
            else:
                self.filters.append('MATERIAL_IGNORE', item.material.name, True)

        elif item.line_type == 'MODIFIER':
            # self.modifier.append(item.modifier_type)
            self.filters.append('MODIFIER', item.modifier_type)

        elif item.line_type == 'MODIFIER_CONTAINS':
            if item.contains == '':
                return
            # self.modifier_contains.append(item.contains)
            self.filters.append('MODIFIER_CONTAINS', item.contains)

        elif item.line_type == 'MODIFIER_IGNORE':
            # self.modifier_ignore.append(item.modifier_type)
            if not priority:
                self.filters_ignore.append('MODIFIER_IGNORE', item.modifier_type, True)
            else:
                self.filters.append('MODIFIER_IGNORE', item.modifier_type, True)

        elif item.line_type == 'VERTEX_GROUP_CONTAINS':
            if item.contains == '':
                return
            # self.vertex_group_contains.append(item.contains)
            self.filters.append('VERTEX_GROUP_CONTAINS', item.contains)

        elif item.line_type == 'VERTEX_GROUP_IGNORE':
            if item.contains == '':
                return
            # self.vertex_group_ignore.append(item.contains)
            if not priority:
                self.filters_ignore.append('VERTEX_GROUP_IGNORE', item.contains, True)
            else:
                self.filters.append('VERTEX_GROUP_IGNORE', item.contains, True)

        elif item.line_type == 'SHAPE_KEY_CONTAINS':
            if item.contains == '':
                return
            # self.shape_key_contains.append(item.contains)
            self.filters.append('SHAPE_KEY_CONTAINS', item.contains)

        elif item.line_type == 'SHAPE_KEY_IGNORE':
            if item.contains == '':
                return
            # self.shape_key_ignore.append(item.contains)
            if not priority:
                self.filters_ignore.append('SHAPE_KEY_IGNORE', item.contains, True)
            else:
                self.filters.append('SHAPE_KEY_IGNORE', item.contains, True)

        elif item.line_type == 'CONSTRAINT':
            # self.constraint.append(item.constraint_type)
            self.filters.append('CONSTRAINT', item.constraint_type)

        elif item.line_type == 'CONSTRAINT_IGNORE':
            # self.constraint_ignore.append(item.constraint_type)
            if not priority:
                self.filters_ignore.append('CONSTRAINT_IGNORE', item.constraint_type, True)
            else:
                self.filters.append('CONSTRAINT_IGNORE', item.constraint_type, True)

    def clear(self):
        self.filters.clear()
        self.filters_ignore.clear()
        self.groups.clear()
        self.already_checked.clear()

    def getGroups(self, context):
        scene = context.scene
        if scene.hidemanager_group_only_active:
            index = scene.hidemanager_group_index
            try:
                item = scene.hidemanager_group[index]
                if not item.line_enable:
                    return {'FINISHED'}
            except IndexError:
                pass
            else:
                for x in item.group.split(','):
                    if x == '':
                        continue
                    else:
                        if '-' in x:
                            try:
                                x = x.split('-')
                                for i in range(int(x[0]), int(x[1]) + 1):
                                    self.groups.append(i)
                            except ValueError:
                                self.report({'ERROR'},
                                            'Group id must be a number, group range "%s" ignored' % (x[0] + '-' + x[1]))
                        else:
                            try:
                                self.groups.append(int(x))
                            except ValueError:
                                self.report({'ERROR'}, 'Group id must be a number, group "%s" ignored' % x)
        else:
            for item in scene.hidemanager_group:
                if not item.line_enable:
                    continue
                if item.group == '':
                    continue

                for x in item.group.split(','):
                    if x == '':
                        continue
                    else:
                        if '-' in x:
                            try:
                                x = x.split('-')
                                for i in range(int(x[0]), int(x[1]) + 1):
                                    self.groups.append(i)
                            except ValueError:
                                self.report({'ERROR'},
                                            'Group id must be a number, group range "%s" ignored' % (x[0] + '-' + x[1]))
                        else:
                            try:
                                self.groups.append(int(x))
                            except ValueError:
                                self.report({'ERROR'}, 'Group id must be a number, group "%s" ignored' % x)
        # self.groups = (list(set(self.groups)))


class HIDEMANAGER_OT_Edit(Operator):
    bl_idname = 'hidemanager.edit'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    operation: EnumProperty(default='SELECT', items=[
        ('SELECT', 'Select', 'Select mesh by selected filter'),
        ('DESELECT', 'Deselect', 'Deselect mesh by selected filter'),
        ('SELECT_INVERT', 'Select Invert', 'Select inverse mesh by selected filter'),
        ('HIDE', 'Hide', 'Hide objects by selected filter'),
        ('SHOW', 'Show', 'Show objects by selected filter'),
    ])

    @classmethod
    def description(cls, context, properties):
        obj = context.active_object
        txt = ''
        if obj.hidemanager_edit_only_active:
            txt = 'selected filter'
        else:
            txt = 'all enabled filters'
        if properties.operation == 'SELECT':
            return 'Select mesh by %s' % txt
        elif properties.operation == 'DESELECT':
            return 'Deselect mesh by %s' % txt
        elif properties.operation == 'SELECT_INVERT':
            return 'Select inverse mesh by %s' % txt
        elif properties.operation == 'HIDE':
            return 'Hide mesh by %s' % txt
        elif properties.operation == 'SHOW':
            return 'Show mesh by %s' % txt

    def execute(self, context):
        scene = context.scene
        obj = context.active_object
        index = obj.hidemanager_edit_index
        already_checked = []

        if obj.hidemanager_edit_only_active:
            try:
                item = obj.hidemanager_edit[index]
                if not item.line_enable:
                    return {'FINISHED'}
            except IndexError:
                pass
            else:
                obj = context.active_object
                if item.line_type == 'MATERIAL':
                    self.material(obj, item.material)
                elif item.line_type == 'MATERIAL_CONTAINS':
                    self.materialContains(obj, item.contains)
                elif item.line_type == 'VERTEX_GROUP_CONTAINS':
                    self.vertexGroupContains(obj, item.contains)
        else:
            obj = context.active_object
            for filter in obj.hidemanager_edit:
                if not filter.line_enable:
                    continue
                if filter.line_type == 'MATERIAL':
                    self.material(obj, filter.material)
                elif filter.line_type == 'MATERIAL_CONTAINS':
                    self.materialContains(obj, filter.contains)
                elif filter.line_type == 'VERTEX_GROUP_CONTAINS':
                    self.vertexGroupContains(obj, filter.contains)

        if context.mode == 'EDIT_MESH':
            if self.operation == 'SELECT_INVERT':
                bpy.ops.mesh.select_all(action='INVERT')
        else:
            self.report({'WARNING'}, 'Edit mode is not active')
        return {'FINISHED'}

    def material(self, obj, material):
        material_idx = obj.data.materials.find(material.name)
        if material_idx == -1:
            return
        if self.operation == 'SELECT' or self.operation == 'SELECT_INVERT':
            obj.active_material_index = material_idx
            object.material_slot_select()
        elif self.operation == 'DESELECT':
            obj.active_material_index = material_idx
            object.material_slot_deselect()
        elif self.operation == 'HIDE':
            obj.active_material_index = material_idx
            object.material_slot_select()
            bpy.ops.mesh.hide()
        elif self.operation == 'SHOW':
            obj.active_material_index = material_idx
            object.material_slot_select()
            bpy.ops.mesh.reveal()
            bpy.ops.mesh.select_all(action='DESELECT')

    def materialContains(self, obj, contains):
        for mat in obj.data.materials:
            if contains in mat.name:
                material_idx = obj.data.materials.find(mat.name)
                if self.operation == 'SELECT' or self.operation == 'SELECT_INVERT':
                    obj.active_material_index = material_idx
                    object.material_slot_select()
                elif self.operation == 'DESELECT':
                    obj.active_material_index = material_idx
                    object.material_slot_deselect()
                elif self.operation == 'HIDE':
                    obj.active_material_index = material_idx
                    object.material_slot_select()
                    bpy.ops.mesh.hide()
                elif self.operation == 'SHOW':
                    obj.active_material_index = material_idx
                    object.material_slot_select()
                    bpy.ops.mesh.reveal()
                    bpy.ops.mesh.select_all(action='DESELECT')

    def vertexGroupContains(self, obj, contains):
        for vgroup in obj.vertex_groups:
            if contains in vgroup.name:
                if self.operation == 'SELECT' or self.operation == 'SELECT_INVERT':
                    obj.vertex_groups.active_index = vgroup.index
                    object.vertex_group_select()
                elif self.operation == 'DESELECT':
                    obj.vertex_groups.active_index = vgroup.index
                    object.vertex_group_deselect()
                elif self.operation == 'HIDE':
                    obj.vertex_groups.active_index = vgroup.index
                    object.vertex_group_select()
                    bpy.ops.mesh.hide()
                elif self.operation == 'SHOW':
                    obj.vertex_groups.active_index = vgroup.index
                    object.vertex_group_select()
                    bpy.ops.mesh.reveal()
                    bpy.ops.mesh.select_all(action='DESELECT')
