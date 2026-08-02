import json


class Device:
    device_name: str
    address: int
    button1_command: int
    # button2_command: int
    # button3_command: int
    # button4_command: int
    # button5_command: int
    button_release: int


class Storage:
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, data: list[Device]):
        with open(self.filename, "w") as f:
            json.dump(data, f)

    def load(self) -> list[Device]:
        try:
            with open(self.filename, "r") as f:
                return json.load(f)

        except FileNotFoundError:
            return []
