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

    directory: bpy.props.StringProperty(name = "Image Directory", default = "", subtype = 'DIR_PATH')
    columns: bpy.props.IntProperty(name = "Columns", default = 4, min = 1)
    frame_width: bpy.props.IntProperty(name = "Frame Width", default = 2048, min = 1)
    frame_height: bpy.props.IntProperty(name = "Frame Height", default = 858, min = 1)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        func.generate_contact_sheet(context, directory = self.directory, columns = self.columns, frame_width = self.frame_width, frame_height = self.frame_height)
        return {'FINISHED'}


class COMP_OT_generate_credits_roll(bpy.types.Operator):
    """Sets up the scene for rendering a clean, jitter-free credit roll based on a single image"""

    bl_idname = "milkshake.comp_ot_generate_credits_roll"
    bl_label = "Generate Credits Roll"
    bl_options = {'REGISTER', 'UNDO'}

    image_filepath: bpy.props.StringProperty(name = "Image", default = "", subtype = 'FILE_PATH')
    speed: bpy.props.IntProperty(name = "Pixels per Frame", default = 5, min = 1, max = 7)
    width: bpy.props.IntProperty(name = "Frame Width", default = 4096, min = 1)
    height: bpy.props.IntProperty(name = "Frame Height", default = 1716, min = 1)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        func.generate_credits_roll(context, image_filepath = self.image_filepath, speed = self.speed, frame_width = self.frame_width, frame_height = self.frame_height)
        return {'FINISHED'}



##############################################################################
# Panels
##############################################################################


class COMPOSITOR_PT_generators(bpy.types.Panel):

    bl_idname = "COMPOSITOR_PT_generators"
    bl_label = "Generators"
    bl_region_type = 'UI'
    bl_space_type = 'NODE_EDITOR'
    bl_category = "Milkshake"

    def draw(self, context):
        lay = self.layout
        lay.operator("milkshake.comp_ot_generate_contact_sheet")
        lay.operator("milkshake.comp_ot_generate_credits_roll")


##############################################################################
# Registration
##############################################################################


classes = [
    COMP_OT_generate_contact_sheet,
    COMP_OT_generate_credits_roll,
    COMPOSITOR_PT_generators
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
