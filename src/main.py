from utime import sleep_ms
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.core.state import State
from universal_remote.lib.managers.remote_manager import Remote
from universal_remote.lib.managers.learn_manager import Learn
from universal_remote.lib.managers.power_manager import Power
from universal_remote.lib.managers.device_manager import DeviceManager
from universal_remote.lib.managers.display_manager import Display
from universal_remote.lib.managers.button_manager import Buttons
from universal_remote.lib.storage.storage import Storage
from universal_remote.lib.core.types import Events, Device, AllButtons, Commands

remote = Device(
    id=0,
    name=f"Remote {0}",
    protocol_name="NEC_8",
    address=0 + 1,
    commands={AllButtons.NAV_OK: Commands(press=0 + 2, release=0 + 3)},
)

event_bus = EventBus()

storage = Storage(
    state_path="state.json",
    devices_path="universal_remote/lib/storage/remotes.json",
)

remotes = []
print(storage.load_devices(), "<<<<<<<<<")
for device in storage.load_devices():
    print(remote, "<<<<>>>", remote.name)
    remotes.append(Device(**device))
remote = Remote(event_bus, remotes)

power = Power(event_bus)

display = Display(
    event_bus,
    remote_names=remote.get_all_remote_names(),
    protocol_name=remote.get_active_protocol(),
    battery_charge=power.state,
)

learn = Learn(event_bus, remote)

device_manager = DeviceManager(event_bus, State(event_bus), power, display, learn)

buttons = Buttons(event_bus)


def print_ir_data(ir_datas):
    count = 0
    for data in ir_datas:
        print(
            data.address, "<<>>", data.command, "<<>>", data.ticks_diff, "<<>>", count
        )
        count += 1


def print_button(button):
    print("Button pressed: ", button)


def print_device_change(device):
    print(device.name)


event_bus.subscribe(Events.IR_RECEIVED, print_ir_data)
event_bus.subscribe(Events.BUTTON_RELEASED, print_button)
event_bus.subscribe(Events.DEVICE_CHANGED, print_device_change)

count = 0
while True:
    device_manager.update()
    buttons.update()
    if count % 10 == 0:
        print(device_manager.state.get(), "<<< state     ")
    count += 1
    sleep_ms(100)
