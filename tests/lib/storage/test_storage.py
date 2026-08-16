import json
import pytest
from universal_remote.lib.storage.storage import Storage
from universal_remote.lib.core.types import AppState


@pytest.fixture
def storage(tmp_path):
    state_file_path = tmp_path / "state.json"
    devices_file_path = tmp_path / "devices.json"

    return Storage(state_file_path, devices_file_path)


@pytest.fixture
def storage_saved_state(storage):
    with open(storage.state_path, "w") as file:
        json.dump(AppState.NORMAL, file)

    return storage


@pytest.fixture
def devices():
    return [
        {
            "id": 0,
            "device_name": "TV Remote",
            "protocol_name": "NEC_8",
            "address": 44,
            "commands": {
                "nav_ok": {"press": 4, "release": 0},
                "nav_down": {"press": 3, "release": 0},
            },
        },
        {
            "id": 1,
            "device_name": "Lights",
            "protocol_name": "NEC_16",
            "address": 22,
            "commands": {
                "nav_up": {"press": 2, "release": 10},
                "nav_lef": {"press": 1, "release": 20},
            },
        },
    ]


@pytest.fixture
def storage_saved_devices(storage, devices):
    with open(storage.devices_path, "w") as file:
        json.dump(devices, file)

    return storage


class TestState:
    class TestSaveState:
        def test_save_state_writes_state(self, storage):
            expected = AppState.NORMAL

            storage.save_state(expected)

            assert storage.state_path.exists()

            with open(storage.state_path) as files:
                data = json.load(files)

            assert data == expected

        def test_save_invalid_state_raises_error(self, storage):
            with pytest.raises(ValueError, match="Invalid state"):
                storage.save_state("BANANA")

    class TestLoadState:
        def test_load_state_returns_saved_state(self, storage_saved_state):
            state = storage_saved_state.load_state()

            assert state == AppState.NORMAL

        def test_load_state_uses_default_when_missing(self, storage):
            state = storage.load_state()

            assert state == AppState.NORMAL

        def test_load_default_state_on_invalid_data(self, storage):
            with open(storage.state_path, "w") as file:
                json.dump("BANANA", file)

            state = storage.load_state()

            assert state == AppState.NORMAL

    class TestSaveAndLoadState:

        def test_state_saves_and_loads_through_persistent_memory(self, storage):
            expected_one = AppState.NORMAL
            storage.save_state(expected_one)
            assert storage.state_path.exists()
            with open(storage.state_path) as file:
                data = json.load(file)
            assert data == expected_one
            output = storage.load_state()
            assert output == expected_one

            expected_two = AppState.LEARNING
            storage.save_state(expected_two)
            assert storage.state_path.exists()
            with open(storage.state_path) as file:
                data = json.load(file)
            assert data == expected_two
            output = storage.load_state()
            assert output == expected_two


class TestDevices:
    class TestSaveDevices:
        def test_save_devices_writes_devices(self, storage, devices):
            storage.save_devices(devices)

            assert storage.devices_path.exists()

            with open(storage.devices_path) as file:
                output_devices = json.load(file)

            assert len(output_devices) > 0

            device_keys = devices[0].keys()
            for device in output_devices:
                for key, value in device.items():
                    assert key in device_keys
                    assert type(value) == type(devices[0][key])

        def test_any_invalid_remote_is_not_saved(self, storage, devices):
            devices.append({"id": 777})
            storage.save_devices(devices)

            assert storage.devices_path.exists()

            with open(storage.devices_path) as file:
                output_devices = json.load(file)

            assert len(output_devices) > 0

            device_keys = devices[0].keys()
            for device in output_devices:
                for key, value in device.items():
                    assert key in device_keys
                    assert type(value) == type(devices[0][key])

                    if key == "id":
                        assert value != 777

    """
    test_load_devices_returns_saved_devices
    test_load_devices_returns_empty_list_on_failure
    test_load_devices_rejects_invalid_data
    test_devices_saves_and_loads_through_persistent_memory
    """

    class TestLoadDevices:
        def test_load_devices_returns_saved_devices(
            self, storage_saved_devices, devices
        ):
            output_devices = storage_saved_devices.load_devices()

            assert len(output_devices) > 0

            valid_keys = devices[0]
            for device in output_devices:
                for key, value in device.items():
                    assert key in valid_keys
                    assert type(value) == type(devices[0][key])

        def test_load_devices_returns_empty_list_on_failure(self, storage):
            output_devices = storage.load_devices()

            assert len(output_devices) == 0
            assert isinstance(output_devices, list)

        def test_load_devices_rejects_invalid_data(self, storage):
            with open(storage.devices_path, "w") as file:
                json.dump([{"id": 1}], file)

            output_devices = storage.load_devices()

            assert len(output_devices) == 0
            assert isinstance(output_devices, list)

    class TestSaveAndLoadDevices:

        def test_devices_saves_and_loads_through_persistent_memory(
            self, storage, devices
        ):
            expected_one = devices
            storage.save_devices(expected_one)
            assert storage.devices_path.exists()
            with open(storage.devices_path) as file:
                output_devices = json.load(file)
            assert len(output_devices) == len(devices)
            valid_keys = devices[0]
            for device in output_devices:
                for key, value in device.items():
                    assert key in valid_keys
                    assert type(value) == type(devices[0][key])

            expected_two = [devices[0]]
            storage.save_devices(expected_two)
            output_devices = storage.load_devices()
            assert len(output_devices) == 1
            for device in output_devices:
                for key, value in device.items():
                    assert key in valid_keys
                    assert type(value) == type(devices[0][key])
