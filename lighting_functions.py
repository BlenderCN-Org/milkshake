##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def render_defaults(context:bpy.types.Context):
    """Apply default render settings"""

    scene = context.scene
    render = scene.render
    cycles = scene.cycles

    # Noise reduction
    cycles.blur_glossy                        = 2
    cycles.caustics_reflective                = False
    cycles.caustics_refractive                = False
    cycles.diffuse_bounces                    = 3
    cycles.glossy_bounces                     = 3
    cycles.max_bounces                        = 32
    cycles.preview_samples                    = 0
    cycles.sample_all_lights_direct           = True
    cycles.sample_all_lights_indirect         = True
    cycles.sample_clamp_direct                = 0.0
    cycles.sample_clamp_indirect              = 10
    cycles.samples                            = 250
    cycles.transmission_bounces               = 3
    cycles.transparent_max_bounces            = 32
    cycles.transparent_min_bounces            = 32
    cycles.use_animated_seed                  = True
    cycles.volume_bounces                     = 0


    # Motion blur
    cycles.motion_blur_position               = "CENTER"
    cycles.rolling_shutter_type               = "NONE"
    cycles.use_motion_blur                    = True
    render.motion_blur_shutter                = 0.3

    # Colour management
    cycles.film_transparent                   = True
    scene.display_settings.display_device     = "sRGB"
    scene.sequencer_colorspace_settings.name  = "Filmic Log"
    scene.view_settings.look                  = "Filmic - Base Contrast"
    scene.view_settings.view_transform        = "Filmic"

    # Performance
    render.engine                             = "CYCLES"
    render.tile_x                             = 32
    render.tile_y                             = 32
    cycles.tile_order                         = "CENTER"

    # Add a light falloff node to every light that doesn't already have one
    core.log("Applied render defaults.")


def layer_setup(context:bpy.types.Context):
    """Set up the view layers"""

    # Set up collections
    sc = context.scene.collection.children
    collections = bpy.data.collections
    for collection in collections:
        collections.remove(collection)

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

    all_collections = [animprops, bg01_sets, bg02_sets, characters, dust, lights, bg_lights, fg_lights, vol_lights, hidden]
    for collection in all_collections:
        sc.link(collection)

    # Set up view layers
    layer_templates = [
        {
            "name": "VOL",
            "exclude": [dust, lights, bg_lights, fg_lights, hidden],
            "filter": ["solid", "strand"],
            "passes": ["combined"],
            "default": True
        },
        {
            "name": "DUST",
            "indirect_only": [animprops, bg01_sets, bg02_sets, characters],
            "exclude": [hidden, vol_lights],
            "holdout": [animprops, bg01_sets, bg02_sets, characters],
            "filter": ["sky", "solid", "strand"],
            "passes": ["combined", "z", "vector"],
            "default": False
        },
        {
            "name": "FG",
            "indirect_only": [bg01_sets, bg02_sets],
            "exclude": [dust, bg_lights, vol_lights, hidden],
            "holdout": [bg01_sets, bg02_sets],
            "filter": ["sky", "ao", "solid", "strand"],
            "passes": ["combined", "z", "vector", "subsurface_direct", "mist", "ambient_occlusion"],
            "crypto": ["object", "material"],
            "default": True,
            "denoising": ["use", "store"]
        },
        {
            "name": "BG01",
            "indirect_only": [animprops, characters],
            "exclude": [dust, fg_lights, hidden, vol_lights],
            "holdout": [bg02_sets],
            "filter": ["sky", "ao", "solid", "strand"],
            "passes": ["combined", "z", "vector", "mist", "ambient_occlusion"],
            "crypto": ["object", "material"],
            "default": True,
            "denoising": ["use", "store"]
        },
        {
            "name": "BG02",
            "indirect_only": [animprops, bg01_sets, characters],
            "exclude": [dust, fg_lights, hidden, vol_lights],
            "holdout": [],
            "filter": ["sky", "ao", "solid", "strand"],
            "passes": ["combined", "z", "vector", "mist", "ambient_occlusion"],
            "crypto": ["object", "material"],
            "default": True,
            "denoising": ["use", "store"]
        }
    ]

    # Remove existing
    layers = context.scene.view_layers
    for layer in layers:
        try:
            layers.remove(layer)
        except:
            pass
    layers[0].name = "delete"

    # Create new ones
    for template in layer_templates:

        # Create layer and enable/disable it by default.
        layer = layers.new(template["name"])
        if "default" in template:
            layer.use = template["default"]
        core.log(f"{layer.name} layer rendering is set to {layer.use}.")

        # Set per-layer collection overrides.
        indirect_only_collections = template.get("indirect_only", [])
        exclude_collections = template.get("exclude", [])
        holdout_collections = template.get("holdout", [])
        for collection in all_collections:
            # setattr(layer, "override_indirect_only", collection in indirect_only_collections)
            # setattr(layer, "override_exclude", collection in exclude_collections)
            # setattr(layer, "override_holdout", collection in holdout_collections)
            pass

        # Set any configured filter, disable the rest.
        filters = template.get("filters", [])
        all_filters = ["sky", "ao", "solid", "strand", "freestyle"]
        for filter_name in all_filters:
            setattr(layer, f"use_{filter_name}", filter_name in filters)

        # Set any configured pass, disable the rest.
        passes = template.get("passes", [])
        all_passes = ["combined", "z", "mist", "normal", "vector", "uv", "object_index", "material_index", "diffuse_direct", "diffuse_indirect", "glossy_direct", "glossy_indirect", "transmission_direct", "transmission_indirect", "subsurface_direct", "subsurface_indirect", "emit", "environment", "shadow", "ambient_occlusion"]
        for pass_name in all_passes:
            setattr(layer, f"use_pass_{pass_name}", pass_name in passes)

        # Cryptomatte
        crypto_modes = template.get("crypto", [])
        all_crypto_modes = ["object", "material", "asset"]
        for crypto_mode in all_crypto_modes:
            setattr(layer.cycles, f"use_pass_crypto_{crypto_mode}", crypto_mode in crypto_modes)
        layer.cycles.pass_crypto_depth = 6
        layer.cycles.pass_crypto_accurate = True

        # Denoising
        denoise_options = template.get("denoise", [])
        all_denoise_options = ["use", "store"]
        for denoise_option in all_denoise_options:
            layer.cycles.use_denoising = "store" in denoise_options

        # Set alpha treshold to zero (prevents Z/index/vector/normal/uv pass glitches on transparent surfaces with variable roughness)
        layer.cycles.pass_alpha_treshold = 0

        core.log(f"{layer.name} layer is set up.")

    layers.remove(layers[0])
