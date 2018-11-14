bl_info = {
    "name": "Milkshake",
    "description": "A random collection of tools I've written over the years, as and when they came in handy.",
    "author": "Sam Van Hulle",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tools",
    "category": "Tools"
}


##############################################################################
# Imports
##############################################################################


import bpy
from . import cleanup, core_functions, render, modeling, sequencer, utilities
core_functions.log("Loaded package modules.")

if "bpy" in locals():
    from importlib import reload
    for m in modules:
        reload(m)
    core_functions.log("Reloaded package modules.")


##############################################################################
# Properties
##############################################################################


class MilkshakeSequencerShot(bpy.types.PropertyGroup):

    code                            : bpy.props.StringProperty(name = "Shot Code", default = "Shot")
    duration                        : bpy.props.IntProperty(name = "Frames", default = 24, min = 1)
    camera                          : bpy.props.PointerProperty(name = "Camera", type = bpy.types.Camera)


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_main(bpy.types.Panel):

    bl_context = ".objectmode"
    bl_idname = "milkshake.properties_pt_main"
    bl_label = "Milkshake"
    bl_region_type = "WINDOW"
    bl_space_type = "PROPERTIES"

    def draw(self, context):
        lay = self.layout

        lay.label(text = "Auto-rename:")
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.operator("milkshake.cleanup_ot_rename", text = "Objects").rename_datablock = False
        sub.operator("milkshake.cleanup_ot_rename", text = "Data").rename_datablock = True
        sub.operator("milkshake.cleanup_ot_rename_images")

        lay.label(text = "Modeling and Setdress:")
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.operator("milkshake.modeling_ot_clear_sharp", icon = "EDGESEL")
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.operator("milkshake.modeling_ot_generate_placeholders", icon = "OUTLINER_OB_EMPTY")
        sub = col.split(align = True, factor = 0.6)
        sub.scale_y = 1.5
        sub.operator("milkshake.modeling_ot_set_subdivision", icon = "MOD_SUBSURF")
        sub.operator("milkshake.modeling_ot_set_subdivision_to_adaptive")

        lay.label(text = "Rendering:")
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.operator("milkshake.render_ot_render_defaults", icon = "QUESTION")
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.operator("milkshake.render_ot_layer_setup", icon = "RENDERLAYERS")
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.prop(context.scene.cycles, "preview_pause", icon = "PAUSE", text = "Pause Viewport Renders")

        lay.label(text = "Utilities:")
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.operator("milkshake.utilities_ot_unlock_transforms", icon = "UNLOCKED")


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
    PROPERTIES_PT_main,
    PROPERTIES_PT_sequencer
]


def register():
    for m in modules:
        m.register()
    for i in classes:
        bpy.utils.register_class(i)
    bpy.types.Scene.milkshake_shots = bpy.props.CollectionProperty(type = MilkshakeSequencerShot)


def unregister():
    for m in modules:
        m.unregister()
    for i in classes:
        bpy.utils.unregister_class(i)
    try:
        del bpy.types.Scene.milkshake_shots
    except:
        pass


if __name__  ==  "__main__":
    register()
