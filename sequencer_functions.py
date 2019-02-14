##############################################################################
# Imports
##############################################################################


import bpy, math
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def autorename_shots(context = None):
    """Auto-rename all shots and their associated cameras"""

    for index, shot in enumerate(context.scene.milkshake_shots):
        shot.code = f"SH{index + 1 :02}"
        shot.camera.name = f"{shot.code}.CAMX.000"
        for obj in bpy.data.objects:
            if obj.data == shot.camera:
                obj.name = shot.camera.name
                break
        core.log(f"Renamed shot {shot.code} and camera {shot.camera.name}.")


def camera_collection(context = None):
    """Return the scene's camera collection"""

    if not "Cameras" in bpy.data.collections.keys():
        camera_collection = bpy.data.collections.new("Cameras")
    else:
        camera_collection = bpy.data.collections['Cameras']
    if not "Cameras" in context.scene.collection.children:
        context.scene.collection.children.link(camera_collection)
    return camera_collection


def delete_shot(context = None, index = None):
    """Delete the selected shot and the associated camera"""

    shot = context.scene.milkshake_shots[index]
    if shot.camera:
        bpy.data.cameras.remove(shot.camera)
    context.scene.milkshake_shots.remove(index)


def clear_shots(context = None):
    """Clear the shot list and delete the associated cameras"""

    for shot in context.scene.milkshake_shots:
        bpy.data.cameras.remove(shot.camera)
    context.scene.milkshake_shots.clear()


def new_shot(context = None):
    """Create a new shot and camera"""

    shot = context.scene.milkshake_shots.add()
    camera = bpy.data.cameras.new("Camera")
    camera.cycles.aperture_blades = 5
    camera.cycles.aperture_fstop = 4
    camera.cycles.aperture_ratio = 2
    camera.cycles.aperture_rotation = math.radians(10)
    camera.cycles.aperture_type = 'FSTOP'
    camera.display_size = 0.1
    camera.dof_distance = 1
    camera.gpu_dof.blades = 5
    camera.gpu_dof.fstop = 4
    camera.lens = 35
    camera.passepartout_alpha = 0.85
    camera.sensor_fit = 'HORIZONTAL'
    camera.sensor_height = 13.365
    camera.sensor_width = 23.76
    camera_object = bpy.data.objects.new("Camera", camera)

    cam_collection = camera_collection(context)
    cam_collection.objects.link(camera_object)
    shot.camera = camera
    core.log("Created new shot and camera.")


def sync_timeline(context = None):
    """Sync Blender's timeline and markers with the shot list"""

    context.scene.timeline_markers.clear()
    new_start_frame = 1001
    for shot in context.scene.milkshake_shots:
        marker = context.scene.timeline_markers.new(shot.code, frame = new_start_frame)
        for obj in context.scene.objects:
            if obj.data == shot.camera:
                marker.camera = obj
                core.log(f"Synced shot {shot.code}")
                break
        new_start_frame += shot.duration
    context.scene.frame_start = 1001
    context.scene.frame_end = new_start_frame - 1
