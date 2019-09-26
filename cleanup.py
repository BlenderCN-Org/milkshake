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


class CLEANUP_OT_minimize_empties(bpy.types.Operator):
    """Minimize draw size for empties.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_minimize_empties"
    bl_label = "Minimize Empties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.minimize_empties(context)
        return {'FINISHED'}


class CLEANUP_OT_remove_unused_material_slots(bpy.types.Operator):
    """Remove unused material slots from meshes and curves.\nOn selection or everything"""

    bl_idname = "milkshake.remove_unused_material_slots"
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


class CLEANUP_OT_set_collection_instance_offset(bpy.types.Operator):
    """Set the object's collections' instance offset to the object's origin.\nOn selection or everything."""

    bl_idname = "milkshake.cleanup_ot_set_collection_instance_offset"
    bl_label = "Set Collection Instance Offset"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.set_collection_instance_offset(context)
        return {'FINISHED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_milkshake_cleanup(bpy.types.Panel):

    bl_idname = "PROPERTIES_PT_milkshake_cleanup"
    bl_label = "Milkshake: Scene Cleanup"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True

        lay.label(text = "Auto-rename:")
        autorename = lay.column(align = True)
        objects_data = autorename.row(align = True)
        objects_data.operator("milkshake.cleanup_ot_rename_objects_from_data", icon = 'OBJECT_DATA').data_from_objects = False
        objects_data.operator("milkshake.cleanup_ot_rename_objects_from_data", text = "Data From Objects", icon = 'MESH_DATA').data_from_objects = True
        autorename.operator("milkshake.cleanup_ot_rename_images_from_filenames", icon = 'OUTLINER_OB_IMAGE')
        autorename.operator("milkshake.cleanup_ot_rename_materials_from_textures", icon = 'MATERIAL')
        autorename.operator("milkshake.cleanup_ot_rename_instances_from_collections", icon = 'OUTLINER_OB_GROUP_INSTANCE')

        lay.label(text = "Auto-remove:")
        lay.operator("milkshake.remove_unused_material_slots", icon = 'MATERIAL')

        lay.separator()

        lay.operator("milkshake.cleanup_ot_set_collection_instance_offset", icon = 'OUTLINER_OB_EMPTY')
        lay.operator("milkshake.cleanup_ot_minimize_empties", icon = 'OUTLINER_OB_EMPTY')


##############################################################################
# Registration
##############################################################################


classes = [
    CLEANUP_OT_minimize_empties,
    CLEANUP_OT_remove_unused_material_slots,
    CLEANUP_OT_rename_images_from_filenames,
    CLEANUP_OT_rename_instances_from_collections,
    CLEANUP_OT_rename_materials_from_textures,
    CLEANUP_OT_rename_objects_from_data,
    CLEANUP_OT_set_collection_instance_offset,
    PROPERTIES_PT_milkshake_cleanup
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
