################################################################################
#
# sequencer_functions.py
#
################################################################################


import bpy


def sync_timeline(context:bpy.types.Context):
    """Syncs the list of shots to the Blender timeline, including markers."""

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


def new_shot(context:bpy.types.Context):
    """"""

    context.scene.milkshake_shots.add()


def delete_shot(context:bpy.types.Context, index:bpy.props.IntProperty):
    """"""

    context.scene.milkshake_shots.remove(index)
