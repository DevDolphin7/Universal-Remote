from lib.drivers.ir_rx.nec import NEC_8, NEC_16, SAMSUNG
from lib.drivers.ir_rx.philips import RC5_IR, RC6_M0
from lib.drivers.ir_rx.sony import SONY_12, SONY_15, SONY_20
from lib.drivers.ir_rx.mce import MCE
from lib.drivers.ir_tx.nec import NEC as NEC_TX
from lib.drivers.ir_tx.philips import RC5 as RC5_TX, RC6_M0_TX
from lib.drivers.ir_tx.sony import (
    SONY_12 as SONY_12_TX,
    SONY_15 as SONY_15_TX,
    SONY_20 as SONY_20_TX,
)
from lib.drivers.ir_tx.mce import MCE_TX
from lib.drivers.hardware import Hardware

RxProtocolType = type[
    NEC_8 | NEC_16 | SAMSUNG | RC5_IR | RC6_M0 | SONY_12 | SONY_15 | SONY_20 | MCE
]

TxProtocolType = type[
    NEC_TX | RC5_TX | RC6_M0_TX | SONY_12_TX | SONY_15_TX | SONY_20_TX | MCE_TX
]


class RxProtocol:
    def __init__(
        self,
        name: str,
        protocol: RxProtocolType,
    ):
        self.name = name
        self.protocol = protocol


class TxProtocol:
    def __init__(
        self,
        name: str,
        protocol: TxProtocolType,
    ):
        self.name = name
        self.protocol = protocol


class IRProtocol:
    def __init__(self, start_index: int = 0) -> None:
        """Initializes the IRProtocol with a starting index and sets up the available RX and TX protocols."""
        self.index: int = start_index
        self._rx_protocols = [
            RxProtocol("NEC_8", NEC_8),
            RxProtocol("NEC_16", NEC_16),
            RxProtocol("SAMSUNG", SAMSUNG),
            RxProtocol("RC5_IR", RC5_IR),
            RxProtocol("RC6_M0", RC6_M0),
            RxProtocol("SONY_12", SONY_12),
            RxProtocol("SONY_15", SONY_15),
            RxProtocol("SONY_20", SONY_20),
            RxProtocol("MCE", MCE),
        ]
        self._tx_protocols = [
            TxProtocol("NEC_8", NEC_TX),
            TxProtocol("NEC_16", NEC_TX),
            TxProtocol("SAMSUNG", NEC_TX),
            TxProtocol("RC5_IR", RC5_TX),
            TxProtocol("RC6_M0", RC6_M0_TX),
            TxProtocol("SONY_12", SONY_12_TX),
            TxProtocol("SONY_15", SONY_15_TX),
            TxProtocol("SONY_20", SONY_20_TX),
            TxProtocol("MCE", MCE_TX),
        ]

    def get_rx_name(self) -> str:
        """Returns the name of the current RX protocol."""
        return self._rx_protocols[self.index].name

    def get_rx(self) -> RxProtocolType:
        """Returns the class of the current RX protocol."""
        return self._rx_protocols[self.index].protocol

    def get_tx_name(self) -> str:
        """Returns the name of the current TX protocol."""
        return self._tx_protocols[self.index].name

    def get_tx(self) -> TxProtocolType:
        """Returns the class of the current TX protocol."""
        return self._tx_protocols[self.index].protocol

    def next_protocol(self, rx_callback) -> None:
        """Changes the current IR protocol for both the receiver and transmitter."""
        self.index += 1
        if self.index >= len(self._rx_protocols):
            self.index = 0

        self.set_rx(rx_callback)
        self.set_tx()

    def change_protocol_to_named(self, protocol_name, rx_callback) -> None:
        """Changes the current IR protocol for both the receiver and transmitter."""
        protocol_index = None
        for index, protocol in enumerate(self._tx_protocols):
            if protocol_name == protocol.name:
                protocol_index = index

        if protocol_index == None:
            raise IndexError("Protocol name provided is not recognised")

        self.index = protocol_index

        self.set_rx(rx_callback)
        self.set_tx()

    def set_rx(self, callback) -> None:
        """Sets the RX protocol to the current index."""
        self.rx = self.get_rx()(Hardware.ir_rx, callback)

    def set_tx(self) -> None:
        """Sets the TX protocol to the current index."""
        self.tx = self.get_tx()(Hardware.ir_tx)
