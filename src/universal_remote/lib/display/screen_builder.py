from universal_remote.lib.drivers.epd1in54_V2 import EPD


class AllScreens(EPD):
    def __init__(self, protocol_name: str = ""):
        self.protocol_name = protocol_name

        self._screen_width = 200
        self._screen_height = 200

        self._battery_x_y = (160, 190)
        self._battery_height = 8
        self._battery_width = 22
        self._number_battery_icons = 4

    def build_useful_info(self) -> None:
        self.frame_buffer.text(f"Protocol: {self.protocol_name}", 20, 190, 0)

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
        x = self._battery_x_y[0]
        y = self._battery_x_y[1]

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


class NormalScreen(AllScreens):
    def __init__(self, menu_items: list[str] = [], protocol_name: str = ""):
        super().__init__(protocol_name)
        self.set_menu_items(menu_items)

    def get_visible_items(self, selected: int) -> list[str]:
        """Returns a list of menu items that should be visible on the screen based on the selected item."""
        visible_items = [item for item in self.menu_items]

        if len(visible_items) > 6:
            visible_items = visible_items + visible_items
            visible_items = visible_items[selected : selected + 6]

        return visible_items

    def set_menu_items(self, items: list[str]) -> None:
        """Updates the list of menu items (remotes) to be displayed on the screen."""
        self.menu_items = [item for item in items] + ["Add New"]

    def set_protocol_name(self, protocol_name: str) -> None:
        """Updates the protocol name to be displayed on the screen."""
        self.protocol_name = protocol_name

    def build(self, selected_remote: int = 0, battery_charge: int = 0) -> None:
        self.build_menu(selected_remote)

        # class AllScreens methods
        self.build_useful_info()
        self.build_battery_icon()
        self.build_battery_charge(battery_charge)

    def build_menu(self, selected: int) -> None:
        """Draws the main menu on the e-paper display, highlighting the selected item and showing battery voltage."""
        self.frame_buffer.fill(1)
        self.frame_buffer.text("Remotes", 50, 10, 0)
        self.frame_buffer.hline(45, 20, 65, 0)

        y = 50

        for index, item in enumerate(self.get_visible_items(selected)):
            if len(item) > 20:
                item = item[:20]  # Truncate the item to fit within the screen width
            if index == 0:
                text = "-> " + item
            else:
                text = "   " + item

            self.frame_buffer.text(text, 20, y, 0)
            y += 25
