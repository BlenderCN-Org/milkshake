################################################################################
#
# setdress_functions.py
#
################################################################################


import bpy


def generate_placeholders(context:bpy.types.Context):
    """"""

    for o in context.selected_objects:
        if "{}.placeholders".format(o.name) in bpy.data.objects:
            category_empty = bpy.data.objects["{}.placeholders".format(o.name)]
        else:
            category_empty = bpy.data.objects.new("{}.placeholders".format(o.name), None)
        context.scene.objects.link(category_empty)
        object_empty = bpy.data.objects.new("{}.placeholder".format(o.name), None)
        context.scene.objects.link(object_empty)
        object_empty.parent = category_empty
        object_empty.location = o.location
