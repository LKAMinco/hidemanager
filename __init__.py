import bpy
from bpy.utils import previews

from .hidemanager import *
from .hidemanager_ui import *
from .hidemanager_data import *
from bpy.types import AddonPreferences
from .icons import icons

bl_info = {
    "name": "HideManager Pro",
    "author": "LKAMinco",
    "description": "Tools for custom hide parameters for objects",
    "blender": (2, 80, 0),
    "version": (1, 2, 0),
    "location": "View3D",
    "warning": "",
    "category": "3D View",
}

addon_keymaps = []


# Addon preferences
class HIDEMANAGER_AddonPreferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        row = self.layout.row()
        wm = bpy.context.window_manager
        km_items = wm.keyconfigs.addon.keymaps['3D View'].keymap_items
        km_item = None

        for km_item_i in km_items:
            if km_item_i.idname == 'wm.call_menu_pie':
                if km_item_i.name == 'Hide Manager Pie Menu':
                    km_item = km_item_i
                    break

        if km_item is not None:
            row = self.layout.box().row()
            row.label(text=km_item.name)
            row.prop(km_item, 'type', text='', full_event=True)

        km_item = km_items['hidemanager.edit_menu_dialog']
        row = self.layout.box().row()
        row.label(text=km_item.name)
        row.prop(km_item, 'type', text='', full_event=True)

        box = self.layout.box()

        row = box.row()
        row.label(text='Use Hide / Show operation in Pie Menu')
        row.prop(context.scene, 'hidemanager_use_hide', text=str(context.scene.hidemanager_use_hide), toggle=True)

        row = box.row()
        row.label(text='Use Select / Deselect operation in Pie Menu')
        row.prop(context.scene, 'hidemanager_use_select', text=str(context.scene.hidemanager_use_select), toggle=True)

        row = box.row()
        row.label(text='Use Disable / Enable in Renders operation in Pie Menu')
        row.prop(context.scene, 'hidemanager_use_render', text=str(context.scene.hidemanager_use_render), toggle=True)

        row = box.row()
        row.label(text='Use Disable / Enable in Viewport operation in Pie Menu')
        row.prop(context.scene, 'hidemanager_use_viewport', text=str(context.scene.hidemanager_use_viewport), toggle=True)

        row = box.row()
        row.label(text='Use operations settings in Pie Menu')
        row.prop(context.scene, 'hidemanager_use_settings', text=str(context.scene.hidemanager_use_settings), toggle=True)

        row = box.row()
        row.label(text='Use Force operations in Pie Menu')
        row.prop(context.scene, 'hidemanager_use_force', text=str(context.scene.hidemanager_use_force), toggle=True)


bpy.types.Scene.hidemanager_index = bpy.props.IntProperty()
bpy.types.Scene.hidemanager_only_active = bpy.props.BoolProperty(default=False, name='Only Selected', description='If enabled, only selected filter will be executed')
bpy.types.Scene.hidemanager_priority = bpy.props.BoolProperty(default=True, name='Priority',
                                                              description='If enabled, filters will be executed in order that are specified. If disabled, first will be executed ignore filters and then other. This can speedup the process of filtering')
bpy.types.Scene.hidemanager_group_index = bpy.props.IntProperty()
bpy.types.Scene.hidemanager_group_only_active = bpy.props.BoolProperty(default=True, name='Only Selected',
                                                                       description='If enabled, only selected group filter will be executed. If disabled, all group filters will be executed. If order is enabled and selected group disabled, filters will be executed in order that are specified in from lowes enabled group to highest (duplicates are executed also e.g. 3,1,3 -> 3 will be executed as first but after 1 will be executed too)')
bpy.types.Scene.hidemanager_group_order = bpy.props.BoolProperty(default=True, name='Use filter order',
                                                                 description='If enabled, filters will be executed in order that are specified in group. If disabled, first will be executed ignore filters and then other')
bpy.types.Scene.hidemanager_edit_index = bpy.props.IntProperty()
bpy.types.Scene.hidemanager_edit_only_active = bpy.props.BoolProperty(default=True, name='Only Selected', description='If enabled, only selected filter will be executed.')
bpy.types.Scene.hidemanager_use_hide = bpy.props.BoolProperty(default=True, description='Use Hide / Show operation in Pie Menu')
bpy.types.Scene.hidemanager_use_select = bpy.props.BoolProperty(default=True, description='Use Select / Deselect operation in Pie Menu')
bpy.types.Scene.hidemanager_use_render = bpy.props.BoolProperty(default=False, description='Use Disable / Enable in Renders operation in Pie Menu')
bpy.types.Scene.hidemanager_use_viewport = bpy.props.BoolProperty(default=False, description='Use Disable / Enable in Viewport operation in Pie Menu')
bpy.types.Scene.hidemanager_use_settings = bpy.props.BoolProperty(default=True, description='Use operations settings in Pie Menu')
bpy.types.Scene.hidemanager_use_force = bpy.props.BoolProperty(default=True, description='Use Force operations in Pie Menu')

classes = (
    HIDEMANAGER_PG_CustomCollectionFilters,
    HIDEMAANGER_PG_CustomCollectionGroups,
    HIDEMAANGER_PG_CustomCollectionEdit,
    HIDEMANAGER_PT_List,
    HIDEMANAGER_PT_GroupList,
    HIDEMANAGER_PT_EditList,
    HIDEMANAGER_UL_Items,
    HIDEMANAGER_UL_GroupItems,
    HIDEMANAGER_UL_EditItems,
    HIDEMANAGER_OT_Actions,
    HIDEMANAGER_OT_GroupActions,
    HIDEMANAGER_OT_EditActions,
    HIDEMANAGER_OT_State,
    HIDEMANAGER_OT_Selected,
    HIDEMANAGER_OT_All,
    HIDEMANAGER_OT_Edit,
    HIDEMANAGER_OT_Force,
    HIDEMANAGER_MT_Menu,
    HIDEMANAGER_OT_EditMenuDialog,
    HIDEMANAGER_AddonPreferences
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.hidemanager = bpy.props.CollectionProperty(type=HIDEMANAGER_PG_CustomCollectionFilters)
    bpy.types.Scene.hidemanager_group = bpy.props.CollectionProperty(type=HIDEMAANGER_PG_CustomCollectionGroups)
    bpy.types.Scene.hidemanager_edit = bpy.props.CollectionProperty(type=HIDEMAANGER_PG_CustomCollectionEdit)

    # add keymap entry
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi_mnu = km.keymap_items.new("wm.call_menu_pie", "F", "PRESS", ctrl=True, shift=True)
    kmi_mnu.properties.name = HIDEMANAGER_MT_Menu.bl_idname

    addon_keymaps.append((km, kmi_mnu))

    kmi_mnu = km.keymap_items.new("hidemanager.edit_menu_dialog", "D", "PRESS", ctrl=True, shift=True)
    addon_keymaps.append((km, kmi_mnu))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.hidemanager
    del bpy.types.Scene.hidemanager_group

    # remove keymap entry
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    previews.remove(icons)
