from time import ticks_ms, ticks_diff
from lib.managers.ir_protocol import IRProtocol
from lib.core.event_bus import event_bus
from lib.core.types import Events, IRData


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
