import pytest
from unittest.mock import Mock
from universal_remote.lib.core.event_bus import EventBus


@pytest.fixture
def bus() -> EventBus:
    return EventBus()


@pytest.fixture
def handler() -> Mock:
    return Mock()


class TestSubscribe:
    def test_can_subscribe_handler_to_event(self, bus, handler):
        bus.subscribe("BUTTON_PRESS", handler)

        assert bus._subscribers["BUTTON_PRESS"][0] is handler

    def test_same_handler_cant_subscribe_again(self, bus, handler):
        bus.subscribe("BUTTON_PRESS", handler)
        bus.subscribe("BUTTON_PRESS", handler)
        bus.subscribe("BUTTON_PRESS", handler)

        assert len(bus._subscribers["BUTTON_PRESS"]) == 1

        bus.publish("BUTTON_PRESS")

        handler.assert_called_once()


class TestPublish:
    def test_publishing_event_calls_handler(self, bus, handler):
        bus.subscribe("BUTTON_PRESS", handler)
        bus.publish("BUTTON_PRESS")

        handler.assert_called_once()

    def test_event_calls_handler_with_args(self, bus, handler):
        bus.subscribe("BUTTON_PRESS", handler)
        bus.publish("BUTTON_PRESS", "data", "test", hello="world")

        handler.assert_called_once_with("data", "test", hello="world")

    def test_multiple_handlers_subscribe_to_event(self, bus, handler):
        handler_one = handler
        handler_two: Mock = Mock()

        bus.subscribe("BUTTON_PRESS", handler_one)
        bus.subscribe("BUTTON_PRESS", handler_two)

        bus.publish("BUTTON_PRESS", "data")

        handler_one.assert_called_once_with("data")
        handler_two.assert_called_once_with("data")

    def test_different_events_do_not_cross_fire(self, bus, handler):
        handler_one = handler
        handler_two: Mock = Mock()

        bus.subscribe("BUTTON_PRESS", handler_one)
        bus.subscribe("BUTTON_RELEASE", handler_two)

        bus.publish("BUTTON_PRESS", "data")

        handler_one.assert_called_once_with("data")
        handler_two.assert_not_called()

    def test_publishing_event_with_no_subscribers_does_nothing(self, bus, handler):
        bus.publish("BUTTON_PRESS", "data")

        handler.assert_not_called()


class TestUnsubscribe:
    def test_handler_can_be_undsubscribed(self, bus, handler):
        bus.subscribe("BUTTON_PRESS", handler)
        bus.unsubscribe("BUTTON_PRESS", handler)

        assert len(bus._subscribers) is 0

        bus.publish("BUTTON_PRESS", "data")

        handler.assert_not_called()
