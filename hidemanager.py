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
            item.line_type = 'CONTAINS'
            item.object_type = 'MESH'
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


# TODO maybe add filter for collections
# TODO maybe add filter for modifiers
# TODO maybe add filter for vertex groups
# TODO maybe add filter for shape keys
# TODO maybe add filter for constraints
# TODO maybe add filter for greasepencil layers
# TODO add hide for render
# TODO add method to operations
# TODO rework to use inheritance of class with operations
# TODO check for default values for groups in ui
# TODO rework hide/unhide to enum
class HIDEMANAGER_OT_Selected(Operator):
    bl_idname = 'hidemanager.selected'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    hide: BoolProperty(default=False)

    render: BoolProperty(default=False)

    viewport: BoolProperty(default=False)

    select: BoolProperty(default=False)

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

            if item.line_type == 'MODIFIER':
                logging.log(logging.WARNING, str(item.modifier_type))
                logging.log(logging.WARNING, item.mod_items)

            for obj in scene.view_layers[0].objects:
                if item.line_type == 'CONTAINS':
                    if item.contains == '':
                        break
                    if item.contains in obj.name:
                        self.objectAction(obj)

                elif item.line_type == 'TYPE':
                    if obj.type == item.object_type:
                        self.objectAction(obj)

                elif item.line_type == 'TYPE_IGNORE':
                    if obj.type != item.object_type:
                        self.objectAction(obj)

                elif item.line_type == "IGNORE":
                    if item.contains_ignore == '':
                        break
                    if item.contains_ignore not in obj.name:
                        self.objectAction(obj)

                elif item.line_type == 'MATERIAL':
                    if obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE' or obj.type == "META" or obj.type == "FONT":
                        if item.material is None:
                            break
                        if item.material.name in obj.data.materials:
                            self.objectAction(obj)

                elif item.line_type == 'MATERIAL_CONTAINS':
                    if obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE' or obj.type == "META" or obj.type == "FONT":
                        if item.material is None:
                            break
                        for mat in obj.data.materials:
                            if item.material_contains in mat.name:
                                if self.select:
                                    obj.select_set(True)
                                else:
                                    obj.hide_set(self.hide)

                elif item.line_type == 'MATERIAL_IGNORE':
                    if obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE' or obj.type == "META" or obj.type == "FONT":
                        if item.material_ignore is None:
                            break
                        if item.material_ignore.name not in obj.data.materials:
                            if self.select:
                                obj.select_set(True)
                            else:
                                obj.hide_set(self.hide)

                elif item.line_type == 'HIERARCHY':
                    if item.object is None:
                        break
                    if obj is item.object:
                        if self.select:
                            obj.select_set(True)
                        else:
                            obj.hide_set(self.hide)
                        for child in item.object.children_recursive:
                            if self.select:
                                child.select_set(True)
                            else:
                                child.hide_set(self.hide)

        self.select = False
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


