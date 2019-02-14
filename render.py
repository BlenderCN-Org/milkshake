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
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            func.camera_bounds_to_render_border(context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


class RENDER_OT_layer_setup(bpy.types.Operator):
    """Set up view layers for compositing"""

    bl_idname = "milkshake.render_ot_layer_setup"
    bl_label = "Layer Setup"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            func.layer_setup(context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


class RENDER_OT_render_defaults(bpy.types.Operator):
    """Apply default render settings"""

    bl_idname = "milkshake.render_ot_render_defaults"
    bl_label = "Set Render Defaults"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            func.render_defaults(context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_render(bpy.types.Panel):

    bl_idname = "milkshake.properties_pt_render"
    bl_label = "Rendering"
    bl_parent_id = "milkshake.properties_pt_main"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        col.scale_y = 1.5
        col.operator("milkshake.render_ot_camera_bounds_to_render_border", icon = 'SHADING_BBOX')
        col.operator("milkshake.render_ot_render_defaults", icon = 'QUESTION')
        col.operator("milkshake.render_ot_layer_setup", icon = 'RENDERLAYERS')
        col.prop(context.scene.cycles, "preview_pause", icon = 'PAUSE', text = "Pause Viewport Renders")


##############################################################################
# Registration
##############################################################################


classes = [
    PROPERTIES_PT_render,
    RENDER_OT_camera_bounds_to_render_border,
    RENDER_OT_render_defaults,
    RENDER_OT_layer_setup
]

register, unregister = bpy.utils.register_classes_factory(classes)
