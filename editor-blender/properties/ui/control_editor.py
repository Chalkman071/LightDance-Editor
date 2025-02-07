from typing import cast

import bpy

from ...core.actions.property.control_editor import (
    update_multi_select_alpha,
    update_multi_select_color,
    update_multi_select_effect,
)
from ...core.states import state
from ...icons import icon_collections
from ..types import ColorPaletteItemType, LightType, ObjectType


def get_effect_lists(
    self: bpy.types.PropertyGroup, context: bpy.types.Context | None
) -> list[tuple[str, str, str, str, int] | tuple[str, str, str]]:
    possible_effects: set[str] = set()

    data_objects = cast(dict[str, bpy.types.Object], bpy.data.objects)
    for obj_name in state.selected_obj_names:
        obj = data_objects[obj_name]
        ld_object_type: str = getattr(obj, "ld_object_type")
        if ld_object_type != ObjectType.LIGHT.value:
            continue

        ld_light_type: str = getattr(obj, "ld_light_type")
        if ld_light_type != LightType.LED.value:
            continue

        ld_model_name: str = getattr(obj, "ld_model_name")
        ld_part_name: str = getattr(obj, "ld_part_name")

        if len(possible_effects) == 0:
            possible_effects.update(state.led_map[ld_model_name][ld_part_name])
        else:
            possible_effects = possible_effects.intersection(
                state.led_map[ld_model_name][ld_part_name]
            )

    effect_list: list[str] = list(possible_effects)
    effect_list.sort()

    # NOTE: Don't show [bulb Color] here
    effect_list = ["no-change"] + effect_list

    return [(effect, effect, "", "", index) for index, effect in enumerate(effect_list)]


def get_color_lists(
    self: bpy.types.PropertyGroup, context: bpy.types.Context | None
) -> list[tuple[str, str, str, str, int] | tuple[str, str, str]]:
    collection = icon_collections["main"]

    if not bpy.context:
        return []
    ld_color_palette: list[ColorPaletteItemType] = getattr(
        bpy.context.window_manager, "ld_color_palette"
    )
    color_list = [
        (
            color.color_name,
            color.color_name,
            "",
            collection[color.color_name].icon_id,  # type: ignore
            color.color_id,
        )
        for color in ld_color_palette
    ]
    if not all(
        [
            getattr(bpy.data.objects[obj_name], "ld_object_type")
            != ObjectType.LIGHT.value
            for obj_name in state.selected_obj_names
        ]
    ):
        color_list.insert(0, ("[gradient]", "[gradient]", "", "MOD_ARRAY", -1))

    return color_list  # pyright: ignore


def get_show_fiber(self: bpy.types.PropertyGroup) -> bool:
    return self["show_fiber"]


def set_show_fiber(self: bpy.types.PropertyGroup, value: bool) -> None:
    if value:
        self["show_fiber"] = value
        self["show_led"] = False
        self["show_all"] = False


def get_show_led(self: bpy.types.PropertyGroup) -> bool:
    return self["show_led"]


def set_show_led(self: bpy.types.PropertyGroup, value: bool) -> None:
    if value:
        self["show_fiber"] = False
        self["show_led"] = value
        self["show_all"] = False


def get_show_all(self: bpy.types.PropertyGroup) -> bool:
    return self["show_all"]


def set_show_all(self: bpy.types.PropertyGroup, value: bool) -> None:
    if value:
        self["show_fiber"] = False
        self["show_led"] = False
        self["show_all"] = value


class ControlEditorStatus(bpy.types.PropertyGroup):
    """Status of the Control Editor"""

    multi_select: bpy.props.BoolProperty(  # type: ignore
        name="Multi Select",
        description="Multi select",
        default=False,
    )
    multi_select_color: bpy.props.EnumProperty(  # type: ignore
        name="Multi Select Color",
        description="Color of multi select",
        items=get_color_lists,
        default=0,  # type: ignore
        update=update_multi_select_color,
    )
    multi_select_effect: bpy.props.EnumProperty(  # type: ignore
        name="Multi Select Effect",
        description="Effect of multi select",
        items=get_effect_lists,
        default=0,  # type: ignore
        update=update_multi_select_effect,
    )
    multi_select_alpha: bpy.props.IntProperty(  # type: ignore
        name="Multi Select Alpha",
        description="Alpha of multi select",
        min=1,
        max=255,
        update=update_multi_select_alpha,
    )

    show_fiber: bpy.props.BoolProperty(  # type: ignore
        name="Show Fiber",
        description="Show Fiber",
        get=get_show_fiber,
        set=set_show_fiber,
    )
    show_led: bpy.props.BoolProperty(  # type: ignore
        name="Show LED",
        description="Show LED",
        get=get_show_led,
        set=set_show_led,
    )
    show_all: bpy.props.BoolProperty(  # type: ignore
        name="Show All",
        description="Show All",
        get=get_show_all,
        set=set_show_all,
    )


def register():
    bpy.utils.register_class(ControlEditorStatus)
    setattr(
        bpy.types.WindowManager,
        "ld_ui_control_editor",
        bpy.props.PointerProperty(type=ControlEditorStatus),
    )


def unregister():
    bpy.utils.unregister_class(ControlEditorStatus)
    delattr(bpy.types.WindowManager, "ld_ui_control_editor")
