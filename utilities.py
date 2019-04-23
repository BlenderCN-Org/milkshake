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


class UTILITIES_OT_show_all_edges(bpy.types.Operator):
    """Show all edges for all objects"""

    bl_idname = "milkshake.utilities_ot_show_all_edges"
    bl_label = "Enable All Edges"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            func.show_all_edges()
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


class UTILITIES_OT_unlock_transforms(bpy.types.Operator):
    """Unlock all transforms.\nOn selection or everything"""

    bl_idname = "milkshake.utilities_ot_unlock_transforms"
    bl_label = "Unlock Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            func.unlock_transforms(context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_utilities(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_utilities"
    bl_label = "Utilities"
    bl_parent_id = "PROPERTIES_PT_main"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        col.scale_y = 1.5
        sub = col.row(align = True)
        sub.operator("milkshake.utilities_ot_show_all_edges", icon = 'EDGESEL')
        sub.operator("milkshake.utilities_ot_unlock_transforms", icon = 'UNLOCKED')


##############################################################################
# Registration
##############################################################################


classes = [
    PROPERTIES_PT_utilities,
    UTILITIES_OT_show_all_edges,
    UTILITIES_OT_unlock_transforms
]

register, unregister = bpy.utils.register_classes_factory(classes)
