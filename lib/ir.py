from machine import Pin
from time import sleep_ms

from ir_rx.nec import NEC_8
from ir_tx.nec import NEC


class IR_Reciever:
    def __init__(self):
        self.ir_rx_pin = NEC_8(Pin(10, Pin.IN), self.print_received)

    def print_received(self, data, address, *control):
        print(f"Address: {address:#04x}, Command: {data:#04x}, Control: {control}")
        print("---")


class IR_Transmitter:
    def __init__(self):
        self._address = 0x0004
        self._command = 0x0044
        self._previous = 1
        self._timeout = 500  # ms
        self._timeout_interval = 20  # ms

        self.button = Pin(14, Pin.IN, Pin.PULL_UP)
        self.ir_tx_pin = NEC(Pin(11, Pin.IN))

    def transmit_and_wait(self, address, command):
        self.ir_tx_pin.transmit(address, command)

        time_elapsed = 0
        while self.ir_tx_pin.busy() and time_elapsed < self._timeout:
            sleep_ms(self._timeout_interval)
            time_elapsed += self._timeout_interval

            if time_elapsed > self._timeout:
                raise TimeoutError("Transmission timeout")

    def handle_button_press(self):
        current = self.button.value()

        if self._previous == 1 and current == 0:
            print("sent 0")
            self.transmit_and_wait(self._address, 0x0041)
            print("sent 1")
            self.transmit_and_wait(self._address, self._command)
            print("sent 2")

        self._previous = current
