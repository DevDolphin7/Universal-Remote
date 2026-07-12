from machine import Pin
from time import sleep_ms
from ir_protocol import IRProtocol
from hardware import HW


class IR:
    def __init__(self):
        self._previous = 1
        self._protocol = IRProtocol()
        self.rx = IRReciever(self._protocol)
        self.tx = IRTransmitter(4, self._protocol)

        self.button = HW.ir_protocol_button

    def handle_button_press(self):
        current = self.button.value()

        if self._previous == 1 and current == 0:
            self.rx.close()
            self._protocol.change_protocol()
            self.rx.set_rx()
            self.tx.set_tx()
        self._previous = current


class IRReciever:
    def __init__(self, protocol: IRProtocol):
        self.protocol = protocol

        self.set_rx()

    def print_received(self, data, address, *control):
        print(f"Address: {address:#04x}, Command: {data:#04x}, Control: {control}")
        print("---")

    def set_rx(self):
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

        self.set_tx()
        self.button = HW.ir_tx_button1

    def set_tx(self):
        self.tx = self.protocol.get_tx()(HW.ir_tx)

    def transmit_and_wait(self, address, command):
        self.tx.transmit(address, command)

        time_elapsed = 0
        while self.tx.busy() and time_elapsed < self._timeout:
            sleep_ms(self._timeout_interval)
            time_elapsed += self._timeout_interval

            if time_elapsed > self._timeout:
                raise TimeoutError("Transmission timeout")

    def handle_button_press(self, command: int):
        current = self.button.value()

        if self._previous == 1 and current == 0:
            self.transmit_and_wait(self._address, 0x0041)
            self.transmit_and_wait(self._address, command)

        self._previous = current
