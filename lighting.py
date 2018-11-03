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


class LIGHTING_OT_render_setup(bpy.types.Operator):
    """Sets up the scene and layers for rendering"""

    bl_idname = "milkshake.lighting_ot_render_setup"
    bl_label = "Render Setup"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.render_setup(context)
        return {"FINISHED"}


##############################################################################
# Registration
##############################################################################


classes = [
    LIGHTING_OT_render_setup
]

register, unregister = bpy.utils.register_classes_factory(classes)
