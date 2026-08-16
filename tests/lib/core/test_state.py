import pytest
from unittest.mock import Mock
from universal_remote.lib.core.state import State
from universal_remote.lib.core.types import AppState, Events


@pytest.fixture
def event_bus() -> Mock:
    return Mock()


@pytest.fixture
def state(event_bus) -> State:
    return State(event_bus)


class TestMode:
    def test_starts_in_normal_mode(self, state):
        assert state._mode == AppState.NORMAL

    def test_can_change_mode(self, state):
        state.set(AppState.LEARNING)

        assert state._mode == AppState.LEARNING

    def test_get_mode_returns_active_mode(self, state):
        assert state.get() == AppState.NORMAL

        state.set(AppState.LEARNING)

        assert state.get() == AppState.LEARNING

    def test_mode_change_publishes_event_with_state(self, state, event_bus):
        state.set(AppState.LEARNING)

        event_bus.publish.assert_called_once_with(
            Events.STATE_CHANGED, AppState.LEARNING
        )

        state.set(AppState.NORMAL)

        assert event_bus.publish.call_count == 2
        event_bus.publish.assert_called_with(Events.STATE_CHANGED, AppState.NORMAL)

    def test_same_mode_transition_does_nothing(self, state, event_bus):
        state.set(AppState.NORMAL)
        state.set(AppState.LEARNING)
        state.set(AppState.LEARNING)

        event_bus.publish.assert_called_once_with(
            Events.STATE_CHANGED, AppState.LEARNING
        )

    def test_invalid_mode_change_raises_error(self, state):
        with pytest.raises(ValueError, match="Invalid state provided"):
            state.set("BANANA")


class TestDataPersistence:
    def test_to_dict_serialises_state(self, state):
        output = state.to_dict()

        assert len(output.items()) == 1

        for key, value in output.items():
            assert key == "mode"
            assert value == AppState.NORMAL

    def test_from_dict_restores_state(self, state):
        from_storage = {"mode": "LEARNING", "other_data": "BANANA"}

        output = state.from_dict(from_storage)

        assert len(output.keys()) == 1
        for key, value in output.items():
            assert key == "mode"
            assert value == AppState.LEARNING

        assert state._mode == AppState.LEARNING

    def test_from_dict_with_invalid_keys_throws_error(self, state):
        with pytest.raises(KeyError, match="Dictionary provided missing key 'mode'"):
            state.from_dict({"hello": AppState.NORMAL})

    def test_from_dict_with_invalid_mode_throws_error(self, state):
        with pytest.raises(ValueError, match="Invalid state provided"):
            state.from_dict({"mode": "BANANA"})
