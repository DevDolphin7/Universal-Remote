from utime import sleep_ms
from lib.core.event_bus import event_bus, Events
from lib.managers.hardware import Hardware, Buttons


class ButtonManager:
    def __init__(self):
        self.buttons = {
            Buttons.MENU_SELECT: Hardware.epd_button1,
            Buttons.CHANGE_IR_PROTOCOL: Hardware.ir_protocol_button,
            Buttons.TRANSMIT_IR: Hardware.ir_tx_button1,
            Buttons.LEARN_IR: Hardware.learn_ir_button,
        }
        self._pressed_buttons = []

        self._event_bus = event_bus

    def update(self):
        for button_name, button_pin in self.buttons.items():
            if self.poll(button_name, button_pin):
                self._event_bus.publish(Events.BUTTON_PRESSED, button_name)
                print(f"Button pressed: {button_name}")

        for button in self._pressed_buttons:
            if button["pin"].value() != 0:
                self._event_bus.publish(Events.BUTTON_RELEASED, button["name"])
                self._pressed_buttons.remove(button)
                print(f"Button released: {button['name']}")

    def poll(self, button_name, button_pin):
        if button_pin.value() == 0:
            for button in self._pressed_buttons:
                if button["name"] == button_name:
                    return False  # Already pressed

            sleep_ms(20)  # Prevent debouncing issues

            if button_pin.value() == 0:
                self._pressed_buttons.append({"name": button_name, "pin": button_pin})
                return True

        return False
