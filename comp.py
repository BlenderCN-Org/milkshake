##############################################################################
# Imports
##############################################################################


import bpy
from . import comp_functions as func
from importlib import reload
reload(func)


##############################################################################
# Operators
##############################################################################


class COMP_OT_generate_contact_sheet(bpy.types.Operator):
    """Generates a contact sheet based on the files in a given folder"""

    bl_idname = "milkshake.comp_ot_generate_contact_sheet"
    bl_label = "Generate Contact Sheet"
    bl_options = {'REGISTER', 'UNDO'}

    directory: bpy.props.StringProperty(default = "")

    def execute(self, context):
        try:
            func.generate_contact_sheet(context, directory = self.directory)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


##############################################################################
# Panels
##############################################################################


class COMPOSITOR_PT_contactsheets(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_contactsheets"
    bl_label = "Contact Sheets"
    bl_parent_id = "PROPERTIES_PT_compositor"
    bl_region_type = 'WINDOW'
    bl_space_type = 'NODE_EDITOR'

    def draw(self, context):
        lay = self.layout
        lay.operator("milkshake.comp_ot_generate_contact_sheet")


##############################################################################
# Registration
##############################################################################


classes = [
    COMP_OT_generate_contact_sheet,
    COMPOSITOR_PT_contactsheets
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
