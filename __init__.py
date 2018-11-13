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


if "bpy" in locals():
    from importlib import reload
    for m in modules:
        reload(m)
    print("[Milkshake] Reloaded package modules")

else:
    from . import cleanup, lighting, modeling, sequencer, setdress, utilities
    modules = [ cleanup, lighting, modeling, sequencer, setdress, utilities ]
    print("[Milkshake] Loaded package modules")

import bpy


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


class VIEW3D_PT_main(bpy.types.Panel):

    bl_context = "objectmode"
    bl_idname = "milkshake.view3d_pt_main"
    bl_label = "Milkshake Scene Tools"
    bl_region_type = "TOOLS"
    bl_space_type = "VIEW_3D"

    def draw(self, context):
        lay = self.layout

        lay.label(text = "Cleanup")
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.label(text = "Rename")
        sub.operator("milkshake.cleanup_ot_rename", text = "Objects").object_to_data = False
        sub.operator("milkshake.cleanup_ot_rename", text = "Data").object_to_data = True
        col.operator("milkshake.cleanup_ot_rename_images")

        lay.label(text = "Modeling")
        col = lay.column(align = True)
        col.operator("milkshake.modeling_ot_clear_sharp", icon = "EDGESEL")
        row = col.row(align = True)
        row.operator("milkshake.modeling_ot_set_subdivision", icon = "MOD_SUBSURF")
        row.operator("milkshake.modeling_ot_set_subdivision_to_adaptive")

        lay.label(text = "Setdress")
        col = lay.column(align = True)
        col.operator("milkshake.setdress_ot_generate_placeholders", icon = "OUTLINER_OB_EMPTY")

        lay.label(text = "Utilities")
        col = lay.column(align = True)
        col.operator("milkshake.utilities_ot_unlock_transforms", icon = "UNLOCKED")


class PROPERTIES_PT_render(bpy.types.Panel):

    bl_context = "render"
    bl_idname = "milkshake.properties_pt_render"
    bl_label = "Milkshake Render Tools"
    bl_region_type = "WINDOW"
    bl_space_type = "PROPERTIES"

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.operator("milkshake.lighting_ot_render_defaults", icon = "QUESTION")
        sub = col.row(align = True)
        sub.scale_y = 1.5
        sub.operator("milkshake.lighting_ot_layer_setup", icon = "RENDERLAYERS")


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
    PROPERTIES_PT_render,
    VIEW3D_PT_main
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
