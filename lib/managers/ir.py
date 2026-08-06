from lib.managers.ir_protocol import IRProtocol
from lib.managers.reciever import IRReciever
from lib.managers.transmitter import IRTransmitter
from lib.managers.hardware import Buttons
from lib.managers.device import device
from lib.core.event_bus import event_bus
from lib.core.types import Events, Device


class IRManager:
    def __init__(self) -> None:
        """Initializes the IR manager, sets up the IR receiver and transmitter, and subscribes to button events."""
        self.last_recieved = None

        self._protocol = IRProtocol()
        self.rx = IRReciever(self._protocol)
        self.tx = IRTransmitter(4, self._protocol)

        self._event_bus = event_bus
        self._event_bus.subscribe(Events.BUTTON_PRESSED, self._on_button_press)
        self._event_bus.subscribe(Events.BUTTON_RELEASED, self._on_button_release)
        self._event_bus.subscribe(Events.SLEEP_IDLE, self._on_idle)
        self._event_bus.subscribe(Events.WAKE, self._on_wake)

    def _on_button_press(self, button_name, *args, **kwargs) -> None:
        """Handles button press events for IR-related actions such as changing protocols, transmitting commands, and recieving new commands."""
        if button_name == Buttons.CHANGE_IR_PROTOCOL:
            self.change_protocol()
            self._event_bus.publish(
                Events.IR_PROTOCOL_CHANGED, self._protocol.get_rx_name()
            )

        elif button_name == Buttons.TRANSMIT_IR:
            self.tx.send_hex_command(0x0041)
            self._event_bus.publish(Events.IR_TRANSMITTED, 0x0041)

        elif button_name == Buttons.MENU_SELECT:
            self.set_up_from_device(device.get())

    def _on_button_release(self, button_name, *args, **kwargs) -> None:
        """Handles button release events for IR-related actions."""
        if button_name == Buttons.TRANSMIT_IR:
            self.tx.send_hex_command(0x0000)
            self._event_bus.publish(Events.IR_TRANSMITTED, 0x0000)

    def _on_idle(self, *args, **kwargs):
        print("Turning rx off")
        self.rx.close()

    def _on_wake(self, *args, **kwargs):
        print("Turning rx on")
        self.rx.start()

    def change_protocol(self) -> None:
        """Changes the current IR protocol for both the receiver and transmitter."""
        self.rx.close()
        self._protocol.change_protocol(self.rx.log_received_ir)

    def set_up_from_device(self, device: Device) -> None:
        self.change_protocol()
