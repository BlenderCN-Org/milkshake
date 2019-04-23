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
    bl_label = "Rename"
    bl_options = {'REGISTER', 'UNDO'}

    rename_datablock : bpy.props.BoolProperty(name = "Data from Object", default = False)

    def execute(self, context):
        try:
            func.rename(context, rename_datablock = self.rename_datablock)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}



class CLEANUP_OT_rename_images(bpy.types.Operator):
    """Auto-rename all images to their respective filename"""

    bl_idname = "milkshake.cleanup_ot_rename_images"
    bl_label = "Rename Images"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            func.rename_images(context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_cleanup(bpy.types.Panel):

    bl_context = "scene"
    bl_idname = "PROPERTIES_PT_cleanup"
    bl_label = "Milkshake Scene Tools"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True
        lay.prop(context.scene, "milkshake_renamer_keyword")
        lay.separator()
        lay.label(text = "Auto-rename all:")
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.operator("milkshake.cleanup_ot_rename", text = "Objects").rename_datablock = False
        sub.label(text = "to their data")
        sub = col.row(align = True)
        sub.operator("milkshake.cleanup_ot_rename", text = "Datablocks").rename_datablock = True
        sub.label(text = "to their object")
        sub = col.row(align = True)
        sub.operator("milkshake.cleanup_ot_rename_images", text = "Images")
        sub.label(text = "to their filename")


##############################################################################
# Registration
##############################################################################


classes = [
    CLEANUP_OT_rename,
    CLEANUP_OT_rename_images,
    PROPERTIES_PT_cleanup
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)
    bpy.types.Scene.milkshake_renamer_keyword = bpy.props.StringProperty(name = "Rename Selection", update = func.rename_selection)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
    try:
        del bpy.types.Scene.milkshake_renamer_keyword
    except:
        pass
