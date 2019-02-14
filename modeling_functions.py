##############################################################################
# Imports
##############################################################################


import bpy, re
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def add_selection_to_tt_set(context = None, tt_set = None):
    """Add selection of objects to the transfer transforms lists"""

    if tt_set == 'a':
        for obj in context.selected_objects:
            item = context.scene.milkshake_tt_set_a.add()
            item.obj_name = obj.name
    elif tt_set == 'b':
        for obj in context.selected_objects:
            item = context.scene.milkshake_tt_set_b.add()
            item.obj_name = obj.name
    else:
        return False
    return True


def clear_sharp(context = None):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    meshes = [obj for obj in objects if obj.type == "MESH"]
    for mesh in meshes:
        for edge in mesh.data.edges:
            edge.use_edge_sharp = False


def clear_tt_set(context = None, tt_set = None):
    if tt_set == 'a':
        context.scene.milkshake_tt_set_a.clear()
    elif tt_set == 'b':
        context.scene.milkshake_tt_set_b.clear()
    else:
        return False


def generate_placeholders(context = None):
    """Generate empty placeholders for the selected objects"""

    if "Placeholders" in context.scene.collection.children.keys():
        main_collection = bpy.data.collections["Placeholders"]
    else:
        main_collection = bpy.data.collections.new("Placeholders")
        context.scene.collection.children.link(main_collection)

    for original in context.selected_objects:
        keyword = re.sub(r"\.[\d]+$", "", original.name)
        if f'{keyword}.placeholders' in main_collection.children:
            group = main_collection.children[f'{keyword}.placeholders']
        else:
            group = bpy.data.collections.new(f"{keyword}.placeholders")
            main_collection.children.link(group)
        placeholder = bpy.data.objects.new(f"{keyword}.placeholder", None)
        placeholder.location = original.location
        placeholder.rotation_euler = original.rotation_euler
        placeholder.scale = original.scale
        group.objects.link(placeholder)


def select_unsubdivided(context = None):
    """Select all objects with a mesh data block and no subdivisions"""

    bpy.ops.object.select_all(action = 'DESELECT')
    meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    for mesh in meshes:
        has_enabled_subsurf_modifiers = False
        for mod in mesh.modifiers:
            if mod.type == 'SUBSURF':
                has_enabled_subsurf_modifiers = mod.show_render and (mod.render_levels > 0 or mesh.cycles.use_adaptive_subdivision)
                break
        mesh.select = not has_enabled_subsurf_modifiers


def set_subdivision(context = None, iterations = None):
    """Add or set subdivision iterations for meshes.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    meshes = [obj for obj in objects if obj.type == 'MESH']
    for mesh in meshes:
        for mod in mesh.modifiers:
            if mod.type == 'SUBSURF':
                mesh.modifiers.remove(mod)
        bpy.ops.object.shade_flat()
        if iterations > 0:
            subsurf = mesh.modifiers.new(name = "Smooth Mesh", type = 'SUBSURF')
            subsurf.levels = 1
            subsurf.render_levels = iterations
            subsurf.uv_smooth = 'PRESERVE_CORNERS'
            # context.scene.objects.active = mesh <--- doesn't work in 2.8
            bpy.ops.object.shade_smooth()
        core.log(f"Set subdivision for {mesh.name} to {iterations}")


def set_subdivision_to_adaptive(context = None):
    """Set subdivision to adaptive for meshes.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    for obj in objects:
        obj.cycles.use_adaptive_subdivision = True
        core.log(f"Enabled adaptive subdivision for {obj.name}")


def transfer_transforms(context = None):
    """Copy transformation values from a set of objects to another"""

    set_a = context.scene.milkshake_tt_set_a
    set_b = context.scene.milkshake_tt_set_b

    if len(set_a) != len(set_b):
        raise ValueError("Both sets of objects must have equal length.")

    else:

        for ob in set_a:
            if ob.obj_name not in context.scene.objects.keys():
                raise ReferenceError(f"Object '{ob.obj_name}' doesn't exist anymore.")
        for ob in set_b:
            if ob.obj_name not in context.scene.objects.keys():
                raise ReferenceError(f"Object '{ob.obj_name}' doesn't exist anymore.")

        for index, ob in enumerate(set_b):
            object_a = context.scene.objects[set_a[index].obj_name]
            object_b = context.scene.objects[ob.obj_name]
            object_b.location = object_a.location
            object_b.rotation_euler = object_a.rotation_euler
            object_b.scale = object_a.scale
