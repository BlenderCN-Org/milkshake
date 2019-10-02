##############################################################################
# Imports
##############################################################################


import bpy, re, math
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def auto_smooth(context):
    """Set meshes to auto smooth and maximum angle to 80 degrees.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not ob.data.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.data.library]

    for ob in objects:
        ob.data.use_auto_smooth = True
        ob.data.auto_smooth_angle = math.radians(80)


def add_selection_to_tt_set(context, tt_set):
    """Add selection of objects to the transfer transforms lists"""

    if tt_set == 'a':
        for ob in context.selected_objects:
            if not ob.library:
                item = context.scene.milkshake_tt_set_a.add()
                item.obj_name = ob.name
    elif tt_set == 'b':
        for ob in context.selected_objects:
            if not ob.library:
                item = context.scene.milkshake_tt_set_b.add()
                item.obj_name = ob.name
    else:
        raise MilkshakeError("There's no active selection set.")


def clear_tt_set(context, tt_set):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    if tt_set == 'a':
        context.scene.milkshake_tt_set_a.clear()
    elif tt_set == 'b':
        context.scene.milkshake_tt_set_b.clear()
    else:
        raise MilkshakeError("There's no active selection set.")


def minimize_empties(context):
    """Minimize draw size for empties.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.type == 'EMPTY' and not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'EMPTY' and not ob.library]

    for ob in objects:
        ob.empty_display_size = 0


def select_unsubdivided(context):
    """Select all objects with a mesh data block and no subdivisions"""

    objects = [ob for ob in context.scene.objects if ob.type == 'MESH' and not ob.library]

    bpy.ops.object.select_all(action = 'DESELECT')

    for ob in objects:
        has_enabled_subsurf_modifiers = False
        for mod in ob.modifiers:
            if mod.type == 'SUBSURF':
                has_enabled_subsurf_modifiers = mod.show_render and (mod.render_levels > 0 or ob.cycles.use_adaptive_subdivision)
                break
        if ob.name in context.view_layer.objects:
            ob.select_set(not has_enabled_subsurf_modifiers)


def set_collection_instance_offset(context):
    """Set the object's collections' instance offset to the object's origin.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if not ob.library]

    for ob in objects:
        collections = [coll for coll in bpy.data.collections if ob.name in coll.objects]
        for coll in collections:
            coll.instance_offset = ob.location
            core.log(f"Set instance offset for {coll.name} to {ob.location[0]}, {ob.location[1]}, {ob.location[2]}.")


def set_subdivision(context, iterations):
    """Add or set subdivision iterations for meshes.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if ob.type == 'MESH' and not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.library]

    for ob in objects:
        for mod in ob.modifiers:
            if mod.type == 'SUBSURF':
                ob.modifiers.remove(mod)
        bpy.ops.object.shade_flat()
        if iterations > 0:
            subsurf = ob.modifiers.new(name = "Smooth Mesh", type = 'SUBSURF')
            subsurf.levels = 1
            subsurf.render_levels = iterations
            subsurf.uv_smooth = 'PRESERVE_CORNERS'
            context.view_layer.objects.active = ob
            bpy.ops.object.shade_smooth()
        core.log(f"Set subdivision for {ob.name} to {iterations}")


def snap_rotation(context):
    """Snap rotation to 90-degree steps"""

    if len(context.selected_objects) > 0:
        objects = [ob for ob in context.selected_objects if not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if not ob.library]

    for ob in objects:
        for i in range(3):
            original_in_degrees = math.degrees(ob.rotation_euler[i]) % 360
            if 45 < original_in_degrees < 90:
                ob.rotation_euler[i] = math.radians(90)
            elif 90 < original_in_degrees < 135:
                ob.rotation_euler[i] = math.radians(90)
            elif 135 < original_in_degrees < 180:
                ob.rotation_euler[i] = math.radians(180)
            elif 180 < original_in_degrees < 225:
                ob.rotation_euler[i] = math.radians(180)
            elif 225 < original_in_degrees < 270:
                ob.rotation_euler[i] = math.radians(270)
            elif 270 < original_in_degrees < 315:
                ob.rotation_euler[i] = math.radians(270)
            else:
                ob.rotation_euler[i] = 0


def transfer_transforms(context):
    """Copy transformation values from a set of objects to another"""

    set_a = context.scene.milkshake_tt_set_a
    set_b = context.scene.milkshake_tt_set_b

    if len(set_a) != len(set_b):
        raise MilkshakeError("Both sets of objects must have equal length.")

    else:
        for ob in set_a:
            if ob.obj_name not in context.scene.objects.keys():
                raise MilkshakeError(f"Object '{ob.obj_name}' doesn't exist anymore.")
        for ob in set_b:
            if ob.obj_name not in context.scene.objects.keys():
                raise MilkshakeError(f"Object '{ob.obj_name}' doesn't exist anymore.")
        for index, ob in enumerate(set_b):
            object_a = context.scene.objects[set_a[index].obj_name]
            object_b = context.scene.objects[ob.obj_name]
            object_b.location = object_a.location
            object_b.rotation_euler = object_a.rotation_euler
            object_b.scale = object_a.scale
