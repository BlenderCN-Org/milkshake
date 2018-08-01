bl_info = {
    "name": "Milkshake",
    "description": "A random collection of tools I've written over the years, as and when they came in handy.",
    "author": "Sam Van Hulle",
    "version": (1, 0, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tools",
    "category": "Tools"
}


##############################################################################
# Imports
##############################################################################


if "bpy" in locals():
    from importlib import reload
    reload(cleanup)
    reload(lighting)
    reload(modeling)
    reload(sequencer)
    reload(setdress)
    reload(utilities)
    print("[Milkshake] Reloaded package modules")

else:
    from . import cleanup, lighting, modeling, sequencer, setdress, utilities
    print("[Milkshake] Loaded package modules")

import bpy


##############################################################################
# Properties
##############################################################################


class Milkshake_Log(bpy.types.PropertyGroup):

    output                          = bpy.props.StringProperty(name = "Output Log", default = "")


class Milkshake_SequencerShot(bpy.types.PropertyGroup):

    code                            = bpy.props.StringProperty(name = "Shot Code", default = "Shot")
    duration                        = bpy.props.IntProperty(name = "Frames", default = 24, min = 1)
    camera                          = bpy.props.PointerProperty(name = "Camera", type = bpy.types.Camera)


##############################################################################
# Panels
##############################################################################


class VIEW3D_PT_milkshake_cleanup(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Milkshake"
    bl_context = "objectmode"
    bl_label = "Cleanup"
    bl_idname = "milkshake_cleanup_panel"

    def draw(self, context):
        lay = self.layout
        lay.label(text = "Rename:", icon = "OUTLINER_OB_FONT")
        row = lay.row(align = True)
        row.operator("object.milkshake_rename", text = "Object to Data")
        row.operator("object.milkshake_rename", text = "Data to Object").data_to_object = False


class VIEW3D_PT_milkshake_lighting(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Milkshake"
    bl_context = "objectmode"
    bl_label = "Lookdev"
    bl_idname = "milkshake_lighting_panel"

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        col.operator("object.milkshake_assign_material", icon = "MATERIAL")
        col.operator("scene.milkshake_render_setup", icon = "RENDERLAYERS")


class VIEW3D_PT_milkshake_modeling(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Milkshake"
    bl_context = "objectmode"
    bl_label = "Modeling"
    bl_idname = "milkshake_modeling_panel"

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        col.operator("object.milkshake_clear_sharp", icon = "EDGESEL")
        lay.label(text = "Subdivisions:", icon = "MOD_SUBSURF")
        row = lay.row(align = True)
        row.operator("object.milkshake_set_subdivision")
        row.operator("object.milkshake_set_subdivision_to_adaptive")


class VIEW3D_PT_milkshake_sequencer(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Milkshake"
    bl_context = "objectmode"
    bl_label = "Sequencer"
    bl_idname = "milkshake_sequencer_panel"

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        sub = col.row(align = True)
        sub.operator("scene.milkshake_new_shot", icon = "ZOOMIN")
        sub.operator("scene.milkshake_sync_timeline", icon = "FILE_REFRESH")
        sub = col.row(align = True)
        sub.operator("scene.milkshake_autorename_shots", icon = "FONT_DATA")
        sub.operator("scene.milkshake_clear_shots", icon = "X")
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
            sub.operator("scene.milkshake_delete_shot", icon = "X").index = index


class VIEW3D_PT_milkshake_setdress(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Milkshake"
    bl_context = "objectmode"
    bl_label = "Setdress"
    bl_idname = "milkshake_setdress_panel"

    def draw(self, context):
        lay = self.layout
        lay.operator("scene.milkshake_generate_placeholders", icon = "OUTLINER_OB_EMPTY")


class VIEW3D_PT_milkshake_utilities(bpy.types.Panel):

    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Milkshake"
    bl_context = "objectmode"
    bl_label = "Utilities"
    bl_idname = "milkshake_utilities_panel"

    def draw(self, context):
        lay = self.layout
        col = lay.column(align = True)
        col.operator("scene.milkshake_toggle_wire", icon = "WIRE")
        col.operator("scene.milkshake_unlock_transforms", icon = "UNLOCKED")


##############################################################################
# Registration
##############################################################################


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.milkshake_log = bpy.props.PointerProperty(type = Milkshake_Log)
    bpy.types.Scene.milkshake_shots = bpy.props.CollectionProperty(type = Milkshake_SequencerShot)


def unregister():
    bpy.utils.unregister_module(__name__)
    try:
        del bpy.types.Scene.milkshake_log
        del bpy.types.Scene.milkshake_shots
    except:
        pass


if __name__  ==  "__main__":
    register()
