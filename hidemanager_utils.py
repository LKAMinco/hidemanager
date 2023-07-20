import bpy
import rna_keymap_ui
import logging

context = bpy.context

has_material = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL']
has_modifier = ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'VOLUME', 'GPENCIL', 'GREASEPENCIL', 'LATTICE']
has_vertex_group = ['MESH', 'LATTICE']
has_shape_key = ['MESH', 'CURVE', 'SURFACE', 'LATTICE']


def objectAction(operation: str, obj: bpy.types.Object) -> None:
    """Performs the action selected in the enum

    :param bpy.types.Object obj: Object to be affected by operation
    :return: None
    """

    if operation == 'SELECT':
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
            text = str(getattr(context.scene, 'hidemanager_' + use_operation))
            row.prop(context.scene, 'hidemanager_' + use_operation, text=str(text), toggle=True)
        if getattr(context.scene, 'hidemanager_' + use_operation):
            if use_icons:
                row = box.row()
                row.label(text='Use icons instead of text')
                text = str(getattr(context.scene, 'hidemanager_' + use_icons))
                row.prop(context.scene, 'hidemanager_' + use_icons, text=str(text), toggle=True)
            if separated_ops:
                row = box.row()
                row.label(text='Use separated operations')
                text = str(getattr(context.scene, 'hidemanager_' + separated_ops))
                row.prop(context.scene, 'hidemanager_' + separated_ops, text=str(text), toggle=True)


def getText(enabled):
    if enabled == 'use_icons_hide':
        if getattr(bpy.context.scene, 'hidemanager_use_icons_hide'):
            return '', ''
        else:
            return 'Hide Objects', 'Show Objects'
    elif enabled == 'use_icons_select':
        if getattr(bpy.context.scene, 'hidemanager_use_icons_hide'):
            return '', ''
        else:
            return 'Select Objects', 'Deselect Objects'
    elif enabled == 'use_icons_render':
        if getattr(bpy.context.scene, 'hidemanager_use_icons_render'):
            return '', ''
        else:
            return 'Disable in Renders', 'Enable in Renders'
    elif enabled == 'use_icons_viewport':
        if getattr(bpy.context.scene, 'hidemanager_use_icons_viewport'):
            return '', ''
        else:
            return 'Disable in Viewport', 'Enable in Viewport'
    elif enabled == 'use_icons_force':
        if getattr(bpy.context.scene, 'hidemanager_use_icons_force'):
            if bpy.context.mode == 'EDIT_MESH':
                return '', ''
            else:
                return '', '', ''
        else:
            if bpy.context.mode == 'EDIT_MESH':
                return 'Assign', 'Remove'
            else:
                return 'Mark', 'Unmark', 'Mark Ignore'
