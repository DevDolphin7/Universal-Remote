import json


class Device:
    def __init__(self, device):
        self.device_name: str = device["device_name"]
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


class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.data = []

    def save(self, data: list[Device]) -> None:
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def load(self) -> list[Device]:
        with open(self.filename, "r") as f:
            self.data = [Device(device) for device in json.load(f)]
        return self.data

    def get_device_names(self) -> list[str]:
        return [device.device_name for device in self.data]


memory = Storage("lib/storage/remotes.json")
