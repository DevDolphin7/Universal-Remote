from ir_rx.nec import NEC_8, NEC_16, SAMSUNG
from ir_rx.philips import RC5_IR, RC6_M0
from ir_rx.sony import SONY_12, SONY_15, SONY_20
from ir_rx.mce import MCE
from ir_tx.nec import NEC as NEC_TX
from ir_tx.philips import RC5 as RC5_TX, RC6_M0 as RC6_M0_TX
from ir_tx.sony import (
    SONY_12 as SONY_12_TX,
    SONY_15 as SONY_15_TX,
    SONY_20 as SONY_20_TX,
)
from ir_tx.mce import MCE as MCE_TX


class IRProtocol:
    def __init__(self, start_index=0):
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
        return self._rx_protocols[self._index][0]

    def get_rx(self) -> type:
        return self._rx_protocols[self._index][1]

    def set_index_from_rx(self, rx_name: str):
        for index, item in enumerate(self._rx_protocols):
            if rx_name == item[0]:
                self._index = index

    def get_tx_name(self) -> str:
        return self._tx_protocols[self._index][0]

    def get_tx(self) -> type:
        return self._tx_protocols[self._index][1]

    def change_protocol(self):
        self._index += 1
        if self._index >= len(self._rx_protocols):
            self._index = 0

        print(f"Changed protocol to Rx: {self.get_rx()} and Tx: {self.get_tx()}")

        return self.get_rx()
