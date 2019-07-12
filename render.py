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
        func.get_render_border(context)
        return {'FINISHED'}


class RENDER_OT_camera_bounds_to_render_border(bpy.types.Operator):
    """Set the render border to the camera bounds"""

    bl_idname = "milkshake.camera_bounds_to_render_border"
    bl_label = "Camera to Render Border"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.camera_bounds_to_render_border(context)
        return {'FINISHED'}


class RENDER_OT_layer_setup(bpy.types.Operator):
    """Set up view layers for compositing"""

    bl_idname = "milkshake.layer_setup"
    bl_label = "Layer Setup"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.layer_setup(context)
        return {'FINISHED'}


class RENDER_OT_remove_view_layer(bpy.types.Operator):
    """Delete the selected layer"""

    bl_idname = "milkshake.remove_view_layer"
    bl_label = "Remove View Layer"
    bl_options = {'REGISTER', 'UNDO'}

    layer_name = bpy.props.StringProperty()

    def execute(self, context):
        func.remove_view_layer(context, layer_name = self.layer_name)
        return {'FINISHED'}


class RENDER_OT_render_defaults(bpy.types.Operator):
    """Apply default render settings"""

    bl_idname = "milkshake.render_defaults"
    bl_label = "Set Defaults"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.render_defaults(context)
        return {'FINISHED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_render(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_render"
    bl_label = "Milkshake: Rendering Tools"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_context = 'render'

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
        lay.operator("milkshake.camera_bounds_to_render_border", icon = 'CAMERA_DATA', text = "Set to Camera Bounds")


class PROPERTIES_PT_layer_manager(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_layer_manager"
    bl_label = "Milkshake: Layer Manager"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_context = 'render'

    def draw(self, context):
        lay = self.layout
        box = lay.box()
        box.prop(context.scene.render, "use_single_layer")
        lay.label(text = "Layers in this scene:")
        col = lay.column(align = True)
        for layer in context.scene.view_layers:
            row = col.row(align = True)
            row.prop(layer, "use", text = "")
            row.label(text = layer.name)
            row.operator("milkshake.remove_view_layer", icon = 'PANEL_CLOSE', text = "").layer_name = layer.name


##############################################################################
# Registration
##############################################################################


classes = [
    MilkshakeRenderBorder,
    PROPERTIES_PT_render,
    PROPERTIES_PT_layer_manager,
    RENDER_OT_camera_bounds_to_render_border,
    RENDER_OT_get_render_border,
    RENDER_OT_remove_view_layer,
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
