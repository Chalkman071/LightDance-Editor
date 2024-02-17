from enum import Enum
from typing import Literal, Tuple


class LoginPanelStatusType:
    username: str
    password: str


class ColorPaletteStatusType:
    edit_index: int
    edit_mode: str


class ColorPaletteEditModeType(Enum):
    IDLE = "idle"
    EDIT = "edit"
    NEW = "new"


class ControlEditorStatusType:
    multi_select: bool
    multi_select_color: str
    multi_select_alpha: int

    show_fiber: bool
    show_led: bool
    show_all: bool


class PosEditorStatusType:
    multi_select: bool
    multi_select_delta_transform: Tuple[float, float, float]
    multi_select_delta_transform_ref: Tuple[float, float, float]


class LEDEditorEditModeType(Enum):
    IDLE = "idle"
    EDIT = "edit"
    NEW = "new"


class LEDEditorStatusType:
    edit_mode: str
    edit_model: str
    edit_dancer: str
    edit_part: str
    edit_effect: str
    new_effect: str

    multi_select: bool
    multi_select_color: str
    multi_select_alpha: int


class CommandCenterStatusType:
    color: Literal["red", "green", "blue", "yellow", "magenta", "cyan"]
    command: str
    connected: bool
    countdown: int


class CommandCenterRPiStatusType:
    name: str
    IP: str
    MAC: str
    connected: bool
    message: str
    statusCode: int
    interface_type: Literal["ethernet", "wifi"]
    selected: bool


class TimeShiftStatusType:
    frame_type: str
    start: int
    end: int
    displacement: int
