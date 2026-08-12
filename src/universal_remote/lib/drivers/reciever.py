from time import ticks_ms, ticks_diff
from universal_remote.lib.core.types import IRData
from lib.drivers.protocol_registry import IRProtocol


class Reciever:
    def __init__(self, protocol: IRProtocol) -> None:
        """Initializes the IR receiver with a given protocol and sets up the callback for received data."""
        self.last_commands = []

        self._recieved_ticks = 0
        self._last_receievd_ticks = 0

        self.set_protocol(protocol)

    def set_protocol(self, protocol: IRProtocol) -> None:
        try:
            self.close()
        finally:
            self._protocol = protocol
            self.start()

    def start(self) -> None:
        self._protocol.set_rx(self.log_received_ir)

    def log_received_ir(self, data, address, *control) -> None:
        """Callback function to handle received IR data, printing it and storing it in the last_commands list."""
        if address is not None:
            ticks = ticks_ms()
            ticks_since_last_packet = ticks_diff(ticks, self._recieved_ticks)
            if ticks_since_last_packet < 250:
                self.last_commands.append(
                    {
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
                        ticks_diff(ticks_ms(), self._last_receievd_ticks),
                    ),
                )
                self._last_receievd_ticks = ticks_ms()

    def close(self) -> None:
        """Closes the IR receiver."""
        self._protocol.rx.close()
