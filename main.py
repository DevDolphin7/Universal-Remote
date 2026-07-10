from machine import Pin
from epd1in54_V2 import EPD
from time import sleep_ms

epd = EPD()
epd.update
button = Pin(15, Pin.IN, Pin.PULL_UP)

menu = ["Weather", "Clock", "Settings", "About"]
selected = 0


def draw_menu():
    epd.frame_buffer.fill(1)
    epd.frame_buffer.text("Main Menu", 50, 10, 0)
    epd.frame_buffer.text("-------", 50, 20, 0)

    y = 50

    for index, item in enumerate(menu):
        if index == selected:
            text = "> " + item
        else:
            text = "  " + item

        epd.frame_buffer.text(text, 20, y, 0)
        y += 25

    epd.update()


draw_menu()

while True:
    if button.value() == 0:

        sleep_ms(50)

        if button.value() == 0:
            selected += 1

            if selected >= len(menu):
                selected = 0

            draw_menu()

            while button.value() == 0:
                sleep_ms(10)

    sleep_ms(100)
