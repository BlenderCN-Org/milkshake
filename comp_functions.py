##############################################################################
# Imports
##############################################################################


import bpy, glob, os, math
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def generate_contact_sheet(context, directory):

    # Input folder (make sure there's PNGs in there)
    columns = 4
    image_width = 2048
    image_height = 858

    # Get image list and determine row count
    images = sorted(glob.glob(os.path.join(directory, "*.png")))
    image_count = len(images)

    if image_count < 2:
        return False

    else:
        rows = math.ceil(image_count / columns)

        # Enable compositing nodes
        bpy.context.scene.use_nodes = True
        bpy.context.scene.render.use_compositing = True
        compositor = bpy.context.scene.node_tree

        # Dimensions
        bpy.context.scene.render.resolution_x = columns * image_width
        bpy.context.scene.render.resolution_y = rows * image_height

        # Output node
        output_node = compositor.nodes.new(type = 'CompositorNodeComposite')
        output_node.label = "Contact Sheet"
        output_node.location = ((columns + 1) * 250, 0)

        # Render layers node
        tx_node = compositor.nodes.new(type = 'CompositorNodeTexture')
        tx_node.hide = True

        # Image nodes

        column = 0
        row = 0
        last_merge_node = None
        last_translate_node = None

        for num, filename in enumerate(images):

            # Image node
            image_node = compositor.nodes.new(type = 'CompositorNodeImage')
            image_node.image = bpy.data.images.load(filename, check_existing = True)
            image_node.location = (column * 250, row * -50)
            image_node.hide = True
            image_node.label = os.path.basename(filename).split(".")[0]

            # Translate node
            translate_node = compositor.nodes.new(type = 'CompositorNodeTransform')
            translate_node.location = (column * 250 + 100, row * -50)
            translate_node.hide = True
            translate_node.filter_type = 'BICUBIC'

            # Link image to transform
            compositor.links.new(image_node.outputs[0], translate_node.inputs[0])

            # Horizontal translation
            column_zero_translation = -1 * (1 + round(columns / 2)) * (image_width / 2)
            translate_node.inputs[1].default_value = column_zero_translation + column * image_width

            # Vertical translation
            row_zero_translation = (1 + math.floor(rows / 2)) * (image_height / 2)
            translate_node.inputs[2].default_value = row_zero_translation - row * image_height

            if num > 0:

                # Merge node
                merge_node = compositor.nodes.new(type = 'CompositorNodeAlphaOver')
                merge_node.location = (columns * 250 + 50, (num - 1) * -50)
                merge_node.hide = True
                merge_node.label = "Merge"

                if num == 1:
                    # First make another merge
                    merge_node_2 = compositor.nodes.new(type = 'CompositorNodeAlphaOver')
                    merge_node.hide = True
                    # Then link the texture and the first merge to the second one
                    compositor.links.new(tx_node.outputs[1], merge_node_2.inputs[1])
                    compositor.links.new(merge_node.outputs[0], merge_node_2.inputs[2])
                    # Then link the first images to the first merge
                    compositor.links.new(last_translate_node.outputs[0], merge_node.inputs[1])
                    compositor.links.new(translate_node.outputs[0], merge_node.inputs[2])
                    last_merge_node = merge_node_2

                else:
                    # Then always take the last merge
                    compositor.links.new(last_merge_node.outputs[0], merge_node.inputs[1])
                    compositor.links.new(translate_node.outputs[0], merge_node.inputs[2])
                    last_merge_node = merge_node

            # The last merge needs to go into the composite node
            if num == image_count - 1:
                compositor.links.new(merge_node.outputs[0], output_node.inputs[0])

            last_translate_node = translate_node

            if column < columns - 1:
                column += 1
            else:
                column = 0
                row += 1

        return True
