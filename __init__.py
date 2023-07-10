import bpy
from .hidemanager import *
from .hidemanager_ui import *
from .hidemanager_data import *

bl_info = {
    "name": "Hide Manager",
    "author": "LKAMinco",
    "description": "Tools for custom hide parameters for objects",
    "blender": (2, 80, 0),
    "location": "View3D",
    "warning": "",
    "category": "Object"
}

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
    HIDEMANAGER_OT_All
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.hidemanager = bpy.props.CollectionProperty(type=HIDEMANAGER_PG_CustomCollection)
    bpy.types.Scene.hidemanager_index = bpy.props.IntProperty()
    bpy.types.Scene.hidemanager_only_active = bpy.props.BoolProperty(default=False)
    bpy.types.Scene.hidemanager_group = bpy.props.CollectionProperty(type=HIDEMANAGER_PG_CustomCollection)
    bpy.types.Scene.hidemanager_priority = bpy.props.BoolProperty(default=True, name='Priority',
                                                                  description='If enabled, filters will be executed in order that are specified. If disabled, first will be executed ignore filters and then other. This can speedup the process of filtering')
    bpy.types.Scene.hidemanager_group_index = bpy.props.IntProperty()
    bpy.types.Scene.hidemanager_group_only_active = bpy.props.BoolProperty(default=True)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.hidemanager
    del bpy.types.Scene.hidemanager_index
