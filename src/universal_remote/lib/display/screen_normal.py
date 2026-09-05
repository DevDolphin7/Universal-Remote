from universal_remote.lib.display.screen_common import AllScreens


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

    def build(self, selected_remote: int = 0, battery_charge: int = 0) -> None:
        self.build_menu(selected_remote)
        self.build_footer(battery_charge)

    def build_menu(self, selected: int) -> None:
        """Draws the main menu on the e-paper display, highlighting the selected item and showing battery voltage."""
        self.frame_buffer.fill(1)
        self.frame_buffer.text("Remotes", 50, 10, 0)
        self.frame_buffer.hline(45, 20, 65, 0)

        y = 40

        for index, item in enumerate(self.get_visible_items(selected)):
            if len(item) > 20:
                item = item[:20]  # Truncate the item to fit within the screen width
            if index == 0:
                text = "-> " + item
            else:
                text = "   " + item

            self.frame_buffer.text(text, 20, y, 0)
            y += 25
