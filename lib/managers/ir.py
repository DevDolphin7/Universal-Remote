from time import sleep_ms, ticks_ms, ticks_diff
from lib.core.event_bus import event_bus
from lib.managers.ir_protocol import IRProtocol
from lib.managers.hardware import Buttons
from lib.managers.device import device
from lib.core.types import Events, Device, IRData


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
        print(self._protocol.get_rx_name())


class IRReciever:
    def __init__(self, protocol: IRProtocol) -> None:
        """Initializes the IR receiver with a given protocol and sets up the callback for received data."""
        self.last_commands = []

        self._protocol = protocol
        self._received_index = 0
        self._recieved_ticks = 0
        self._last_receievd_ticks = 0

        self._event_bus = event_bus

        self.start()

    def start(self) -> None:
        self._protocol.set_rx(self.log_received_ir)

    def log_received_ir(self, data, address, *control) -> None:
        """Callback function to handle received IR data, printing it and storing it in the last_commands list."""
        print(data, "<<<<<<")
        if address is not None:
            ticks = ticks_ms()
            self._received_index += 1
            ticks_since_last_packet = ticks_diff(ticks, self._recieved_ticks)
            if ticks_since_last_packet < 250:
                self.last_commands.append(
                    {
                        "index": self._received_index,
                        "address": address,
                        "command": data,
                        "ticks diff": ticks_since_last_packet,
                    }
                )
            else:
                if len(self.last_commands) > 1:
                    self.last_commands.pop(1)
                self.last_commands.insert(
                    0,
                    IRData(
                        address,
                        data,
                        self._protocol.get_rx_name(),
                        self._received_index,
                        ticks_diff(ticks_ms(), self._last_receievd_ticks),
                    ),
                )
                self._last_receievd_ticks = ticks_ms()

            if self._received_index > 255:
                self._received_index = 0

            self._event_bus.publish(Events.IR_RECEIVED, self.last_commands)

    def close(self) -> None:
        """Closes the IR receiver."""
        self._protocol.rx.close()


class IRTransmitter:
    def __init__(self, address: int, protocol: IRProtocol) -> None:
        """Initializes the IR transmitter with a given address and protocol."""
        self._address = address
        self._previous = 1
        self._timeout = 500  # ms
        self._timeout_interval = 20  # ms

        self._protocol = protocol
        self._protocol.set_tx()

    def transmit_and_wait(self, address, command) -> None:
        """Transmits an IR command and waits for the transmission to complete, raising a TimeoutError if it takes too long."""
        self._protocol.tx.transmit(address, command)

        time_elapsed = 0
        while self._protocol.tx.busy() and time_elapsed < self._timeout:
            sleep_ms(self._timeout_interval)
            time_elapsed += self._timeout_interval

            if time_elapsed > self._timeout:
                raise TimeoutError("Transmission timeout")

    def send_hex_command(self, command: int) -> None:
        """Sends a hexadecimal IR command"""
        self.transmit_and_wait(self._address, command)
