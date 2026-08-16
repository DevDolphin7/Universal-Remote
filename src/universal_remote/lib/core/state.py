from universal_remote.lib.core.types import AppState, Events


class State:
    def __init__(self, event_bus) -> None:
        self._mode = AppState.NORMAL
        self._bus = event_bus

    def get(self) -> str:
        """Get the current mode"""
        return self._mode

    def set(self, state: str) -> None:
        """Change the mode to a valid AppState"""
        if self._mode == state:
            return

        if state not in AppState.ALL:
            raise ValueError("Invalid state provided")

        self._mode = state
        self._bus.publish(Events.STATE_CHANGED, state)

    def to_dict(self) -> dict[str, str]:
        """Convert the State to a dictionary."""
        return {"mode": self._mode}

    def from_dict(self, data: dict[str, str]) -> dict[str, str]:
        """Load the State from a valid dictionary, requires a key 'mode'. Returns"""
        try:
            self.set(data["mode"])
        except KeyError:
            raise KeyError("Dictionary provided missing key 'mode'")
        return {"mode": data["mode"]}
