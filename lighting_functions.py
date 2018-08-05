##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def assign_material(context:bpy.types.Context, material:bpy.props.EnumProperty):
    # Delete everything
    for i in context.selected_objects:
        if i.type == "MESH":
            context.scene.objects.active = i
            slots = i.material_slots
            for d in range(len(slots)):
                i.active_material_index = d
                bpy.ops.object.material_slot_remove()
            # Now assign whatever is selected
            if material != "None":
                bpy.ops.object.material_slot_add()
                slots[0].material = bpy.data.materials[material]
            core.log("Assigned {} to {}".format(material, i.name))


def read_materials(self, context:bpy.types.Context):
    """Provides a list of materials for the user interface of the Assign Material tool."""

    materials = [("None", "None", "None")]
    if bpy.data:
        materials.extend([(m.name, m.name, m.name) for m in bpy.data.materials])
    return materials


def render_setup(context:bpy.types.Context):
    """Sets up the render layers."""

    named_layers = context.scene.namedlayers.layers
    scene_layers = context.scene.layers
    render_layers = context.scene.render.layers

    context.scene.use_nodes = True
    tree = context.scene.node_tree
    for node in tree.nodes:
        tree.nodes.remove(node)

    # Set up scene layers

    for i in range(20):
        named_layers[i].name = "Not in use"
        scene_layers[i] = False

    layer_templates = []

    named_layers[0].name = "BG01 objects"
    scene_layers[0] = True
    named_layers[1].name = "FG objects"
    scene_layers[1] = True
    named_layers[2].name = "DUST"
    scene_layers[2] = True
    named_layers[3].name = "FX objects"
    scene_layers[3] = True
    named_layers[4].name = "BG02 objects"
    scene_layers[4] = True
    named_layers[5].name = "BG lights"
    scene_layers[5] = True
    named_layers[6].name = "FG lights"
    scene_layers[6] = True
    named_layers[7].name = "BG + FG lights"
    scene_layers[7] = True
    named_layers[8].name = "VOL lights"
    scene_layers[8] = True
    named_layers[10].name = "BG-LightControl lights"
    scene_layers[10] = True
    named_layers[11].name = "FX-LightControl lights"
    scene_layers[11] = True
    named_layers[19].name = "Hidden"
    scene_layers[19] = False

    # Set up render layers

    render_layer_templates = [
        {
            "name": "TECH",
            "primary_visibility": [0,1,4],
            "accept_influence_of": [0,1,4],
            "dont": ["sky"],
            "passes": ["ambient_occlusion"],
            "default": True
        },
        {
            "name": "VOL",
            "primary_visibility": [0,1,3,4,8],
            "accept_influence_of": [0,1,3,4,8],
            "dont": ["ao", "sky"],
            "passes": ["combined"],
            "samples": 500,
            "default": True
        },
        {
            "name": "DUST",
            "primary_visibility": [2],
            "accept_influence_of": [2],
            "enable_matte": [0,1,3,4],
            "dont": ["ao", "sky"],
            "passes": ["combined", "z", "vector"],
            "default": False
        },
        {
            "name": "FX",
            "primary_visibility": [3],
            "accept_influence_of": [3],
            "enable_matte": [0,1,4],
            "dont": ["ao", "sky"],
            "passes": ["combined", "z", "vector"],
            "default": False
        },
        {
            "name": "FX-LightControl",
            "primary_visibility": [0,1,4,11],
            "accept_influence_of": [0,1,4,11],
            "dont": ["ao", "sky"],
            "passes": ["combined"],
            "default": False
        },
        {
            "name": "BG-LightControl",
            "primary_visibility": [0,1,4,10],
            "accept_influence_of": [0,1,4,10],
            "dont": ["ao", "sky"],
            "passes": ["combined"],
            "default": False
        },
        {
            "name": "FG",
            "primary_visibility": [1,6,7],
            "accept_influence_of": [0,1,4,6,7],
            "enable_matte": [0,4],
            "passes": ["combined", "z", "vector", "subsurface_direct"],
            "default": True
        },
        {
            "name": "BG01",
            "primary_visibility": [0,5,7],
            "accept_influence_of": [0,1,4,5,7],
            "enable_matte": [4],
            "passes": ["combined", "z", "vector"],
            "default": True
        },
        {
            "name": "BG02",
            "primary_visibility": [4,5,7],
            "accept_influence_of": [0,1,4,5,7],
            "passes": ["combined", "z", "vector"],
            "default": True
        }
    ]

    # Remove existing

    for l in render_layers:
        try:
            render_layers.remove(l)
        except:
            pass

    old = render_layers[0]
    old.name = "delete"

    # Create new ones

    for l in range(len(render_layer_templates)):
        template = render_layer_templates[l]
        layer = render_layers.new(template["name"])
        layer.name = template["name"]
        if "primary_visibility" in template:
            layer.layers = _translate_layer_configuration(template["primary_visibility"])
        if "accept_influence_of" in template:
            layer.layers_exclude = _translate_layer_configuration(template["accept_influence_of"], invert = True)
        if "enable_matte" in template:
            layer.layers_zmask = _translate_layer_configuration(template["enable_matte"])
        if "passes" in template:
            layer.use_pass_combined = False
            layer.use_pass_z = False
            for p in template["passes"]:
                setattr(layer, "use_pass_{}".format(p), True)
        if "dont" in template:
            for d in template["dont"]:
                setattr(layer, "use_{}".format(d), False)
        if "default" in template:
            layer.use = template["default"]
        if "samples" in template:
            layer.samples = template["samples"]

    render_layers.remove(old)

    core.log("Finished setting up render layers.")


def _translate_layer_configuration(layer_numbers:list, invert:bool = False):
    output = [False for i in range(20)]
    if not invert:
        for j in layer_numbers:
            output[j] = True
    else:
        output = [True for k in range(20)]
        for l in layer_numbers:
            output[l] = False
    return output
