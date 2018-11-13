##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def unlock_transforms(context:bpy.types.Context):
    """Unlock all transforms of the selection"""

    for obj in context.selected_objects:
        obj.lock_location = (False, False, False)
        obj.lock_rotation = (False, False, False)
        obj.lock_scale = (False, False, False)
        core.log(f"Unlocked transforms for {obj.name}")


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
