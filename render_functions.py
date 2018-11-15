##############################################################################
# Imports
##############################################################################


import bpy, os, json
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def camera_bounds_to_render_border(context):
    """Copy the camera bounds to the render border"""

    render = context.scene.render
    render.use_border = True
    render.border_min_x = 0
    render.border_min_y = 0
    render.border_max_x = 1
    render.border_max_y = 1
    core.log("Render border set to camera bounds")


def layer_setup(context):
    """Set up the view layers"""

    config = json.load(os.path.join(os.path.dirname(os.path.abspath(__file__))), "files", "layer_templates.json")
    layers = context.scene.view_layers

    # Create collections that don't exist yet
    existing_collection_names = set(bpy.data.collections.keys())
    all_collection_names = set(config["all_collection_names"])
    required_collection_names = all_collection_names - existing_collection_names
    for collection_name in required_collection_names:
        bpy.data.collections.new(collection_name)
    for collection_name in all_collection_names:
        context.scene.collection.children.link(bpy.data.collections[collection_name])

    # Remove existing view layers
    for layer in layers:
        try:
            layers.remove(layer)
        except:
            pass
    layers[0].name = "delete"

    # Create new ones
    for template in config["layer_templates"]:

        # Create layer and enable/disable it by default.
        layer = layers.new(template["name"])
        if "enabled" in template:
            layer.use = template["enabled"]
        core.log(f"{layer.name} rendering is set to {layer.use}.")

        # Set per-layer collection overrides.
        indirect_collection_names = template.get("indirect", [])
        exclude_collection_names = template.get("exclude", [])
        holdout_collection_names = template.get("holdout", [])
        for collection in all_collections:
            # setattr(layer, "override_indirect_only", collection in indirect_collection_names)
            # setattr(layer, "override_exclude", collection in exclude_collection_names)
            # setattr(layer, "override_holdout", collection in holdout_collection_names)
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

    # Remove the old remaining layer
    layers.remove(layers[0])

    # Set active layer to BG01
    context.view_layer = context.scene.view_layers[layer_templates[0]["name"]]


def render_defaults(context):
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
    cycles.max_bounces                        = 3
    cycles.preview_samples                    = 0
    cycles.sample_all_lights_direct           = True
    cycles.sample_all_lights_indirect         = True
    cycles.sample_clamp_direct                = 0.0
    cycles.sample_clamp_indirect              = 10
    cycles.samples                            = 250
    cycles.transmission_bounces               = 3
    cycles.transparent_max_bounces            = 12
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
    scene.view_settings.exposure              = 0
    scene.view_settings.gamma                 = 1
    scene.view_settings.look                  = "Filmic - Base Contrast"
    scene.view_settings.view_transform        = "Filmic"
    # Performance
    render.engine                             = "CYCLES"
    render.tile_x                             = 32
    render.tile_y                             = 32
    cycles.tile_order                         = "CENTER"
    # TODO: Add a light falloff node to every light that doesn't already have one
    core.log("Applied render defaults.")
