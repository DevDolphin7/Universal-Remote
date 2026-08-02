from machine import Pin, ADC
import lib.core.config as config


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

    menu_select_button = Pin(config.GPIO_MENU_SELECT_BUTTON, Pin.IN, Pin.PULL_UP)
    change_ir_protocol_button = Pin(
        config.GPIO_CHANGE_IR_PROTOCOL_BUTTON, Pin.IN, Pin.PULL_UP
    )
    transmit_ir_button = Pin(config.GPIO_TRANSMIT_IR_BUTTON, Pin.IN, Pin.PULL_UP)
    learn_ir_button = Pin(config.GPIO_LEARN_IR_BUTTON, Pin.IN, Pin.PULL_UP)


class Buttons:
    MENU_SELECT = config.MENU_SELECT_BUTTON
    CHANGE_IR_PROTOCOL = config.CHANGE_IR_PROTOCOL_BUTTON
    TRANSMIT_IR = config.TRANSMIT_IR_BUTTON
    LEARN_IR = config.LEARN_IR_BUTTON
