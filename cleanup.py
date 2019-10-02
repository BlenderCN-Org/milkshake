##############################################################################
# Imports
##############################################################################


import bpy
from . import cleanup_functions as func
from importlib import reload
reload(func)


##############################################################################
# Operators
##############################################################################


class CLEANUP_OT_remove_sharp_edges(bpy.types.Operator):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_remove_sharp_edges"
    bl_label = "Sharp Edges"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.clear_sharp(context)
        return {'FINISHED'}


class CLEANUP_OT_remove_vertex_groups(bpy.types.Operator):
    """Delete all vertex groups.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_remove_vertex_groups"
    bl_label = "Vertex Groups"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.clear_vertex_groups(context)
        return {'FINISHED'}


class CLEANUP_OT_remove_unused_material_slots(bpy.types.Operator):
    """Remove unused material slots from meshes and curves.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_remove_unused_material_slots"
    bl_label = "Unused Material Slots"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.remove_unused_material_slots(context)
        return {'FINISHED'}


class CLEANUP_OT_rename_objects_from_data(bpy.types.Operator):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_rename_objects_from_data"
    bl_label = "Objects From Data"
    bl_options = {'REGISTER', 'UNDO'}

    data_from_objects : bpy.props.BoolProperty(name = "Data From Objects", default = False)

    def execute(self, context):
        func.rename_objects_from_data(context, data_from_objects = self.data_from_objects)
        return {'FINISHED'}


class CLEANUP_OT_rename_instances_from_collections(bpy.types.Operator):
    """Auto-rename the selected empties to the collection they instance.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_rename_instances_from_collections"
    bl_label = "Instances From Collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.rename_instances_from_collections(context)
        return {'FINISHED'}


class CLEANUP_OT_rename_materials_from_textures(bpy.types.Operator):
    """Auto-rename all materials to the name of their first Image Texture node's datablock"""

    bl_idname = "milkshake.cleanup_ot_rename_materials_from_textures"
    bl_label = "Materials From Image Textures"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.rename_materials_from_textures(context)
        return {'FINISHED'}


class CLEANUP_OT_rename_images_from_filenames(bpy.types.Operator):
    """Auto-rename all images to their respective filename"""

    bl_idname = "milkshake.cleanup_ot_rename_images_from_filenames"
    bl_label = "Images From Filenames"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.rename_images_from_filenames(context)
        return {'FINISHED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_milkshake_cleanup(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_milkshake_cleanup"
    bl_label = "Cleanup"
    bl_category = "Milkshake"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True

        lay.label(text = "Rename:")
        autorename = lay.column(align = True)
        autorename.scale_y = 1.5
        autorename.operator("milkshake.cleanup_ot_rename_objects_from_data", icon = 'OBJECT_DATA').data_from_objects = False
        autorename.operator("milkshake.cleanup_ot_rename_objects_from_data", text = "Data From Objects", icon = 'MESH_DATA').data_from_objects = True
        autorename.separator()
        autorename.operator("milkshake.cleanup_ot_rename_images_from_filenames", icon = 'OUTLINER_OB_IMAGE')
        autorename.operator("milkshake.cleanup_ot_rename_materials_from_textures", icon = 'MATERIAL')
        autorename.separator()
        autorename.operator("milkshake.cleanup_ot_rename_instances_from_collections", icon = 'OUTLINER_OB_GROUP_INSTANCE')

        lay.label(text = "Remove:")
        autoremove = lay.column(align = True)
        autoremove.scale_y = 1.5
        autoremove.operator("milkshake.cleanup_ot_remove_sharp_edges", icon = 'EDGESEL')
        autoremove.operator("milkshake.cleanup_ot_remove_unused_material_slots", icon = 'MATERIAL')
        autoremove.operator("milkshake.cleanup_ot_remove_vertex_groups", icon = 'GROUP_VERTEX')


##############################################################################
# Registration
##############################################################################


classes = [
    CLEANUP_OT_remove_sharp_edges,
    CLEANUP_OT_remove_vertex_groups,
    CLEANUP_OT_remove_unused_material_slots,
    CLEANUP_OT_rename_images_from_filenames,
    CLEANUP_OT_rename_instances_from_collections,
    CLEANUP_OT_rename_materials_from_textures,
    CLEANUP_OT_rename_objects_from_data,
    PROPERTIES_PT_milkshake_cleanup
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
