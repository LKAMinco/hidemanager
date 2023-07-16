import logging

import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import PropertyGroup, UIList, Panel
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

        split.prop(item, 'group', text='', toggle=False, slider=True)

    def invoke(self, context, event):
        pass


class HIDEMANAGER_PT_List(Panel):
    bl_idname = 'HIDEMANAGER_PT_List'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Hide Manager'
    bl_label = 'Hide Manager Filters'
    bl_order = 1
    bl_description = 'Hide Manager Filters'

    def draw(self, context):
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
                          rows=5)

        col = row.column(align=True)
        col.operator('hidemanager.actions', icon='ADD', text='').action = 'ADD'
        col.operator('hidemanager.actions', icon='REMOVE', text='').action = 'REMOVE'
        col.separator()
        col.operator("hidemanager.actions", icon='TRIA_UP', text="").action = 'UP'
        col.operator("hidemanager.actions", icon='TRIA_DOWN', text="").action = 'DOWN'

        row = layout.row()
        col = row.column(align=True)

        col.separator()
        row = col.row(align=True)

        priority = scene.hidemanager_priority
        selected = scene.hidemanager_only_active

        if not selected and not priority:
            row.label(text='!!! ALL ENABLED FILTERS, IGNORE FILTERS FIRST, THEN OTHER FILTERS !!!')
        elif not selected and priority:
            row.label(text='!!! ALL ENABLED FILTERS, FILTERS IN ORDER THAT ARE SPECIFIED !!!')
        elif selected and not priority:
            row.label(text='!!! ONLY SELECTED FILTER !!!')
        elif selected and priority:
            row.label(text='!!! ONLY SELECTED FILTER !!!')
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


class HIDEMANAGER_PT_GroupList(Panel):
    bl_idname = 'HIDEMANAGER_PT_GroupList'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Hide Manager'
    bl_label = 'Hide Manager Groups'
    bl_order = 2
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
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

        if not selected and not order:
            row.label(text='!!! ALL GROUPS, IGNORE FILTERS FIRST, THEN OTHER FILTERS !!!')
        elif not selected and order:
            row.label(text='!!! ALL GROUPS, FILTERS IN ORDER THAT ARE SPECIFIED IN GROUPS !!!')
        elif selected and not order:
            row.label(text='!!! ONLY SELECTED GROUP, IGNORE FILTERS FIRST THEN OTHER FILTERS !!!')
        elif selected and order:
            row.label(text='!!! ONLY SELECTED GROUP, FILTERS IN ORDER THAT ARE SPECIFIED IN GROUP !!!')
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
