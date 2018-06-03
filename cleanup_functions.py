################################################################################
#
# cleanup_functions.py
#
################################################################################


import bpy


def rename(context:bpy.types.Context, data_to_object:bpy.props.BoolProperty):
    for i in context.selected_objects:
        if i.data:
            if data_to_object:
                i.name = i.data.name
            else:
                i.data.name = i.name
