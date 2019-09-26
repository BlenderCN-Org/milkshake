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


class MODELING_OT_auto_smooth(bpy.types.Operator):
    """Set meshes to auto smooth and maximum angle to 80 degrees.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_auto_smooth"
    bl_label = "Auto Smooth"
    bl_options = {'REGISTER'}

    def execute(self, context):
        func.auto_smooth(context)
        return {'FINISHED'}


class MODELING_OT_replace_tt_set_with_selection(bpy.types.Operator):
    """Replace transfer transform list with selection of objects"""

    bl_idname = "milkshake.modeling_ot_replace_tt_set_with_selection"
    bl_label = "Replace With Selection"
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


class MODELING_OT_clear_vertex_groups(bpy.types.Operator):
    """Delete all vertex groups.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_clear_vertex_groups"
    bl_label = "Clear Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.clear_vertex_groups(context)
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


class MODELING_OT_snap_rotation(bpy.types.Operator):
    """Snap rotation to 90-degree steps.\nOn selection or everything"""

    bl_idname = "milkshake.modeling_ot_snap_rotation"
    bl_label = "Snap Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.snap_rotation(context)
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


class PROPERTIES_PT_milkshake_modeling(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_milkshake_modeling"
    bl_label = "Modeling"
    bl_category = "Milkshake"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        lay = self.layout

        col = lay.column(align = True)
        col.scale_y = 1.5
        col.operator("milkshake.modeling_ot_auto_smooth", icon = 'MOD_SMOOTH')
        col.operator("milkshake.modeling_ot_clear_sharp", icon = 'EDGESEL')
        col.operator("milkshake.modeling_ot_clear_vertex_groups", icon = 'GROUP_VERTEX')
        col.operator("milkshake.modeling_ot_select_unsubdivided", icon = 'MOD_SUBSURF')
        col.operator("milkshake.modeling_ot_set_subdivision", icon = 'MOD_SUBSURF')
        col.operator("milkshake.modeling_ot_set_subdivision_to_adaptive")
        col.operator("milkshake.modeling_ot_snap_rotation", icon = 'CON_ROTLIMIT')

        # Transfer Transforms
        lay.label(text = "Transfer Transforms:")

        col = lay.column(align = True)

        row_a = col.row(align = True)
        row_a.operator("milkshake.modeling_ot_clear_tt_set", icon = 'X', text = "").tt_set = 'a'
        row_a.operator("milkshake.modeling_ot_replace_tt_set_with_selection", text = f"From {len(context.scene.milkshake_tt_set_a)} objects").tt_set = 'a'

        row_go = col.row(align = True)
        row_go.scale_y = 1.5
        row_go.operator("milkshake.modeling_ot_transfer_transforms", icon = 'TRIA_DOWN')

        row_b = col.row(align = True)
        row_b.operator("milkshake.modeling_ot_clear_tt_set", icon = 'X', text = "").tt_set = 'b'
        row_b.operator("milkshake.modeling_ot_replace_tt_set_with_selection", text = f"To {len(context.scene.milkshake_tt_set_b)} objects").tt_set = 'b'


##############################################################################
# Registration
##############################################################################


classes = [
    MilkshakeSceneObject,
    MODELING_OT_auto_smooth,
    MODELING_OT_clear_sharp,
    MODELING_OT_clear_tt_set,
    MODELING_OT_clear_vertex_groups,
    MODELING_OT_replace_tt_set_with_selection,
    MODELING_OT_select_unsubdivided,
    MODELING_OT_set_subdivision,
    MODELING_OT_set_subdivision_to_adaptive,
    MODELING_OT_snap_rotation,
    MODELING_OT_transfer_transforms,
    PROPERTIES_PT_milkshake_modeling
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
