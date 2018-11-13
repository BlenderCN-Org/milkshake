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
    """Sets up the view layers and render settings."""

    context.scene.render.engine = "CYCLES"
    context.scene.display_settings.display_device = "sRGB"
    context.scene.view_settings.view_transform = "Filmic"
    context.scene.view_settings.look = "Filmic - Base Contrast"
    context.scene.sequencer_colorspace_settings.name = "Filmic Log"
    context.scene.cycles.samples = 250
    context.scene.cycles.preview_samples = 0
    context.scene.cycles.sample_clamp_indirect = 10
    context.scene.cycles.max_bounces = 12
    context.scene.cycles.diffuse_bounces = 3
    context.scene.cycles.glossy_bounces = 3
    context.scene.cycles.transparent_max_bounces = 12
    context.scene.cycles.transmission_bounces = 3
    context.scene.cycles.volume_bounces = 0
    context.scene.cycles.blur_glossy = 2
    context.scene.cycles.caustics_reflective = False
    context.scene.cycles.caustics_refractive = False
    context.scene.cycles.use_motion_blur = False
    context.scene.cycles.film_transparent = True

    # Add a light falloff node to every light that doesn't already have one

    collections = bpy.data.collections
    layers = context.scene.view_layers

    # Set up collections
    for c in collections:
        collections.remove(c)
    new_collections = {
        "animprops"               : collections.new("Animprops"),
        "bg01_sets"               : collections.new("BG01 Sets"),
        "bg02_sets"               : collections.new("BG02 Sets"),
        "characters"              : collections.new("Characters"),
        "dust"                    : collections.new("DUST"),
        "lights"                  : collections.new("BG + FG Lights"),
        "bg_lights"               : collections.new("BG Lights"),
        "fg_lights"               : collections.new("FG Lights"),
        "vol_lights"              : collections.new("VOL Lights"),
        "hidden"                  : collections.new("Hidden")
    }
    for c in new_collections.values():
        context.scene.collection.children.link(c)

    # Set up view layers
    layer_templates = [
        {
            "name": "VOL",
            "exclude": ["dust", "lights", "bg_lights", "fg_lights", "hidden"],
            "filter": ["solid", "strand"],
            "passes": ["combined"],
            "default": True
        },
        {
            "name": "DUST",
            "indirect_only": ["animprops", "bg01_sets", "bg02_sets", "characters"],
            "exclude": ["hidden", "vol_lights"],
            "holdout": ["animprops", "bg01_sets", "bg02_sets", "characters"],
            "filter": ["sky", "solid", "strand"],
            "passes": ["combined", "z", "vector"],
            "default": False
        },
        {
            "name": "FG",
            "indirect_only": ["bg01_sets", "bg02_sets"],
            "exclude": ["dust", "bg_lights", "vol_lights", "hidden"],
            "holdout": ["bg01_sets", "bg02_sets"],
            "filter": ["sky", "ao", "solid", "strand"],
            "passes": ["combined", "z", "vector", "subsurface_direct", "mist", "ambient_occlusion"],
            "crypto": ["object", "material"],
            "default": True
        },
        {
            "name": "BG01",
            "indirect_only": ["animprops", "characters"],
            "exclude": ["dust", "fg_lights", "hidden", "vol_lights"],
            "holdout": ["bg02_sets"],
            "filter": ["sky", "ao", "solid", "strand"],
            "passes": ["combined", "z", "vector", "mist", "ambient_occlusion"],
            "crypto": ["object", "material"],
            "default": True
        },
        {
            "name": "BG02",
            "indirect_only": ["animprops", "bg01_sets", "characters"],
            "exclude": ["dust", "fg_lights", "hidden", "vol_lights"],
            "holdout": [],
            "filter": ["sky", "ao", "solid", "strand"],
            "passes": ["combined", "z", "vector", "mist", "ambient_occlusion"],
            "crypto": ["object", "material"],
            "default": True
        }
    ]

    # Remove existing
    for l in layers:
        try:
            layers.remove(l)
        except:
            pass
    layers[0].name = "delete"

    # Create new ones
    for l in range(len(layer_templates)):
        template = layer_templates[l]
        layer = layers.new(template["name"])
        if "indirect_only" in template:
            # Set per-layer collection override to Indirect only.
            pass
        if "exclude" in template:
            # Set per-layer collection override to Exclude.
            pass
        if "holdout" in template:
            # Set per-layer collection override to Holdout.
            pass
        if "filter" in template:
            filters = ["sky", "ao", "solid", "strand", "freestyle"]
            for d in filters:
                setattr(layer, "use_{}".format(d), False)
            for d in template["filter"]:
                setattr(layer, "use_{}".format(d), True)
        if "passes" in template:
            layer.use_pass_combined = False
            layer.use_pass_z = False
            for p in template["passes"]:
                setattr(layer, "use_pass_{}".format(p), True)
        if "default" in template:
            layer.use = template["default"]

    layers.remove(layers[0])
    core.log(message = "Finished setting up layers.")
