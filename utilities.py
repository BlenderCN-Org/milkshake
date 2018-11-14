##############################################################################
# Imports
##############################################################################


import bpy
from . import utilities_functions as func
from importlib import reload
reload(func)


##############################################################################
# Operators
##############################################################################


class UTILITIES_OT_unlock_transforms(bpy.types.Operator):
    """Unlock all transforms.\nOn selection or everything"""

    bl_idname = "milkshake.utilities_ot_unlock_transforms"
    bl_label = "Unlock Transforms"
    bl_options = {"REGISTER", "UNDO"}

    selection_only : bpy.props.BoolProperty(name = "Selection Only", default = False)

    def execute(self, context):
        func.unlock_transforms(context, selection_only = self.selection_only)
        return {"FINISHED"}


##############################################################################
# Registration
##############################################################################


classes = [
    UTILITIES_OT_unlock_transforms
]

register, unregister = bpy.utils.register_classes_factory(classes)
