from utime import sleep_ms
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.core.state import State
from universal_remote.lib.drivers.protocol_registry import IRProtocolInterface
from universal_remote.lib.managers.remote_manager import Remote
from universal_remote.lib.managers.learn_manager import Learn
from universal_remote.lib.managers.power_manager import Power
from universal_remote.lib.managers.device_manager import DeviceManager
from universal_remote.lib.managers.display_manager import Display
from universal_remote.lib.managers.button_manager import Buttons
from universal_remote.lib.storage.storage import Storage

event_bus = EventBus()

storage = Storage(
    state_path="state.json",
    devices_path="universal_remote/lib/storage/remotes.json",
)

remote = Remote(event_bus, storage)

power = Power(event_bus)

display = Display(
    event_bus,
    remote=remote,
    battery_charge=power.state,
)

ir_protocol_interface = IRProtocolInterface()

state = State(event_bus)

learn = Learn(event_bus, state, remote, ir_protocol_interface)

device_manager = DeviceManager(
    event_bus, state, remote, power, display, learn, ir_protocol_interface
)

buttons = Buttons(event_bus)

display.update()

count = 0
while True:
    device_manager.update()
    buttons.update()
    count += 1
    sleep_ms(100)
