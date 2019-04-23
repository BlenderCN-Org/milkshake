##############################################################################
# Imports
##############################################################################


import bpy, os, json
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def get_render_border(context):
    """Convert Blender's current render border to Milkshake's parameters"""
    render = context.scene.render
    milkshake = context.scene.milkshake_render_border

    border_min_x = render.border_min_x
    border_min_y = render.border_min_y
    border_max_x = render.border_max_x
    border_max_y = render.border_max_y

    milkshake.left = border_min_x * render.resolution_x
    milkshake.top = render.resolution_y - border_max_y * render.resolution_y
    milkshake.width = (border_max_x - border_min_x) * render.resolution_x
    milkshake.height = (border_max_y - border_min_y) * render.resolution_y


def update_render_border_left(self, context):
    """Updates Blender's render border while tweaking the Milkshake property"""
    render = context.scene.render
    milkshake = context.scene.milkshake_render_border
    render.use_border = True
    render.border_min_x = milkshake.left / render.resolution_x
    render.border_max_x = (milkshake.left + milkshake.width) / render.resolution_x
    return None


def update_render_border_top(self, context):
    """Updates Blender's render border while tweaking the Milkshake property"""
    render = context.scene.render
    milkshake = context.scene.milkshake_render_border
    render.use_border = True
    render.border_min_y = 1 - (milkshake.top + milkshake.height) / render.resolution_y
    render.border_max_y = 1 - milkshake.top / render.resolution_y
    return None


def update_render_border_width(self, context):
    """Updates Blender's render border while tweaking the Milkshake property"""
    render = context.scene.render
    milkshake = context.scene.milkshake_render_border
    render.use_border = True
    render.border_max_x = (milkshake.left + milkshake.width) / render.resolution_x
    return None


def update_render_border_height(self, context):
    """Updates Blender's render border while tweaking the Milkshake property"""
    render = context.scene.render
    milkshake = context.scene.milkshake_render_border
    render.use_border = True
    render.border_min_y = 1 - (milkshake.top + milkshake.height) / render.resolution_y
    return None


def camera_bounds_to_render_border(context):
    """Copy the camera bounds to the render border"""

    # Select the first viewport and enable camera view
    viewport = [area for area in bpy.context.screen.areas if area.type == 'VIEW_3D'][0]
    viewport.spaces[0].region_3d.view_perspective = 'CAMERA'

    render = context.scene.render
    render.use_border = True

    milkshake = context.scene.milkshake_render_border
    milkshake.height = render.resolution_y
    milkshake.left = 0
    milkshake.top = 0
    milkshake.width = render.resolution_x


