##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def read_materials(self, context:bpy.types.Context):
    """Provides a list of materials for the user interface of the Assign Material tool."""

    materials = [("None", "None", "None")]
    if bpy.data:
        materials.extend([(m.name, m.name, m.name) for m in bpy.data.materials])
    return materials


def render_setup(context:bpy.types.Context):
    """Sets up the view layers."""

    collections = bpy.data.collections
    layers = context.scene.view_layers

    # Set up collections
    animprops               = collections.new("Animprops")
    bg01_sets               = collections.new("BG01 Sets")
    bg02_sets               = collections.new("BG02 Sets")
    characters              = collections.new("Characters")
    dust                    = collections.new("DUST")
    lights                  = collections.new("BG + FG Lights")
    bg_lights               = collections.new("BG Lights")
    fg_lights               = collections.new("FG Lights")
    vol_lights              = collections.new("VOL Lights")
    hidden                  = collections.new("Hidden")

    # Set up view layers
    layer_templates = [
        {
            "name": "VOL",
            "exclude": [dust, lights, bg_lights, fg_lights, hidden],
            "filter": ["ao", "sky"],
            "passes": ["combined"],
            "default": True
        },
        {
            "name": "DUST",
            "indirect_only": [animprops, bg01_sets, bg02_sets, characters],
            "exclude": [hidden, vol_lights],
            "holdout": [animprops, bg01_sets, bg02_sets, characters],
            "filter": ["ao"],
            "passes": ["combined", "z", "vector"],
            "default": False
        },
        {
            "name": "FG",
            "indirect_only": [bg01_sets, bg02_sets],
            "exclude": [dust, bg_lights, vol_lights, hidden],
            "holdout": [bg01_sets, bg02_sets],
            "filter": [],
            "passes": ["combined", "z", "vector", "subsurface_direct", "mist", "ambient_occlusion", "crypto_material"],
            "default": True
        },
        {
            "name": "BG01",
            "indirect_only": [animprops, characters],
            "exclude": [dust, fg_lights, hidden, vol_lights],
            "holdout": [bg02_sets],
            "passes": ["combined", "z", "vector", "mist", "ambient_occlusion", "crypto_material"],
            "default": True
        },
        {
            "name": "BG02",
            "indirect_only": [animprops, bg01_sets, characters],
            "exclude": [dust, fg_lights, hidden, vol_lights],
            "holdout": [],
            "passes": ["combined", "z", "vector", "mist", "ambient_occlusion", "crypto_material"],
            "default": True
        }
    ]

    # Remove existing
    for l in layers:
        try:
            layers.remove(l)
        except:
            pass
    old = layers[0]
    old.name = "delete"

    # Create new ones
    for l in range(len(layer_templates)):
        template = layer_templates[l]
        layer = layers.new(template["name"])
        layer.name = template["name"]
        if "indirect_only" in template:
            # Adapt to 2.80
        if "exclude" in template:
            # Adapt to 2.80
        if "holdout" in template:
            # Adapt to 2.80
        if "passes" in template:
            layer.use_pass_combined = False
            layer.use_pass_z = False
            for p in template["passes"]:
                setattr(layer, "use_pass_{}".format(p), True)
        if "filter" in template:
            for d in template["filter"]:
                setattr(layer, "use_{}".format(d), False)
        if "default" in template:
            layer.use = template["default"]
    layers.remove(old)

    core.log(message = "Finished setting up layers.")
