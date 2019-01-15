##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def autorename_shots(context):
    """Auto-rename all shots and their associated cameras"""

    for index, shot in enumerate(context.scene.milkshake_shots):
        shot.code = f"SH{index + 1 :02}"
        shot.camera.name = f"{shot.code}.CAMX.000"
        for obj in bpy.data.objects:
            if obj.data == shot.camera:
                obj.name = shot.camera.name
                break
        core.log(f"Renamed shot {shot.code} and camera {shot.camera.name}.")


def camera_collection(context):
    """Return the scene's camera collection"""

    if not "Cameras" in bpy.data.collections.keys():
        camera_collection = bpy.data.collections.new("Cameras")
    else:
        camera_collection = bpy.data.collections["Cameras"]
    try:
        context.scene.collection.children.link(camera_collection)
    except:
        pass
    return camera_collection


def delete_shot(context, index):
    """Delete the selected shot and the associated camera"""

    shot = context.scene.milkshake_shots[index]
    camera = shot.camera
    if camera:
        bpy.data.cameras.remove(camera) # crashes on Linux
    context.scene.milkshake_shots.remove(index)


def new_shot(context):
    """Create a new shot and camera"""

    shot = context.scene.milkshake_shots.add()
    camera = bpy.data.cameras.new("Camera")
    camera.show_passepartout = True
    camera.passepartout_alpha = 1
    camera_object = bpy.data.objects.new("Camera", camera)

    cam_collection = camera_collection(context)
    cam_collection.objects.link(camera_object)
    shot.camera = camera
    core.log("Created new shot and camera.")


def sync_timeline(context):
    """Sync Blender's timeline and markers with the shot list"""

    context.scene.timeline_markers.clear()
    new_start_frame = 1001
    for shot in context.scene.milkshake_shots:
        marker = context.scene.timeline_markers.new(shot.code, frame = new_start_frame)
        for obj in context.scene.objects:
            if obj.data == shot.camera:
                marker.camera = obj
                core.log("Synced shot {}".format(shot.code))
                break
        new_start_frame += shot.duration
    context.scene.frame_start = 1001
    context.scene.frame_end = new_start_frame - 1
