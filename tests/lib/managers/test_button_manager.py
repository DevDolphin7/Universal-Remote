import pytest
from unittest.mock import Mock
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.managers.button_manager import Buttons
from universal_remote.lib.core.types import Events, AllButtons


@pytest.fixture
def event_bus():
    return EventBus()


class TestButtons:
    def test_button_press_publishes_press_event_and_button(
        self, event_bus, mock_mode_button
    ):
        mock: Mock = Mock()
        event_bus.subscribe(Events.BUTTON_PRESSED, mock)

        buttons = Buttons(event_bus)

        mock_mode_button.value.return_value = 0

        buttons.update()

        mock.assert_called_once_with(AllButtons.MODE)

    def test_button_release_publishes_release_event_and_button(
        self, event_bus, mock_mode_button
    ):
        mock: Mock = Mock()
        event_bus.subscribe(Events.BUTTON_RELEASED, mock)

        buttons = Buttons(event_bus)

        mock_mode_button.value.return_value = 0
        buttons.update()

        mock_mode_button.value.return_value = 1
        buttons.update()

        mock.assert_called_once_with(AllButtons.MODE)

    def test_button_hold_publishes_held_event_and_button(
        self, event_bus, mock_mode_button
    ):
        mock: Mock = Mock()
        event_bus.subscribe(Events.BUTTON_HELD, mock)

        buttons = Buttons(event_bus)

        mock_mode_button.value.return_value = 0
        buttons.update()
        buttons.update()
        buttons.update()

        mock_mode_button.value.return_value = 1
        buttons.update()

        mock.assert_called_once_with(AllButtons.MODE)
