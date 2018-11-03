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


class UTILITIES_OT_toggle_wire(bpy.types.Operator):
    """Toggles wire display for all objects."""

    bl_idname = "milkshake.utilities_ot_toggle_wire"
    bl_label = "Toggle Wire Display"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.toggle_wire(context)
        return {"FINISHED"}


class UTILITIES_OT_unlock_transforms(bpy.types.Operator):
    """Unlocks all transforms of the selection."""

    bl_idname = "milkshake.utilities_ot_unlock_transforms"
    bl_label = "Unlock Transforms"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.unlock_transforms(context)
        return {"FINISHED"}


##############################################################################
# Registration
##############################################################################


classes = [
    UTILITIES_OT_toggle_wire,
    UTILITIES_OT_unlock_transforms
]

register, unregister = bpy.utils.register_classes_factory(classes)
