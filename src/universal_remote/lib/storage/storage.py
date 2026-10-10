import json
from universal_remote.lib.core.types import AppState, Device, Commands


class Storage:
    def __init__(
        self, state_path: str, devices_path: str, default_state: str = AppState.NORMAL
    ) -> None:
        """Initialise persistent storage"""
        self.state_path = state_path
        self.devices_path = devices_path
        self.default_state = default_state

    def save_state(self, state: str) -> None:
        """Save the state provided in non-volatile memory"""
        self._validate_state(state)

        with open(self.state_path, "w") as file:
            json.dump(state, file)

    def load_state(self) -> str:
        """Load the state from non-volatile memory"""
        try:
            with open(self.state_path, "r") as file:
                state: str = json.load(file)

            self._validate_state(state)
        except (OSError, ValueError):
            return self.default_state

        return state

    def _validate_state(self, state) -> None:
        if state not in AppState.ALL:
            raise ValueError("Invalid state")

    def save_devices(self, devices: list[Device]) -> None:
        """Save the devices provided in non-volatile memory"""
        with open(self.devices_path, "w") as file:
            json.dump(self._devices_to_dict(devices), file)

    def load_devices(self) -> list[Device]:
        """Load the devices from non-volatile memory"""
        try:
            with open(self.devices_path, "r") as file:
                devices: list[dict] = json.load(file)

            return self._validate_devices(devices)
        except (OSError, ValueError):
            return []

    def _devices_to_dict(self, devices: list[Device]) -> list[dict]:
        """Convert devices to a list of dictionaries"""
        remote_dicts = []

        for device in devices:
            commands_dict = {}
            for key, command in device.commands.items():
                commands_dict[key] = {
                    "press": command.press,
                    "release": command.release,
                }

            remote_dicts.append(
                {
                    "id": device.id,
                    "name": device.name,
                    "protocol_name": device.protocol_name,
                    "address": device.address,
                    "commands": commands_dict,
                }
            )

        return remote_dicts

    def _validate_devices(self, devices: list[dict]) -> list[Device]:
        """Validate each device in a list, remove items that are not devices"""
        valid_devices = []

        for device in devices:
            try:
                commands = {}
                for key, command_dict in device["commands"].items():
                    try:
                        commands[key] = Commands(
                            press=command_dict["press"], release=command_dict["release"]
                        )
                    except KeyError:
                        commands[key] = Commands(press=command_dict["press"])

                valid_devices.append(
                    Device(
                        device["id"],
                        device["name"],
                        device["protocol_name"],
                        device["address"],
                        commands,
                    )
                )
            except (TypeError, KeyError, ValueError):
                continue

        return valid_devices
