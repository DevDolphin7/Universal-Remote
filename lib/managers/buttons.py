from utime import sleep_ms
from lib.managers.hardware import Hardware, Buttons
from lib.core.event_bus import event_bus
from lib.core.types import Events


class ButtonManager:
    def __init__(self) -> None:
        self.buttons = {
            Buttons.MENU_SELECT: Hardware.menu_select_button,
            Buttons.CHANGE_IR_PROTOCOL: Hardware.change_ir_protocol_button,
            Buttons.TRANSMIT_IR: Hardware.transmit_ir_button,
            Buttons.LEARN_IR: Hardware.learn_ir_button,
        }
        self._pressed_buttons = []

        self._event_bus = event_bus

    def update(self) -> None:
        """Polls the state of the buttons and publishes events for button presses and releases."""
        for button_name, button_pin in self.buttons.items():
            if self.poll(button_name, button_pin):
                self._event_bus.publish(Events.BUTTON_PRESSED, button_name)

        for button in self._pressed_buttons:
            if button["pin"].value() != 0:
                self._event_bus.publish(Events.BUTTON_RELEASED, button["name"])
                self._pressed_buttons.remove(button)

    def poll(self, button_name, button_pin) -> bool:
        """Returns True once for a given button press, handles debouncing."""
        if button_pin.value() == 0:
            for button in self._pressed_buttons:
                if button["name"] == button_name:
                    return False  # Already pressed

            sleep_ms(20)  # Prevent debouncing issues

            if button_pin.value() == 0:
                self._pressed_buttons.append({"name": button_name, "pin": button_pin})
                return True

        return False
