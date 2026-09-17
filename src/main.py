from utime import sleep_ms
from universal_remote.lib.core.event_bus import EventBus
from universal_remote.lib.managers.learn_manager import Learn
from universal_remote.lib.core.types import Events, Device, AllButtons, Commands

remote = Device(
    id=0,
    name=f"Remote {0}",
    protocol_name="NEC_8",
    address=0 + 1,
    commands={AllButtons.NAV_OK: Commands(press=0 + 2, release=0 + 3)},
)

event_bus = EventBus()

learn = Learn(event_bus, remote)


def print_ir_data(ir_datas):
    count = 0
    for data in ir_datas:
        print(
            data.address, "<<>>", data.command, "<<>>", data.ticks_diff, "<<>>", count
        )
        count += 1


event_bus.subscribe(Events.IR_RECEIVED, print_ir_data)

while True:
    sleep_ms(100)
