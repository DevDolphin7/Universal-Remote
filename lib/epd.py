from machine import Pin
from epd1in54_V2 import EPD
from time import sleep_ms


class E_Paper_Display(EPD):
    def __init__(self):
        super().__init__()
        self.menu = ["Weather", "Clock", "Settings", "About"]
        self.selected = 0
        self.draw_menu()

    def draw_menu(self):
        self.frame_buffer.fill(1)
        self.frame_buffer.text("Main Menu", 50, 10, 0)
        self.frame_buffer.text("-------", 50, 20, 0)

        y = 50

        for index, item in enumerate(self.menu):
            if index == self.selected:
                text = "> " + item
            else:
                text = "  " + item

            self.frame_buffer.text(text, 20, y, 0)
            y += 25

        self.update()

    def handle_button_press(self):
        button = Pin(15, Pin.IN, Pin.PULL_UP)

        if button.value() == 0:
            sleep_ms(50)

            if button.value() == 0:
                self.selected += 1

                if self.selected >= len(self.menu):
                    self.selected = 0

                self.draw_menu()

                while button.value() == 0:
                    sleep_ms(10)
