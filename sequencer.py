################################################################################
#
# sequencer.py
#
################################################################################


import bpy
from . import sequencer_functions as func
from . import properties
from importlib import reload
reload(func)


class VIEW3D_OT_milkshake_sync_timeline(bpy.types.Operator):
    """Syncs Blender's timeline and markers with the pipeline information."""

    bl_idname = "scene.milkshake_sync_timeline"
    bl_label = "Timeline"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.sync_timeline(context)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_new_shot(bpy.types.Operator):
    """Creates a new shot."""

    bl_idname = "scene.milkshake_new_shot"
    bl_label = "New Shot"
    bl_options = {"REGISTER","UNDO"}

    def execute(self, context):
        func.new_shot(context)
        return {"FINISHED"}


class VIEW3D_OT_milkshake_delete_shot(bpy.types.Operator):
    """Deletes the selected shot."""

    bl_idname = "scene.milkshake_delete_shot"
    bl_label = "Delete"
    bl_options = {"REGISTER","UNDO"}
    index = bpy.props.IntProperty()

    def execute(self, context):
        func.delete_shot(context, self.index)
        return {"FINISHED"}
