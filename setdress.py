##############################################################################
# Imports
##############################################################################


import bpy
from . import setdress_functions as func
from importlib import reload
reload(func)


##############################################################################
# Operators
##############################################################################


class SETDRESS_OT_generate_placeholders(bpy.types.Operator):
    """Generate placeholders for the selected objects"""

    bl_idname = "milkshake.setdress_ot_generate_placeholders"
    bl_label = "Generate Placeholders"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.generate_placeholders(context)
        return {"FINISHED"}


##############################################################################
# Registration
##############################################################################


classes = [
    SETDRESS_OT_generate_placeholders
]

register, unregister = bpy.utils.register_classes_factory(classes)
