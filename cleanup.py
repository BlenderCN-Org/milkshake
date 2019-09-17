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


class CLEANUP_OT_remove_unused_materials(bpy.types.Operator):
    """Remove unused material slots from meshes and curves.\nOn selection or everything"""

    bl_idname = "milkshake.remove_unused_materials"
    bl_label = "Unused materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.remove_unused_materials(context)
        return {'FINISHED'}


class CLEANUP_OT_rename(bpy.types.Operator):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_rename"
    bl_label = "Objects From Data"
    bl_options = {'REGISTER', 'UNDO'}

    rename_datablock : bpy.props.BoolProperty(name = "Data From Objects", default = False)

    def execute(self, context):
        func.rename(context, rename_datablock = self.rename_datablock)
        return {'FINISHED'}


class CLEANUP_OT_rename_collection_instances(bpy.types.Operator):
    """Auto-rename the selected empties to the collection they instance.\nOn selection or everything"""

    bl_idname = "milkshake.cleanup_ot_rename_collection_instances"
    bl_label = "Instances From Collections"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.rename_collection_instances(context)
        return {'FINISHED'}


class CLEANUP_OT_rename_materials_to_texture(bpy.types.Operator):
    """Auto-rename all materials to the name of their first Image Texture node's datablock"""

    bl_idname = "milkshake.cleanup_ot_rename_materials_to_texture"
    bl_label = "Materials From Image Textures"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.rename_materials_to_texture(context)
        return {'FINISHED'}


class CLEANUP_OT_rename_images(bpy.types.Operator):
    """Auto-rename all images to their respective filename"""

    bl_idname = "milkshake.cleanup_ot_rename_images"
    bl_label = "Images From Filenames"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.rename_images(context)
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

        lay.prop(context.scene, "milkshake_renamer_keyword")

        lay.separator()

        lay.label(text = "Auto-rename:")
        autorename = lay.column(align = True)
        objects_data = autorename.row(align = True)
        objects_data.operator("milkshake.cleanup_ot_rename", icon = 'OBJECT_DATA').rename_datablock = False
        objects_data.operator("milkshake.cleanup_ot_rename", text = "Data From Objects", icon = 'MESH_DATA').rename_datablock = True
        autorename.operator("milkshake.cleanup_ot_rename_images", icon = 'OUTLINER_OB_IMAGE')
        autorename.operator("milkshake.cleanup_ot_rename_materials_to_texture", icon = 'MATERIAL')
        autorename.operator("milkshake.cleanup_ot_rename_collection_instances", icon = 'OUTLINER_OB_GROUP_INSTANCE')

        lay.label(text = "Auto-remove:")
        lay.operator("milkshake.remove_unused_materials", icon = 'MATERIAL')


##############################################################################
# Registration
##############################################################################


classes = [
    CLEANUP_OT_remove_unused_materials,
    CLEANUP_OT_rename,
    CLEANUP_OT_rename_collection_instances,
    CLEANUP_OT_rename_images,
    CLEANUP_OT_rename_materials_to_texture,
    PROPERTIES_PT_milkshake_cleanup
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)
    bpy.types.Scene.milkshake_renamer_keyword = bpy.props.StringProperty(name = "Rename Selection", update = func.rename_selection)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
    try:
        del bpy.types.Scene.milkshake_renamer_keyword
    except:
        pass
