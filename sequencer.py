##############################################################################
# Imports
##############################################################################


import bpy
from . import sequencer_functions as func
from importlib import reload
reload(func)


##############################################################################
# PropertyGroups
##############################################################################


class MilkshakeSequencerShot(bpy.types.PropertyGroup):

    code                            : bpy.props.StringProperty(name = "Shot Code", default = "Shot")
    duration                        : bpy.props.IntProperty(name = "Frames", default = 24, min = 1)
    camera                          : bpy.props.PointerProperty(name = "Camera", type = bpy.types.Camera)


##############################################################################
# Operators
##############################################################################


class SEQUENCER_OT_autorename_shots(bpy.types.Operator):
    """Auto-rename all shots and their associated cameras"""

    bl_idname = "milkshake.sequencer_ot_autorename_shots"
    bl_label = "Rename All"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.autorename_shots(context)
        func.sync_timeline(context)
        return {"FINISHED"}


class SEQUENCER_OT_clear_shots(bpy.types.Operator):
    """Clear the shot list"""

    bl_idname = "milkshake.sequencer_ot_clear_shots"
    bl_label = "Clear"
    bl_options = {"REGISTER", "UNDO"}

    index : bpy.props.IntProperty()

    def execute(self, context):
        context.scene.milkshake_shots.clear()
        func.sync_timeline(context)
        return {"FINISHED"}


class SEQUENCER_OT_delete_shot(bpy.types.Operator):
    """Delete the selected shot and the associated camera"""

    bl_idname = "milkshake.sequencer_ot_delete_shot"
    bl_label = "Delete"
    bl_options = {"REGISTER", "UNDO"}

    index : bpy.props.IntProperty()

    def execute(self, context):
        func.delete_shot(context, self.index)
        func.autorename_shots(context)
        func.sync_timeline(context)
        return {"FINISHED"}


class SEQUENCER_OT_new_shot(bpy.types.Operator):
    """Create a new shot and camera"""

    bl_idname = "milkshake.sequencer_ot_new_shot"
    bl_label = "New Shot"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.new_shot(context)
        func.autorename_shots(context)
        func.sync_timeline(context)
        return {"FINISHED"}


class SEQUENCER_OT_sync_timeline(bpy.types.Operator):
    """Sync Blender's timeline and markers with the shot list"""

    bl_idname = "milkshake.sequencer_ot_sync_timeline"
    bl_label = "Sync Timeline"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        func.sync_timeline(context)
        return {"FINISHED"}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_sequencer(bpy.types.Panel):

    bl_context = "scene"
    bl_idname = "milkshake.properties_pt_sequencer"
    bl_label = "Milkshake Sequencer"
    bl_region_type = "WINDOW"
    bl_space_type = "PROPERTIES"

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.operator("milkshake.sequencer_ot_new_shot", icon = "PLUS")
        sub.operator("milkshake.sequencer_ot_sync_timeline", icon = "FILE_REFRESH")
        sub = col.row(align = True)
        sub.operator("milkshake.sequencer_ot_autorename_shots", icon = "FONT_DATA")
        sub.operator("milkshake.sequencer_ot_clear_shots", icon = "X")
        box_shots = col.box()
        if len(context.scene.milkshake_shots) == 0:
            box_shots.label(text = "No shots yet.")
        for index, shot in enumerate(context.scene.milkshake_shots):
            col_shot = box_shots.column(align = True)
            sub = col_shot.row(align = True)
            sub.prop(shot, "code", text = "")
            sub.prop(data = shot, property = "duration", text = "Frames")
            sub = col_shot.row(align = True)
            sub.prop(data = shot, property = "camera", text = "")
            sub.operator("milkshake.sequencer_ot_delete_shot", icon = "X").index = index


##############################################################################
# Registration
##############################################################################


classes = [
    MilkshakeSequencerShot,
    PROPERTIES_PT_sequencer,
    SEQUENCER_OT_autorename_shots,
    SEQUENCER_OT_clear_shots,
    SEQUENCER_OT_delete_shot,
    SEQUENCER_OT_new_shot,
    SEQUENCER_OT_sync_timeline
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)
    bpy.types.Scene.milkshake_shots = bpy.props.CollectionProperty(type = MilkshakeSequencerShot)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
    try:
        del bpy.types.Scene.milkshake_shots
    except:
        pass
