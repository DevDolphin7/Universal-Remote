from time import sleep_ms
from lib.storage import Storage
from lib.epd import EPaperDisplay
from lib.ir import IR


class UniversalRemote:
    def __init__(self):
        self.storage = Storage("remotes.json")
        self.devices = self.storage.load()

        self.epd = EPaperDisplay()
        self.ir = IR()

    def run(self):
        while True:
            self.epd.handle_button_press()
            self.ir.handle_button_press()
            self.ir.get_custom_button_data()
            self.ir.tx.handle_button_press(0x0044)
            sleep_ms(100)


UniversalRemote().run()
