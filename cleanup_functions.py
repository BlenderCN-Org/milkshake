##############################################################################
# Imports
##############################################################################


import bpy, os
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def rename(context, rename_datablock, selection_only):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    if selection_only:
        objects = context.selected_objects
    else:
        objects = bpy.data.objects

    for obj in objects:
        if obj.data:
            if rename_datablock:
                if obj.data.is_library_indirect:
                    core.log(f"Datablock {obj.data.name} is linked from a library.")
                else:
                    obj.data.name = obj.name
                    core.log(f"Renamed datablock {obj.data.name}")
            else:
                if obj.is_library_indirect:
                    core.log(f"Object {obj.name} is linked from a library.")
                else:
                    obj.name = obj.data.name
                    core.log(f"Renamed object {obj.name}")


def rename_images(context):
    """Auto-rename all images to their respective filename"""

    for image in bpy.data.images:
        filename = os.path.splitext(os.path.basename(image.filepath))[0]
        if filename != "":
            image.name = filename
            core.log(f"Renamed {image.name}")
