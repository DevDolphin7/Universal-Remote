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
    # Mock the EPD module
    fake_epd_driver = types.ModuleType("universal_remote.lib.drivers.epd1in54_V2")

    class MockEPD:
        frame_buffer = MagicMock(name="EPD")
        update = lambda *_: None

    fake_epd_driver.EPD = MockEPD
    sys.modules["universal_remote.lib.drivers.epd1in54_V2"] = fake_epd_driver

    # Mock the utime module
    fake_utime = types.ModuleType("utime")
    fake_utime.sleep_ms = lambda _: None
    fake_utime.ticks_ms = lambda _: 123456789
    fake_utime.ticks_diff = lambda a, b: 1000
    sys.modules["utime"] = fake_utime

    # Mock the Hardware driver
    fake_hardware = types.ModuleType("universal_remote.lib.drivers.hardware")

    class MockHardware:
        vsys = MagicMock(spec=["read_u16"])

        mode = MagicMock(spec=["value"])

        vol_up = MagicMock(spec=["value"])
        vol_down = MagicMock(spec=["value"])
        ch_up = MagicMock(spec=["value"])
        ch_down = MagicMock(spec=["value"])

        nav_up = MagicMock(spec=["value"])
        nav_right = MagicMock(spec=["value"])
        nav_down = MagicMock(spec=["value"])
        nav_left = MagicMock(spec=["value"])
        nav_ok = MagicMock(spec=["value"])

    fake_hardware.Hardware = MockHardware
    sys.modules["universal_remote.lib.drivers.hardware"] = fake_hardware

    # Mock the IRProtocolInterface driver
    fake_protocol_registry = types.ModuleType(
        "universal_remote.lib.drivers.protocol_registry"
    )

    class MockIRProtocolInterface:
        change_protocol_to_named = MagicMock()

    fake_protocol_registry.IRProtocolInterface = MockIRProtocolInterface
    sys.modules["universal_remote.lib.drivers.protocol_registry"] = (
        fake_protocol_registry
    )


@pytest.fixture
def mock_vsys():
    return sys.modules["universal_remote.lib.drivers.hardware"].Hardware.vsys


@pytest.fixture
def mock_mode_button():
    return sys.modules["universal_remote.lib.drivers.hardware"].Hardware.mode
