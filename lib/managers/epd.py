from machine import Pin
from lib.drivers.epd1in54_V2 import EPD
from time import sleep_ms
from lib.managers.hardware import Buttons
from lib.core.event_bus import event_bus, Events


class EPaperDisplay(EPD):
    def __init__(self):
        super().__init__()
        self._timeout_interval = 20  # ms

        self.menu = ["Weather", "Clock", "Settings", "About"]
        self.selected = 0

        self._event_bus = event_bus
        self._event_bus.subscribe(Events.BUTTON_PRESSED, self.on_button_press)

    def draw_menu(self, voltage=0.0):
        self.frame_buffer.fill(1)
        self.frame_buffer.text("Main Menu", 50, 10, 0)
        self.frame_buffer.text("-------", 50, 20, 0)

        y = 50

        for index, item in enumerate(self.menu):
            if index == self.selected:
                text = "> " + item
            else:
                text = "  " + item

            self.frame_buffer.text(text, 20, y, 0)
            y += 25

        self.frame_buffer.text(f"Battery: {voltage:.2f}V", 20, 180, 0)

        self.update()

    def on_button_press(self, button_name):
        if button_name == Buttons.MENU_SELECT:
            self.selected += 1

            if self.selected >= len(self.menu):
                self.selected = 0

            self.draw_menu()
