import json
from universal_remote.lib.core.types import AppState, Device


class Storage:
    def __init__(
        self, state_path: str, devices_path: str, default_state: str = AppState.NORMAL
    ) -> None:
        """Initialise persistent storage"""
        self.state_path = state_path
        self.devices_path = devices_path
        self.default_state = default_state

    def save_state(self, state: str) -> None:
        """Save the state provided in non-voltile memory"""
        self._validate_state(state)

        with open(self.state_path, "w") as file:
            json.dump(state, file)

    def load_state(self) -> str:
        """Load the state from non-voltile memory"""
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

    def save_devices(self, devices: list[dict]) -> None:
        """Save the devices provided in non-voltile memory"""
        valid_devices = self._validate_devices(devices)

        with open(self.devices_path, "w") as file:
            json.dump(valid_devices, file)

    def load_devices(self) -> list[dict]:
        """Load the devices from non-voltile memory"""
        try:
            with open(self.devices_path, "r") as file:
                devices: list[dict] = json.load(file)

            return self._validate_devices(devices)
        except (OSError, ValueError):
            return []

    def _validate_devices(self, devices: list[dict]) -> list[dict]:
        """Validate each device in a list, remove items that are not devices"""
        valid_devices = []

        for device in devices:
            try:
                Device(**device)
                valid_devices.append(device)
            except (TypeError, ValueError):
                continue

        return valid_devices
