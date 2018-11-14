##############################################################################
# Imports
##############################################################################


import bpy
from . import cleanup_functions as func
from importlib import reload
reload(func)


##############################################################################
# Operators
##############################################################################


class CLEANUP_OT_rename(bpy.types.Operator):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_rename"
    bl_label = "Rename Objects or Datablocks"
    bl_options = {"REGISTER","UNDO"}

    selection_only : bpy.props.BoolProperty(name = "Selection Only", default = False)
    rename_datablock : bpy.props.BoolProperty(name = "Data from Object", default = False)

    def execute(self, context):
        func.rename(context, rename_datablock = self.rename_datablock, selection_only = self.selection_only)
        return {"FINISHED"}


class CLEANUP_OT_rename_images(bpy.types.Operator):
    """Auto-rename all images to their respective filename"""

    bl_idname = "milkshake.cleanup_ot_rename_images"
    bl_label = "Images"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.rename_images(context)
        return {"FINISHED"}


##############################################################################
# Registration
##############################################################################


classes = [
    CLEANUP_OT_rename,
    CLEANUP_OT_rename_images
]

register, unregister = bpy.utils.register_classes_factory(classes)
