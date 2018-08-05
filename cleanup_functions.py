##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def rename(context:bpy.types.Context, data_to_object:bpy.props.BoolProperty):
    """Auto-rename the selected objects."""

    for i in context.selected_objects:
        if i.data:
            if data_to_object:
                i.name = i.data.name
            else:
                i.data.name = i.name
            core.log("Renamed {}".format(i.name))
