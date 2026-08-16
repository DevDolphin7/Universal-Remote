class ProgrammableButtons:
    NAV_UP = "NAV_UP"
    NAV_DOWN = "NAV_DOWN"
    NAV_LEFT = "NAV_LEFT"
    NAV_RIGHT = "NAV_RIGHT"
    NAV_OK = "NAV_OK"

    VOL_UP = "VOL_UP"
    VOL_DOWN = "VOL_DOWN"

    CH_UP = "CH_UP"
    CH_DOWN = "CH_DOWN"


class AllButtons(ProgrammableButtons):
    MODE = "MODE"


class Commands:
    def __init__(self, press: int | None = None, release: int | None = None):
        self.press = press
        self.release = release


class Device:
    def __init__(
        self,
        id: int,
        device_name: str,
        protocol_name: str,
        address: int,
        commands: dict[ProgrammableButtons, Commands],
    ):
        self.id = id
        self.device_name = device_name
        self.protocol_name = protocol_name
        self.address = address
        self.commands = commands


class Events:
    BUTTON_PRESSED = "BUTTON_PRESS"
    BUTTON_RELEASED = "BUTTON_RELEASE"
    BUTTON_LEARNED = "BUTTON_LEARNED"
    DEVICE_CHANGED = "DEVICE_CHANGED"
    IR_PROTOCOL_CHANGED = "IR_PROTOCOL_CHANGED"
    IR_RECEIVED = "IR_RECEIVED"
    IR_TRANSMITTED = "IR_TRANSMITTED"
    LOW_BATTERY = "LOW_BATTERY"
    SLEEP_IDLE = "SLEEP_IDLE"
    SLEEP_DEEP = "SLEEP_DEEP"
    WAKE = "WAKE"


class IRData:
    def __init__(self, address: int, command: int, protocol_name: str, ticks_diff: int):
        self.address = address
        self.command = command
        self.protocol_name = protocol_name
        self.ticks_diff = ticks_diff


class PowerState:
    ACTIVE = 0
    IDLE = 1
    DEEP_SLEEP = 2


class AppState:
    NORMAL = "NORMAL"
    LEARNING = "LEARNING"
