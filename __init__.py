import bpy
import logging
from .src.hidemanager import HIDEMANAGER_OT_Actions, HIDEMANAGER_OT_GroupActions, HIDEMANAGER_OT_EditActions, HIDEMANAGER_OT_State, HIDEMANAGER_OT_Selected, HIDEMANAGER_OT_All, HIDEMANAGER_OT_Edit, HIDEMANAGER_OT_Force
from .src.hidemanager_ui import HIDEMANAGER_UL_Items, HIDEMANAGER_UL_GroupItems, HIDEMANAGER_UL_EditItems, HIDEMANAGER_MT_Menu, HIDEMANAGER_OT_MenuDialog, HIDEMANAGER_PT_List, HIDEMANAGER_PT_GroupList, HIDEMANAGER_PT_EditList
from .src.hidemanager_data import HIDEMANAGER_PG_CustomCollectionFilters, HIDEMANAGER_PG_CustomCollectionGroups, HIDEMANAGER_PG_CustomCollectionEdit
from .src.hidemanager_utils import drawKeymapItems, drawSettingsItems, getAddonPrefs
from bpy.types import AddonPreferences, Scene, Object, PropertyGroup, Modifier, GpencilModifier, Constraint
from bpy.props import IntProperty, BoolProperty, CollectionProperty, EnumProperty
from bpy.utils import register_class, unregister_class
from .src.hidemanager_icons import regIcons, unregIcons

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
icons = None


# Addon preferences
class HIDEMANAGER_AddonPreferences(AddonPreferences):
    bl_idname = __package__

    pop_hide: BoolProperty(default=False)
    pop_select: BoolProperty(default=False)
    pop_render: BoolProperty(default=False)
    pop_viewport: BoolProperty(default=False)
    pop_force: BoolProperty(default=False)
    pop_settings: BoolProperty(default=False)

    use_hide: BoolProperty(default=True, description='Use Hide / Show operation in Pie Menu')
    use_select: BoolProperty(default=True, description='Use Select / Deselect operation in Pie Menu')
    use_render: BoolProperty(default=False, description='Use Disable / Enable in Renders operation in Pie Menu')
    use_viewport: BoolProperty(default=False, description='Use Disable / Enable in Viewport operation in Pie Menu')
    use_settings: BoolProperty(default=True, description='Use operations settings in Pie Menu')
    use_force: BoolProperty(default=True, description='Use Force operations in Pie Menu')

    use_icons_hide: BoolProperty(default=False)
    use_separated_ops_hide: BoolProperty(default=False)
    use_icons_select: BoolProperty(default=False)
    use_separated_ops_select: BoolProperty(default=False)
    use_icons_render: BoolProperty(default=False)
    use_separated_ops_render: BoolProperty(default=False)
    use_icons_viewport: BoolProperty(default=False)
    use_separated_ops_viewport: BoolProperty(default=False)
    use_icons_force: BoolProperty(default=False)

    use_objectmode_filters_in_editmode: BoolProperty(default=True, name='Use object mode filters in edit mode', description='If enabled, object mode filters will be executed in edit mode too')

    def draw(self, context):
        global icons
        row = self.layout.row()
        wm = bpy.context.window_manager

        box = self.layout.box()

        split = box.split(factor=0.5)

        keys = {'PIEMENU': [{'label': 'Pie Menu', 'keymap': '3D View', 'idname': 'wm.call_menu_pie', 'properties': 'HIDEMANAGER_MT_Menu'}],
                'DIALOGMENU': [{'label': 'Dialog Menu', 'keymap': '3D View', 'idname': 'hidemanager.edit_menu_dialog'}],
                }

        box = split.box()
        box.label(text='Keymaps')
        drawKeymapItems(wm.keyconfigs.user, '3D View', keys['PIEMENU'], box)
        drawKeymapItems(wm.keyconfigs.user, '3D View', keys['DIALOGMENU'], box)

        box = split.box()
        box.label(text='Settings')

        row = box.row()
        row.label(text='Use object mode filters in edit mode')
        row.prop(self, 'use_objectmode_filters_in_editmode', text=str(self.use_objectmode_filters_in_editmode), toggle=True)

        drawSettingsItems(self, box, context, 'pop_hide', 'Hide / Show operation', 'use_hide', 'use_icons_hide', 'use_separated_ops_hide')
        drawSettingsItems(self, box, context, 'pop_select', 'Select / Deselect operation', 'use_select', 'use_icons_select', 'use_separated_ops_select')
        drawSettingsItems(self, box, context, 'pop_render', 'Disable / Enable in Renders operation', 'use_render', 'use_icons_render', 'use_separated_ops_render')
        drawSettingsItems(self, box, context, 'pop_viewport', 'Disable / Enable in Viewport operation', 'use_viewport', 'use_icons_viewport', 'use_separated_ops_viewport')
        drawSettingsItems(self, box, context, 'pop_settings', 'Operations settings', 'use_settings')
        drawSettingsItems(self, box, context, 'pop_force', 'Force operations', 'use_force', 'use_icons_force')


