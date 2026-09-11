from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.core.types import Events, Device, AppState, AllButtons


class Remote:
    def __init__(
        self,
        event_bus: EventBus,
        remotes: list[Device],
        selected: int = 0,
        app_state: str = "NORMAL",
    ):
        self.event_bus = event_bus
        self.set_remotes(remotes)
        self.set_selected(selected)
        self._app_state = app_state

        self.event_bus.subscribe(Events.BUTTON_RELEASED, self.handle_button_released)
        self.event_bus.subscribe(Events.STATE_CHANGED, self.handle_state_change)
        self.event_bus.subscribe(Events.DEVICE_LEARNED, self.handle_device_learn)
        self.event_bus.subscribe(
            Events.IR_PROTOCOL_CHANGED, self.handle_ir_protocol_change
        )

    def get_active_remote(self) -> Device:
        return self._remotes[self._selected]

    def get_all_remotes(self) -> list[Device]:
        return self._remotes

    def get_all_remote_names(self) -> list[str]:
        return [remote.name for remote in self._remotes]

    def get_active_protocol(self) -> str:
        return self.get_active_remote().protocol_name

    def set_remotes(self, remotes: list[Device]):
        self._remotes = list(remotes)

    def set_selected(self, selected: int):
        self._selected = selected

    def increment_selected(self) -> None:
        if self._selected == len(self._remotes) - 1:
            self._selected = 0
        else:
            self._selected += 1

    def handle_button_released(self, button: str) -> None:
        if button == AllButtons.MODE and self._app_state == AppState.NORMAL:
            self.increment_selected()
            self.event_bus.publish(Events.DEVICE_CHANGED, self.get_active_remote())

    def handle_state_change(self, state: str) -> None:
        self._app_state = state

    def handle_device_learn(self, remote: Device) -> None:
        self._remotes.append(remote)
        self.set_selected(len(self._remotes) - 1)
        self.event_bus.publish(Events.DEVICE_ADDED, self.get_all_remotes())

    def handle_ir_protocol_change(self, protocol_name: str) -> None:
        self.get_active_remote().protocol_name = protocol_name
