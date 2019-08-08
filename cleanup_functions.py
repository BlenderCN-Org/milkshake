##############################################################################
# Imports
##############################################################################


import bpy, os
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def remove_unused_materials(context):
    """Remove unused material slots from meshes and curves.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = context.selected_objects
    else:
        objects = context.scene.objects

    for obj in objects:
        if obj.type == 'MESH' or obj.type == 'CURVE':
            context.view_layer.objects.active = obj
            bpy.ops.object.material_slot_remove_unused()


def rename(context, rename_datablock):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    for obj in objects:
        if obj.data:
            if rename_datablock:
                if obj.data.library:
                    core.log(f"Datablock {obj.data.name} is linked from a library.")
                else:
                    obj.data.name = obj.name
                    core.log(f"Renamed datablock {obj.data.name}")
            else:
                if obj.library:
                    core.log(f"Object {obj.name} is linked from a library.")
                else:
                    obj.name = obj.data.name
                    core.log(f"Renamed object {obj.name}")


def rename_images(context):
    """Auto-rename all images to their respective filename"""

    for image in bpy.data.images:
        if not image.library:
            filename = os.path.splitext(os.path.basename(image.filepath))[0]
            if filename != "":
                image.name = filename
                core.log(f"Renamed {image.name}")


def rename_materials_to_texture(context):
    """Auto-rename all materials to the name of their first Image Texture node's datablock"""

    for mat in bpy.data.materials:
        first_image_texture = None
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                if node.image:
                    first_image_texture = node
                    break
        if first_image_texture:
            mat.name = first_image_texture.image.name
            core.log(f"Renamed material {mat.name}")


def rename_selection(self, context):
    """Rename the selected objects using the given keyword"""

    keyword = context.scene.milkshake_renamer_keyword
    selection = context.selected_objects
    if keyword != "":
        if len(selection) > 0:
            for obj in selection:
                if not obj.library:
                    obj.name = keyword
                    if obj.data:
                        obj.data.name = keyword
        else:
            raise IndexError("No objects selected.")
    else:
        raise ValueError("You have to provide a name.")
