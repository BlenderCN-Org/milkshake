##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def show_all_edges():
    """Show all edges for all objects"""

    for ob in bpy.data.objects:
        ob.show_all_edges = True


def unlock_transforms(context = None):
    """Unlock all transforms.\nOn selection or everything"""

    if len(context.selected_objects) > 0:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    for obj in context.selected_objects:
        obj.lock_location = (False, False, False)
        obj.lock_rotation = (False, False, False)
        obj.lock_scale = (False, False, False)
