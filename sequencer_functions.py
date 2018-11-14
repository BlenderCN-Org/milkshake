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
        shot.code = "SH" + f"{index + 1 :02}"
        shot.camera.name = f"{shot.code}.CAMX.000"
        for obj in bpy.data.objects:
            if obj.data == shot.camera:
                obj.name = shot.camera.name
                break
        core.log(f"Renamed shot {shot.code} and camera {shot.camera.name}")


def delete_shot(context, index):
    """Delete the selected shot and the associated camera"""

    shot = context.scene.milkshake_shots[index]
    camera = shot.camera
    bpy.data.cameras.remove(camera) # crashes
    context.scene.milkshake_shots.remove(index)


def new_shot(context):
    """Create a new shot and camera"""

    shot = context.scene.milkshake_shots.add()
    camera = bpy.data.cameras.new("Camera")
    camera_object = bpy.data.objects.new("Camera", camera)

    sc = context.scene.collection.children
    collections = bpy.data.collections
    if not "Cameras" in bpy.data.collections.keys():
        camera_collection = collections.new("Cameras")
    else:
        camera_collection = bpy.data.collections["Cameras"]
    try:
        sc.link(camera_collection)
    except:
        pass
    camera_collection.objects.link(camera_object)
    shot.camera = camera
    core.log("Created new shot and camera.")


def sync_timeline(context):
    """Sync Blender's timeline and markers with the shot list"""

    context.scene.timeline_markers.clear()
    start_frame = 0
    for shot in context.scene.milkshake_shots:
        marker = context.scene.timeline_markers.new(shot.code, frame = start_frame)
        for obj in context.scene.objects:
            if obj.data == shot.camera:
                marker.camera = obj
                core.log(f"Synced shot {shot.code}")
                break
        start_frame += shot.duration
    context.scene.frame_start = 1001
    context.scene.frame_end = start_frame - 1
