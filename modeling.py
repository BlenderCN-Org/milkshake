################################################################################
#
# modeling.py
#
################################################################################


import bpy
from . import modeling_functions as func
from importlib import reload
reload(func)


class VIEW3D_OT_milkshake_clear_sharp(bpy.types.Operator):
    """Clear all sharp edges in the Blender file."""

    bl_idname = "object.milkshake_clear_sharp"
    bl_label = "Clear All Sharp Edges"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.clear_sharp()
        return {"FINISHED"}


class VIEW3D_OT_milkshake_set_subdivision(bpy.types.Operator):
    """Add or set the subdivision modifier for all selected objects."""

    bl_idname = "object.milkshake_set_subdivision"
    bl_label = "Set Subdivisions"
    bl_options = {"REGISTER","UNDO"}
    iterations = bpy.props.IntProperty(name = "Iterations", default = 1, min = 0, max = 11)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        func.set_subdivision(context, self.iterations)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_set_subdivision_to_adaptive(bpy.types.Operator):
    """Set subdivision to adaptive."""

    bl_idname = "object.milkshake_set_subdivision_to_adaptive"
    bl_label = "To Adaptive"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.set_subdivision_to_adaptive(context)
        return {"FINISHED"}
