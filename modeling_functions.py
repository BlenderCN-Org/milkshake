##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def clear_sharp():
    for me in bpy.data.meshes:
        for e in me.edges:
            e.use_edge_sharp = False
        core.log(message = "Cleared sharp edges for {}".format(me.name))


def set_subdivision(context:bpy.types.Context, iterations:bpy.props.IntProperty):
    for i in context.selected_objects:
        if i.type == "MESH":
            mods = i.modifiers
            for m in mods:
                if m.type == "SUBSURF":
                    mods.remove(m)
            bpy.ops.object.shade_flat()
            if iterations > 0:
                s = mods.new(name = "Smooth Mesh", type = "SUBSURF")
                s.levels = 1
                s.render_levels = iterations
                s.use_opensubdiv = True
                s.use_subsurf_uv = True
                context.scene.objects.active = i
                bpy.ops.object.shade_smooth()
                core.log(message = "Set subdivision for {} to {}".format(i.name, iterations))


def set_subdivision_to_adaptive(context:bpy.types.Context):
    for i in context.selected_objects:
        i.cycles.use_adaptive_subdivision = True
        core.log(message = "Enabled adaptive subdivision for {}".format(i.name))
