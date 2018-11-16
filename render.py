##############################################################################
# Imports
##############################################################################


import bpy
from . import render_functions as func
from importlib import reload
reload(func)


##############################################################################
# Operators
##############################################################################


class RENDER_OT_camera_bounds_to_render_border(bpy.types.Operator):
    """Set the render border to the camera bounds"""

    bl_idname = "milkshake.render_ot_camera_bounds_to_render_border"
    bl_label = "Camera to Render Border"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.camera_bounds_to_render_border(context)
        return {"FINISHED"}


class RENDER_OT_layer_setup(bpy.types.Operator):
    """Set up view layers for compositing"""

    bl_idname = "milkshake.render_ot_layer_setup"
    bl_label = "Layer Setup"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.layer_setup(context)
        return {"FINISHED"}


class RENDER_OT_render_defaults(bpy.types.Operator):
    """Apply default render settings"""

    bl_idname = "milkshake.render_ot_render_defaults"
    bl_label = "Set Render Defaults"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.render_defaults(context)
        return {"FINISHED"}


##############################################################################
# Registration
##############################################################################


classes = [
    RENDER_OT_camera_bounds_to_render_border,
    RENDER_OT_render_defaults,
    RENDER_OT_layer_setup
]

register, unregister = bpy.utils.register_classes_factory(classes)
