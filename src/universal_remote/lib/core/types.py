class IRData:
    def __init__(
        self,
        address: int,
        command: int,
        protocol_name: str,
        ticks_diff: int,
    ):
        self.address = address
        self.command = command
        self.protocol = protocol_name
        self.ticks_diff = ticks_diff


class Device:
    def __init__(self, device):
        self.device_name: str = device["device_name"]
        self.protocol: str = device["protocol"]
        self.id: int = device["id"]
        self.address: int = device["address"]
        self.button1_press_command: int = device["button1_press_command"]
        # button2_press_command: int
        # button3_press_command: int
        # button4_press_command: int
        # button5_press_command: int
        self.button1_release_command: int = device["button1_release_command"]
        # button2_release_command: int
        # button3_release_command: int
        # button4_release_command: int
        # button5_release_command: int

    def to_dict(self):
        return {
            "device_name": self.device_name,
            "protocol": self.protocol,
            "id": self.id,
            "address": self.address,
            "button1_press_command": self.button1_press_command,
            "button1_release_command": self.button1_release_command,
        }

    def update(self, data: IRData):
        self.protocol = data.protocol
        self.address = data.address

    def set_press_command(self, command: int):
        self.button1_press_command = command

    def set_release_command(self, command: int):
        self.button1_release_command = command


class Buttons:
    MODE = "MODE"

    NAV_UP = "NAV_UP"
    NAV_DOWN = "NAV_DOWN"
    NAV_LEFT = "NAV_LEFT"
    NAV_RIGHT = "NAV_RIGHT"
    NAV_OK = "NAV_OK"

    VOL_UP = "VOL_UP"
    VOL_DOWN = "VOL_DOWN"

    CH_UP = "CH_UP"
    CH_DOWN = "CH_DOWN"


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


class PowerState:
    ACTIVE = 0
    IDLE = 1
    DEEP_SLEEP = 2
