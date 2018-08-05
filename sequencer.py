##############################################################################
# Imports
##############################################################################


import bpy
from . import sequencer_functions as func
from importlib import reload
reload(func)


##############################################################################
# Functions
##############################################################################


class VIEW3D_OT_milkshake_sync_timeline(bpy.types.Operator):
    """Syncs Blender's timeline and markers with the pipeline information."""

    bl_idname = "scene.milkshake_sync_timeline"
    bl_label = "Sync Timeline"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.sync_timeline(context)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_new_shot(bpy.types.Operator):
    """Creates a new shot and camera."""

    bl_idname = "scene.milkshake_new_shot"
    bl_label = "New Shot"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.new_shot(context)
        func.autorename_shots(context)
        func.sync_timeline(context)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_delete_shot(bpy.types.Operator):
    """Deletes the selected shot."""

    bl_idname = "scene.milkshake_delete_shot"
    bl_label = "Delete"
    bl_options = {"REGISTER","UNDO"}
    index = bpy.props.IntProperty()

    def execute(self, context):
        context.scene.milkshake_shots.remove(self.index)
        func.autorename_shots(context)
        func.sync_timeline(context)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_autorename_shots(bpy.types.Operator):
    """Auto renames all shots and their associated cameras."""

    bl_idname = "scene.milkshake_autorename_shots"
    bl_label = "Rename All"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.autorename_shots(context)
        func.sync_timeline(context)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_clear_shots(bpy.types.Operator):
    """Clears the shot list."""

    bl_idname = "scene.milkshake_clear_shots"
    bl_label = "Clear"
    bl_options = {"REGISTER","UNDO"}
    index = bpy.props.IntProperty()

    def execute(self, context):
        context.scene.milkshake_shots.clear()
        func.sync_timeline(context)
        return {"FINISHED"}
