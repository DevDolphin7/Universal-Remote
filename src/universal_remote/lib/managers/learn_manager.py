from utime import ticks_ms, ticks_diff
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.managers.remote_manager import Remote
from universal_remote.lib.drivers.protocol_registry import IRProtocolInterface
from universal_remote.lib.core.types import Events, IRData, AllButtons, Commands, Device


class Learn:
    def __init__(self, event_bus: EventBus, remote: Remote) -> None:
        self.event_bus = event_bus
        self.remote = remote

        self.latest_ir_data: list[IRData] = []
        self._last_rx_ticks = 0
        self._active_button = AllButtons.CH_UP
        self._blank_remote = None

        self.set_protocol_interface()

        event_bus.subscribe(Events.BUTTON_RELEASED, self.handle_button_release)
        event_bus.subscribe(Events.IR_RECEIVED, self.handle_ir_received)
        event_bus.subscribe(Events.NEW_DEVICE, self.handle_new_device)

    def request_new_remote(self) -> None:
        self.event_bus.publish(Events.NEW_DEVICE_REQUESTED)

    def set_protocol_interface(self) -> None:
        remote = self.remote.get_active_remote()

        self._protocol_interface = IRProtocolInterface()
        self._protocol_interface.change_protocol_to_named(
            remote.protocol_name, self.receive_ir
        )

    def receive_ir(self, data: int, address: int, ctrl: int) -> None:
        """Callback function to handle received IR data, printing it and storing it in the latest_ir_data list."""
        if address is None:
            return

        if len(self.latest_ir_data) > 1:
            self.latest_ir_data.pop(1)

        current_ticks = ticks_ms()
        ticks_since_last = ticks_diff(current_ticks, self._last_rx_ticks)

        self.latest_ir_data.insert(
            0,
            IRData(
                address,
                data,
                self._protocol_interface.get_rx_name(),
                ticks_since_last,
            ),
        )

        self._last_rx_ticks = current_ticks

        if ticks_since_last < 200:
            publish_data = [self.latest_ir_data[0]]
        else:
            publish_data = self.latest_ir_data

        self.event_bus.publish(Events.IR_RECEIVED, publish_data)

    def handle_ir_received(self, datas: list[IRData]) -> None:
        if self._blank_remote:
            remote = self._blank_remote
            self._blank_remote = None
        else:
            remote = self.remote.get_active_remote()

        remote.address = datas[0].address
        remote.protocol_name = datas[0].protocol_name

        if len(datas) == 1:
            remote.commands[self._active_button] = Commands(press=datas[0].command)
        elif len(datas) == 2:
            remote.commands[self._active_button] = Commands(
                press=datas[0].command, release=datas[1].command
            )

        if remote.name == "Add New":
            remote.name = "Remote " + str(len(self.remote.get_all_remote_names()))
            self.event_bus.publish(Events.DEVICE_LEARNED, remote)
        else:
            self.event_bus.publish(Events.BUTTON_LEARNED, self._active_button, remote)

    def handle_button_release(self, button: str) -> None:
        if button in AllButtons.PROGRAMMABLE:
            self._active_button = button

    def handle_new_device(self, device: Device) -> None:
        self._blank_remote = device
