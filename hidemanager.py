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
# TODO rework to use inheritance of class with operations
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


# TODO maybe add filter for greasepencil layers
# TODO rework to use inheritance of class with operations
class HIDEMANAGER_OT_All(Operator):
    bl_idname = 'hidemanager.all'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    contains = []
    ignore = []
    types = []
    types_ignore = []
    hierarchy = []
    hierarchy_ignore = []
    collection = []
    collection_ignore = []
    material = []
    material_contains = []
    material_ignore = []
    modifier = []
    modifier_contains = []
    modifier_ignore = []
    vertex_group_contains = []
    vertex_group_ignore = []
    shape_key_contains = []
    shape_key_ignore = []
    constraint = []
    constraint_ignore = []
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

    def execute(self, context):
        scene = context.scene
        self.clear()
        self.getConfig(context, self.group)

        if len(scene.hidemanager) == 0:
            return {'FINISHED'}

        ignore_count = len(self.ignore) + len(self.types_ignore) + len(self.hierarchy_ignore) + len(
            self.collection_ignore) + len(self.material_ignore) + len(self.modifier_ignore) + len(
            self.vertex_group_ignore) + len(self.shape_key_ignore) + len(self.constraint_ignore)

        filter_count = len(self.contains) + len(self.types) + len(self.hierarchy) + len(self.collection) + len(
            self.material) + len(self.material_contains) + len(self.modifier) + len(self.modifier_contains) + len(
            self.vertex_group_contains) + len(self.shape_key_contains) + len(
            self.constraint)

        if ignore_count > 0:
            # 2 loops needed to check for ignored objects first
            for obj in scene.view_layers[0].objects:
                if obj in self.already_checked:
                    continue

                # only ignore filters -> everything except ignored objects are selected
                if self.getIgnoredObjects(obj) and filter_count == 0:
                    self.objectAction(obj)

        if filter_count > 0:
            for obj in scene.view_layers[0].objects:
                if obj in self.already_checked:
                    continue

                if self.checkObject(obj):
                    self.objectAction(obj)
                    self.already_checked.append(obj)

        return {'FINISHED'}

    def getIgnoredObjects(self, obj: bpy.types.Object) -> bool:
        """Process ignored objects and add them to already_checked list

        :param bpy.types.Object obj: Object to check
        :return: None
        """
        has_material = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL']
        has_modifier = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL', 'LATTICE']
        has_vertex_group = ['MESH', 'LATTICE']
        has_shape_key = ['MESH', 'CURVE', 'SURFACE', 'LATTICE']

        if obj in self.hierarchy_ignore:
            self.already_checked.append(obj)
            for child in obj.children_recursive:
                self.already_checked.append(child)
            return False

        if obj.type in self.types_ignore:
            self.already_checked.append(obj)
            return False

        if obj.users_collection in self.collection_ignore:
            self.already_checked.append(obj)
            return False

        for contain in self.ignore:
            if contain in obj.name:
                self.already_checked.append(obj)
                return False

        if obj.type in has_modifier:
            for mod in obj.modifiers:
                if mod.type in self.modifier_ignore:
                    self.already_checked.append(obj)
                    return False

        if obj.type in has_material:
            for mat in self.material_ignore:
                if mat in obj.material_slots:
                    self.already_checked.append(obj)
                    return False

        for const in obj.constraints:
            if const.type in self.constraint_ignore:
                self.already_checked.append(obj)
                return False

        if obj.type in has_vertex_group:
            for contain in self.vertex_group_ignore:
                for vg in obj.vertex_groups:
                    if contain in vg.name:
                        self.already_checked.append(obj)
                        return False

        if obj.type in has_shape_key:
            if obj.data.shape_keys is not None:
                for contain in self.shape_key_ignore:
                    for sk in obj.data.shape_keys.key_blocks:
                        if contain in sk.name:
                            self.already_checked.append(obj)
                            return False

        return True

    def checkObject(self, obj: bpy.types.Object) -> bool:
        """Process objects and return if can be processed

        :param bpy.types.Object obj: Object to check
        :return: Bool
        """
        has_material = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL']
        has_modifier = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL', 'LATTICE']
        has_vertex_group = ['MESH', 'LATTICE']
        has_shape_key = ['MESH', 'CURVE', 'SURFACE', 'LATTICE']

        # vertex_group_contains, shape_key_contains, constraint

        if obj.type in self.types:
            return True

        for contain in self.contains:
            if contain in obj.name:
                return True

        if len(self.constraint) > 0:
            for const in obj.constraints:
                if const.type in self.constraint:
                    return True

        if obj in self.hierarchy:
            self.objectAction(obj)
            self.already_checked.append(obj)
            for child in obj.children_recursive:
                self.objectAction(child)
                self.already_checked.append(child)
            return False

        if obj.users_collection in self.collection:
            return False

        if obj.type in has_modifier:
            if len(self.modifier) > 0:
                for mod in obj.modifiers:
                    if mod.type in self.modifier:
                        return True

                    for contain in self.modifier_contains:
                        if contain in mod.name:
                            return True

        if obj.type in has_material:
            if (len(self.material) + len(self.material_contains)) > 0:
                for mat in obj.material_slots:
                    if mat.name in self.material:
                        return True

                    for contain in self.material_contains:
                        if contain in mat.name:
                            return True

        if obj.type in has_vertex_group:
            if len(self.vertex_group_contains) > 0:
                for vg in obj.vertex_groups:
                    for contain in self.vertex_group_contains:
                        if contain in vg.name:
                            return True

        if obj.type in has_shape_key:
            if obj.data.shape_keys is not None:
                if len(self.shape_key_contains) > 0:
                    for sk in obj.data.shape_keys.key_blocks:
                        for contain in self.shape_key_contains:
                            if contain in sk.name:
                                return True

        return False

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

    def getConfig(self, context, group=False):
        scene = context.scene
        if group:
            self.getGroups(context)

        idx = 0
        for item in scene.hidemanager:
            # in case of group, skip filter when is not in group
            idx += 1
            if idx not in self.groups and group:
                continue

            # skip filter if is not enabled
            if not item.line_enable and not group:
                continue

            if item.line_type == 'CONTAINS':
                if item.contains == '':
                    continue
                self.contains.append(item.contains)

            elif item.line_type == 'IGNORE':
                if item.contains_ignore == '':
                    continue
                self.ignore.append(item.contains)

            elif item.line_type == 'TYPE':
                self.types.append(item.object_type)

            elif item.line_type == 'TYPE_IGNORE':
                self.types_ignore.append(item.object_type)

            elif item.line_type == 'HIERARCHY':
                if item.object is None:
                    continue
                self.hierarchy.append(item.object)

            elif item.line_type == 'HIERARCHY_IGNORE':
                if item.object is None:
                    continue
                self.hierarchy_ignore.append(item.object)

            elif item.line_type == 'COLLECTION':
                if item.collection is None:
                    continue
                self.collection.append(item.collection)

            elif item.line_type == 'COLLECTION_IGNORE':
                if item.collection is None:
                    continue
                self.collection_ignore.append(item.collection)

            elif item.line_type == 'MATERIAL':
                if item.material is None:
                    continue
                self.material.append(item.material.name)

            elif item.line_type == 'MATERIAL_CONTAINS':
                if item.contains == '':
                    continue
                self.material_contains.append(item.contains)

            elif item.line_type == 'MATERIAL_IGNORE':
                if item.material is None:
                    continue
                self.material_ignore.append(item.material.name)

            elif item.line_type == 'MODIFIER':
                self.modifier.append(item.modifier_type)

            elif item.line_type == 'MODIFIER_CONTAINS':
                if item.contains == '':
                    continue
                self.modifier_contains.append(item.contains)

            elif item.line_type == 'MODIFIER_IGNORE':
                self.modifier_ignore.append(item.modifier_type)

            elif item.line_type == 'VERTEX_GROUP_CONTAINS':
                if item.contains == '':
                    continue
                self.vertex_group_contains.append(item.contains)

            elif item.line_type == 'VERTEX_GROUP_IGNORE':
                if item.contains == '':
                    continue
                self.vertex_group_ignore.append(item.contains)

            elif item.line_type == 'SHAPE_KEY_CONTAINS':
                if item.contains == '':
                    continue
                self.shape_key_contains.append(item.contains)

            elif item.line_type == 'SHAPE_KEY_IGNORE':
                if item.contains == '':
                    continue
                self.shape_key_ignore.append(item.contains)

            elif item.line_type == 'CONSTRAINT':
                self.constraint.append(item.constraint_type)

            elif item.line_type == 'CONSTRAINT_IGNORE':
                self.constraint_ignore.append(item.constraint_type)

            self.group = False

    def clear(self):
        self.contains.clear()
        self.ignore.clear()
        self.types.clear()
        self.types_ignore.clear()
        self.hierarchy.clear()
        self.hierarchy_ignore.clear()
        self.collection.clear()
        self.collection_ignore.clear()
        self.material.clear()
        self.material_contains.clear()
        self.material_ignore.clear()
        self.modifier.clear()
        self.modifier_contains.clear()
        self.modifier_ignore.clear()
        self.vertex_group_contains.clear()
        self.vertex_group_ignore.clear()
        self.shape_key_contains.clear()
        self.shape_key_ignore.clear()
        self.constraint.clear()
        self.constraint_ignore.clear()
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
        self.groups = (list(set(self.groups)))
