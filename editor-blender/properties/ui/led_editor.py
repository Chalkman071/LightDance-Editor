from typing import List, Tuple

import bpy

from ...core.actions.property.led_editor import (
    update_edit_dancer,
    update_edit_part,
    update_multi_select_color,
)
from ...core.models import PartType
from ...core.states import state
from ..types import ColorPaletteItemType
from .types import LEDEditorEditModeType


def get_dancer_lists(
    self: bpy.types.PropertyGroup, context: bpy.types.Context
) -> List[Tuple[str, str, str, str, int] | Tuple[str, str, str]]:
    dancer_list = []
    # dancer_list.append(("none", "none", "", "", -1))

    for index, dancer_name in enumerate(state.dancer_names):
        if bpy.data.objects.get(dancer_name) is not None:
            dancer_list.append((dancer_name, dancer_name, "", "OBJECT_DATA", index))

    return dancer_list  # pyright: ignore


def get_edit_dancer(self: bpy.types.PropertyGroup) -> int:
    return self["edit_dancer"]


def set_edit_dancer(self: bpy.types.PropertyGroup, value: int):
    if self["edit_dancer"] != value:
        self["edit_dancer"] = value
        self["edit_part"] = -1
        self["edit_effect"] = -1


def get_part_lists(
    self: bpy.types.PropertyGroup, context: bpy.types.Context
) -> List[Tuple[str, str, str, str, int] | Tuple[str, str, str]]:
    part_list = []
    # part_list.append(("none", "none", "", "", -1))

    dancer_name = getattr(self, "edit_dancer")

    if dancer_name == "":
        return part_list  # pyright: ignore

    dancer_parts = state.dancers[dancer_name]

    for index, part_name in enumerate(dancer_parts):
        part_type = state.part_type_map[part_name]
        if part_type != PartType.LED:
            continue

        part_list.append((part_name, part_name, "", "OBJECT_DATA", index))

    return part_list  # pyright: ignore


def get_edit_part(self: bpy.types.PropertyGroup) -> int:
    return self["edit_part"]


def set_edit_part(self: bpy.types.PropertyGroup, value: int):
    if self["edit_part"] != value:
        self["edit_part"] = value
        self["edit_effect"] = -1


def get_effect_lists(
    self: bpy.types.PropertyGroup, context: bpy.types.Context
) -> List[Tuple[str, str, str, str, int] | Tuple[str, str, str]]:
    effect_list = []

    dancer_name = getattr(self, "edit_dancer")
    part_name = getattr(self, "edit_part")

    if dancer_name == "" or part_name == "":
        return effect_list  # pyright: ignore

    effects = state.led_map[part_name]
    for effect_name, effect in effects.items():
        effect_list.append((effect_name, effect_name, "", "MATERIAL", effect.id))

    return effect_list  # pyright: ignore


def get_color_lists(
    self: bpy.types.PropertyGroup, context: bpy.types.Context
) -> List[Tuple[str, str, str, str, int] | Tuple[str, str, str]]:
    ld_color_palette: List[ColorPaletteItemType] = getattr(
        bpy.context.window_manager, "ld_color_palette"
    )
    color_list = [
        (color.color_name, color.color_name, "", "MATERIAL", color.color_id)
        for color in ld_color_palette
    ]

    return color_list  # pyright: ignore


class LEDEditorStatus(bpy.types.PropertyGroup):
    """Status of the PosEditor"""

    edit_mode: bpy.props.EnumProperty(  # type: ignore
        items=[
            (LEDEditorEditModeType.IDLE.value, "", ""),
            (LEDEditorEditModeType.EDIT.value, "", ""),
            (LEDEditorEditModeType.NEW.value, "", ""),
        ],
        default=LEDEditorEditModeType.IDLE.value,
    )
    edit_dancer: bpy.props.EnumProperty(  # type: ignore
        items=get_dancer_lists,
        default=-1,  # pyright: ignore
        update=update_edit_dancer,
        get=get_edit_dancer,
        set=set_edit_dancer,
    )
    edit_part: bpy.props.EnumProperty(  # type: ignore
        items=get_part_lists,
        default=-1,  # pyright: ignore
        update=update_edit_part,
        get=get_edit_part,
        set=set_edit_part,
    )
    edit_effect: bpy.props.EnumProperty(  # type: ignore
        items=get_effect_lists,
        default=-1,  # pyright: ignore
    )

    multi_select: bpy.props.BoolProperty(  # type: ignore
        name="Multi Select",
        description="Multi select",
        default=False,
    )
    multi_select_color: bpy.props.EnumProperty(  # type: ignore
        name="Multi Select Color",
        description="Color of multi select",
        items=get_color_lists,
        default=0,  # pyright: ignore
        update=update_multi_select_color,
    )
    multi_select_alpha: bpy.props.IntProperty(  # type: ignore
        name="Multi Select Alpha",
        description="Alpha of multi select",
        min=1,
        max=255,
        # update=update_multi_select_alpha,
    )


def register():
    bpy.utils.register_class(LEDEditorStatus)
    setattr(
        bpy.types.WindowManager,
        "ld_ui_led_editor",
        bpy.props.PointerProperty(type=LEDEditorStatus),
    )


def unregister():
    bpy.utils.unregister_class(LEDEditorStatus)
    delattr(bpy.types.WindowManager, "ld_ui_led_editor")