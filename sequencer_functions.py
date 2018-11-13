##############################################################################
# Imports
##############################################################################


import bpy
from . import core_functions as core


##############################################################################
# Functions
##############################################################################


def new_shot(context):
    """Creates a new shot and camera"""

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
    core.log(message = "Created new shot and camera.")


def delete_shot(context, index):
    """Deletes the selected shot and the associated camera."""

    shot = context.scene.milkshake_shots[index]
    camera = shot.camera
    bpy.data.cameras.remove(camera) # crashes
    context.scene.milkshake_shots.remove(index)


def sync_timeline(context):
    """Syncs the list of shots to the Blender timeline, including markers"""

    context.scene.timeline_markers.clear()
    start_frame = 0
    for s in context.scene.milkshake_shots:
        marker = context.scene.timeline_markers.new(s.code, frame = start_frame)
        for o in context.scene.objects:
            if o.data == s.camera:
                marker.camera = o
                core.log(message = "Synced shot {}".format(s.code))
                break
        start_frame += s.duration
    context.scene.frame_start = 1001
    context.scene.frame_end = start_frame - 1


def autorename_shots(context):
    """Auto renames all shots and their associated cameras"""

    for index, shot in enumerate(context.scene.milkshake_shots):
        shot.code = "SH" + "{0:02d}".format(index + 1)
        shot.camera.name = "{}.CAMX.000".format(shot.code)
        for i in bpy.data.objects:
            if i.data == shot.camera:
                i.name = shot.camera.name
                break
        core.log(message = "Renamed shot {} and camera {}".format(shot.code, shot.camera.name))
