################################################################################
#
# sequencer_functions.py
#
################################################################################


import bpy


def new_shot(context:bpy.types.Context):
    """Creates a new shot and camera"""

    shot = context.scene.milkshake_shots.add()
    camera = bpy.data.cameras.new("Camera")
    camera_object = bpy.data.objects.new("Camera", camera)
    context.scene.objects.link(camera_object)
    shot.camera = camera


def sync_timeline(context:bpy.types.Context):
    """Syncs the list of shots to the Blender timeline, including markers"""

    context.scene.timeline_markers.clear()
    start_frame = 0
    for s in context.scene.milkshake_shots:
        marker = context.scene.timeline_markers.new(s.code[-6:], frame = start_frame)
        for o in context.scene.objects:
            if o.data == s.camera:
                marker.camera = o
                break
        start_frame += s.duration
    context.scene.frame_start = 0
    context.scene.frame_end = start_frame - 1


def autorename_shots(context:bpy.types.Context):
    """Auto renames all shots and their associated cameras"""

    for index, shot in enumerate(context.scene.milkshake_shots):
        shot.code = "SH" + "{0:02d}".format(index + 1)
        shot.camera.name = "{}.CAMX.000".format(shot.code)
        for i in bpy.data.objects:
            if i.data == shot.camera:
                i.name = shot.camera.name
                break
        print("[Milkshake] Renamed shot {} and camera {}".format(shot.code, shot.camera.name))
