##############################################################################
# Imports
##############################################################################


import bpy, glob, os, math
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def generate_contact_sheet(context, directory, columns, frame_width, frame_height):

    # Get image list and determine row count
    images = sorted(glob.glob(os.path.join(directory, "*.jpg")))
    image_count = len(images)

    if image_count < 2:
        raise MilkshakeError(f"{directory} contains less than two images.")

    else:
        rows = math.ceil(image_count / columns)

        # Enable compositing nodes
        bpy.context.scene.use_nodes = True
        bpy.context.scene.render.use_compositing = True
        compositor = bpy.context.scene.node_tree
        compositor.nodes.clear()

        # Dimensions
        bpy.context.scene.render.resolution_x = columns * frame_width
        bpy.context.scene.render.resolution_y = rows * frame_height

        # Output node
        output_node = compositor.nodes.new(type = 'CompositorNodeComposite')
        output_node.label = "Contact Sheet"
        output_node.location = ((columns + 1) * 300, 0)

        # Image nodes

        column = 0
        row = 0
        last_merge_node = None
        last_translate_node = None

        for num, filename in enumerate(images):

            # Image node
            image_node = compositor.nodes.new(type = 'CompositorNodeImage')
            image_node.image = bpy.data.images.load(filename, check_existing = True)
            image_node.location = (column * 300, row * -50)
            image_node.hide = True
            image_node.label = os.path.basename(filename).split(".")[0]

            # Translate node
            translate_node = compositor.nodes.new(type = 'CompositorNodeTransform')
            translate_node.location = (column * 300 + 150, row * -50)
            translate_node.hide = True
            translate_node.filter_type = 'BICUBIC'

            # Link image to transform
            compositor.links.new(image_node.outputs[0], translate_node.inputs[0])

            # Horizontal translation
            column_zero_translation = -1 * (1 + math.floor(columns / 2)) * (frame_width / 2)
            translate_node.inputs[1].default_value = column_zero_translation + column * frame_width

            # Vertical translation
            row_zero_translation = (1 + math.floor(rows / 2)) * (frame_height / 2)
            translate_node.inputs[2].default_value = row_zero_translation - row * frame_height

            core.log(f"Column zero translation: {column_zero_translation}")
            core.log(f"Row zero translation: {row_zero_translation}")

            if num > 0:

                # Merge node
                merge_node = compositor.nodes.new(type = 'CompositorNodeAlphaOver')
                merge_node.location = (columns * 300 + 50, (num - 1) * -50)
                merge_node.hide = True
                merge_node.label = "Merge"

                if num == 1:
                    compositor.links.new(last_translate_node.outputs[0], merge_node.inputs[1])
                else:
                    compositor.links.new(last_merge_node.outputs[0], merge_node.inputs[1])

                compositor.links.new(translate_node.outputs[0], merge_node.inputs[2])
                last_merge_node = merge_node

            last_translate_node = translate_node

            # The last merge needs to go into the composite node
            if num == image_count - 1:
                compositor.links.new(merge_node.outputs[0], output_node.inputs[0])

            if column < columns - 1:
                column += 1
            else:
                column = 0
                row += 1


def generate_credits_roll(context, image_filepath, speed, frame_width, frame_height):

    # Enable compositing nodes
    bpy.context.scene.use_nodes = True
    bpy.context.scene.render.use_compositing = True
    compositor = bpy.context.scene.node_tree
    compositor.nodes.clear()

    # Output node
    output_node = compositor.nodes.new(type = 'CompositorNodeComposite')
    output_node.label = "Credits Roll"
    output_node.location = (0, 0)

    # Transform node
    xform_node = compositor.nodes.new(type = 'CompositorNodeTransform')
    xform_node.location = (-200, 0)
    xform_node.filter_type = 'NEAREST'

    # Image node
    img_node = compositor.nodes.new(type = 'CompositorNodeImage')
    img_node.location = (-400, 0)
    img_node.image = bpy.data.images.load(image_filepath, check_existing = True)
    img_node.image.colorspace_settings.name = 'Input - Generic - sRGB - Texture'

    # Create links
    compositor.links.new(img_node.outputs[0], xform_node.inputs[0])
    compositor.links.new(xform_node.outputs[0], output_node.inputs[0])

    # Set frame dimensions
    context.scene.render.resolution_x = frame_width
    context.scene.render.resolution_y = frame_height

    # Calculate translation extrema of the credits image
    boundary = math.floor(frame_height / 2 + img_node.image.size[1] / 2)

    # Transform node Y input
    y_translate = xform_node.inputs[2]

    # Set first keyframe (1001) to the negative boundary
    y_translate.default_value = -boundary
    y_translate.keyframe_insert('default_value', frame = 1001)

    # Since we know neither the pixels-per-frame nor the duration
    # of the sequence, we have to count the number of frames that
    # that will be necessary to reach the positive boundary.
    end_frame = 1001
    end_value = -boundary
    while end_value < boundary:
        end_value += speed
        end_frame += 1

    # Set the second keyframe
    y_translate.default_value = end_value
    y_translate.keyframe_insert('default_value', frame = end_frame)
    context.scene.frame_end = end_frame

    # Interpolation needs to be linear
    context.scene.node_tree.animation_data.action.fcurves[0].keyframe_points[0].interpolation = 'LINEAR'

    core.log(f"Created {end_frame - 1000} frames ({(end_frame - 1000) / 24} seconds) of ending credits roll.")
