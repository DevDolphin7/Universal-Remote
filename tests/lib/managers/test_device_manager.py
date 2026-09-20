import pytest
from unittest.mock import Mock
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.core.state import State
from universal_remote.lib.managers.power_manager import Power
from universal_remote.lib.managers.display_manager import Display
from universal_remote.lib.managers.learn_manager import Learn
from universal_remote.lib.managers.remote_manager import Remote
from universal_remote.lib.managers.device_manager import DeviceManager
from universal_remote.lib.core.types import AppState, Events, AllButtons, IRData, Device

"""
TestNormalMode
test_defaults_to_appstate_normal_on_wake
test_on_normal_appstate_enters_sleep_after_thirty_seconds
test_on_state_change_to_learning_load_learn_mode


TestLearningMode
test_on_normal_state_mode_button_release_publishes_learning_appstate
test_mode_button_held_returns_to_normal_state
test_does_not_sleep_during_learning_mode

TestLearnedMode
test_on_learned_state_programmable_button_release_publishes_learning_state
test_mode_button_held_returns_to_normal_state
test_on_learned_appstate_sleeps_after_thirty_seconds

TestFactoryReset
test_on_mode_button_and_nav_ok_hold_for_ten_seconds_publish_factory_reset
"""


def create_press_ir_data(number: int) -> IRData:
    return IRData(
        address=number, command=number + 1, protocol_name="NEC_16", ticks_diff=1000
    )


def create_device(number: int) -> Device:
    return Device(
        id=number,
        name="Test",
        protocol_name="NEC_8",
        address=number + 1,
        commands={},
    )


@pytest.fixture
def event_bus():
    return EventBus()


@pytest.fixture
def state(event_bus):
    return State(event_bus)


@pytest.fixture
def power(event_bus):
    return Power(event_bus)


@pytest.fixture
def display(event_bus):
    return Display(
        event_bus=event_bus,
        remote_names=["Test"],
        protocol_name="Test",
        battery_charge=2,
    )


@pytest.fixture
def learn(event_bus):
    remote = Remote(event_bus, [create_device(0)])
    return Learn(event_bus, remote)


class TestDeviceManager:
    class TestNormalMode:
        def test_defaults_to_appstate_normal_on_wake(
            self, event_bus, state, power, display, learn
        ):
            DeviceManager(event_bus, state, power, display, learn)

            assert state.get() == AppState.NORMAL

        def test_on_mode_button_pressed_selects_new_remote(
            self, event_bus, state, power, display, learn
        ):
            device_manager = DeviceManager(event_bus, state, power, display, learn)

            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.MODE)

            all_remotes = device_manager.learn.remote.get_all_remotes()
            active_remote = device_manager.learn.remote.get_active_remote()
            assert all_remotes.index(active_remote) == 1

        def test_on_normal_appstate_enters_sleep_after_thirty_seconds(
            self, event_bus, state, power, display, learn
        ):
            mock: Mock = Mock()
            event_bus.subscribe(Events.SLEEP_DEEP, mock)

            device_manager = DeviceManager(event_bus, state, power, display, learn)
            device_manager.update()

            device_manager._last_button_interaction -= 30001
            device_manager.update()

            mock.assert_called_once()

        # def test_on_state_change_to_learning_load_learn_mode(
        #     self, event_bus, state, power, display, learn
        # ):
        #     device_manager = DeviceManager(event_bus, state, power, display, learn)
        #     event_bus.publish(Events.BUTTON_RELEASED, AllButtons.MODE)

        #     assert

    class TestLearningMode:
        def test_on_normal_state_mode_button_held_publishes_learning_appstate(
            self, event_bus, state, power, display, learn
        ):
            DeviceManager(event_bus, state, power, display, learn)

            event_bus.publish(Events.BUTTON_HELD, AllButtons.MODE)

            assert state.get() == AppState.LEARNING

        def test_mode_button_held_returns_to_normal_state(
            self, event_bus, state, power, display, learn
        ):
            DeviceManager(event_bus, state, power, display, learn)

            event_bus.publish(Events.BUTTON_HELD, AllButtons.MODE)
            assert state.get() == AppState.LEARNING

            event_bus.publish(Events.BUTTON_HELD, AllButtons.MODE)
            assert state.get() == AppState.NORMAL

        def test_does_not_sleep_during_learning_mode(
            self, event_bus, state, power, display, learn
        ):
            mock: Mock = Mock()
            event_bus.subscribe(Events.SLEEP_DEEP, mock)

            device_manager = DeviceManager(event_bus, state, power, display, learn)
            event_bus.publish(Events.BUTTON_HELD, AllButtons.MODE)
            assert state.get() == AppState.LEARNING

            device_manager._last_button_interaction -= 30001
            device_manager.update()

            mock.assert_not_called()

    class TestLearnedMode:
        def test_on_learned_state_programmable_button_release_publishes_learning_state(
            self, event_bus, state, power, display, learn
        ):
            DeviceManager(event_bus, state, power, display, learn)

            event_bus.publish(Events.BUTTON_HELD, AllButtons.MODE)
            assert state.get() == AppState.LEARNING

            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.NAV_UP)
            event_bus.publish(Events.IR_RECEIVED, [create_press_ir_data(0)])
            assert state.get() == AppState.LEARNED

            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.CH_DOWN)
            assert state.get() == AppState.LEARNING

        def test_mode_button_held_returns_to_normal_state(
            self, event_bus, state, power, display, learn
        ):
            DeviceManager(event_bus, state, power, display, learn)

            event_bus.publish(Events.BUTTON_HELD, AllButtons.MODE)
            assert state.get() == AppState.LEARNING

            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.NAV_UP)
            event_bus.publish(Events.IR_RECEIVED, [create_press_ir_data(0)])
            assert state.get() == AppState.LEARNED

            event_bus.publish(Events.BUTTON_HELD, AllButtons.MODE)
            assert state.get() == AppState.NORMAL

        def test_on_learned_appstate_sleeps_after_thirty_seconds(
            self, event_bus, state, power, display, learn
        ):
            mock: Mock = Mock()
            event_bus.subscribe(Events.SLEEP_DEEP, mock)

            device_manager = DeviceManager(event_bus, state, power, display, learn)
            event_bus.publish(Events.BUTTON_HELD, AllButtons.MODE)
            assert state.get() == AppState.LEARNING

            event_bus.publish(Events.BUTTON_RELEASED, AllButtons.NAV_UP)
            event_bus.publish(Events.IR_RECEIVED, [create_press_ir_data(0)])
            assert state.get() == AppState.LEARNED

            device_manager._last_button_interaction -= 30001
            device_manager.update()

            mock.assert_called_once()

    class TestFactoryReset:
        """Not implemented prior to Integration Testing on Hardware"""

        pass
