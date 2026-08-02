from time import sleep_ms
from machine import SPI, Pin
from framebuf import FrameBuffer, MONO_HLSB
from lib.managers.hardware import Hardware as HW

"""
Driver for Waveshare e-Paper 1.54in V2

Note: This is for V2, check for V2 sticker on back of module.

Datasheet: https://files.waveshare.com/upload/e/e5/1.54inch_e-paper_V2_Datasheet.pdf
"""


class EPD:
    BUSY = const(1)
    SOFTWARE_RESET = const(0x12)
    DRIVER_OUTPUT = const(0x01)
    DATA_ENTRY_MODE = const(0x11)
    BORDER_WAVE_FORM = const(0x3C)
    ACTIVATE_DISPLAY_UPDATE_SEQUENCE = const(0x20)
    DISPLAY_UPDATE_SEQUENCE_OPTION = const(0x22)
    SET_RAM_X_ADDRESS_START_END_POSITION = const(0x44)
    SET_RAM_Y_ADDRESS_START_END_POSITION = const(0x45)
    SET_RAM_X_ADDRESS_COUNTER = const(0x4E)
    SET_RAM_Y_ADDRESS_COUNTER = const(0x4F)
    WRITE_RAM_BW = const(0x24)
    DEEP_SLEEP_MODE = const(0x10)

    def __init__(
        self,
        spi=SPI(0, baudrate=2000000, sck=HW.epd_sdk, mosi=HW.epd_mosi),
        cs=HW.epd_cs,
        dc=HW.epd_dc,
        rst=HW.epd_rst,
        busy=HW.epd_busy,
        width=200,
        height=200,
    ):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.busy = busy
        self.width = width
        self.height = height

        cs.init(mode=Pin.OUT, value=1)
        dc.init(mode=Pin.OUT, value=0)
        rst.init(mode=Pin.OUT, value=1)
        busy.init(mode=Pin.IN)

        h_pixels = int((self.width / 8) if (self.width % 8 == 0) else (self.width / 9))

        self.buffer = bytearray(h_pixels * self.height)
        self.frame_buffer = FrameBuffer(self.buffer, self.width, self.height, MONO_HLSB)

        self._initialize()

    def _initialize(self):
        self.reset()
        self.wait()
        self._command(SOFTWARE_RESET)
        self.wait()

        self._command(DRIVER_OUTPUT, b"\xc7\x00\x01")
        self._command(DATA_ENTRY_MODE, b"\x01")

        self._set_windows(0, self.height - 1, self.width - 1, 0)

        self._command(BORDER_WAVE_FORM, b"\x01")
        self._command(0x18, b"\x80")
        self._command(DISPLAY_UPDATE_SEQUENCE_OPTION, b"\xb1")
        self._command(ACTIVATE_DISPLAY_UPDATE_SEQUENCE)
        self._set_cursor(0, self.height - 1)
        self.wait()

        self.clear()

    def _set_windows(self, xstart, ystart, xend, yend):
        self._command(
            SET_RAM_X_ADDRESS_START_END_POSITION,
            bytearray([(xstart >> 3) & 0xFF, (xend >> 3) & 0xFF]),
        )
        self._command(
            SET_RAM_Y_ADDRESS_START_END_POSITION,
            bytearray(
                [ystart & 0xFF, (ystart >> 8) & 0xFF, yend & 0xFF, (yend >> 8) & 0xFF]
            ),
        )

    def _set_cursor(self, xstart, ystart):
        self._command(SET_RAM_X_ADDRESS_COUNTER, bytearray([xstart & 0xFF]))
        self._command(
            SET_RAM_Y_ADDRESS_COUNTER, bytearray([ystart & 0xFF, (ystart >> 8) & 0xFF])
        )

    def _turn_on_display(self):
        self._command(DISPLAY_UPDATE_SEQUENCE_OPTION, b"\xc7")
        self._command(ACTIVATE_DISPLAY_UPDATE_SEQUENCE)
        self.wait()

    def wait(self):
        while self.busy.value() == BUSY:
            sleep_ms(10)

    def sleep(self):
        self._command(DEEP_SLEEP_MODE, b"\x01")
        sleep_ms(100)

    def reset(self):
        self.rst(1)
        sleep_ms(200)
        self.rst(0)
        sleep_ms(2)
        self.rst(1)
        sleep_ms(200)

    def clear(self):
        self.frame_buffer.fill(0xFF)
        # self.frame_buffer.rect(10, 20, 30, 50, 0, True)

        self.update()

    def pixel(self, x, y, c=1):
        self.frame_buffer.pixel(x, y, c)

    def rect(self, x, y, width, height, c=1):
        self.frame_buffer.rect(x, y, width, height, c, True)

    def update(self):
        self._command(WRITE_RAM_BW)
        self._data(self.buffer)

        self._turn_on_display()

    def _command(self, command, data=None):
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([command]))
        self.cs(1)

        if data is not None:
            self._data(data)

    def _data(self, data):
        self.dc(1)
        self.cs(0)
        self.spi.write(data)
        self.cs(1)
