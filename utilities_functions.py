##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def toggle_wire(context:bpy.types.Context):
    """"""

    on = context.scene.objects[0].show_wire
    for i in context.scene.objects:
        i.show_wire = not on
        i.show_all_edges = True
        core.log(message = "Toggled wire display for {}".format(i.name))


def unlock_transforms(context:bpy.types.Context):
    """"""

    for i in context.selected_objects:
        i.lock_location = (False, False, False)
        i.lock_rotation = (False, False, False)
        i.lock_scale = (False, False, False)
        core.log(message = "Unlocked transforms for {}".format(i.name))


def get_bounding_box_limits(m):
    """Extract only useful information from the given mesh's bounding box"""
    return {
        "x_min": m.bound_box[0][0],
        "y_min": m.bound_box[0][1],
        "z_min": m.bound_box[0][2],
        "x_max": m.bound_box[6][0],
        "y_max": m.bound_box[6][1],
        "z_max": m.bound_box[6][2]
    }
