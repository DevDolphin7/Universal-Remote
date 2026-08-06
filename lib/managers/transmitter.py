from time import sleep_ms
from lib.managers.ir_protocol import IRProtocol


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
