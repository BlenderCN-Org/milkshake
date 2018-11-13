##############################################################################
# Imports
##############################################################################


import bpy
from . import lighting_functions as func
from importlib import reload
reload(func)


##############################################################################
# Operators
##############################################################################


class LIGHTING_OT_render_defaults(bpy.types.Operator):
    """Apply default render settings"""

    bl_idname = "milkshake.lighting_ot_render_defaults"
    bl_label = "Set Render Defaults"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.render_defaults(context)
        return {"FINISHED"}


class LIGHTING_OT_layer_setup(bpy.types.Operator):
    """Set up the view layers"""

    bl_idname = "milkshake.lighting_ot_layer_setup"
    bl_label = "Layer Setup"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.layer_setup(context)
        return {"FINISHED"}


##############################################################################
# Registration
##############################################################################


classes = [
    LIGHTING_OT_render_defaults,
    LIGHTING_OT_layer_setup
]

register, unregister = bpy.utils.register_classes_factory(classes)
