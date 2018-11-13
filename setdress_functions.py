##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def generate_placeholders(context:bpy.types.Context):
    """Generate placeholders for the selected objects"""

    main_collection = bpy.data.collections.new("Placeholders")
    context.scene.collection.children.link(main_collection)

    for o in context.selected_objects:
        if f"{o.name}.placeholders" in main_collection.children:
            category_collection = main_collection.children[f"{o.name}.placeholders"]
        else:
            category_collection = main_collection.children.new(f"{o.name}.placeholders")
        object_empty = bpy.data.objects.new("{}.placeholder".format(o.name), None)
        object_empty.location = o.location
        category_collection.objects.link(object_empty)
        core.log(f"Created placeholder {object_empty.name}")
