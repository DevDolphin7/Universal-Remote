from universal_remote.lib.drivers.epd1in54_V2 import EPD


class AllScreens(EPD):
    def __init__(self, protocol_name: str = ""):
        super().__init__()
        self.protocol_name = protocol_name

        self._screen_width = 200
        self._screen_height = 200

        self._battery_x_y = (165, 190)
        self._battery_height = 8
        self._battery_width = 22
        self._number_battery_icons = 4

    def build_useful_info(self) -> None:
        text = self.protocol_name
        if len(text) > 8:
            text = text[:8]  # Truncate the protocol name to fit within the screen width
        self.frame_buffer.text(f"Protocol: {text}", 10, 190, 0)

    def build_battery_icon(self) -> None:
        """Draws the outline of a battery icon"""
        x = self._battery_x_y[0]
        y = self._battery_x_y[1]

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

    def build_battery_charge(self, battery_charge: int) -> None:
        """Draws the charge icons within a battery icon"""
        x = self._battery_x_y[0] + 1
        y = self._battery_x_y[1] + 2

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
        pattern = pattern[0 : (battery_charge * battery_charge_width)]

        # Draw the pattern
        for offset, draw in enumerate(pattern):
            if draw:
                self.frame_buffer.vline(x + offset, y, self._battery_height - 4, 0)

    def build_footer(self, battery_charge: int) -> None:
        """Draws the footer of the screen, including the battery icon and charge level"""
        self.frame_buffer.hline(10, 185, 180, 0)
        self.build_useful_info()
        self.build_battery_icon()
        self.build_battery_charge(battery_charge)
