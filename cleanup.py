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


class CLEANUP_OT_rename(bpy.types.Operator):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_rename"
    bl_label = "Rename Objects or Datablocks"
    bl_options = {"REGISTER","UNDO"}

    selection_only : bpy.props.BoolProperty(name = "Selection Only", default = False)
    rename_datablock : bpy.props.BoolProperty(name = "Data from Object", default = False)

    def execute(self, context):
        func.rename(context, rename_datablock = self.rename_datablock, selection_only = self.selection_only)
        return {"FINISHED"}


class CLEANUP_OT_rename_images(bpy.types.Operator):
    """Auto-rename all images to their respective filename"""

    bl_idname = "milkshake.cleanup_ot_rename_images"
    bl_label = "Images"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.rename_images(context)
        return {"FINISHED"}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_cleanup(bpy.types.Panel):

    bl_idname = "milkshake.properties_pt_cleanup"
    bl_label = "Cleanup"
    bl_parent_id = "milkshake.properties_pt_main"
    bl_region_type = "WINDOW"
    bl_space_type = "PROPERTIES"

    def draw(self, context):
        lay = self.layout
        lay.label(text = "Auto-rename:")
        col = lay.column(align = True)
        col.scale_y = 1.5
        sub = col.row(align = True)
        sub.operator("milkshake.cleanup_ot_rename", text = "Objects")
        sub.operator("milkshake.cleanup_ot_rename", text = "Data").rename_datablock = True
        sub.operator("milkshake.cleanup_ot_rename_images")


##############################################################################
# Registration
##############################################################################


classes = [
    CLEANUP_OT_rename,
    CLEANUP_OT_rename_images,
    PROPERTIES_PT_cleanup
]

register, unregister = bpy.utils.register_classes_factory(classes)
