from lib.managers.storage import Storage
from lib.managers.hardware import Buttons
from lib.core.event_bus import event_bus
from lib.core.types import Device, Events, IRData


class DeviceManager:
    def __init__(self):
        self._storage = Storage("/lib/storage/remotes.json")
        self.devices = self._storage.load_devices()

        self.learn_mode = False
        self._index = 0

        self._event_bus = event_bus
        self._event_bus.subscribe(Events.IR_RECEIVED, self.learn_button)
        self._event_bus.subscribe(Events.BUTTON_PRESSED, self._on_button_press)
        self._event_bus.subscribe(Events.SLEEP_IDLE, self._on_idle)
        self._event_bus.subscribe(Events.BUTTON_LEARNED, self.stop_learning)

    def _on_button_press(self, button_name, *args, **kwargs) -> None:
        if button_name == Buttons.MENU_SELECT:
            self.change()

        elif button_name == Buttons.LEARN_IR:
            self.add_remote()
            print(
                [
                    (
                        device.address,
                        device.button1_press_command,
                        device.button1_release_command,
                    )
                    for device in self.devices
                ],
                "------------------",
                sep="\n",
            )

    def _on_idle(self, *args, **kwargs):
        self.learn_mode = False

    def get(self) -> Device:
        return self.devices[self._index]

    def get_index(self) -> int:
        return self._index

    def get_from_index(self, index) -> Device:
        return self.devices[index]

    def get_names(self) -> list[str]:
        return [device.device_name for device in self.devices]

    def change(self) -> None:
        self._index += 1
        if self._index >= len(self.devices):
            self._index = 0

    def update_and_save(self, updated_device: Device) -> Device:
        self.devices[self._index] = updated_device
        self._storage.save_devices(self.devices)
        return self.devices[self._index]

    def add_remote(self):
        self.learn_mode = True

    def learn_button(self, ir_signals: list[IRData]):
        if not self.learn_mode or not len(ir_signals) > 1:
            return

        device = self.get()
        last_signal = ir_signals[1]
        prior_signal = ir_signals[0]

        device.update(last_signal)

        if last_signal.ticks_diff < 200:
            device.set_press_command(prior_signal.command)
            device.set_release_command(last_signal.command)
        else:
            device.set_press_command(last_signal.command)

        self.update_and_save(device)
        self._event_bus.publish(Events.BUTTON_LEARNED)

    def stop_learning(self, *args, **kwargs):
        print("Learned a button")
        self.learn_mode = False


device = DeviceManager()
