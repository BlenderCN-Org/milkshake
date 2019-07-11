##############################################################################
# Imports
##############################################################################


import bpy
from . import sequencer_functions as func
from importlib import reload
reload(func)


##############################################################################
# Properties
##############################################################################


class MilkshakeSequencerShot(bpy.types.PropertyGroup):

    code                            : bpy.props.StringProperty(name = "Shot Code", default = "Shot")
    duration                        : bpy.props.IntProperty(name = "Frames", default = 24, min = 1, update = func.sync_timeline)
    camera                          : bpy.props.PointerProperty(name = "Camera", type = bpy.types.Camera, update = func.sync_timeline)


##############################################################################
# Operators
##############################################################################


class SEQUENCER_OT_clear_shots(bpy.types.Operator):
    """Clear the shot list and delete the associated cameras"""

    bl_idname = "milkshake.sequencer_ot_clear_shots"
    bl_label = "Clear"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        func.clear_shots(context)
        func.sync_timeline(self, context)
        return {'FINISHED'}


class SEQUENCER_OT_delete_shot(bpy.types.Operator):
    """Delete the selected shot and the associated camera"""

    bl_idname = "milkshake.sequencer_ot_delete_shot"
    bl_label = "Delete"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        func.delete_shot(context, self.index)
        func.autorename_shots(context)
        func.sync_timeline(self, context)
        return {'FINISHED'}


class SEQUENCER_OT_new_shot(bpy.types.Operator):
    """Create a new shot and camera"""

    bl_idname = "milkshake.sequencer_ot_new_shot"
    bl_label = "New Shot"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        func.new_shot(context)
        func.autorename_shots(context)
        return {'FINISHED'}


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_sequencer(bpy.types.Panel):

    bl_context = "scene"
    bl_idname = "PROPERTIES_PT_sequencer"
    bl_label = "Milkshake Sequencer"
    bl_region_type = 'WINDOW'
    bl_space_type = 'PROPERTIES'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.operator("milkshake.sequencer_ot_new_shot", icon = 'ADD', text = "")
        sub.operator("milkshake.sequencer_ot_clear_shots", icon = 'X', text = "")
        box_shots = col.box()
        if len(context.scene.milkshake_shots) == 0:
            box_shots.label(text = "No shots yet.")
        for index, shot in enumerate(context.scene.milkshake_shots):
            row_shot = box_shots.row(align = True)
            sub = row_shot.split(align = True, factor = 0.25)
            sub.label(text = shot.code)
            sub.prop(data = shot, property = "camera", text = "")
            sub = row_shot.row(align = True)
            sub.prop(data = shot, property = "duration", text = "")
            sub.operator("milkshake.sequencer_ot_delete_shot", icon = 'REMOVE', text = "").index = index


##############################################################################
# Registration
##############################################################################


classes = [
    MilkshakeSequencerShot,
    PROPERTIES_PT_sequencer,
    SEQUENCER_OT_clear_shots,
    SEQUENCER_OT_delete_shot,
    SEQUENCER_OT_new_shot
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
