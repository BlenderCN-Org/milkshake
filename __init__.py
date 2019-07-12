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


from . import cleanup, comp, core_functions, render, modeling, sequencer
modules = [cleanup, comp, render, modeling, sequencer]
core_functions.log("Loaded package modules.")

if "bpy" in locals():
    from importlib import reload
    for m in modules:
        reload(m)
    core_functions.log("Reloaded package modules.")
else:
    import bpy

##############################################################################
# Milkshake Error
##############################################################################


class MilkshakeError(Exception):

    def __init__(self, message):
        self.message = message


##############################################################################
# Registration
##############################################################################


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()


if __name__  ==  "__main__":
    register()
