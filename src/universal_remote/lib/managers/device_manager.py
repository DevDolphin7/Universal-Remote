from utime import ticks_ms
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.core.state import State
from universal_remote.lib.managers.power_manager import Power
from universal_remote.lib.managers.display_manager import Display
from universal_remote.lib.managers.learn_manager import Learn
from universal_remote.lib.core.types import AppState, Events, AllButtons


class DeviceManager:
    def __init__(
        self,
        event_bus: EventBus,
        state: State,
        power: Power,
        display: Display,
        learn: Learn,
    ) -> None:
        self.event_bus = event_bus
        self.state = state
        self.power = power
        self.display = display
        self.learn = learn

        self._last_button_interaction = ticks_ms()

        self.event_bus.subscribe(Events.BUTTON_HELD, self.handle_button_held)
        self.event_bus.subscribe(Events.BUTTON_LEARNED, self.handle_button_learned)
        self.event_bus.subscribe(Events.BUTTON_RELEASED, self.handle_button_release)

    def update(self) -> None:
        if self.state.get() == AppState.LEARNING:
            return

        if ticks_ms() > self._last_button_interaction + 30000:
            self.power.sleep()

    def handle_button_held(self, button: str) -> None:
        state = self.state.get()
        if state == AppState.NORMAL:
            if button == AllButtons.MODE:
                self.state.set(AppState.LEARNING)
        else:
            if button == AllButtons.MODE:
                self.state.set(AppState.NORMAL)
            elif button in AllButtons.PROGRAMMABLE:
                self.state.set(AppState.LEARNING)

    def handle_button_learned(self, *args, **kwargs) -> None:
        self.state.set(AppState.LEARNED, self.learn.remote.get_active_remote())

    def handle_button_release(self, button: str, *args, **kwargs) -> None:
        if self.state.get() == AppState.LEARNED:
            if button in AllButtons.PROGRAMMABLE:
                self.state.set(AppState.LEARNING)
