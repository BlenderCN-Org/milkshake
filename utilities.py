################################################################################
#
# utilities.py
#
################################################################################


import bpy
from . import utilities_functions as func
from importlib import reload
reload(func)


class VIEW3D_OT_milkshake_toggle_wire(bpy.types.Operator):
    """Toggles wire display for all objects."""

    bl_idname = "scene.milkshake_toggle_wire"
    bl_label = "Toggle Wire Display"
    bl_options = {"REGISTER"}

    def execute(self, context):
        func.toggle_wire(context)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_unlock_transforms(bpy.types.Operator):
    """Unlocks all transforms of the selection."""

    bl_idname = "scene.milkshake_unlock_transforms"
    bl_label = "Unlock Transforms"
    bl_options = {"REGISTER"}

    def execute(self, context):
        func.unlock_transforms(context)
        return {"FINISHED"}
