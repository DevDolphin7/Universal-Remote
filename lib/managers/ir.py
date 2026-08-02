from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff
from lib.managers.ir_protocol import IRProtocol
from lib.managers.hardware import Buttons, Hardware as HW
from lib.core.event_bus import event_bus, Events


class IR:
    def __init__(self):
        self.last_recieved = None
        self._button_learn_timeout = 10000  # ms
        self._button_learn_interval = 100  # ms

        self._protocol = IRProtocol()
        self.rx = IRReciever(self._protocol)
        self.tx = IRTransmitter(4, self._protocol)

        self._event_bus = event_bus
        self._event_bus.subscribe(Events.BUTTON_PRESSED, self.on_button_press)
        self._event_bus.subscribe(Events.BUTTON_RELEASED, self.on_button_release)

    def on_button_press(self, button_name):
        if button_name == Buttons.CHANGE_IR_PROTOCOL:
            self.change_protocol()

        if button_name == Buttons.TRANSMIT_IR:
            print("Transmitting IR command: 0x0041")
            self.tx.send_hex_command(0x0041)

        if button_name == Buttons.LEARN_IR:
            self.get_custom_button_data()

    def on_button_release(self, button_name):
        if button_name == Buttons.TRANSMIT_IR:
            self.tx.send_hex_command(-0x0001)

    def change_protocol(self):
        self.rx.close()
        self._protocol.change_protocol()
        self.rx.set_protocol()
        self.tx.set_protocol()

    def get_custom_button_data(self):
        commands = self.rx.last_commands
        timeout = 0

        print("here we go")
        while self.rx.last_commands[0]["index"] == commands[0]["index"]:
            sleep_ms(self._button_learn_interval)
            timeout += self._button_learn_interval
            if timeout > self._button_learn_timeout:
                TimeoutError("No IR data recieved prior to timeout")
        self.last_recieved = self.rx.last_commands
        print(f"set last recieved: {self.last_recieved}")

        return self.last_recieved


class IRReciever:
    def __init__(self, protocol: IRProtocol):
        self.protocol = protocol
        self._received_index = 0
        self._recieved_ticks = 0
        self.last_commands = []

        self.set_protocol()

    def print_received(self, data, address, *control):
        print(f"Address: {address:#04x}, Command: {data:#04x}, Control: {control}")
        print("---")
        if address is not None:
            ticks = ticks_ms()
            self._received_index += 1
            ticks_since_last_packet = ticks_diff(ticks, self._recieved_ticks)
            if ticks_since_last_packet < 250:
                self.last_commands.append(
                    {
                        "index": self._received_index,
                        "address": address,
                        "button1_command": data,
                        "ticks diff": ticks_since_last_packet,
                    }
                )
            else:
                self.last_commands = [
                    {
                        "index": self._received_index,
                        "address": address,
                        "button1_command": data,
                        "ticks diff": 0,
                    }
                ]
            if self._received_index > 255:
                self._received_index = 0

    def set_protocol(self):
        self.rx = self.protocol.get_rx()(HW.ir_rx, self.print_received)

    def close(self):
        self.rx.close()


class IRTransmitter:
    def __init__(self, address: int, protocol: IRProtocol):
        self._address = address
        self._previous = 1
        self._timeout = 500  # ms
        self._timeout_interval = 20  # ms

        self.protocol = protocol

        self.set_protocol()

    def set_protocol(self):
        self.tx = self.protocol.get_tx()(HW.ir_tx)

    def transmit_and_wait(self, address, command):
        self.tx.transmit(address, command)

        time_elapsed = 0
        while self.tx.busy() and time_elapsed < self._timeout:
            sleep_ms(self._timeout_interval)
            time_elapsed += self._timeout_interval

            if time_elapsed > self._timeout:
                raise TimeoutError("Transmission timeout")

    def send_hex_command(self, command: int):
        self.transmit_and_wait(self._address, command)
