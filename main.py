from time import sleep_ms
from lib.storage import Storage
from lib.epd import EPaperDisplay
from lib.ir import IR
from lib.battery_manager import BatteryManager


class UniversalRemote:
    def __init__(self):
        self.storage = Storage("remotes.json")
        self.devices = self.storage.load()

        self.epd = EPaperDisplay()
        self.ir = IR()
        self.bat_man = BatteryManager()
        self.count = 0

    def run(self):
        while True:
            self.epd.handle_button_press()
            self.ir.handle_button_press()
            self.ir.get_custom_button_data()
            self.ir.tx.handle_button_press(0x0044)
            print(self.bat_man.get_voltage())
            sleep_ms(100)
            self.count += 1
            if self.count == 1:
                self.test()

    def test(self):
        self.epd.draw_menu(voltage=self.bat_man.get_voltage())


UniversalRemote().run()
