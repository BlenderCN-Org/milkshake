################################################################################
# Imports
################################################################################


import bpy


##############################################################################
# Functions
##############################################################################


def log(msg):
    """Output the given message to the console"""

    print(f"[Milkshake] {msg}")


def get_bounding_box_limits(mesh):
    """Extract only useful information from the given mesh's bounding box"""
    return {
        "x_min": mesh.bound_box[0][0],
        "y_min": mesh.bound_box[0][1],
        "z_min": mesh.bound_box[0][2],
        "x_max": mesh.bound_box[6][0],
        "y_max": mesh.bound_box[6][1],
        "z_max": mesh.bound_box[6][2]
    }
