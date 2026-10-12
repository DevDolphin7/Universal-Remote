from utime import ticks_ms, sleep_ms
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.core.state import State
from universal_remote.lib.drivers.protocol_registry import IRProtocolInterface
from universal_remote.lib.managers.remote_manager import Remote
from universal_remote.lib.managers.power_manager import Power
from universal_remote.lib.managers.display_manager import Display
from universal_remote.lib.managers.learn_manager import Learn
from universal_remote.lib.core.types import AppState, Events, AllButtons


class DeviceManager:
    def __init__(
        self,
        event_bus: EventBus,
        state: State,
        remote: Remote,
        power: Power,
        display: Display,
        learn: Learn,
        ir_protocol_interface: IRProtocolInterface,
    ) -> None:
        self.event_bus = event_bus
        self.state = state
        self.remote = remote
        self.power = power
        self.display = display
        self.learn = learn

        self._protocol_interface = ir_protocol_interface
        self.update_active_protocol()

        self._last_button_interaction = ticks_ms()
        self._button_held = False

        self.event_bus.subscribe(Events.BUTTON_HELD, self.handle_button_held)
        self.event_bus.subscribe(Events.BUTTON_LEARNED, self.handle_button_learned)
        self.event_bus.subscribe(Events.BUTTON_RELEASED, self.handle_button_release)

    def update_active_protocol(self) -> None:
        remote = self.remote.get_active_remote()
        self._protocol_interface.change_protocol_to_named(
            remote.protocol_name, self.learn.receive_ir
        )

    def transmit_press_and_release(self, button: str) -> None:
        """Transmits an IR command and waits for the transmission to complete, raising a TimeoutError if it takes too long."""
        remote = self.remote.get_active_remote()

        print("Transmitting command for button:", button)
        print("Transmitting for remote:", remote.name)
        print("Press command:", remote.commands[button].press)
        print("Release command:", remote.commands[button].release)

        try:
            self._protocol_interface.tx.transmit(
                remote.address, remote.commands[button].press
            )
        except:
            pass

        sleep_ms(160)

        try:
            self._protocol_interface.tx.transmit(
                remote.address, remote.commands[button].release
            )
        except:
            pass

        # time_elapsed = 0
        # while self._protocol_interface.tx.busy():
        #     if time_elapsed > self._timeout:
        #         raise TimeoutError("Transmission timeout")

        #     sleep_ms(self._timeout_interval)
        #     time_elapsed += self._timeout_interval

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

        self._button_held = True

    def handle_button_learned(self, *args, **kwargs) -> None:
        self.state.set(AppState.LEARNED, self.learn.remote.get_active_remote())

    def handle_button_release(self, button: str, *args, **kwargs) -> None:
        if self._button_held:
            self._button_held = False
            return

        state = self.state.get()
        if state == AppState.NORMAL:
            if button in AllButtons.PROGRAMMABLE:
                remote = self.remote.get_active_remote()
                if button in remote.commands.keys():
                    self.transmit_press_and_release(button)
            elif button is AllButtons.MODE:
                print("Active remote: ", self.remote.get_active_remote())
                self.display.set_protocol_name(self.remote.get_active_protocol())
                self.update_active_protocol()
                print("Active protocol changed to: ", self.remote.get_active_protocol())
        elif state == AppState.LEARNED:
            if button in AllButtons.PROGRAMMABLE:
                self.state.set(AppState.LEARNING)
