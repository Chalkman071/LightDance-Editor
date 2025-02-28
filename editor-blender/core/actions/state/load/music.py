import os
from typing import Any, cast

import bpy

from ....config import config
from ....states import state


def setup_music():
    """
    set music
    """
    if not bpy.context:
        return
    scene = bpy.context.scene
    if not scene.sequence_editor:
        scene.sequence_editor_create()
    music_filepath = os.path.normpath(
        config.ASSET_PATH + state.init_temps.assets_load["Music"]
    )
    if scene.sequence_editor.sequences:
        sequence = cast(bpy.types.SoundSequence, scene.sequence_editor.sequences[0])
        scene.sequence_editor.sequences.remove(sequence)

    strip = scene.sequence_editor.sequences.new_sound(
        "music", filepath=music_filepath, channel=1, frame_start=0
    )

    bpy.context.scene.lock_frame_selection_to_range = True

    # set retiming
    duration = strip.frame_duration
    state.partial_load_frames = (0, duration)

    strip.select = True
    bpy.context.scene.sequence_editor.active_strip = strip

    bpy.ops.sequencer.retiming_reset()
    bpy.ops.sequencer.retiming_key_add()
    bpy.ops.sequencer.retiming_key_add(timeline_frame=duration)
    bpy.ops.sequencer.retiming_segment_speed_set()

    bpy.context.window_manager["ld_play_speed"] = 1.0
