import bpy
from bpy.props import EnumProperty, StringProperty
from bpy.types import PropertyGroup, UIList, Panel
class HIDEMANAGER_UL_Items(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.03)
        split.prop(item, 'line_enable', text='', toggle=False, slider=True)
        split = split.split(factor=0.05)
        split.enabled = item.line_enable
        split.label(text=str(index + 1) + '.')
        split = split.split(factor=0.3)
        split.prop(item, 'line_type', text='', toggle=False, slider=True)

        if item.line_type == 'CONTAINS':
            split.prop(item, 'contains', text='', toggle=False, slider=True)
        elif item.line_type == 'IGNORE':
            split.prop(item, 'contains_ignore', text='', toggle=False, slider=True)
        elif item.line_type == 'TYPE':
            split.prop(item, 'object_type', text='', toggle=False, slider=True)
        elif item.line_type == 'TYPE_IGNORE':
            split.prop(item, 'object_type', text='', toggle=False, slider=True)
        elif item.line_type == 'MATERIAL':
            split.prop(item, 'material', text='', toggle=False, slider=True, icon='MATERIAL')
        elif item.line_type == 'MATERIAL_CONTAINS':
            split.prop(item, 'material_contains', text='', toggle=False, slider=True)
        elif item.line_type == 'MATERIAL_IGNORE':
            split.prop(item, 'material_ignore', text='', toggle=False, slider=True, icon='MATERIAL')
        elif item.line_type == 'HIERARCHY':
            split.prop(item, 'object', text='', toggle=False, slider=True)
        elif item.line_type == 'MODIFIER':
            split.prop(item, 'modifier_type', text='', toggle=False, slider=True)

    def invoke(self, context, event):
        pass


class HIDEMANAGER_UL_GroupItems(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.03)
        split.prop(item, 'line_enable', text='', toggle=False, slider=True)
        split = split.split(factor=0.05)
        split.enabled = item.line_enable
        split.label(text=str(index + 1) + '.')
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
        row = col.row(align=True)
        row.label(text='Use only active group')
        row.prop(scene, 'hidemanager_only_active', text=str(scene.hidemanager_only_active), toggle=True, slider=True)
        row = col.row()

        if scene.hidemanager_only_active:
            row.operator('hidemanager.selected', text='Select Objects', icon='RESTRICT_SELECT_OFF').select = True
            row = col.row(align=True)
            row.operator('hidemanager.selected', text='Hide', icon='HIDE_OFF').hide = True
            row.operator('hidemanager.selected', text='Unhide', icon='HIDE_ON').hide = False
            row = col.row(align=True)
            op = row.operator('hidemanager.selected', text='Enable In Renders', icon='RESTRICT_RENDER_OFF')
            op.hide = False
            op.render = True
            op.viewport = False
            op = row.operator('hidemanager.selected', text='Disable In Renders', icon='RESTRICT_RENDER_ON')
            op.hide = True
            op.render = True
            op.viewport = False
            row = col.row(align=True)
            op = row.operator('hidemanager.selected', text='Enable In Viewports', icon='RESTRICT_VIEW_OFF')
            op.hide = False
            op.render = False
            op.viewport = True
            op = row.operator('hidemanager.selected', text='Disable In Viewports', icon='RESTRICT_VIEW_ON')
            op.hide = True
            op.render = False
            op.viewport = True
        else:
            row.operator('hidemanager.all', text='Select Objects', icon='RESTRICT_SELECT_OFF').select = True
            row = col.row(align=True)
            row.operator('hidemanager.all', text='Hide', icon='HIDE_OFF').hide = True
            row.operator('hidemanager.all', text='Unhide', icon='HIDE_ON').hide = False


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
        row = col.row(align=True)
        row.label(text='Use only active group')
        row.prop(scene, 'hidemanager_group_only_active', text=str(scene.hidemanager_group_only_active), toggle=True,
                 slider=True)
        row = col.row()

        op = row.operator('hidemanager.all', text='Select Objects', icon='RESTRICT_SELECT_OFF')
        op.select = True
        op.group = True
        row = col.row(align=True)

        op = row.operator('hidemanager.all', text='Hide', icon='HIDE_OFF')
        op.hide = True
        op.group = True

        op = row.operator('hidemanager.all', text='Unhide', icon='HIDE_ON')
        op.hide = False
        op.group = True