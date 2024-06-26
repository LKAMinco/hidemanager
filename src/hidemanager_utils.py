import logging

import bpy
import rna_keymap_ui
from os import path

context = bpy.context

has_material = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL']
has_modifier = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL', 'LATTICE']
has_vertex_group = ['MESH', 'LATTICE']
has_shape_key = ['MESH', 'CURVE', 'SURFACE', 'LATTICE']

icons = None


def getDefaultIcon(name):
    if name == 'CONTAINS':
        return 'ALIGN_LEFT'
    elif name == 'TYPE':
        return 'SCENE_DATA'
    elif name == 'EXACT_OBJECT':
        return 'OBJECT_DATA'
    elif name == 'HIERARCHY':
        return 'EMPTY_DATA'
    elif name == 'COLLECTION':
        return 'OUTLINER_COLLECTION'
    elif name == 'MATERIAL':
        return 'MATERIAL_DATA'
    elif name == 'MATERIAL_CONTAINS':
        return 'MATERIAL_DATA'
    elif name == 'MODIFIER':
        return 'MODIFIER_DATA'
    elif name == 'MODIFIER_CONTAINS':
        return 'MODIFIER_DATA'
    elif name == 'VERTEX_GROUP_CONTAINS':
        return 'GROUP_VERTEX'
    elif name == 'SHAPE_KEY_CONTAINS':
        return 'SHAPEKEY_DATA'
    elif name == 'CONSTRAINT':
        return 'CONSTRAINT'


def getAddonName():
    try:
        return path.basename(path.dirname(path.dirname(path.realpath(__file__))))
    except:
        return 'hidemanager_pro'


def getAddonPrefs():
    return bpy.context.preferences.addons[getAddonName()].preferences


def getIcon(name):
    global icons

    if not icons:
        from .. import icons

    return icons[name]


def objectAction(operation: str, obj: bpy.types.Object) -> None:
    """Performs the action selected in the enum

    :param bpy.types.Object obj: Object to be affected by operation
    :return: None
    """

    if operation == 'SELECT' or operation == 'SELECT_INVERT':
        obj.select_set(True)
    elif operation == 'DESELECT':
        obj.select_set(False)
    elif operation == 'HIDE':
        obj.hide_set(True)
    elif operation == 'SHOW':
        obj.hide_set(False)
    elif operation == 'ENABLE_RENDER':
        obj.hide_render = False
    elif operation == 'DISABLE_RENDER':
        obj.hide_render = True
    elif operation == 'ENABLE_VIEWPORT':
        obj.hide_viewport = False
    elif operation == 'DISABLE_VIEWPORT':
        obj.hide_viewport = True


def drawKeymapItems(kc, name, keylist, layout, skip_box_label=False):
    drawn = []

    idx = 0

    for item in keylist:
        keymap = item.get("keymap")
        isdrawn = False

        if keymap:
            km = kc.keymaps.get(keymap)

            kmi = None
            if km:

                idname = item.get("idname")
                for kmitem in km.keymap_items:
                    if kmitem.idname == idname:
                        properties = item.get("properties")

                        if properties:
                            if getattr(kmitem.properties, 'name') == properties:
                                kmi = kmitem
                                break

                        else:
                            kmi = kmitem
                            break

            if kmi:
                if idx == 0:
                    box = layout.box()

                label = item.get("label", None)

                if not label:
                    label = name.title().replace("_", " ")

                if len(keylist) > 1:
                    if idx == 0 and not skip_box_label:
                        box.label(text=name.title().replace("_", " "))

                row = box.split(factor=0.17)
                row.label(text=label)

                rna_keymap_ui.draw_kmi(["ADDON", "USER", "DEFAULT"], kc, km, kmi, row, 0)

                infos = item.get("info", [])
                for text in infos:
                    row = box.split(factor=0.15)
                    row.separator()
                    row.label(text=text, icon="INFO")

                isdrawn = True
                idx += 1

        drawn.append(isdrawn)
    return drawn


def drawSettingsItems(self, layout, context, enable_ui=None, label=None, use_operation=None, use_icons=None, separated_ops=None):
    box = layout.box()
    row = box.row()
    if getattr(self, enable_ui):
        icon = 'TRIA_DOWN'
    else:
        icon = 'TRIA_RIGHT'
    row.prop(self, enable_ui, emboss=False, icon=icon, text='')
    row.label(text=label)

    if getattr(self, enable_ui):
        if use_operation:
            row = box.row()
            row.label(text='Use in pie menu')
            text = str(getattr(self, use_operation))
            row.prop(self, use_operation, text=str(text), toggle=True)
        if getattr(self, use_operation):
            if use_icons:
                row = box.row()
                row.label(text='Use icons instead of text')
                text = str(getattr(self, use_icons))
                row.prop(self, use_icons, text=str(text), toggle=True)
            if separated_ops:
                row = box.row()
                row.label(text='Use separated operations')
                text = str(getattr(self, separated_ops))
                row.prop(self, separated_ops, text=str(text), toggle=True)


def getText(enabled):
    if enabled == 'use_icons_hide':
        if getattr(getAddonPrefs(), 'use_icons_hide'):
            return '', ''
        else:
            return 'Hide Objects', 'Show Objects'
    elif enabled == 'use_icons_select':
        if getattr(getAddonPrefs(), 'use_icons_select'):
            return '', '', ''
        else:
            return 'Select Objects', 'Select Invert objects', 'Deselect Objects'
    elif enabled == 'use_icons_render':
        if getattr(getAddonPrefs(), 'use_icons_render'):
            return '', ''
        else:
            return 'Disable in Renders', 'Enable in Renders'
    elif enabled == 'use_icons_viewport':
        if getattr(getAddonPrefs(), 'use_icons_viewport'):
            return '', ''
        else:
            return 'Disable in Viewport', 'Enable in Viewport'
    elif enabled == 'use_icons_force':
        if getattr(getAddonPrefs(), 'use_icons_force'):
            if bpy.context.mode == 'EDIT_MESH' and not getAddonPrefs().use_objectmode_filters_in_editmode:
                return '', ''
            else:
                return '', '', ''
        else:
            if bpy.context.mode == 'EDIT_MESH' and not getAddonPrefs().use_objectmode_filters_in_editmode:
                return 'Assign', 'Remove'
            else:
                return 'Mark', 'Unmark', 'Mark Ignore'
