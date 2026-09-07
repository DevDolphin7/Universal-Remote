from universal_remote.lib.display.screen_common import AllScreens


class LearnScreen(AllScreens):
    def __init__(
        self, remote: str = "", buttons: list[str] = ["TBC"], protocol_name: str = ""
    ):
        super().__init__(protocol_name)
        self.set_remote(remote)
        self._buttons = buttons

    def set_remote(self, remote: str) -> None:
        if len(remote) > 20:
            name = remote[:20]
        else:
            name = remote

        self._remote = name

    def set_protocol_name(self, protocol_name: str) -> None:
        """Updates the protocol name to be displayed on the screen."""
        self.protocol_name = protocol_name

    def build_learning(self, selected_button: int = 0, battery_charge: int = 0) -> None:
        self.build_header()
        self.build_currently_learning(selected_button)
        self.build_footer(battery_charge)

    def build_learned(
        self,
        selected_button: int,
        id: int,
        address: int,
        press_command: int | None,
        release_command: int | None,
        battery_charge: int = 0,
    ) -> None:
        self.build_header()
        self.build_learned_info(
            selected_button, id, address, press_command, release_command
        )
        self.build_footer(battery_charge)

    def build_header(self) -> None:
        """Draws the header on the e-paper display, showing the remote name and a prompt to learn a button."""
        self.frame_buffer.fill(1)
        self.frame_buffer.text(self._remote, 20, 10, 0)
        self.frame_buffer.hline(10, 20, 180, 0)

    def build_currently_learning(self, selected: int) -> None:
        self.frame_buffer.text(f"Learning: {self._buttons[selected]}", 20, 50, 0)

    def build_learned_info(
        self,
        selected: int,
        id: int,
        address: int,
        press_command: int | None,
        release_command: int | None,
    ) -> None:
        self.frame_buffer.text(f"Learned: {self._buttons[selected]}", 20, 50, 0)
        self.frame_buffer.text(f"ID: {id}", 20, 90, 0)
        self.frame_buffer.text(f"Address: {hex(address)}", 20, 110, 0)

        if press_command is not None:
            self.frame_buffer.text(f"Press: {hex(press_command)}", 20, 130, 0)
        if release_command is not None:
            self.frame_buffer.text(f"Release: {hex(release_command)}", 20, 150, 0)
