import network
from utime import sleep_ms
from lib.managers.battery import battery
from lib.managers.buttons import ButtonManager
from lib.managers.device import device
from lib.managers.epd import EPaperDisplay
from lib.managers.ir import IRManager


class UniversalRemote:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(False)

        self.epd = EPaperDisplay()
        self.ir = IRManager()
        self.buttons = ButtonManager()

        self._loop_interval = 100  # ms
        self._battery_check_interval = 10000  # ms
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
