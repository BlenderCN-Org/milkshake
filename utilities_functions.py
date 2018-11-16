##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def unlock_transforms(context, selection_only):
    """Unlock all transforms.\nOn selection or everything"""

    if selection_only:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    for obj in context.selected_objects:
        obj.lock_location = (False, False, False)
        obj.lock_rotation = (False, False, False)
        obj.lock_scale = (False, False, False)
        core.log(f"Unlocked transforms for {obj.name}")