def layer_setup(context):
    """Set up the view layers"""

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "files", "layer_setup.json"), 'r') as config_file:
        config = json.load(config_file)
    layers = context.scene.view_layers

    # Create missing collections
    collection_names_existing = set(context.scene.collection.children.keys())
    collection_names_all = set(config['collection_names_all'])
    collection_names_required = collection_names_all - collection_names_existing
    collection_names_excluded = collection_names_existing - collection_names_all
    for collection_name in collection_names_required:
        new_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(new_collection)

    # Remove existing view layers
    for layer in layers:
        if len(layers) > 1:
            layers.remove(layer)
    layers[0].name = "delete"

    # Create new ones
    for layer_template in config['layer_templates']:

        # Create layer and enable/disable it by default.
        layer = layers.new(layer_template['name'])
        if 'enabled' in layer_template:
            layer.use = layer_template['enabled']
        core.log(f"{layer.name} rendering is set to {layer.use}.")

        # Set per-layer collection influence.
        indirect_collection_names = layer_template.get('indirect', [])
        exclude_collection_names = layer_template.get('exclude', [])
        holdout_collection_names = layer_template.get('holdout', [])
        for collection_name in collection_names_all:
            layer.layer_collection.children[collection_name].indirect_only = collection_name in indirect_collection_names
            layer.layer_collection.children[collection_name].exclude = collection_name in exclude_collection_names
            layer.layer_collection.children[collection_name].holdout = collection_name in holdout_collection_names
        for collection_name in collection_names_excluded:
            layer.layer_collection.children[collection_name].exclude = True

        # Set any configured filter, disable the rest.
        filters = layer_template.get('filter', [])
        all_filters = ['sky', 'ao', 'solid', 'strand', 'freestyle']
        for filter_name in all_filters:
            setattr(layer, f"use_{filter_name}", filter_name in filters)

        # Set any configured pass, disable the rest.
        passes = layer_template.get('passes', [])
        all_passes = ['combined', 'z', 'mist', 'normal', 'vector', 'uv', 'object_index', 'material_index', 'diffuse_direct', 'diffuse_indirect', 'glossy_direct', 'glossy_indirect', 'transmission_direct', 'transmission_indirect', 'subsurface_direct', 'subsurface_indirect', 'emit', 'environment', 'shadow', 'ambient_occlusion']
        for pass_name in all_passes:
            setattr(layer, f"use_pass_{pass_name}", pass_name in passes)

        # Cryptomatte
        crypto_modes = layer_template.get('crypto', [])
        all_crypto_modes = ['object', 'material', 'asset']
        for crypto_mode in all_crypto_modes:
            setattr(layer.cycles, f"use_pass_crypto_{crypto_mode}", crypto_mode in crypto_modes)
        layer.cycles.pass_crypto_depth = 6
        layer.cycles.pass_crypto_accurate = True

        # Denoising
        denoise_options = layer_template.get('denoise', [])
        all_denoise_options = ['use', 'store']
        for denoise_option in all_denoise_options:
            layer.cycles.use_denoising = 'use' in denoise_options
            layer.cycles.denoising_store_passes = 'store' in denoise_options

        # Set alpha treshold to zero. This prevents
        # Z/index/vector/normal/uv pass glitches on
        # transparent surfaces with variable roughness.
        layer.cycles.pass_alpha_treshold = 0

        core.log(f"{layer.name} layer is set up.")

    layers.remove(layers['delete'])


def render_defaults(context):
    """Apply default render settings"""

    scene = context.scene
    render = scene.render
    cycles = scene.cycles
    # Noise reduction
    cycles.blur_glossy                          = 2
    cycles.caustics_reflective                  = False
    cycles.caustics_refractive                  = False
    cycles.diffuse_bounces                      = 3
    cycles.glossy_bounces                       = 3
    cycles.max_bounces                          = 12
    cycles.preview_samples                      = 0
    cycles.sample_all_lights_direct             = True
    cycles.sample_all_lights_indirect           = True
    cycles.sample_clamp_direct                  = 0.0
    cycles.sample_clamp_indirect                = 10
    cycles.samples                              = 250
    cycles.transmission_bounces                 = 3
    cycles.transparent_max_bounces              = 12
    cycles.use_animated_seed                    = True
    cycles.volume_bounces                       = 0
    # Motion blur
    cycles.motion_blur_position                 = 'CENTER'
    cycles.rolling_shutter_type                 = 'NONE'
    cycles.use_motion_blur                      = True
    render.motion_blur_shutter                  = 0.3
    # Colour management
    cycles.film_transparent                     = True
    scene.display_settings.display_device       = 'sRGB'
    scene.sequencer_colorspace_settings.name    = 'Filmic Log Encoding'
    scene.view_settings.exposure                = 0
    scene.view_settings.gamma                   = 1
    scene.view_settings.look                    = 'Base Contrast'
    scene.view_settings.view_transform          = 'Filmic Log Encoding Base'
    # Performance
    render.display_mode                         = 'AREA'
    render.engine                               = 'CYCLES'
    render.tile_x                               = 32
    render.tile_y                               = 32
    cycles.tile_order                           = 'CENTER'
    # Output
    render.resolution_x                         = 2048
    render.resolution_y                         = 858
    scene.frame_start                           = 1001
    scene.frame_end                             = 1250
    scene.frame_step                            = 1
    render.use_compositing                      = False
    render.use_sequencer                        = False
    render.image_settings.file_format           = 'PNG'
    render.image_settings.color_mode            = 'RGB'
    render.image_settings.color_depth           = '8'
    render.image_settings.compression           = 100

    core.log("Applied render defaults.")