classes = (
    HIDEMANAGER_AddonPreferences,
    HIDEMANAGER_PG_CustomCollectionFilters,
    HIDEMANAGER_PG_CustomCollectionGroups,
    HIDEMANAGER_PG_CustomCollectionEdit,
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
    HIDEMANAGER_OT_MenuDialog
)


def register():
    global icons
    icons = regIcons()

    for cls in classes:
        register_class(cls)

    Scene.hidemanager = CollectionProperty(type=HIDEMANAGER_PG_CustomCollectionFilters)
    Scene.hidemanager_group = CollectionProperty(type=HIDEMANAGER_PG_CustomCollectionGroups)
    Object.hidemanager_edit = CollectionProperty(type=HIDEMANAGER_PG_CustomCollectionEdit)

    Scene.hidemanager_index = IntProperty()
    Scene.hidemanager_only_active = BoolProperty(default=False, name='Only Selected', description='If enabled, only selected filter will be executed')
    Scene.hidemanager_priority = BoolProperty(default=True, name='Priority',
                                              description='If enabled, filters will be executed in order that are specified. If disabled, first will be executed ignore filters and then other. This can speedup the process of filtering')
    Scene.hidemanager_group_index = IntProperty()
    Scene.hidemanager_group_only_active = BoolProperty(default=True, name='Only Selected',
                                                       description='If enabled, only selected group filter will be executed. If disabled, all group filters will be executed. If order is enabled and selected group disabled, filters will be executed in order that are specified in from lowes enabled group to highest (duplicates are executed also e.g. 3,1,3 -> 3 will be executed as first but after 1 will be executed too)')
    Scene.hidemanager_group_order = BoolProperty(default=True, name='Use filter order',
                                                 description='If enabled, filters will be executed in order that are specified in group. If disabled, first will be executed ignore filters and then other')
    Object.hidemanager_edit_index = IntProperty()
    Object.hidemanager_edit_only_active = BoolProperty(default=True, name='Only Selected', description='If enabled, only selected filter will be executed.')

    Scene.hidemanager_filters_enabled = BoolProperty(default=False)
    Scene.hidemanager_groups_enabled = BoolProperty(default=False)

    Scene.hidemanager_pages = EnumProperty(default='FILTERS', items=[('FILTERS', 'Filters', 'Filters'), ('GROUPS', 'Groups', 'Groups')])
    Scene.hidemanager_edit_pages = EnumProperty(default='EDIT', items=[('FILTERS', 'Filters', 'Filters'), ('GROUPS', 'Groups', 'Groups'), ('EDIT', 'Edit', 'Edit')])

    # add keymap entry
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    kmi_mnu = km.keymap_items.new("wm.call_menu_pie", "F", "PRESS", ctrl=True, shift=True)
    kmi_mnu.properties.name = "HIDEMANAGER_MT_Menu"

    addon_keymaps.append((km, kmi_mnu))

    kmi_mnu = km.keymap_items.new("hidemanager.edit_menu_dialog", "D", "PRESS", ctrl=True, shift=True)
    addon_keymaps.append((km, kmi_mnu))


def unregister():
    for cls in classes:
        unregister_class(cls)

    # remove keymap entry
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()

    global icons
    unregIcons(icons)

    del Scene.hidemanager
    del Scene.hidemanager_group
    del Object.hidemanager_edit

    del Scene.hidemanager_index
    del Scene.hidemanager_only_active
    del Scene.hidemanager_priority

    del Scene.hidemanager_group_index
    del Scene.hidemanager_group_only_active
    del Scene.hidemanager_group_order

    del Object.hidemanager_edit_index
    del Object.hidemanager_edit_only_active

    del Scene.hidemanager_filters_enabled
    del Scene.hidemanager_groups_enabled

    del Scene.hidemanager_pages
    del Scene.hidemanager_edit_pages
