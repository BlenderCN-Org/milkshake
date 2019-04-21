##############################################################################
# Imports
##############################################################################


import bpy
from . import render_functions as func
from importlib import reload
reload(func)


##############################################################################
# Properties
##############################################################################


class MilkshakeRenderBorder(bpy.types.PropertyGroup):

    left                            : bpy.props.IntProperty(name = "Left", subtype = 'PIXEL', min = 0, update = func.update_render_border_left)
    top                             : bpy.props.IntProperty(name = "Top", subtype = 'PIXEL', min = 0, update = func.update_render_border_top)
    width                           : bpy.props.IntProperty(name = "Width", subtype = 'PIXEL', min = 0, update = func.update_render_border_width)
    height                          : bpy.props.IntProperty(name = "Height", subtype = 'PIXEL', min = 0, update = func.update_render_border_height)


##############################################################################
# Operators
##############################################################################


class RENDER_OT_get_render_border(bpy.types.Operator):
    """Set the render border to the camera bounds"""

    bl_idname = "milkshake.get_render_border"
    bl_label = "Get Render Border"
    bl_options = {'REGISTER'}

    def execute(self, context):
        try:
            func.get_render_border(context = context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


class RENDER_OT_camera_bounds_to_render_border(bpy.types.Operator):
    """Set the render border to the camera bounds"""

    bl_idname = "milkshake.camera_bounds_to_render_border"
    bl_label = "Camera to Render Border"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            func.camera_bounds_to_render_border(context = context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


class RENDER_OT_layer_setup(bpy.types.Operator):
    """Set up view layers for compositing"""

    bl_idname = "milkshake.layer_setup"
    bl_label = "Layer Setup"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            func.layer_setup(context = context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


class RENDER_OT_render_defaults(bpy.types.Operator):
    """Apply default render settings"""

    bl_idname = "milkshake.render_defaults"
    bl_label = "Set Render Defaults"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        try:
            func.render_defaults(context = context)
            return {'FINISHED'}
        except Exception as e:
            self.report(type = {'ERROR'}, message = str(e))
            return {'CANCELLED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_render(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_render"
    bl_label = "Milkshake"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_context = 'render'

    @classmethod
    def poll(cls, context):
        func.update_render_border(context = context)
        return True

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        col.scale_y = 1.5
        sub = col.row(align = True)
        sub.operator("milkshake.render_defaults", icon = 'SCENE')
        sub.operator("milkshake.layer_setup", icon = 'RENDERLAYERS')
        col.prop(context.scene.cycles, "preview_pause", icon = 'PAUSE', text = "Pause Viewport Renders")
        lay.label(text = "Set Render Border:")
        col = lay.column(align = True)
        row = col.row(align = True)
        row.scale_y = 1.5
        row.operator("milkshake.get_render_border", icon = 'SHADING_BBOX')
        row = col.row(align = True)
        sub = row.column(align = True)
        sub.prop(context.scene.milkshake_render_border, "top")
        sub.prop(context.scene.milkshake_render_border, "left")
        sub = row.column(align = True)
        sub.prop(context.scene.milkshake_render_border, "width")
        sub.prop(context.scene.milkshake_render_border, "height")
        row = col.row(align = True)
        row.scale_y = 1.5
        row.operator("milkshake.camera_bounds_to_render_border", icon = 'CAMERA_DATA', text = "Set to Camera Bounds")


##############################################################################
# Registration
##############################################################################


classes = [
    MilkshakeRenderBorder,
    PROPERTIES_PT_render,
    RENDER_OT_camera_bounds_to_render_border,
    RENDER_OT_get_render_border,
    RENDER_OT_render_defaults,
    RENDER_OT_layer_setup
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)
    bpy.types.Scene.milkshake_render_border = bpy.props.PointerProperty(type = MilkshakeRenderBorder)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
    try:
        del bpy.types.Scene.milkshake_render_border
    except:
        pass