# TODO maybe add filter for collections
# TODO maybe add filter for modifiers
# TODO maybe add filter for vertex groups
# TODO maybe add filter for shape keys
# TODO maybe add filter for constraints
# TODO add hide for render
# TODO add method to operations
# TODO rework to use inheritance of class with operations
# TODO check for default values for groups in ui
# TODO rework hide/unhide to enum
class HIDEMANAGER_OT_All(Operator):
    bl_idname = 'hidemanager.all'
    bl_label = ''
    bl_description = ''
    bl_options = {'REGISTER'}

    contains = []
    hierarchy = []
    ignore = []
    material = []
    material_contains = []
    material_ignore = []
    types = []
    types_ignore = []
    groups = []

    hide: BoolProperty(default=False)

    render: BoolProperty(default=False)

    select: BoolProperty(default=False)

    group: BoolProperty(default=False)

    @classmethod
    def description(cls, context, properties):
        if not properties.group:
            hdmng_context = 'objects by all active filters'

            if properties.select:
                return 'Select %s' % hdmng_context
            else:
                if properties.hide:
                    return 'Hide %s' % hdmng_context
                else:
                    return 'Show %s' % hdmng_context
        else:
            if context.scene.hidemanager_group_only_active:
                hdmng_context = 'objects by active group'
            else:
                hdmng_context = 'objects by all active groups'
            if properties.select:
                return 'Select %s' % hdmng_context
            else:
                if properties.hide:
                    return 'Hide %s' % hdmng_context
                else:
                    return 'Show %s' % hdmng_context

    def execute(self, context):
        scene = context.scene
        self.clear()
        self.getConfig(context, self.group)
        skip_objects = []

        # logging.log(logging.WARNING, 'HIDEMANAGER groups: %s' % self.groups)
        # logging.log(logging.WARNING, 'HIDEMANAGER types: %s' % self.types)
        # logging.log(logging.WARNING, 'HIDEMANAGER types_ignore: %s' % self.types_ignore)
        # logging.log(logging.WARNING, 'HIDEMANAGER contains: %s' % self.contains)
        # logging.log(logging.WARNING, 'HIDEMANAGER ignore: %s' % self.ignore)
        # logging.log(logging.WARNING, 'HIDEMANAGER material: %s' % self.material)
        # logging.log(logging.WARNING, 'HIDEMANAGER material_contains: %s' % self.material_contains)
        # logging.log(logging.WARNING, 'HIDEMANAGER material_ignore: %s' % self.material_ignore)
        # logging.log(logging.WARNING, 'HIDEMANAGER hierarchy: %s' % self.hierarchy)

        for obj in scene.view_layers[0].objects:
            if len(scene.hidemanager) == 0:
                break

            if obj in skip_objects:
                continue

            if obj in self.hierarchy:
                result = self.checkObject(obj)
                if result:
                    self.objectAction(context, obj)

                for child in obj.children_recursive:
                    result = self.checkObject(child, True)
                    if not result:
                        continue
                    else:
                        self.objectAction(context, child)
                        skip_objects.append(child)
                        continue
                continue

            result = self.checkObject(obj)
            if not result:
                continue
            else:
                self.objectAction(context, obj)
                continue

        self.select = False
        return {'FINISHED'}

    def checkObject(self, obj, hierarchy=False):
        if obj.type in self.types_ignore:
            return False

        for ign in self.ignore:
            if ign in obj.name:
                return False
        # TODO change to list of valid types
        if obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE' or obj.type == "META" or obj.type == "FONT":
            if len(obj.data.materials) != 0:
                for mat in self.material_ignore:
                    if mat in obj.data.materials:
                        return False

        if obj.type in self.types:
            return True

        for contain in self.contains:
            if contain in obj.name:
                return True

        if obj.type == 'MESH' or obj.type == 'CURVE' or obj.type == 'SURFACE' or obj.type == "META" or obj.type == "FONT":
            if len(obj.data.materials) != 0:
                for mat in self.material:
                    if mat in obj.data.materials:
                        return True

                for mat in self.material_contains:
                    for mat_obj in obj.data.materials:
                        if mat in mat_obj.name:
                            return True
        if hierarchy:
            return True

        return False

    def objectAction(self, context, obj):
        if self.select:
            obj.select_set(True)
        else:
            if self.render:
                obj.hide_render = self.render
            elif self.viewport:
                obj.hide_viewport = self.viewport
            else:
                obj.hide_set(self.hide)

    def getConfig(self, context, group=False):
        scene = context.scene
        if group:
            self.getGroups(context)
        idx = 0
        for item in scene.hidemanager:
            idx += 1
            if idx not in self.groups and group:
                continue

            if not item.line_enable and not group:
                continue

            if item.line_type == 'CONTAINS':
                if item.contains == '':
                    continue
                self.contains.append(item.contains)

            elif item.line_type == 'IGNORE':
                if item.contains_ignore == '':
                    continue
                self.ignore.append(item.contains_ignore)

            elif item.line_type == 'TYPE':
                self.types.append(item.object_type)

            elif item.line_type == 'TYPE_IGNORE':
                self.types_ignore.append(item.object_type)

            elif item.line_type == 'MATERIAL':
                if item.material is None:
                    continue
                self.material.append(item.material.name)

            elif item.line_type == 'MATERIAL_CONTAINS':
                if item.material_contains is None:
                    continue
                self.material_contains.append(item.material_contains)

            elif item.line_type == 'MATERIAL_IGNORE':
                if item.material_ignore is None:
                    continue
                self.material_ignore.append(item.material_ignore.name)

            elif item.line_type == 'HIERARCHY':
                if item.object is None:
                    continue
                self.hierarchy.append(item.object)

    def clear(self):
        self.contains.clear()
        self.ignore.clear()
        self.types.clear()
        self.types_ignore.clear()
        self.material.clear()
        self.material_contains.clear()
        self.material_ignore.clear()
        self.hierarchy.clear()
        self.groups.clear()

    def getGroups(self, context):
        scene = context.scene
        if scene.hidemanager_group_only_active:
            index = scene.hidemanager_group_index
            try:
                item = scene.hidemanager_group[index]
                if not item.line_enable:
                    self.select = False
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
