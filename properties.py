################################################################################
#
# properties.py
#
################################################################################


import bpy


class Milkshake_Log(bpy.types.PropertyGroup):

    output                          = bpy.props.StringProperty(name = "Output Log", default = "")


class Milkshake_SequencerShot(bpy.types.PropertyGroup):

    code                            = bpy.props.StringProperty(name = "Shot Code", default = "Shot")
    camera_name                     = bpy.props.StringProperty(name = "Camera", default = "")
    duration                        = bpy.props.IntProperty(name = "Frames", default = 24, min = 1)
    camera                          = bpy.props.PointerProperty(name = "Camera", type = bpy.types.Camera)
