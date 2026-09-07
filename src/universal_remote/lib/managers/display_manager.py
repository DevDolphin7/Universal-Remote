from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.display.screen_normal import NormalScreen
from universal_remote.lib.display.screen_learning import LearnScreen
from universal_remote.lib.core.types import (
    AppState,
    Events,
    AllButtons,
    ProgrammableButtons,
    Device,
)


class Display:
    def __init__(
        self,
        event_bus: EventBus,
        state: str = AppState.NORMAL,
        remote_names: list[str] = [],
        protocol_name: str = "",
        battery_charge: int = 0,
    ) -> None:
        self._remote_index = 0
        self._learning_remote = ""

        self.set_protocol_name(protocol_name)
        self.set_remote_names(remote_names)
        self.set_battery_charge(battery_charge)
        self.set_buttons()
        self.set_button_index(self._buttons[0])
        self.set_screen(state)

        event_bus.subscribe(Events.BUTTON_RELEASED, self.handle_button_release)
        event_bus.subscribe(Events.STATE_CHANGED, self.handle_state_change)
        event_bus.subscribe(Events.IR_PROTOCOL_CHANGED, self.handle_ir_protocol_change)

    def get_button(self) -> str:
        return self._buttons[self._button_index]

    def set_protocol_name(self, protocol_name: str) -> None:
        self._protocol_name = protocol_name

    def set_remote_names(self, remote_names: list[str]) -> None:
        self._remote_names = remote_names

    def set_screen(self, state: str) -> None:
        if state == AppState.NORMAL:
            self._screen = NormalScreen(
                menu_items=self._remote_names, protocol_name=self._protocol_name
            )
        elif state == AppState.LEARNING:
            self._screen = LearnScreen(
                remote=self._learning_remote,
                buttons=self._buttons,
                protocol_name=self._protocol_name,
            )

    def set_battery_charge(self, charge: int) -> None:
        self._battery_charge = charge

    def set_buttons(self) -> None:
        self._buttons = [
            button for button in dir(ProgrammableButtons) if button[:2] != "__"
        ]

    def set_button_index(self, button: str) -> None:
        self._button_index = self._buttons.index(button)

    def scroll_menu(self) -> None:
        if not isinstance(self._screen, NormalScreen):
            return

        if self._remote_index == len(self._screen.menu_items) - 1:
            self._remote_index = 0
        else:
            self._remote_index += 1

        self.update()

    def update(self, learned: Device | None = None) -> None:
        if isinstance(self._screen, NormalScreen):
            self._screen.build(
                selected_remote=self._remote_index, battery_charge=self._battery_charge
            )
        elif isinstance(self._screen, LearnScreen) and not learned:
            self._screen.build_learning(
                selected_button=self._button_index, battery_charge=self._battery_charge
            )
        elif isinstance(self._screen, LearnScreen) and learned:
            button = self.get_button()

            self._screen.build_learned(
                selected_button=self._button_index,
                id=learned.id,
                address=learned.address,
                press_command=learned.commands[button].press,
                release_command=learned.commands[button].release,
                battery_charge=self._battery_charge,
            )

        self._screen.update()

    def handle_button_release(self, button: str, *args, **kwargs) -> None:
        if button == AllButtons.MODE and isinstance(self._screen, NormalScreen):
            self.scroll_menu()
        elif button in dir(ProgrammableButtons) and isinstance(
            self._screen, LearnScreen
        ):
            self.set_button_index(button)
            self.update()

    def handle_state_change(self, state: str, *args, **kwargs) -> None:
        if state == AppState.LEARNING and isinstance(self._screen, NormalScreen):
            self._learning_remote = self._screen.menu_items[self._remote_index]
            self.set_screen(state)
            self.update()
        elif state == AppState.LEARNED and isinstance(self._screen, LearnScreen):
            self.update(learned=args[0])
        elif state == AppState.NORMAL and isinstance(self._screen, LearnScreen):
            self.set_screen(state)
            self.update()

    def handle_ir_protocol_change(self, protocol: str, *args, **kwargs) -> None:
        if isinstance(self._screen, LearnScreen):
            self._screen.set_protocol_name(protocol)
            self.update()
