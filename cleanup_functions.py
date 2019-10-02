##############################################################################
# Imports
##############################################################################


import bpy, os
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def clear_sharp(context):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not ob.data.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.data.library]

    for ob in objects:
        for edge in ob.data.edges:
            if edge.use_edge_sharp:
                core.log(f"Cleared sharp on edge {edge}")
                edge.use_edge_sharp = False


def clear_vertex_groups(context):
    """Delete all vertex groups.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.library]

    for ob in objects:
        ob.vertex_groups.clear()


def remove_unused_material_slots(context):
    """Remove unused material slots from meshes and curves.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not ob.library and not ob.data.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.library and not ob.data.library]

    for ob in objects:
        if ob.type == 'MESH' or ob.type == 'CURVE':
            context.view_layer.objects.active = ob
            bpy.ops.object.material_slot_remove_unused()


def rename_images_from_filenames(context):
    """Auto-rename all images to their respective filename"""

    images = [image for image in bpy.data.images if not image.library]

    for image in images:
        filename = os.path.splitext(os.path.basename(image.filepath))[0]
        if filename != "":
            image.name = filename
            core.log(f"Renamed {image.name}")


def rename_instances_from_collections(context):
    """Auto-rename the selected empties to the collection they instance.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.instance_type == 'COLLECTION' and not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.instance_type == 'COLLECTION' and not ob.library]

    for ob in objects:
        if ob.library:
            core.log(f"Collection instancer {ob.name} is linked from a library.")
        else:
            ob.name = ob.instance_collection.name
            core.log(f"Renamed instancer to {ob.name}")


def rename_materials_from_textures(context):
    """Auto-rename all materials to the name of their first Image Texture node's datablock"""

    materials = [mat for mat in bpy.data.materials if not mat.library]

    for mat in materials:
        first_image_texture = None
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                if node.image:
                    first_image_texture = node
                    break
        if first_image_texture:
            mat.name = first_image_texture.image.name
            core.log(f"Renamed material {mat.name}")


def rename_objects_from_data(context, data_from_objects):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    def target_is_not_linked(ob):
        if data_from_objects:
            return not ob.data.library
        return not ob.library

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.data and target_is_not_linked(ob)]
    else:
        objects = [ob for ob in bpy.data.objects if ob.data and target_is_not_linked(ob)]

    for ob in objects:
        if data_from_objects:
            ob.data.name = ob.name
            core.log(f"Renamed datablock to {ob.data.name}")
        else:
            ob.name = ob.data.name
            core.log(f"Renamed object to {ob.name}")
