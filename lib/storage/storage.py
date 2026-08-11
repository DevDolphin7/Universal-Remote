import json
from lib.core.types import Device


class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.devices = []

    def save_devices(self, devices: list[Device]) -> None:
        with open(self.filename, "w") as f:
            json.dump([device.to_dict() for device in devices], f)

    def load_devices(self) -> list[Device]:
        with open(self.filename, "r") as f:
            self.devices = [Device(device) for device in json.load(f)]
        return self.devices
