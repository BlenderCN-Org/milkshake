################################################################################
#
# lighting.py
#
################################################################################


import bpy
from . import lighting_functions as func
from importlib import reload
reload(func)


class VIEW3D_OT_milkshake_assign_material(bpy.types.Operator):
    """Assign a material to all selected objects."""

    bl_idname = "object.milkshake_assign_material"
    bl_label = "Assign Material to Selection"
    bl_options = {"REGISTER","UNDO"}
    material = bpy.props.EnumProperty(name = "Material", items = func.read_materials)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        func.assign_material(context, self.material)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_render_setup(bpy.types.Operator):
    """Sets up the scene and layers for rendering."""

    bl_idname = "scene.milkshake_render_setup"
    bl_label = "Render Setup"
    bl_options = {"REGISTER"}

    def execute(self, context):
        func.render_setup(context)
        return {"FINISHED"}

