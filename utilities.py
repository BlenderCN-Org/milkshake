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
# Panels
##############################################################################


class PROPERTIES_PT_utilities(bpy.types.Panel):

    bl_idname = "milkshake.properties_pt_utilities"
    bl_label = "Utilities"
    bl_parent_id = "milkshake.properties_pt_main"
    bl_region_type = "WINDOW"
    bl_space_type = "PROPERTIES"

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        col.scale_y = 1.5
        sub = col.row(align = True)
        sub.operator("milkshake.utilities_ot_unlock_transforms", icon = "UNLOCKED")


##############################################################################
# Registration
##############################################################################


classes = [
    PROPERTIES_PT_utilities,
    UTILITIES_OT_unlock_transforms
]

register, unregister = bpy.utils.register_classes_factory(classes)
