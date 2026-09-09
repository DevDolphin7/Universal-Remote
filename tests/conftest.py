import sys, types
import pytest
from unittest.mock import MagicMock


@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset the mocks before each test."""
    yield
    sys.modules[
        "universal_remote.lib.drivers.epd1in54_V2"
    ].EPD.frame_buffer.reset_mock()


def pytest_configure():
    fake_epd_driver = types.ModuleType("universal_remote.lib.drivers.epd1in54_V2")

    class MockEPD:
        frame_buffer = MagicMock(name="EPD")
        update = lambda *_: None

    fake_epd_driver.EPD = MockEPD
    sys.modules["universal_remote.lib.drivers.epd1in54_V2"] = fake_epd_driver

    fake_hardware = types.ModuleType("universal_remote.lib.drivers.hardware")

    class MockHardware:
        vsys = MagicMock(spec=["read_u16"])
        vsys.read_u16.return_value = 25000

    fake_hardware.Hardware = MockHardware
    sys.modules["universal_remote.lib.drivers.hardware"] = fake_hardware


@pytest.fixture
def mock_vsys():
    return sys.modules["universal_remote.lib.drivers.hardware"].Hardware.vsys
