from machine import Pin, ADC
import universal_remote.lib.core.config as config


class Hardware:
    vsys = ADC(config.VOLTAGE_DIVIDER_PIN)

    epd_sdk = Pin(config.EPD_SCK)
    epd_mosi = Pin(config.EPD_MOSI)
    epd_cs = Pin(config.EPD_CS)
    epd_dc = Pin(config.EPD_DC)
    epd_rst = Pin(config.EPD_RST)
    epd_busy = Pin(config.EPD_BUSY)

    ir_rx = Pin(config.IR_RX, Pin.IN)
    ir_tx = Pin(config.IR_TX, Pin.IN)

    mode = Pin(config.MODE, Pin.IN, Pin.PULL_UP)

    nav_up = Pin(config.NAV_UP, Pin.IN, Pin.PULL_UP)
    nav_down = Pin(config.NAV_DOWN, Pin.IN, Pin.PULL_UP)
    nav_left = Pin(config.NAV_LEFT, Pin.IN, Pin.PULL_UP)
    nav_right = Pin(config.NAV_RIGHT, Pin.IN, Pin.PULL_UP)
    nav_ok = Pin(config.NAV_OK, Pin.IN, Pin.PULL_UP)

    vol_up = Pin(config.VOL_UP, Pin.IN, Pin.PULL_UP)
    vol_down = Pin(config.VOL_DOWN, Pin.IN, Pin.PULL_UP)

    ch_up = Pin(config.CH_UP, Pin.IN, Pin.PULL_UP)
    ch_down = Pin(config.CH_DOWN, Pin.IN, Pin.PULL_UP)
