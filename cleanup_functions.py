##############################################################################
# Imports
##############################################################################


import bpy, os
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def rename(context:bpy.types.Context, object_to_data:bpy.props.BoolProperty = False):
    """Auto-rename the selected objects"""

    if len(context.selected_objects) == 0:
        objects = bpy.data.objects
    else:
        objects = context.selected_objects

    for i in objects:
        if i.data:
            if object_to_data:
                i.data.name = i.name
            else:
                i.name = i.data.name
            core.log(message = "Renamed {}".format(i.name))


def rename_images(context:bpy.types.Context):
    """Auto-rename all images to their respective filename"""

    for image in bpy.data.images:
        filename = os.path.splitext(os.path.basename(image.filepath))[0]
        if filename != "":
            image.name = filename
            core.log(message = "Renamed {}".format(image.name))
