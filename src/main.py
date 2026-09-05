from universal_remote.lib.display.screen_normal import NormalScreen

remote_names = [
    "TV",
    "Sound Bar",
    "Rasputin Robovac",
    "Lights",
    "Fan",
    "Projector",
    "Apple TV",
    "Xbox",
    "PS5",
    "PC",
]

screen = NormalScreen(menu_items=remote_names, protocol_name="NEC")
screen.build(selected_remote=7, battery_charge=4)
screen.update()
