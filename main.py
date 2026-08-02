from time import sleep_ms
from lib.managers.storage import Storage
from lib.managers.epd import EPaperDisplay
from lib.managers.ir import IR
from lib.managers.battery import BatteryManager
from lib.managers.buttons import ButtonManager


class UniversalRemote:
    def __init__(self):
        self.storage = Storage("remotes.json")
        self.devices = self.storage.load()

        self.epd = EPaperDisplay()
        self.ir = IR()
        self.battery = BatteryManager()
        self.buttons = ButtonManager()
        self.count = 0

    def run(self):
        while True:
            self.buttons.update()
            sleep_ms(100)
            self.count += 1
            if self.count == 1:
                self.test()

    def test(self):
        self.epd.draw_menu(voltage=self.battery.get_voltage())


UniversalRemote().run()
