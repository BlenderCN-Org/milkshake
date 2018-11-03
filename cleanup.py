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
    """Auto-rename the selected objects to their data, or vice-versa.\nRenames all objects if there are none selected"""

    bl_idname = "milkshake.cleanup_ot_rename"
    bl_label = "Object to Data"
    bl_options = {"REGISTER","UNDO"}

    object_to_data : bpy.props.BoolProperty(default = True)

    def execute(self, context):
        func.rename(context, object_to_data = self.object_to_data)
        return {"FINISHED"}


class CLEANUP_OT_rename_images(bpy.types.Operator):
    """Auto-rename all images to their respective filename"""

    bl_idname = "milkshake.cleanup_ot_rename_images"
    bl_label = "Images With Filenames"
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
