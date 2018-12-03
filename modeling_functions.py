##############################################################################
# Imports
##############################################################################


import bpy, re
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def add_selection_to_tt_set(context, tt_set):
    """Add selection of objects to the transfer transforms lists"""

    for obj in context.selected_objects:
        if tt_set == "a":
            item = context.scene.milkshake_tt_set_a.add()
            item.obj_name = obj.name
        elif tt_set == "b":
            item = context.scene.milkshake_tt_set_b.add()
            item.obj_name = obj.name


def clear_sharp(context, selection_only):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    if selection_only:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    meshes = [obj for obj in objects if obj.type == "MESH"]
    for mesh in meshes:
        for edge in mesh.data.edges:
            edge.use_edge_sharp = False
        core.log(f"Cleared sharp edges for {mesh.data.name}")


def generate_placeholders(context):
    """Generate empty placeholders for the selected objects"""

    if "Placeholders" in context.scene.collection.children.keys():
        main_collection = bpy.data.collections["Placeholders"]
    else:
        main_collection = bpy.data.collections.new("Placeholders")
        context.scene.collection.children.link(main_collection)

    for original in context.selected_objects:
        keyword = re.sub(r"\.[\d]+$", "", original.name)
        if f"{keyword}.placeholders" in main_collection.children:
            group = main_collection.children[f"{keyword}.placeholders"]
        else:
            group = bpy.data.collections.new(f"{keyword}.placeholders")
            main_collection.children.link(group)
        placeholder = bpy.data.objects.new(f"{keyword}.placeholder", None)
        placeholder.location = original.location
        placeholder.rotation_euler = original.rotation_euler
        placeholder.scale = original.scale
        group.objects.link(placeholder)
        core.log(f"Created placeholder {placeholder.name}")


def reset_viewport_display(context, selection_only):
    """Reset viewport display properties on objects.\nOn selection or everything"""

    if selection_only:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects


def select_unsubdivided(context):
    """Select all objects with a mesh data block and no subdivisions"""

    bpy.ops.object.select_all(action = "DESELECT")
    meshes = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    for mesh in meshes:
        has_enabled_subsurf_modifiers = False
        for mod in mesh.modifiers:
            if mod.type == "SUBSURF":
                has_enabled_subsurf_modifiers = mod.show_render and (mod.render_levels > 0 or mesh.cycles.use_adaptive_subdivision)
                break
        mesh.select = not has_enabled_subsurf_modifiers


def set_subdivision(context, iterations, selection_only):
    """Add or set subdivision iterations for meshes.\nOn selection or everything"""

    if selection_only:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    meshes = [obj for obj in objects if obj.type == "MESH"]
    for mesh in meshes:
        for mod in mesh.modifiers:
            if mod.type == "SUBSURF":
                mesh.modifiers.remove(mod)
        bpy.ops.object.shade_flat()
        if iterations > 0:
            subsurf = mesh.modifiers.new(name = "Smooth Mesh", type = "SUBSURF")
            subsurf.levels = 1
            subsurf.render_levels = iterations
            subsurf.uv_smooth = "PRESERVE_CORNERS"
            # context.scene.objects.active = mesh <--- doesn't work in 2.8
            bpy.ops.object.shade_smooth()
        core.log(f"Set subdivision for {mesh.name} to {iterations}")


def set_subdivision_to_adaptive(context, selection_only):
    """Set subdivision to adaptive for meshes.\nOn selection or everything"""

    if selection_only:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    for obj in objects:
        obj.cycles.use_adaptive_subdivision = True
        core.log(f"Enabled adaptive subdivision for {obj.name}")


def transfer_transforms(context):
    """Copy transformation values from a set of objects to another"""

    if len(context.scene.milkshake_tt_set_a) == len(context.scene.milkshake_tt_set_b):
        context.scene.milkshake_tt_set_a.clear()
        context.scene.milkshake_tt_set_b.clear()
        return True
    else:
        return False
