from time import ticks_ms, ticks_diff
from universal_remote.lib.core.types import IRData
from universal_remote.lib.drivers.protocol_registry import IRProtocolInterface


class Reciever:
    def __init__(self, protocol: IRProtocolInterface) -> None:
        """Initializes the IR receiver with a given protocol and sets up the callback for received data."""
        self.last_commands = []

        self._last_rx_ticks = 0

        self.set_protocol(protocol)

    def set_protocol(self, protocol: IRProtocolInterface) -> None:
        """Set the protocol for the IR reciver"""
        try:
            self.close()
        finally:
            self._protocol = protocol
            self.start()

    def start(self) -> None:
        """Start the IR receiver listening"""
        self._protocol.set_rx(self.handle_ir_data)

    def handle_ir_data(self, data, address, *args, **kwargs) -> None:
        """Callback function to handle received IR data, printing it and storing it in the last_commands list."""
        if address is None:
            return

        if len(self.last_commands) > 1:
            self.last_commands.pop(1)

        self.last_commands.insert(
            0,
            IRData(
                address,
                data,
                self._protocol.get_rx_name(),
                ticks_diff(ticks_ms(), self._last_rx_ticks),
            ),
        )

        self._last_rx_ticks = ticks_ms()

        # Publish event

    def close(self) -> None:
        """Closes the IR receiver."""
        self._protocol.rx.close()
