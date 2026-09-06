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
    fake_driver = types.ModuleType("universal_remote.lib.drivers.epd1in54_V2")

    class MockEPD:
        frame_buffer = MagicMock()
        update = lambda *_: None

    fake_driver.EPD = MockEPD

    sys.modules["universal_remote.lib.drivers.epd1in54_V2"] = fake_driver
