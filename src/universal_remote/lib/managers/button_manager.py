from utime import sleep_ms
from universal_remote.lib.drivers.hardware import Hardware
from universal_remote.lib.core.types import Events, AllButtons


class Buttons:
    def __init__(self, event_bus) -> None:
        self.event_bus = event_bus

        self.buttons = {
            AllButtons.MODE: Hardware.mode,
            AllButtons.VOL_UP: Hardware.vol_up,
            AllButtons.VOL_DOWN: Hardware.vol_down,
            AllButtons.CH_UP: Hardware.ch_up,
            AllButtons.CH_DOWN: Hardware.ch_down,
            AllButtons.NAV_UP: Hardware.nav_up,
            AllButtons.NAV_RIGHT: Hardware.nav_right,
            AllButtons.NAV_DOWN: Hardware.nav_down,
            AllButtons.NAV_LEFT: Hardware.nav_left,
            AllButtons.NAV_OK: Hardware.nav_ok,
        }

        self._pressed_buttons = []
        self._held_threshold = 3  # Number of times update is called with button held before BUTTON_HELD is published

    def update(self) -> None:
        """Polls the state of the buttons and publishes events for button presses and releases."""
        for button_name, button_pin in self.buttons.items():
            if self.poll(button_name, button_pin):
                self.event_bus.publish(Events.BUTTON_PRESSED, button_name)

        for button in self._pressed_buttons:
            if button["pin"].value() != 0:
                self.event_bus.publish(Events.BUTTON_RELEASED, button["name"])
                self._pressed_buttons.remove(button)

    def poll(self, button_name, button_pin) -> bool:
        """Returns True once for a given button press, handles debouncing."""
        if button_pin.value() == 0:
            for button in self._pressed_buttons:
                if button["name"] == button_name:
                    button["held_count"] += 1
                    if button["held_count"] == self._held_threshold:
                        self.event_bus.publish(Events.BUTTON_HELD, button["name"])
                    return False  # Already pressed

            sleep_ms(20)  # Prevent debouncing issues

            if button_pin.value() == 0:
                self._pressed_buttons.append(
                    {"name": button_name, "pin": button_pin, "held_count": 1}
                )
                return True

        return False
