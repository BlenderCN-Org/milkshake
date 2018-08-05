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


class VIEW3D_OT_milkshake_rename(bpy.types.Operator):
    """Auto-rename the selected objects."""

    bl_idname = "object.milkshake_rename"
    bl_label = "Rename Object to Data"
    bl_options = {"REGISTER","UNDO"}
    data_to_object = bpy.props.BoolProperty(default = True)

    def execute(self, context):
        func.rename(context, self.data_to_object)
        return {"FINISHED"}
