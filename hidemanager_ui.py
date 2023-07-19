import logging

import bpy
from bpy.props import EnumProperty, StringProperty, BoolProperty
from bpy.types import PropertyGroup, UIList, Panel, Menu, Operator
from .icons import icons


class HIDEMANAGER_UL_Items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.03, align=True)
        split.prop(item, 'line_enable', text='', toggle=False, slider=True)
        split = split.split(factor=0.05, align=True)
        split.enabled = item.line_enable
        split.label(text=str(index + 1) + '.')
        split = split.split(factor=0.3, align=True)
        if 'IGNORE' in item.line_type:
            split.prop(item, 'line_type', text='', toggle=False, slider=True, icon_value=icons[item.line_type].icon_id)
        else:
            icon = item.bl_rna.properties['line_type'].enum_items[item.line_type].icon
            split.prop(item, 'line_type', text='', toggle=False, slider=True, icon=icon)

        if item.line_type == 'CONTAINS':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'IGNORE':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'TYPE':
            icon = item.bl_rna.properties['object_type'].enum_items[item.object_type].icon
            split.prop(item, 'object_type', text='', toggle=False, slider=True, icon=icon)
        elif item.line_type == 'TYPE_IGNORE':
            icon = item.bl_rna.properties['object_type'].enum_items[item.object_type].icon
            split.prop(item, 'object_type', text='', toggle=False, slider=True, icon=icon)
        elif item.line_type == 'HIERARCHY':
            split.prop(item, 'object', text='', toggle=False, slider=True, icon='OBJECT_DATA')
        elif item.line_type == 'HIERARCHY_IGNORE':
            split.prop(item, 'object', text='', toggle=False, slider=True, icon='OBJECT_DATA')
        elif item.line_type == 'COLLECTION':
            split.prop(item, 'collection', text='', toggle=False, slider=True, icon='OUTLINER_COLLECTION')
        elif item.line_type == 'COLLECTION_IGNORE':
            split.prop(item, 'collection', text='', toggle=False, slider=True, icon='OUTLINER_COLLECTION')
        elif item.line_type == 'MATERIAL':
            if item.material is not None:
                split = split.split(factor=0.06)
                icon = item.material.preview.icon_id
                split.label(text="", icon_value=icon)
            split.prop(item, 'material', text='', toggle=False, slider=True, icon='MATERIAL')
        elif item.line_type == 'MATERIAL_CONTAINS':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'MATERIAL_IGNORE':
            split.prop(item, 'material', text='', toggle=False, slider=True, icon='MATERIAL')
        elif item.line_type == 'MODIFIER':
            icon = item.bl_rna.properties['modifier_type'].enum_items[item.modifier_type].icon
            split.prop(item, 'modifier_type', text='', toggle=False, slider=True, icon=icon)
        elif item.line_type == 'MODIFIER_CONTAINS':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'MODIFIER_IGNORE':
            split.prop(item, 'modifier_type', text='', toggle=False, slider=True)
        elif item.line_type == 'VERTEX_GROUP_CONTAINS':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'VERTEX_GROUP_IGNORE':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'SHAPE_KEY_CONTAINS':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'SHAPE_KEY_IGNORE':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'CONSTRAINT':
            icon = item.bl_rna.properties['constraint_type'].enum_items[item.constraint_type].icon
            split.prop(item, 'constraint_type', text='', toggle=False, slider=True, icon=icon)
        elif item.line_type == 'CONSTRAINT_IGNORE':
            icon = item.bl_rna.properties['constraint_type'].enum_items[item.constraint_type].icon
            split.prop(item, 'constraint_type', text='', toggle=False, slider=True, icon=icon)

    def invoke(self, context, event):
        pass


class HIDEMANAGER_UL_GroupItems(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.03, align=True)
        split.prop(item, 'line_enable', text='', toggle=False, slider=True)
        split = split.split(factor=0.05, align=True)
        split.enabled = item.line_enable
        split.label(text=str(index + 1) + '.')
        split = split.split(factor=0.25, align=True)
        split.prop(item, 'group_name', text='', toggle=False, slider=True, emboss=False)
        split.prop(item, 'group', text='', toggle=False, slider=True, icon_value=icons['ID'].icon_id)

    def invoke(self, context, event):
        pass


