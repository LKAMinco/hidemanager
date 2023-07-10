import logging

import bpy
from bpy.props import EnumProperty, BoolProperty
from bpy.types import Operator


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
        else:
            hdmng_context = context.scene.hidemanager

        for item in hdmng_context:
            if self.action == 'ENABLE':
                item.line_enable = True
            elif self.action == 'DISABLE':
                item.line_enable = False
            elif self.action == 'INVERT':
                item.line_enable = not item.line_enable
        return {'FINISHED'}


# TODO maybe add filter for greasepencil layers
class HIDEMANAGER_OT_Selected(Operator):
    bl_idname = 'hidemanager.selected'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    operation: EnumProperty(default='SELECT', items=[
        ('SELECT', 'Select', 'Select objects by selected filter'),
        ('DESELECT', 'Deselect', 'Deselect objects by selected filter'),
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
            if not item.line_enable:
                self.select = False
                return {'FINISHED'}
        except IndexError:
            pass

        else:
            has_material = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL']
            has_modifier = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL', 'LATTICE']
            has_vertex_group = ['MESH', 'LATTICE']
            has_shape_key = ['MESH', 'CURVE', 'SURFACE', 'LATTICE']
            already_checked = []

            for obj in scene.view_layers[0].objects:
                skip = False

                if obj in already_checked:
                    continue

                if item.line_type == 'CONTAINS':
                    if item.contains == '':
                        break
                    if item.contains in obj.name:
                        self.objectAction(obj)

                elif item.line_type == "IGNORE":
                    if item.contains == '':
                        break
                    if item.contains not in obj.name:
                        self.objectAction(obj)

                elif item.line_type == 'TYPE':
                    if obj.type == item.object_type:
                        self.objectAction(obj)

                elif item.line_type == 'TYPE_IGNORE':
                    if obj.type != item.object_type:
                        self.objectAction(obj)

                elif item.line_type == 'HIERARCHY':
                    if item.object is None:
                        break
                    if obj is item.object:
                        self.objectAction(obj)
                        already_checked.append(obj)
                        for child in obj.children_recursive:
                            self.objectAction(child)
                            already_checked.append(child)

                elif item.line_type == 'HIERARCHY_IGNORE':
                    if item.object is None:
                        break
                    if obj is not item.object:
                        self.objectAction(obj)
                    else:
                        for child in obj.children_recursive:
                            already_checked.append(child)

                elif item.line_type == 'COLLECTION':
                    if item.collection is None:
                        break
                    if item.collection in obj.users_collection:
                        self.objectAction(obj)

                elif item.line_type == 'COLLECTION_IGNORE':
                    if item.collection is None:
                        break
                    if item.collection not in obj.users_collection:
                        self.objectAction(obj)

                elif item.line_type == 'MATERIAL':
                    if obj.type in has_material:
                        if item.material is None:
                            break
                        if item.material.name in obj.data.materials:
                            self.objectAction(obj)

                elif item.line_type == 'MATERIAL_CONTAINS':
                    if obj.type in has_material:
                        if item.contains == '':
                            break
                        for mat in obj.data.materials:
                            if item.contains in mat.name:
                                self.objectAction(obj)

                elif item.line_type == 'MATERIAL_IGNORE':
                    if obj.type in has_material:
                        if item.material is None:
                            break
                        if item.material.name not in obj.data.materials:
                            self.objectAction(obj)

                elif item.line_type == 'MODIFIER':
                    if obj.type in has_modifier:
                        for mod in obj.modifiers:
                            if mod.type == item.modifier_type:
                                self.objectAction(obj)

                elif item.line_type == 'MODIFIER_CONTAINS':
                    if item.contains == '':
                        break
                    if obj.type in has_modifier:
                        for mod in obj.modifiers:
                            if item.contains in mod.name:
                                self.objectAction(obj)

                elif item.line_type == 'MODIFIER_IGNORE':
                    if obj.type in has_modifier:
                        mod_types = [mod.type for mod in obj.modifiers]
                        if item.modifier_type not in mod_types:
                            self.objectAction(obj)

                elif item.line_type == 'VERTEX_GROUP_CONTAINS':
                    if item.contains == '':
                        break
                    if obj.type in has_vertex_group:
                        for vg in obj.vertex_groups:
                            if item.contains in vg.name:
                                self.objectAction(obj)

                elif item.line_type == 'VERTEX_GROUP_IGNORE':
                    if item.contains == '':
                        break
                    if obj.type in has_vertex_group:
                        for vg in obj.vertex_groups:
                            if item.contains in vg.name:
                                skip = True
                        if not skip:
                            self.objectAction(obj)

                elif item.line_type == 'SHAPE_KEY_CONTAINS':
                    if item.contains == '':
                        break
                    if obj.type in has_shape_key:
                        if obj.data.shape_keys is not None:
                            for sk in obj.data.shape_keys.key_blocks:
                                if item.contains in sk.name:
                                    self.objectAction(obj)

                elif item.line_type == 'SHAPE_KEY_IGNORE':
                    if item.contains == '':
                        break
                    if obj.type in has_shape_key:
                        if obj.data.shape_keys is not None:
                            for sk in obj.data.shape_keys.key_blocks:
                                if item.contains in sk.name:
                                    skip = True
                            if not skip:
                                self.objectAction(obj)
                        else:
                            self.objectAction(obj)

                elif item.line_type == 'CONSTRAINT':
                    for con in obj.constraints:
                        if con.type == item.constraint_type:
                            self.objectAction(obj)

                elif item.line_type == 'CONSTRAINT_IGNORE':
                    con_types = [con.type for con in obj.constraints]
                    if item.constraint_type not in con_types:
                        self.objectAction(obj)

        return {'FINISHED'}

    def objectAction(self, obj: bpy.types.Object) -> None:
        """Performs the action selected in the enum

        :param bpy.types.Object obj: Object to be affected by operation
        :return: None
        """

        if self.operation == 'SELECT':
            obj.select_set(True)
        elif self.operation == 'DESELECT':
            obj.select_set(False)
        elif self.operation == 'HIDE':
            obj.hide_set(True)
        elif self.operation == 'SHOW':
            obj.hide_set(False)
        elif self.operation == 'ENABLE_RENDER':
            obj.hide_render = False
        elif self.operation == 'DISABLE_RENDER':
            obj.hide_render = True
        elif self.operation == 'ENABLE_VIEWPORT':
            obj.hide_viewport = False
        elif self.operation == 'DISABLE_VIEWPORT':
            obj.hide_viewport = True


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
    priority = ['HIERARCHY', 'TYPE', 'CONTAINS', 'CONSTRAINT', 'COLLECTION', 'MODIFIER', 'MODIFIER_CONTAINS',
                'MATERIAL', 'MATERIAL_CONTAINS', 'VERTEX_GROUP_CONTAINS', 'SHAPE_KEY_CONTAINS']
    has_material = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL']
    has_modifier = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL', 'LATTICE']
    has_vertex_group = ['MESH', 'LATTICE']
    has_shape_key = ['MESH', 'CURVE', 'SURFACE', 'LATTICE']
    operation = ''
    already_checked = None

    def execFilters(self, obj):
        for filter in self.filters:
            filter_exec = getattr(self, filter.type)
            res = filter_exec(obj, filter.value)
            if res:
                self.already_checked.append(obj.name)
                if self.non_ignorable_count == 0:
                    self.objectAction(obj)
                break

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

    def objectAction(self, obj: bpy.types.Object) -> None:
        """Performs the action selected in the enum

        :param bpy.types.Object obj: Object to be affected by operation
        :return: None
        """

        if self.operation == 'SELECT':
            obj.select_set(True)
        elif self.operation == 'DESELECT':
            obj.select_set(False)
        elif self.operation == 'HIDE':
            obj.hide_set(True)
        elif self.operation == 'SHOW':
            obj.hide_set(False)
        elif self.operation == 'ENABLE_RENDER':
            obj.hide_render = False
        elif self.operation == 'DISABLE_RENDER':
            obj.hide_render = True
        elif self.operation == 'ENABLE_VIEWPORT':
            obj.hide_viewport = False
        elif self.operation == 'DISABLE_VIEWPORT':
            obj.hide_viewport = True

    def CONTAINS(self, obj, value):
        if value in obj.name:
            self.objectAction(obj)
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
            self.objectAction(obj)
            return True
        return False

    def TYPE_IGNORE(self, obj, value):
        if obj.type == value:
            return True
        return False

    def HIERARCHY(self, obj, value):
        if obj is value:
            self.objectAction(obj)
            for child in obj.children_recursive:
                self.objectAction(child)
                if child not in self.already_checked:
                    self.already_checked.append(child.name)
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
            self.objectAction(obj)
            return True
        return False

    def COLLECTION_IGNORE(self, obj, value):
        if value in obj.users_collection:
            return True
        return False

    def MATERIAL(self, obj, value):
        if obj.type in self.has_material:
            if value in obj.data.materials:
                self.objectAction(obj)
                return True
        return False

    def MATERIAL_CONTAINS(self, obj, value):
        if obj.type in self.has_material:
            for mat in obj.data.materials:
                if value in mat.name:
                    self.objectAction(obj)
                    return True
        return False

    def MATERIAL_IGNORE(self, obj, value):
        if obj.type in self.has_material:
            if value in obj.data.materials:
                return True
        return False

    def MODIFIER(self, obj, value):
        if obj.type in self.has_modifier:
            for mod in obj.modifiers:
                if value == mod.type:
                    self.objectAction(obj)
                    return True
        return False

    def MODIFIER_CONTAINS(self, obj, value):
        if obj.type in self.has_modifier:
            for mod in obj.modifiers:
                if value in mod.name:
                    self.objectAction(obj)
                    return True
        return False

    def MODIFIER_IGNORE(self, obj, value):
        if obj.type in self.has_modifier:
            for mod in obj.modifiers:
                if value == mod.type:
                    return True
        return False

    def VERTEX_GROUP_CONTAINS(self, obj, value):
        if obj.type in self.has_vertex_group:
            for vg in obj.vertex_groups:
                if value in vg.name:
                    self.objectAction(obj)
                    return True
        return False

    def VERTEX_GROUP_IGNORE(self, obj, value):
        if obj.type in self.has_vertex_group:
            for vg in obj.vertex_groups:
                if value in vg.name:
                    return True
        return False

    def SHAPE_KEY_CONTAINS(self, obj, value):
        if obj.type in self.has_shape_key:
            if obj.data.shape_keys is not None:
                for sk in obj.data.shape_keys.key_blocks:
                    if value in sk.name:
                        self.objectAction(obj)
                        return True
        return False

    def SHAPE_KEY_IGNORE(self, obj, value):
        if obj.type in self.has_shape_key:
            if obj.data.shape_keys is not None:
                for sk in obj.data.shape_keys.key_blocks:
                    if value in sk.name:
                        return True
        return False

    def CONSTRAINT(self, obj, value):
        if obj.type in self.has_constraint:
            for con in obj.constraints:
                if value == con.type:
                    self.objectAction(obj)
                    return True
        return False

    def CONSTRAINT_IGNORE(self, obj, value):
        if obj.type in self.has_constraint:
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

    def execFilters(self, obj):
        for filter in self.filters:
            filter_exec = getattr(self, filter.type)
            res = filter_exec(obj, filter.value)
            if res:
                self.already_checked.append(obj.name)
                if self.non_ignorable_count == 0:
                    self.objectAction(obj)
                break

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
            return {'FINISHED'}

        self.clear()
        self.getConfig(context)

        self.filters.already_checked = self.already_checked
        self.filters.operation = self.operation

        if not scene.hidemanager_priority:
            self.filters_ignore.already_checked = self.already_checked
            self.filters_ignore.operation = self.operation

        if not self.filters.use_priority:
            self.filters.sortByFastestPriority()

        if not scene.hidemanager_priority:
            self.filters_ignore.sortByFastestPriority()

            for obj in scene.view_layers[0].objects:
                if obj.name in self.already_checked:
                    continue
                self.filters_ignore.execFilters(obj)

        for obj in scene.view_layers[0].objects:
            if obj.name in self.already_checked:
                continue
            self.filters.execFilters(obj)

        return {'FINISHED'}

    def getConfig(self, context):
        scene = context.scene
        if self.group:
            self.getGroups(context)

        if self.group:
            idxes = []
            for idx in self.groups:
                if scene.hidemanager_priority:
                    idx = 0
                    for item in scene.hidemanager:
                        idx += 1

                        if idx not in self.groups:
                            continue

                        self.getLines(item, scene.hidemanager_priority)
                else:
                    if idx in idxes:
                        continue
                    try:
                        self.getLines(scene.hidemanager[idx - 1], scene.hidemanager_priority)
                        idxes.append(idx)
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
                self.filters_ignore.append('IGNORE', item.contains)
            else:
                self.filters.append('IGNORE', item.contains, True)

        elif item.line_type == 'TYPE':
            # self.types.append(item.object_type)
            self.filters.append('TYPE', item.object_type)

        elif item.line_type == 'TYPE_IGNORE':
            # self.types_ignore.append(item.object_type)
            if not priority:
                self.filters_ignore.append('TYPE_IGNORE', item.object_type)
            else:
                self.filters.append('TYPE_IGNORE', item.object_type, True)

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
                self.filters_ignore.append('HIERARCHY_IGNORE', item.object)
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
                self.filters_ignore.append('COLLECTION_IGNORE', item.collection)
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
                self.filters_ignore.append('MATERIAL_IGNORE', item.material.name)
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
                self.filters_ignore.append('MODIFIER_IGNORE', item.modifier_type)
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
                self.filters_ignore.append('VERTEX_GROUP_IGNORE', item.contains)
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
                self.filters_ignore.append('SHAPE_KEY_IGNORE', item.contains)
            else:
                self.filters.append('SHAPE_KEY_IGNORE', item.contains, True)

        elif item.line_type == 'CONSTRAINT':
            # self.constraint.append(item.constraint_type)
            self.filters.append('CONSTRAINT', item.constraint_type)

        elif item.line_type == 'CONSTRAINT_IGNORE':
            # self.constraint_ignore.append(item.constraint_type)
            if not priority:
                self.filters_ignore.append('CONSTRAINT_IGNORE', item.constraint_type)
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
