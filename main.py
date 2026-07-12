from time import sleep_ms
from lib.epd import E_Paper_Display
from lib.ir import IR_Reciever, IR_Transmitter

epd = E_Paper_Display()
ir_rx = IR_Reciever()
ir_tx = IR_Transmitter()

while True:
    epd.handle_button_press()
    ir_tx.handle_button_press()
    sleep_ms(100)
