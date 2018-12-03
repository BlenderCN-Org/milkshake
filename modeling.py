##############################################################################
# Imports
##############################################################################


import bpy
from . import modeling_functions as func
from importlib import reload
reload(func)


##############################################################################
# PropertyGroups
##############################################################################


class MilkshakeSceneObject(bpy.types.PropertyGroup):

    obj_name                        : bpy.props.StringProperty(name = "Object Name")


##############################################################################
# Lists
##############################################################################


class MODELING_UL_transfer_transforms(bpy.types.UIList):

    bl_idname = "milkshake.modeling_ul_transfer_transforms"

    def draw_item(context, layout, data, item, icon, active_data, active_property):
        print(item)
        if layout.type in {"DEFAULT", "COMPACT"}:
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            layout.label(text = item.obj_name, icon_value = icon)
        elif layout.type in {"GRID"}:
            layout.alignment = "CENTER"
            layout.label(text = "", icon_value = icon)


##############################################################################
# Operators
##############################################################################


class MODELING_OT_add_selection_to_tt_set(bpy.types.Operator):
    """Add selection of objects to the transfer transforms lists"""

    bl_idname = "milkshake.modeling_ot_add_selection_to_tt_set"
    bl_label = "Add Selection"
    bl_options = {"REGISTER", "UNDO"}

    tt_set : bpy.props.EnumProperty(items = [("a", "A", "List A"), ("b", "B", "List B")])

    def execute(self, context):
        func.add_selection_to_tt_set(context, tt_set = self.tt_set)
        return {"FINISHED"}


class MODELING_OT_clear_sharp(bpy.types.Operator):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_clear_sharp"
    bl_label = "Remove Sharp Edges"
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
        if not func.transfer_transforms(context):
            self.report(type = "ERROR", message = "Both sets of objects must have equal length.")
            return {"CANCELLED"}
        return {"FINISHED"}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_modeling(bpy.types.Panel):

    bl_idname = "milkshake.properties_pt_modeling"
    bl_label = "Modeling and Setdress"
    bl_parent_id = "milkshake.properties_pt_main"
    bl_region_type = "WINDOW"
    bl_space_type = "PROPERTIES"

    def draw(self, context):
        lay = self.layout

        col = lay.column(align = True)
        col.scale_y = 1.5
        sub = col.row(align = True)
        sub.operator("milkshake.modeling_ot_clear_sharp", icon = "EDGESEL")
        sub = col.row(align = True)
        sub.operator("milkshake.modeling_ot_generate_placeholders", icon = "OUTLINER_OB_EMPTY")
        sub = col.split(align = True, factor = 0.6)
        sub.operator("milkshake.modeling_ot_set_subdivision", icon = "MOD_SUBSURF")
        sub.operator("milkshake.modeling_ot_set_subdivision_to_adaptive")

        col = lay.column(align = True)
        sub = col.row(align = True)
        col_a = sub.column(align = True)
        col_a.operator("milkshake.modeling_ot_add_selection_to_tt_set").tt_set = "a"
        col_a.template_list("UI_UL_list", "milkshake_tt_set_a", context.scene, "milkshake_tt_set_a", context.scene, "milkshake_tt_set_a_index")
        col_b = sub.column(align = True)
        col_b.operator("milkshake.modeling_ot_add_selection_to_tt_set").tt_set = "b"
        col_b.template_list("UI_UL_list", "milkshake_tt_set_b", context.scene, "milkshake_tt_set_b", context.scene, "milkshake_tt_set_b_index")
        row_button = col.row(align = True)
        row_button.scale_y = 1.5
        row_button.operator("milkshake.modeling_ot_transfer_transforms", icon = "TRIA_RIGHT")


##############################################################################
# Registration
##############################################################################


classes = [
    MilkshakeSceneObject,
    MODELING_OT_add_selection_to_tt_set,
    MODELING_OT_clear_sharp,
    MODELING_OT_generate_placeholders,
    MODELING_OT_reset_viewport_display,
    MODELING_OT_select_unsubdivided,
    MODELING_OT_set_subdivision,
    MODELING_OT_set_subdivision_to_adaptive,
    MODELING_OT_transfer_transforms,
    MODELING_UL_transfer_transforms,
    PROPERTIES_PT_modeling
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)
    bpy.types.Scene.milkshake_tt_set_a = bpy.props.CollectionProperty(type = MilkshakeSceneObject)
    bpy.types.Scene.milkshake_tt_set_a_index = bpy.props.IntProperty(default = 0)
    bpy.types.Scene.milkshake_tt_set_b = bpy.props.CollectionProperty(type = MilkshakeSceneObject)
    bpy.types.Scene.milkshake_tt_set_b_index = bpy.props.IntProperty(default = 0)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
    try:
        del bpy.types.Scene.milkshake_tt_set_a
        del bpy.types.Scene.milkshake_tt_set_b
    except:
        pass
