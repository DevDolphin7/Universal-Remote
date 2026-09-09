import pytest
from unittest.mock import Mock
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.managers.power_manager import Power
from universal_remote.lib.core.types import Events


@pytest.fixture
def event_bus():
    return EventBus()


class TestPower:
    def test_on_battery_charge_level_change_publish_level(self, event_bus, mock_vsys):
        mock: Mock = Mock()
        event_bus.subscribe(Events.BATTERY_LEVEL_CHANGED, mock)

        mock_vsys.read_u16.return_value = 27800
        power = Power(event_bus)

        mock_vsys.read_u16.return_value = 24300
        power.update()

        mock.assert_called_once_with(2)

    def test_on_battery_voltage_low_publish_low_battery(self, event_bus, mock_vsys):
        mock: Mock = Mock()
        event_bus.subscribe(Events.LOW_BATTERY, mock)

        mock_vsys.read_u16.return_value = 22800
        power = Power(event_bus)

        mock_vsys.read_u16.return_value = 20800
        power.update()

        mock.assert_called_once()
        assert power.is_low()
