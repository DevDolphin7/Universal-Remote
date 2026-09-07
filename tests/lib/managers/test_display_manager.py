import pytest, re
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.display.screen_normal import NormalScreen
from universal_remote.lib.display.screen_learning import LearnScreen
from universal_remote.lib.core.types import (
    Events,
    AllButtons,
    AppState,
    ProgrammableButtons,
    IRProtocols,
    Device,
    Commands,
)
from universal_remote.lib.managers.display_manager import Display

"""
NormalScreen
test_mode_button_released_cycles_active_remote
test_state_change_to_learning_changes_to_learn_screen

LearnScreen
test_programmable_button_released_displays_that_button_as_learning
test_ir_protocol_changed_displays_new_protocol
test_state_change_to_learned_displays_button_learned_information
test_state_change_to_normal_changes_to_normal_screen

AllScreens
test_battery_level_changed_event_updates_battery_icon
test_low_battery_event_displays_empty_battery_icon
"""


def assert_text_called_with_specific_text_once(frame_buffer, text: str):
    text_call_args = [call[0][0] for call in frame_buffer.text.call_args_list]
    arg_matches = re.findall(rf"{re.escape(text)}'", str(text_call_args))
    print(text_call_args)
    assert len(arg_matches) == 1


@pytest.fixture
def event_bus():
    return EventBus()


@pytest.fixture
def remote_names():
    return [f"Remote {i}" for i in range(8)]


class TestDisplay:
    class TestNormalScreen:
        def test_device_changed_cycles_active_remote(self, event_bus, remote_names):
            display = Display(event_bus, remote_names=remote_names, protocol_name="NEC")

            assert isinstance(display._screen, NormalScreen)

            device = Device(1, "Remote 1", "NEC", 2, {})
            event_bus.publish(Events.DEVICE_CHANGED, device)

            assert isinstance(display._screen, NormalScreen)

            with pytest.raises(AssertionError):
                assert_text_called_with_specific_text_once(
                    display._screen.frame_buffer, remote_names[0]
                )

            assert_text_called_with_specific_text_once(
                display._screen.frame_buffer, remote_names[1]
            )

        def test_state_change_to_learning_changes_to_learn_screen(
            self, event_bus, remote_names
        ):
            display = Display(event_bus, remote_names=remote_names, protocol_name="NEC")

            assert isinstance(display._screen, NormalScreen)

            event_bus.publish(Events.STATE_CHANGED, AppState.LEARNING)

            assert isinstance(display._screen, LearnScreen)

            assert_text_called_with_specific_text_once(
                display._screen.frame_buffer, "Learning: " + display.get_button()
            )

    class TestLearnScreen:
        def test_programmable_button_released_displays_that_button_as_learning(
            self, event_bus, remote_names
        ):
            display = Display(
                event_bus,
                remote_names=remote_names,
                protocol_name="NEC",
                state=AppState.LEARNING,
            )

            assert isinstance(display._screen, LearnScreen)

            event_bus.publish(Events.BUTTON_RELEASED, ProgrammableButtons.NAV_OK)

            assert_text_called_with_specific_text_once(
                display._screen.frame_buffer, "Learning: " + ProgrammableButtons.NAV_OK
            )

        def test_ir_protocol_changed_displays_new_protocol(
            self, event_bus, remote_names
        ):
            display = Display(
                event_bus,
                remote_names=remote_names,
                protocol_name="NEC",
                state=AppState.LEARNING,
            )

            event_bus.publish(Events.IR_PROTOCOL_CHANGED, IRProtocols.RC6_M0)

            assert_text_called_with_specific_text_once(
                display._screen.frame_buffer, "Protocol: " + IRProtocols.RC6_M0
            )

        def test_state_change_to_learned_displays_button_learned_information(
            self, event_bus, remote_names
        ):
            display = Display(
                event_bus,
                remote_names=remote_names,
                protocol_name="NEC",
                state=AppState.LEARNING,
            )

            learned_device = Device(
                id=1,
                name="Remote",
                protocol_name="NEC",
                address=2,
                commands={"NAV_OK": Commands(press=3, release=4)},
            )

            event_bus.publish(Events.BUTTON_RELEASED, ProgrammableButtons.NAV_OK)
            event_bus.publish(Events.STATE_CHANGED, AppState.LEARNED, learned_device)

            assert_text_called_with_specific_text_once(
                display._screen.frame_buffer, "Address: " + hex(learned_device.address)
            )

        def test_state_change_to_normal_changes_to_normal_screen(
            self, event_bus, remote_names
        ):
            display = Display(
                event_bus,
                remote_names=remote_names,
                protocol_name="NEC",
                state=AppState.LEARNING,
            )

            assert isinstance(display._screen, LearnScreen)

            event_bus.publish(Events.STATE_CHANGED, AppState.NORMAL)

            assert isinstance(display._screen, NormalScreen)
