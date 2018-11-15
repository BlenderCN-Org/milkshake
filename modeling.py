##############################################################################
# Imports
##############################################################################


import bpy
from . import modeling_functions as func
from importlib import reload
reload(func)


##############################################################################
# Operators
##############################################################################


class MODELING_OT_clear_sharp(bpy.types.Operator):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_clear_sharp"
    bl_label = "Clear All Sharp Edges"
    bl_options = {"REGISTER", "UNDO"}

    selection_only : bpy.props.BoolProperty(name = "Selection Only", default = False)

    def execute(self, context):
        func.clear_sharp(context, selection_only = self.selection_only)
        return {"FINISHED"}


class MODELING_OT_generate_placeholders(bpy.types.Operator):
    """Generate empty placeholders for the selected objects"""

    bl_idname = "milkshake.modeling_ot_generate_placeholders"
    bl_label = "Generate Placeholders"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.generate_placeholders(context)
        return {"FINISHED"}


class MODELING_OT_reset_viewport_display(bpy.types.Operator):
    """Reset viewport display properties on objects.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_reset_viewport_display"
    bl_label = "Remove Drawing Overrides"
    bl_options = {"REGISTER", "UNDO"}

    selection_only : bpy.props.BoolProperty(name = "Selection Only", default = False)

    def execute(self, context):
        func.reset_viewport_display(context, selection_only = self.selection_only)
        return {"FINISHED"}


class MODELING_OT_select_unsubdivided(bpy.types.Operator):
    """Select all objects with a mesh data block and no subdivisions"""

    bl_idname = "milkshake.modeling_ot_select_unsubdivided"
    bl_label = "Select Unsubdivided"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.select_unsubdivided(context, selection_only = self.selection_only)
        return {"FINISHED"}


class MODELING_OT_set_subdivision(bpy.types.Operator):
    """Add or set subdivision iterations for meshes.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_set_subdivision"
    bl_label = "Set Subdivisions"
    bl_options = {"REGISTER","UNDO"}

    selection_only : bpy.props.BoolProperty(name = "Selection Only", default = False)
    iterations : bpy.props.IntProperty(name = "Iterations", default = 1, min = 0, max = 11)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        func.set_subdivision(context, iterations = self.iterations, selection_only = self.selection_only)
        return {"FINISHED"}


class MODELING_OT_set_subdivision_to_adaptive(bpy.types.Operator):
    """Set subdivision to adaptive for meshes.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_set_subdivision_to_adaptive"
    bl_label = "To Adaptive"
    bl_options = {"REGISTER", "UNDO"}

    selection_only : bpy.props.BoolProperty(name = "Selection Only", default = False)

    def execute(self, context):
        func.set_subdivision_to_adaptive(context, selection_only = self.selection_only)
        return {"FINISHED"}


class MODELING_OT_transfer_transforms(bpy.types.Operator):
    """Copy transformation values from a set of objects to another"""

    bl_idname = "milkshake.modeling_ot_transfer_transforms"
    bl_label = "Transfer Transforms"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.transfer_transforms(context)
        return {"FINISHED"}


##############################################################################
# Registration
##############################################################################


classes = [
    MODELING_OT_clear_sharp,
    MODELING_OT_generate_placeholders,
    MODELING_OT_reset_viewport_display,
    MODELING_OT_select_unsubdivided,
    MODELING_OT_set_subdivision,
    MODELING_OT_set_subdivision_to_adaptive,
    MODELING_OT_transfer_transforms
]

register, unregister = bpy.utils.register_classes_factory(classes)
