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


from . import cleanup, comp, core_functions, render, modeling, sequencer, utilities
modules = [cleanup, comp, render, modeling, sequencer, utilities]
core_functions.log("Loaded package modules.")

if "bpy" in locals():
    from importlib import reload
    for m in modules:
        reload(m)
    core_functions.log("Reloaded package modules.")
else:
    import bpy


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
        pass


class PROPERTIES_PT_compositor(bpy.types.Panel):

    bl_context = ""
    bl_idname = "milkshake.properties_pt_compositor"
    bl_label = "Milkshake"
    bl_region_type = "WINDOW"
    bl_space_type = "NODE_EDITOR"

    def draw(self, context):
        pass


##############################################################################
# Registration
##############################################################################


def register():
    bpy.utils.register_class(PROPERTIES_PT_main)
    bpy.utils.register_class(PROPERTIES_PT_compositor)
    for module in modules:
        module.register()


def unregister():
    bpy.utils.unregister_class(PROPERTIES_PT_main)
    bpy.utils.unregister_class(PROPERTIES_PT_compositor)
    for module in modules:
        module.unregister()


if __name__  ==  "__main__":
    register()
