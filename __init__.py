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
        if km_item is None:
            return
        row = self.layout.row()
        row.label(text=km_item.name)
        row.prop(km_item, 'type', text='', full_event=True)


bpy.types.Scene.hidemanager_index = bpy.props.IntProperty()
bpy.types.Scene.hidemanager_only_active = bpy.props.BoolProperty(default=False, name='Only Selected',
                                                                 description='If enabled, only selected filter will be executed')
bpy.types.Scene.hidemanager_priority = bpy.props.BoolProperty(default=True, name='Priority',
                                                              description='If enabled, filters will be executed in order that are specified. If disabled, first will be executed ignore filters and then other. This can speedup the process of filtering')
bpy.types.Scene.hidemanager_group_index = bpy.props.IntProperty()
bpy.types.Scene.hidemanager_group_only_active = bpy.props.BoolProperty(default=True, name='Only Selected',
                                                                       description='If enabled, only selected group filter will be executed. If disabled, all group filters will be executed. If order is enabled and selected group disabled, filters will be executed in order that are specified in from lowes enabled group to highest (duplicates are executed also e.g. 3,1,3 -> 3 will be executed as first but after 1 will be executed too)')
bpy.types.Scene.hidemanager_group_order = bpy.props.BoolProperty(default=True, name='Use filter order',
                                                                 description='If enabled, filters will be executed in order that are specified in group. If disabled, first will be executed ignore filters and then other')

classes = (
    HIDEMANAGER_PG_CustomCollection,
    HIDEMANAGER_PT_List,
    HIDEMANAGER_PT_GroupList,
    HIDEMANAGER_UL_Items,
    HIDEMANAGER_UL_GroupItems,
    HIDEMANAGER_OT_Actions,
    HIDEMANAGER_OT_GroupActions,
    HIDEMANAGER_OT_State,
    HIDEMANAGER_OT_Selected,
    HIDEMANAGER_OT_All,
    HIDEMANAGER_MT_Menu,
    HIDEMANAGER_AddonPreferences
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.hidemanager = bpy.props.CollectionProperty(type=HIDEMANAGER_PG_CustomCollection)
    bpy.types.Scene.hidemanager_group = bpy.props.CollectionProperty(type=HIDEMANAGER_PG_CustomCollection)

    # add keymap entry
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi_mnu = km.keymap_items.new("wm.call_menu_pie", "F", "PRESS", ctrl=True, shift=True)
    kmi_mnu.properties.name = HIDEMANAGER_MT_Menu.bl_idname

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
