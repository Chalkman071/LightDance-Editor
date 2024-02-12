from . import animation, keymap, name_tag, objects, waveform


def mount_handlers():
    animation.mount()
    objects.mount()
    waveform.mount()
    name_tag.mount()
    keymap.mount()


def unmount_handlers():
    animation.unmount()
    objects.unmount()
    waveform.unmount()
    name_tag.unmount()
    keymap.unmount()
