from universal_remote.lib.display.screen_learning import LearnScreen

screen = LearnScreen(
    remote="Rasputin Robovac Testing123",
    buttons=["Vol_UP", "Vol_down", "Test"],
    protocol_name="NEC123456789",
)

screen.build_learned(
    selected_button=1,
    id=1,
    address=1,
    press_command=30,
    release_command=0,
    battery_charge=4,
)

screen.update()
