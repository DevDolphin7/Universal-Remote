import network
from utime import sleep_ms
from lib.managers.battery import battery
from lib.managers.storage import memory
from lib.managers.epd import EPaperDisplay
from lib.managers.ir import IRManager
from lib.managers.buttons import ButtonManager


class UniversalRemote:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(False)

        self.memory = memory
        self.devices = self.memory.load()
        print(self.devices)

        self.epd = EPaperDisplay()
        self.ir = IRManager()
        self.buttons = ButtonManager()

        self._loop_interval = 100  # ms
        self._battery_check_interval = 1000  # ms
        self._count = 0

    def run(self):
        while True:
            self.buttons.update()

            self._count += 1
            if (self._count * self._loop_interval) > self._battery_check_interval:
                self._count = 0
                battery.update()

            sleep_ms(self._loop_interval)


UniversalRemote().run()
