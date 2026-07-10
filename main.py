from machine import Pin, SPI
from epd1in54_V2 import EPD

epd = EPD()

epd.frame_buffer.fill(1)
epd.frame_buffer.text("Hello, World!", 40, 90, 0)
epd.update()
