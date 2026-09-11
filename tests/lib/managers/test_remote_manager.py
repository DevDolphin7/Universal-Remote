import pytest
from unittest.mock import Mock
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.managers.remote_manager import Remote
from universal_remote.lib.core.types import (
    Events,
    Device,
    Commands,
    AllButtons,
    AppState,
)


def create_remote(number: int):
    return Device(
        id=number,
        name="New Remote",
        protocol_name="NEC",
        address=number + 1,
        commands={AllButtons.NAV_OK: Commands(press=number + 2, release=number + 3)},
    )


@pytest.fixture
def event_bus():
    return EventBus()


@pytest.fixture
def remotes():
    return [create_remote(i) for i in range(3)]


class TestRemote:
    class TestProvideActiveRemote:
        def test_publishes_device_changed_on_appstate_normal_mode_button_release(
            self, event_bus, remotes
        ):
            mock: Mock = Mock()
            event_bus.subscribe(Events.DEVICE_CHANGED, mock)

            remote = Remote(event_bus, remotes, selected=0)

            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.MODE)

            assert remote._selected == 1
            mock.assert_called_once_with(remotes[1])

            event_bus.publish(Events.STATE_CHANGED, AppState.LEARNING)
            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.MODE)

            # Still called once from before, hasn't increased to 2 calls on BUTTON_RELEASED
            assert remote._selected == 1
            mock.assert_called_once_with(remotes[1])

        def test_provides_the_active_remote_protocol_name(self, event_bus, remotes):
            remote = Remote(event_bus, remotes)

            output = remote.get_active_protocol()

            assert output == remotes[0].protocol_name

        def test_provides_a_list_of_all_available_remote_names(
            self, event_bus, remotes
        ):
            remote = Remote(event_bus, remotes)

            expected = [remote.name for remote in remotes]
            output = remote.get_all_remote_names()

            assert isinstance(output, list)
            assert len(expected) > 0
            for index, name in enumerate(expected):
                assert output[index] == name

        def test_provides_a_list_of_all_available_remotes(self, event_bus, remotes):
            remote = Remote(event_bus, remotes)

            output = remote.get_all_remotes()

            assert isinstance(output, list)
            assert len(remotes) > 0
            for index, remote in enumerate(remotes):
                assert output[index] == remote

    class TestAddRemote:
        def test_adds_a_new_remote_on_appstate_learning_on_add_new(
            self, event_bus, remotes
        ):
            mock: Mock = Mock()
            event_bus.subscribe(Events.DEVICE_ADDED, mock)

            remote = Remote(event_bus, remotes)
            new_remote = create_remote(90)

            event_bus.publish(Events.DEVICE_LEARNED, new_remote)

            expected = list(remotes) + [new_remote]

            assert len(remote.get_all_remote_names()) == len(remotes) + 1
            assert remote._remotes[-1].id == 90
            mock.assert_called_once_with(expected)

        def test_added_remote_is_selected(self, event_bus, remotes):
            remote = Remote(event_bus, remotes)

            new_remote = create_remote(90)

            event_bus.publish(Events.DEVICE_LEARNED, new_remote)

            assert remote.get_active_remote() == new_remote

        def test_remote_protocol_updated_on_ir_protocol_change_in_learning_mode(
            self, event_bus, remotes
        ):
            remote = Remote(event_bus, remotes)

            event_bus.publish(Events.STATE_CHANGED, AppState.LEARNING)
            event_bus.publish(Events.IR_PROTOCOL_CHANGED, "SAMSUNG")

            assert remote.get_active_protocol() == "SAMSUNG"
            assert remote.get_active_remote().protocol_name == "SAMSUNG"
