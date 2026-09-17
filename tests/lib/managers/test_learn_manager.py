import pytest
from unittest.mock import Mock
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.managers.remote_manager import Remote
from universal_remote.lib.managers.learn_manager import Learn
from universal_remote.lib.core.types import Events, Device, AllButtons, Commands, IRData


def create_remote(number: int):
    return Device(
        id=number,
        name=f"Remote {number}",
        protocol_name="NEC_8",
        address=number + 1,
        commands={AllButtons.NAV_OK: Commands(press=number + 2, release=number + 3)},
    )


def create_press_ir_data(number: int):
    return IRData(
        address=number, command=number + 1, protocol_name="NEC_16", ticks_diff=1000
    )


def create_release_ir_data(number: int):
    return IRData(
        address=number, command=number + 1, protocol_name="NEC_16", ticks_diff=100
    )


@pytest.fixture
def event_bus():
    return EventBus()


@pytest.fixture
def remote(event_bus):
    return Remote(event_bus, [create_remote(0)])


class TestLearn:
    class TestUpdateRemote:
        def test_ir_data_recieved_event_updates_active_button_press_command(
            self, event_bus, remote
        ):
            learn = Learn(event_bus, remote)
            fake_ir_data = create_press_ir_data(10)

            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.CH_UP)

            learn.handle_ir_received([fake_ir_data])

            output = learn.remote.get_active_remote()

            learned_buttons = output.commands.keys()
            assert AllButtons.CH_UP in learned_buttons

            output_commands = output.commands[AllButtons.CH_UP]
            assert output_commands.press == fake_ir_data.command

        def test_two_quick_ir_data_recieved_events_updates_button_release_command(
            self, event_bus, remote
        ):
            learn = Learn(event_bus, remote)
            fake_press_data = create_press_ir_data(10)
            fake_release_data = create_release_ir_data(12)

            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.CH_UP)

            learn.handle_ir_received([fake_press_data, fake_release_data])

            output = learn.remote.get_active_remote()

            learned_buttons = output.commands.keys()
            assert AllButtons.CH_UP in learned_buttons

            output_commands = output.commands[AllButtons.CH_UP]
            assert output_commands.press == fake_press_data.command
            assert output_commands.release == fake_release_data.command

        def test_ir_data_recieved_event_updates_remote_with_active_protocol(
            self, event_bus, remote
        ):
            learn = Learn(event_bus, remote)
            fake_ir_data = create_press_ir_data(10)

            learn.handle_ir_received([fake_ir_data])

            output = learn.remote.get_active_remote()

            assert output.protocol_name == fake_ir_data.protocol_name

        def test_ir_data_recieved_event_updates_remote_with_address(
            self, event_bus, remote
        ):
            learn = Learn(event_bus, remote)
            fake_ir_data = create_press_ir_data(10)

            learn.handle_ir_received([fake_ir_data])

            output = learn.remote.get_active_remote()

            assert output.address == fake_ir_data.address

        def test_valid_button_update_publishes_button_learned_event(
            self, event_bus, remote
        ):
            mock: Mock = Mock()
            learn = Learn(event_bus, remote)
            fake_ir_data = create_press_ir_data(10)

            event_bus.subscribe(Events.BUTTON_LEARNED, mock)
            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.CH_UP)

            learn.handle_ir_received([fake_ir_data])

            output = learn.remote.get_active_remote()

            mock.assert_called_once_with(AllButtons.CH_UP, output)

    class TestAddRemote:
        def test_ir_data_recieved_event_on_add_new_remote_creates_new_remote(
            self, event_bus, remote
        ):
            mock: Mock = Mock()
            number_of_remotes = len(remote.get_all_remote_names())

            learn = Learn(event_bus, remote)
            learn.request_new_remote()

            fake_ir_data = create_press_ir_data(10)

            event_bus.subscribe(Events.BUTTON_LEARNED, mock)
            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.CH_UP)

            learn.handle_ir_received([fake_ir_data])

            updated_number_of_remotes = len(remote.get_all_remote_names())
            output = learn.remote.get_active_remote()

            assert updated_number_of_remotes == number_of_remotes + 1
            assert output.address == fake_ir_data.address
            assert output.protocol_name == fake_ir_data.protocol_name

        def test_ir_data_recieved_event_on_add_new_remote_publishes_device_learned(
            self, event_bus, remote
        ):
            mock: Mock = Mock()
            learn = Learn(event_bus, remote)
            event_bus.subscribe(Events.DEVICE_LEARNED, mock)

            learn.request_new_remote()

            fake_ir_data = create_press_ir_data(10)
            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.CH_UP)
            event_bus.publish(Events.IR_RECEIVED, [fake_ir_data])

            output = remote.get_active_remote()
            new_remote_index = len(remote.get_all_remote_names()) - 1
            assert output.name == f"Remote {new_remote_index}"
            assert output.commands[AllButtons.CH_UP].press == fake_ir_data.command
            assert output.address == fake_ir_data.address
            assert output.protocol_name == fake_ir_data.protocol_name

            mock.assert_called_with(output)
