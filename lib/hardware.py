from machine import Pin
import config


class HW:
    epd_sdk = Pin(config.EPD_SCK)
    epd_mosi = Pin(config.EPD_MOSI)
    epd_cs = Pin(config.EPD_CS)
    epd_dc = Pin(config.EPD_DC)
    epd_rst = Pin(config.EPD_RST)
    epd_busy = Pin(config.EPD_BUSY)
    epd_button1 = Pin(config.EPD_BUTTON1, Pin.IN, Pin.PULL_UP)

    ir_rx = Pin(config.IR_RX, Pin.IN)
    ir_protocol_button = Pin(config.IR_PROTOCOL_BUTTON, Pin.IN, Pin.PULL_UP)
    ir_tx = Pin(config.IR_TX, Pin.IN)
    ir_tx_button1 = Pin(config.IR_TX_BUTTON1, Pin.IN, Pin.PULL_UP)
