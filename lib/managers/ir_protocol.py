from lib.drivers.ir_rx.nec import NEC_8, NEC_16, SAMSUNG
from lib.drivers.ir_rx.philips import RC5_IR, RC6_M0
from lib.drivers.ir_rx.sony import SONY_12, SONY_15, SONY_20
from lib.drivers.ir_rx.mce import MCE
from lib.drivers.ir_tx.nec import NEC as NEC_TX
from lib.drivers.ir_tx.philips import RC5 as RC5_TX, RC6_M0 as RC6_M0_TX
from lib.drivers.ir_tx.sony import (
    SONY_12 as SONY_12_TX,
    SONY_15 as SONY_15_TX,
    SONY_20 as SONY_20_TX,
)
from lib.drivers.ir_tx.mce import MCE as MCE_TX
from lib.managers.hardware import Hardware


class IRProtocol:
    def __init__(self, start_index=0) -> None:
        """Initializes the IRProtocol with a starting index and sets up the available RX and TX protocols."""
        self._index = start_index
        self._rx_protocols = [
            ("NEC_8", NEC_8),
            ("NEC_16", NEC_16),
            ("SAMSUNG", SAMSUNG),
            ("RC5_IR", RC5_IR),
            ("RC6_M0", RC6_M0),
            ("SONY_12", SONY_12),
            ("SONY_15", SONY_15),
            ("SONY_20", SONY_20),
            ("MCE", MCE),
        ]
        self._tx_protocols = [
            ("NEC_8", NEC_TX),
            ("NEC_16", NEC_TX),
            ("SAMSUNG", NEC_TX),
            ("RC5_IR", RC5_TX),
            ("RC6_M0", RC6_M0_TX),
            ("SONY_12", SONY_12_TX),
            ("SONY_15", SONY_15_TX),
            ("SONY_20", SONY_20_TX),
            ("MCE", MCE_TX),
        ]

    def get_rx_name(self) -> str:
        """Returns the name of the current RX protocol."""
        return self._rx_protocols[self._index][0]

    def get_rx(
        self,
    ) -> type[
        NEC_8 | NEC_16 | SAMSUNG | RC5_IR | RC6_M0 | SONY_12 | SONY_15 | SONY_20 | MCE
    ]:
        """Returns the class of the current RX protocol."""
        return self._rx_protocols[self._index][1]

    def get_tx_name(self) -> str:
        """Returns the name of the current TX protocol."""
        return self._tx_protocols[self._index][0]

    def get_tx(
        self,
    ) -> type[
        NEC_TX | RC5_TX | RC6_M0_TX | SONY_12_TX | SONY_15_TX | SONY_20_TX | MCE_TX
    ]:
        """Returns the class of the current TX protocol."""
        return self._tx_protocols[self._index][1]

    def change_protocol(self, callback) -> None:
        """Changes the current IR protocol for both the receiver and transmitter."""
        self._index += 1
        if self._index >= len(self._rx_protocols):
            self._index = 0

        self.set_rx(callback)
        self.set_tx()

        print(f"Changed protocol to Rx: {self.get_rx()} and Tx: {self.get_tx()}")

    def set_rx(self, callback) -> None:
        """Sets the RX protocol to the current index."""
        self.rx = self.get_rx()(Hardware.ir_rx, callback)

    def set_tx(self) -> None:
        """Sets the TX protocol to the current index."""
        self.tx = self.get_tx()(Hardware.ir_tx)
