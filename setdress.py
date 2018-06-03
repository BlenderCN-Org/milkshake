################################################################################
#
# setdress.py
#
################################################################################


import bpy
from . import setdress_functions as func
from importlib import reload
reload(func)


class VIEW3D_OT_milkshake_generate_placeholders(bpy.types.Operator):
    """Generates placeholders for the selected objects."""

    bl_idname = "scene.milkshake_generate_placeholders"
    bl_label = "Generate Placeholders"
    bl_options = {"REGISTER"}

    def execute(self, context):
        func.generate_placeholders(context)
        return {"FINISHED"}