class HIDEMANAGER_UL_EditItems(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.03, align=True)
        split.prop(item, 'line_enable', text='', toggle=False, slider=True)
        split = split.split(factor=0.05, align=True)
        split.enabled = item.line_enable
        split.label(text=str(index + 1) + '.')
        split = split.split(factor=0.2, align=True)
        split.prop(item, 'name', text='', toggle=False, slider=True, emboss=False)
        split = split.split(factor=0.35, align=True)
        icon = item.bl_rna.properties['line_type'].enum_items[item.line_type].icon
        split.prop(item, 'line_type', text='', toggle=False, slider=True, icon=icon)

        if item.line_type == 'MATERIAL':
            if item.material is not None:
                split = split.split(factor=0.06)
                icon = item.material.preview.icon_id
                split.label(text="", icon_value=icon)
            split.prop(item, 'material', text='', toggle=False, slider=True, icon='MATERIAL')
        elif item.line_type == 'MATERIAL_CONTAINS':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')
        elif item.line_type == 'VERTEX_GROUP_CONTAINS':
            split.prop(item, 'contains', text='', toggle=False, slider=True, icon='ALIGN_LEFT')

    def invoke(self, context, event):
        pass


class PanelBase:
    def drawEditPanel(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.active_object

        row = layout.row()
        row.label(text='!!! IN EDIT MODE DEPENDS ON SELECT MODE (VERT, EDGES, FACES) !!!')

        row = layout.row(align=True)
        op = row.operator('hidemanager.state', icon='CHECKMARK', text='')
        op.action = 'ENABLE'
        op.edit_mode = True
        op = row.operator('hidemanager.state', icon='X', text='')
        op.action = 'DISABLE'
        op.edit_mode = True
        op = row.operator('hidemanager.state', icon='UV_SYNC_SELECT', text='')
        op.action = 'INVERT'
        op.edit_mode = True
        row.separator()
        row.label(text='Enable / Disable / Invert all filters.')

        row = layout.row()
        row.template_list('HIDEMANAGER_UL_EditItems', '', obj, 'hidemanager_edit', obj, 'hidemanager_edit_index',
                          rows=5)

        col = row.column(align=True)
        col.operator('hidemanager_edit.actions', icon='ADD', text='').action = 'ADD'
        col.operator('hidemanager_edit.actions', icon='REMOVE', text='').action = 'REMOVE'
        col.separator()
        col.operator("hidemanager_edit.actions", icon='TRIA_UP', text="").action = 'UP'
        col.operator("hidemanager_edit.actions", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        col.separator()
        row = col.row(align=True)

        selected = obj.hidemanager_edit_only_active

        if selected:
            row.label(text='!!! ONLY SELECTED FILTER !!!')
        else:
            row.label(text='!!! ALL ENABLED FILTERS !!!')

        row = col.row(align=True)
        col.separator()

        row = col.row(align=True)
        row.label(text='Use only selected group')
        row.prop(obj, 'hidemanager_edit_only_active', text=str(obj.hidemanager_edit_only_active), toggle=True,
                 slider=True)

        hdmg_op = 'hidemanager.edit'

        row = col.row(align=True)
        row.operator(hdmg_op, text='Select Objects', icon='RESTRICT_SELECT_OFF').operation = 'SELECT'

        row.operator(hdmg_op, text='Deselect Objects', icon='RESTRICT_SELECT_ON').operation = 'DESELECT'

        row = col.row(align=True)
        row.operator(hdmg_op, text='Hide Objects', icon='HIDE_ON').operation = 'HIDE'

        row.operator(hdmg_op, text='Show Objects', icon='HIDE_OFF').operation = 'SHOW'

    def drawFilterPanel(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row(align=True)
        row.operator('hidemanager.state', icon='CHECKMARK', text='').action = 'ENABLE'
        row.operator('hidemanager.state', icon='X', text='').action = 'DISABLE'
        row.operator('hidemanager.state', icon='UV_SYNC_SELECT', text='').action = 'INVERT'
        row.separator()
        row.label(text='Enable / Disable / Invert all filters.')

        row = layout.row()
        row.template_list('HIDEMANAGER_UL_Items', '', scene, 'hidemanager', scene, 'hidemanager_index',
                          rows=8)

        col = row.column(align=True)
        col.operator('hidemanager.actions', icon='ADD', text='').action = 'ADD'
        col.operator('hidemanager.actions', icon='REMOVE', text='').action = 'REMOVE'
        col.separator()
        col.operator("hidemanager.actions", icon='TRIA_UP', text="").action = 'UP'
        col.operator("hidemanager.actions", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)

        row = col.row(align=True)
        row.label(text='Force object action')
        row = col.row(align=True)
        row.operator('hidemanager.force', text='Mark', icon='ADD').action = 'MARK'
        row.operator('hidemanager.force', text='Unmark', icon='PANEL_CLOSE').action = 'UNMARK'
        row.operator('hidemanager.force', text='Mark Ignore', icon='REMOVE').action = 'MARK_IGNORE'

        col.separator()
        row = col.row(align=True)

        priority = scene.hidemanager_priority
        selected = scene.hidemanager_only_active

        if selected:
            row.label(text='!!! ONLY SELECTED FILTER !!!')
        else:
            row.label(text='!!! ALL ENABLED FILTERS !!!')

        row = col.row(align=True)

        if priority:
            row.label(text='!!! IGNORE FILTERS FIRST, THEN OTHER FILTERS !!!')
        else:
            row.label(text='!!! FILTERS IN ORDER THAT ARE SPECIFIED !!!')
        col.separator()

        row = col.row(align=True)
        row.label(text='Use only selected filter')
        row.prop(scene, 'hidemanager_only_active', text=str(scene.hidemanager_only_active), toggle=True, slider=True)
        row = col.row(align=True)
        row.label(text='Use filter priority')
        row.prop(scene, 'hidemanager_priority', text=str(scene.hidemanager_priority), toggle=True, slider=True)
        row = col.row(align=True)

        if scene.hidemanager_only_active:
            hdmg_op = 'hidemanager.selected'
            row.operator(hdmg_op, text='Select Objects', icon='RESTRICT_SELECT_OFF').operation = 'SELECT'
            row.operator(hdmg_op, text='Deselect Objects',
                         icon='RESTRICT_SELECT_ON').operation = 'DESELECT'
            row = col.row(align=True)
            row.operator(hdmg_op, text='Hide Objects', icon='HIDE_ON').operation = 'HIDE'
            row.operator(hdmg_op, text='Show Objects', icon='HIDE_OFF').operation = 'SHOW'
            row = col.row(align=True)
            row.operator(hdmg_op, text='Disable In Renders',
                         icon='RESTRICT_RENDER_ON').operation = 'DISABLE_RENDER'
            row.operator(hdmg_op, text='Enable In Renders',
                         icon='RESTRICT_RENDER_OFF').operation = 'ENABLE_RENDER'
            row = col.row(align=True)
            row.operator(hdmg_op, text='Disable In Viewports',
                         icon='RESTRICT_VIEW_ON').operation = 'DISABLE_VIEWPORT'
            row.operator(hdmg_op, text='Enable In Viewports',
                         icon='RESTRICT_VIEW_OFF').operation = 'ENABLE_VIEWPORT'

        else:
            hdmg_op = 'hidemanager.all'
            row.operator(hdmg_op, text='Select Objects', icon='RESTRICT_SELECT_OFF').operation = 'SELECT'
            row.operator(hdmg_op, text='Deselect Objects',
                         icon='RESTRICT_SELECT_ON').operation = 'DESELECT'
            row = col.row(align=True)
            row.operator(hdmg_op, text='Hide Objects', icon='HIDE_ON').operation = 'HIDE'
            row.operator(hdmg_op, text='Show Objects', icon='HIDE_OFF').operation = 'SHOW'
            row = col.row(align=True)
            row.operator(hdmg_op, text='Disable In Renders',
                         icon='RESTRICT_RENDER_ON').operation = 'DISABLE_RENDER'
            row.operator(hdmg_op, text='Enable In Renders',
                         icon='RESTRICT_RENDER_OFF').operation = 'ENABLE_RENDER'
            row = col.row(align=True)
            row.operator(hdmg_op, text='Disable In Viewports',
                         icon='RESTRICT_VIEW_ON').operation = 'DISABLE_VIEWPORT'
            row.operator(hdmg_op, text='Enable In Viewports',
                         icon='RESTRICT_VIEW_OFF').operation = 'ENABLE_VIEWPORT'

    def drawGroupPanel(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.label(text='Groups uses both active and inactive filters from Hide Manager Filters')

        row = layout.row(align=True)
        op = row.operator('hidemanager.state', icon='CHECKMARK', text='')
        op.action = 'ENABLE'
        op.group = True
        op = row.operator('hidemanager.state', icon='X', text='')
        op.action = 'DISABLE'
        op.group = True
        op = row.operator('hidemanager.state', icon='UV_SYNC_SELECT', text='')
        op.action = 'INVERT'
        op.group = True
        row.separator()
        row.label(text='Enable / Disable / Invert all filters.')

        row = layout.row()
        row.template_list('HIDEMANAGER_UL_GroupItems', '', scene, 'hidemanager_group', scene, 'hidemanager_group_index',
                          rows=5)

        col = row.column(align=True)
        col.operator('hidemanager_group.actions', icon='ADD', text='').action = 'ADD'
        col.operator('hidemanager_group.actions', icon='REMOVE', text='').action = 'REMOVE'
        col.separator()
        col.operator("hidemanager_group.actions", icon='TRIA_UP', text="").action = 'UP'
        col.operator("hidemanager_group.actions", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)
        col.separator()
        row = col.row(align=True)

        order = scene.hidemanager_group_order
        selected = scene.hidemanager_group_only_active

        if selected:
            row.label(text='!!! ONLY SELECTED GROUP !!!')
        else:
            row.label(text='!!! ALL ENABLED GROUPS !!!')

        row = col.row(align=True)

        if order:
            row.label(text='!!! FILTERS IN ORDER THAT ARE SPECIFIED IN GROUP !!!')
        else:
            row.label(text='!!! IGNORE FILTERS FIRST, THEN OTHER FILTERS !!!')
        col.separator()

        row = col.row(align=True)
        row.label(text='Use only selected group')
        row.prop(scene, 'hidemanager_group_only_active', text=str(scene.hidemanager_group_only_active), toggle=True,
                 slider=True)
        row = col.row(align=True)
        row.label(text='Use filters in specified order')
        row.prop(scene, 'hidemanager_group_order', text=str(scene.hidemanager_group_order), toggle=True,
                 slider=True)

        hdmg_op = 'hidemanager.all'

        row = col.row(align=True)
        op = row.operator(hdmg_op, text='Select Objects', icon='RESTRICT_SELECT_OFF')
        op.operation = 'SELECT'
        op.group = True

        op = row.operator(hdmg_op, text='Deselect Objects', icon='RESTRICT_SELECT_ON')
        op.operation = 'DESELECT'
        op.group = True

        row = col.row(align=True)
        op = row.operator(hdmg_op, text='Hide Objects', icon='HIDE_ON')
        op.operation = 'HIDE'
        op.group = True

        op = row.operator(hdmg_op, text='Show Objects', icon='HIDE_OFF')
        op.operation = 'SHOW'
        op.group = True

        row = col.row(align=True)
        op = row.operator(hdmg_op, text='Disable In Renders', icon='RESTRICT_RENDER_ON')
        op.operation = 'DISABLE_RENDER'
        op.group = True

        op = row.operator(hdmg_op, text='Enable In Renders', icon='RESTRICT_RENDER_OFF')
        op.operation = 'ENABLE_RENDER'
        op.group = True

        row = col.row(align=True)
        op = row.operator(hdmg_op, text='Disable In Viewports', icon='RESTRICT_VIEW_ON')
        op.operation = 'DISABLE_VIEWPORT'
        op.group = True

        op = row.operator(hdmg_op, text='Enable In Viewports', icon='RESTRICT_VIEW_OFF')
        op.operation = 'ENABLE_VIEWPORT'
        op.group = True


class HIDEMANAGER_PT_List(Panel, PanelBase):
    bl_idname = 'HIDEMANAGER_PT_List'
    bl_space_type = 'VIEW_3D'
    bl_context = 'objectmode'
    bl_region_type = 'UI'
    bl_category = 'Hide Manager'
    bl_label = 'Hide Manager Filters'
    bl_order = 1
    bl_description = 'Hide Manager Filters'

    def draw(self, context):
        self.drawFilterPanel(context)


class HIDEMANAGER_PT_GroupList(Panel, PanelBase):
    bl_idname = 'HIDEMANAGER_PT_GroupList'
    bl_space_type = 'VIEW_3D'
    bl_context = 'objectmode'
    bl_region_type = 'UI'
    bl_category = 'Hide Manager'
    bl_label = 'Hide Manager Groups'
    bl_order = 2
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.drawGroupPanel(context)


class HIDEMANAGER_PT_EditList(Panel, PanelBase):
    bl_idname = 'HIDEMANAGER_PT_EditList'
    bl_space_type = 'VIEW_3D'
    bl_context = 'mesh_edit'
    bl_region_type = 'UI'
    bl_category = 'Hide Manager'
    bl_label = 'Hide Manager Edit Filters'

    @classmethod
    def poll(cls, context):
        if context.mode == 'EDIT_MESH':
            return True
        return False

    def draw(self, context):
        self.drawEditPanel(context)


class HIDEMANAGER_MT_Menu(Menu):
    bl_idname = 'HIDEMANAGER_MT_Menu'
    bl_label = 'Hide Manager Pie Menu'

    def draw(self, context):
        pie = self.layout.menu_pie()

        is_edit = context.mode == 'EDIT_MESH'

        if is_edit:
            hdmg_op = 'hidemanager.edit'
        else:
            if context.scene.hidemanager_only_active:
                hdmg_op = 'hidemanager.selected'
            else:
                hdmg_op = 'hidemanager.all'

        if context.scene.hidemanager_use_select:
            box = pie.box()
            box.operator(hdmg_op, text='Select Objects', icon='RESTRICT_SELECT_OFF').operation = 'SELECT'
            box.operator(hdmg_op, text='Deselect Objects',
                         icon='RESTRICT_SELECT_ON').operation = 'DESELECT'

        if context.scene.hidemanager_use_hide:
            box = pie.box()
            box.operator(hdmg_op, text='Hide Objects', icon='HIDE_ON').operation = 'HIDE'
            box.operator(hdmg_op, text='Show Objects', icon='HIDE_OFF').operation = 'SHOW'

        if not is_edit:
            if context.scene.hidemanager_use_render:
                box = pie.box()
                box.operator(hdmg_op, text='Disable In Renders',
                             icon='RESTRICT_RENDER_ON').operation = 'DISABLE_RENDER'
                box.operator(hdmg_op, text='Enable In Renders',
                             icon='RESTRICT_RENDER_OFF').operation = 'ENABLE_RENDER'

        if not is_edit:
            if context.scene.hidemanager_use_viewport:
                box = pie.box()
                box.operator(hdmg_op, text='Disable In Viewports',
                             icon='RESTRICT_VIEW_ON').operation = 'DISABLE_VIEWPORT'
                box.operator(hdmg_op, text='Enable In Viewports',
                             icon='RESTRICT_VIEW_OFF').operation = 'ENABLE_VIEWPORT'

        if not is_edit:
            if context.scene.hidemanager_use_force:
                row = pie.row(align=True)
                row.operator('hidemanager.force', text='', icon='ADD').action = 'MARK'
                row.operator('hidemanager.force', text='', icon='PANEL_CLOSE').action = 'UNMARK'
                row.operator('hidemanager.force', text='', icon='REMOVE').action = 'MARK_IGNORE'

        if not is_edit:
            if context.scene.hidemanager_use_settings:
                box = pie.box()
                box.prop(context.scene, 'hidemanager_only_active', text='Use only selected filter')
                box.prop(context.scene, 'hidemanager_priority', text='Use filter priority')
        else:
            if context.scene.hidemanager_use_settings:
                box = pie.box()
                box.prop(context.scene, 'hidemanager_edit_only_active', text='Use only selected filter')


class HIDEMANAGER_OT_EditMenuDialog(Operator, PanelBase):
    bl_idname = 'hidemanager.edit_menu_dialog'
    bl_label = 'Hidemanager Popup Dialog'
    bl_description = 'Hidemanager Popup Dialog'
    bl_options = {'REGISTER', 'UNDO'}

    pages: EnumProperty(default='FILTERS', items=[('FILTERS', 'Filters', 'Filters'), ('GROUPS', 'Groups', 'Groups')])

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=450)

    def draw(self, context):
        if context.mode == 'EDIT_MESH':
            self.drawEditPanel(context)
        else:
            layout = self.layout
            row = layout.row(align=True)
            row.prop(self, 'pages', expand=True)

            if self.pages == 'FILTERS':
                self.drawFilterPanel(context)
            elif self.pages == 'GROUPS':
                self.drawGroupPanel(context)

    def execute(self, context):
        return {'FINISHED'}
