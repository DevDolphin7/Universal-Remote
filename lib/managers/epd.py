from lib.drivers.epd1in54_V2 import EPD
from lib.core.event_bus import event_bus
from lib.managers.hardware import Buttons
from lib.managers.battery import battery
from lib.managers.device import device
from lib.core.types import Events


class EPaperDisplay(EPD):
    def __init__(self) -> None:
        """Initializes the EPaperDisplay and sets up the menu and event subscriptions."""
        super().__init__()
        self._timeout_interval = 20  # ms

        self.menu = device.get_names()
        self.selected = device.get_index()

        self._event_bus = event_bus
        self._event_bus.subscribe(Events.BUTTON_PRESSED, self.on_button_press)

        self.draw_menu()

    def draw_menu(self, voltage=0.0) -> None:
        """Draws the main menu on the e-paper display, highlighting the selected item and showing battery voltage."""
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

        self.frame_buffer.text(f"Protocol: {device.get().protocol}", 20, 170, 0)
        self.frame_buffer.text(f"Battery: {battery.get_percentage()}%", 20, 190, 0)

        self.update()

    def on_button_press(self, button_name, *args, **kwargs) -> None:
        """Handles button press events to navigate the menu."""
        if button_name == Buttons.MENU_SELECT:
            self.selected = device.get_index()
            self.draw_menu()
