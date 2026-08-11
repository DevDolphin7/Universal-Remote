from framebuf import FrameBuffer
from lib.drivers.epd1in54_V2 import EPD
from lib.core.event_bus import event_bus
from lib.drivers.hardware import Buttons
from lib.managers.device_manager import device
from lib.core.types import Events


class EPaperDisplay(EPD):
    def __init__(self) -> None:
        """Initializes the EPaperDisplay and sets up the menu and event subscriptions."""
        super().__init__()
        self.menu = device.get_names()
        self.draw = Draw(self.frame_buffer)

        self._battery_x_y = (160, 190)

        self._event_bus = event_bus
        self._event_bus.subscribe(Events.BUTTON_PRESSED, self._on_button_press)
        self._event_bus.subscribe(Events.LOW_BATTERY, self._on_low_battery)

        self.draw.menu(self.menu, device.get_index())
        self.update()

    def _on_button_press(self, button_name, *args, **kwargs) -> None:
        """Handles button press events to navigate the menu."""
        if button_name == Buttons.MENU_SELECT:
            self.draw.menu(self.menu, device.get_index())
            self.draw.useful_info()
            self.draw.battery(self._battery_x_y[0], self._battery_x_y[1])
            if not False:  # battery.is_low():
                self.draw.battery_charge(
                    self._battery_x_y[0] + 1, self._battery_x_y[1] + 2
                )

            self.update()

    def _on_low_battery(self, *args, **kwargs):
        self.draw.menu(self.menu, device.get_index())
        self.draw.useful_info()
        self.draw.battery(self._battery_x_y[0], self._battery_x_y[1])

        self.update()


class Draw:
    def __init__(self, frame_buffer: FrameBuffer) -> None:
        self.frame_buffer = frame_buffer
        self._battery_height = 8
        self._battery_width = 22
        self._number_battery_icons = 4

    def menu(self, menu, selected) -> None:
        """Draws the main menu on the e-paper display, highlighting the selected item and showing battery voltage."""
        self.frame_buffer.fill(1)
        self.frame_buffer.text("Remotes", 50, 10, 0)
        self.frame_buffer.hline(45, 20, 65, 0)

        y = 50

        for index, item in enumerate(menu):
            if index == selected:
                text = "> " + item
            else:
                text = "  " + item

            self.frame_buffer.text(text, 20, y, 0)
            y += 25

    def useful_info(self) -> None:
        self.frame_buffer.text(f"Protocol: {device.get().protocol}", 20, 170, 0)
        self.frame_buffer.text(f"Battery: {battery.get_percentage()}%", 20, 190, 0)

    def battery(self, x, y) -> None:
        """Draws the outline of a battery icon"""
        self.frame_buffer.rect(x, y, self._battery_width, self._battery_height, 0)
        terminal_top = int(self._battery_height / 4)
        terminal_bottom = int(self._battery_height * 3 / 4)
        self.frame_buffer.rect(
            x + self._battery_width,
            y + terminal_top,
            2,
            terminal_bottom - terminal_top,
            0,
        )

    def battery_charge(self, x, y) -> None:
        """Draws the charge icons within a battery icon"""
        battery_width = self._battery_width - 4
        battery_charge_width = int(self._battery_width / self._number_battery_icons)
        pattern = []

        # Create the pattern of drawing a line to create a battery charge icon, no line between battery charge icons
        remaining = 0
        while remaining <= battery_width:
            if remaining % battery_charge_width == 0:
                pattern.append(False)
            else:
                pattern.append(True)
            remaining += 1

        # Cut the pattern short based on what the actual battery charge is
        pattern = pattern[0 : (battery.get_status() * battery_charge_width)]

        # Draw the pattern
        for offset, draw in enumerate(pattern):
            if draw:
                self.frame_buffer.vline(x + offset, y, self._battery_height - 4, 0)
