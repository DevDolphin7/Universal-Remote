from machine import Pin, ADC
import universal_remote.lib.core.config as config


class Hardware:
    vsys = ADC(config.VOLTAGE_DIVIDER_PIN)

    epd_sdk = Pin(config.GPIO_EPD_SCK)
    epd_mosi = Pin(config.GPIO_EPD_MOSI)
    epd_cs = Pin(config.GPIO_EPD_CS)
    epd_dc = Pin(config.GPIO_EPD_DC)
    epd_rst = Pin(config.GPIO_EPD_RST)
    epd_busy = Pin(config.GPIO_EPD_BUSY)

    ir_rx = Pin(config.GPIO_IR_RX, Pin.IN)
    ir_tx = Pin(config.GPIO_IR_TX, Pin.IN)

    mode = Pin(config.GPIO_MODE, Pin.IN, Pin.PULL_UP)
    nav_up = Pin(config.GPIO_NAV_UP, Pin.IN, Pin.PULL_UP)
    nav_down = Pin(config.GPIO_NAV_DOWN, Pin.IN, Pin.PULL_UP)
    nav_ok = Pin(config.GPIO_NAV_OK, Pin.IN, Pin.PULL_UP)


class Buttons:
    MODE = config.MODE

    NAV_UP = config.NAV_UP
    NAV_DOWN = config.NAV_DOWN
    NAV_LEFT = config.NAV_LEFT
    NAV_RIGHT = config.NAV_RIGHT
    NAV_OK = config.NAV_OK

    VOL_UP = config.VOL_UP
    VOL_DOWN = config.VOL_DOWN

    CH_UP = config.CH_UP
    CH_DOWN = config.CH_DOWN
