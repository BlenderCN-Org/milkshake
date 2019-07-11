##############################################################################
# Imports
##############################################################################


import bpy
from . import modeling_functions as func
from importlib import reload
reload(func)


##############################################################################
# Properties
##############################################################################


class MilkshakeSceneObject(bpy.types.PropertyGroup):

    obj_name                        : bpy.props.StringProperty(name = "Object Name")


##############################################################################
# Operators
##############################################################################


class MODELING_OT_add_selection_to_tt_set(bpy.types.Operator):
    """Add selection of objects to the transfer transforms lists"""

    bl_idname = "milkshake.modeling_ot_add_selection_to_tt_set"
    bl_label = "Add Selection"
    bl_options = {'REGISTER'}

    tt_set: bpy.props.EnumProperty(items = [('a', 'A', 'List A'), ('b', 'B', 'List B')])

    def execute(self, context):
        func.clear_tt_set(context, self.tt_set)
        func.add_selection_to_tt_set(context, self.tt_set)
        return {'FINISHED'}


class MODELING_OT_clear_sharp(bpy.types.Operator):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_clear_sharp"
    bl_label = "Remove Sharp Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.clear_sharp(context)
        return {'FINISHED'}


class MODELING_OT_clear_tt_set(bpy.types.Operator):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_clear_tt_set"
    bl_label = "Clear List"
    bl_options = {'REGISTER'}

    tt_set: bpy.props.EnumProperty(items = [('a', 'A', 'List A'), ('b', 'B', 'List B')])

    def execute(self, context):
        func.clear_tt_set(context, self.tt_set)
        return {'FINISHED'}


class MODELING_OT_select_unsubdivided(bpy.types.Operator):
    """Select all objects with a mesh data block and no subdivisions"""

    bl_idname = "milkshake.modeling_ot_select_unsubdivided"
    bl_label = "Select Unsubdivided"
    bl_options = {'REGISTER'}

    def execute(self, context):
        func.select_unsubdivided(context)
        return {'FINISHED'}


class MODELING_OT_set_subdivision(bpy.types.Operator):
    """Add or set subdivision iterations for meshes.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_set_subdivision"
    bl_label = "Set Subdivisions..."
    bl_options = {'REGISTER', 'UNDO'}

    iterations: bpy.props.IntProperty(name = "Iterations", default = 1, min = 0, max = 11)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        func.set_subdivision(context, self.iterations)
        return {'FINISHED'}


class MODELING_OT_set_subdivision_to_adaptive(bpy.types.Operator):
    """Set subdivision to adaptive for meshes.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_set_subdivision_to_adaptive"
    bl_label = "To Adaptive"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.set_subdivision_to_adaptive(context)
        return {'FINISHED'}


class MODELING_OT_transfer_transforms(bpy.types.Operator):
    """Copy transformation values from a set of objects to another"""

    bl_idname = "milkshake.modeling_ot_transfer_transforms"
    bl_label = "Transfer Transforms"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.transfer_transforms(context)
        return {'FINISHED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_modeling(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_modeling"
    bl_label = "Modeling and Setdress"
    bl_parent_id = "PROPERTIES_PT_scene_tools"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        lay = self.layout

        col = lay.column(align = True)
        col.scale_y = 1.5
        sub = col.row(align = True)
        sub.operator("milkshake.modeling_ot_clear_sharp", icon = 'EDGESEL')
        sub = col.split(align = True, factor = 0.6)
        sub.operator("milkshake.modeling_ot_set_subdivision", icon = 'MOD_SUBSURF')
        sub.operator("milkshake.modeling_ot_set_subdivision_to_adaptive")

        # Transfer Transforms
        lay.label(text = "Transfer Transforms:")
        box = lay.box()
        row = box.row()

        col_settings = row.column()

        row_a = col_settings.row(align = True)
        row_a.operator("milkshake.modeling_ot_add_selection_to_tt_set", text = f"From Selection ({len(context.scene.milkshake_tt_set_a)})", icon = 'BACK').tt_set = 'a'
        row_a.operator("milkshake.modeling_ot_clear_tt_set", icon = 'X', text = "").tt_set = 'a'

        row_b = col_settings.row(align = True)
        row_b.operator("milkshake.modeling_ot_add_selection_to_tt_set", text = f"To Selection ({len(context.scene.milkshake_tt_set_b)})", icon = 'FORWARD').tt_set = 'b'
        row_b.operator("milkshake.modeling_ot_clear_tt_set", icon = 'X', text = "").tt_set = 'b'

        col_button = row.column()
        col_button.scale_x = 1.5
        col_button.scale_y = 2.1
        col_button.operator("milkshake.modeling_ot_transfer_transforms", icon = 'TRIA_RIGHT', text = "")


##############################################################################
# Registration
##############################################################################


classes = [
    MilkshakeSceneObject,
    MODELING_OT_add_selection_to_tt_set,
    MODELING_OT_clear_sharp,
    MODELING_OT_clear_tt_set,
    MODELING_OT_select_unsubdivided,
    MODELING_OT_set_subdivision,
    MODELING_OT_set_subdivision_to_adaptive,
    MODELING_OT_transfer_transforms,
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
