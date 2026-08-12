## Architecture

`main.py` - Initialise system and start application loop.

### /lib/core

`event_bus.py` - Publish and subscribe to application events.  
`state.py` - Store current device state and operating mode.  
`protocol_registry.py` - Register and retrieve supported IR protocols.  
`config.py` - Store application constants and configuration values.  
`types.py` - Define shared application data structures and types.

### /lib/drivers

`/ir_rx`  
`/ir_tx`  
`hardware.py` - Create and expose hardware interface instances.  
`epdin54_v2.py` - Low-level Waveshare e-paper hardware driver.  
`battery.py` - Read raw battery voltage from ADC hardware.  
`ir_receiver.py` - Receive raw infrared transmissions from hardware.  
`ir_transmitter.py` - Send infrared commands using active protocol.

### /lib/display

`screen_builder.py` - Generate framebuffers from application state.  
`battery_icon.py` - Convert battery state into display icon graphics.

### lib/managers

`display_manager.py` - Coordinate display updates and screen transitions.  
`device_manager.py` - Coordinate high-level application state and workflows.  
`button_manager.py` - Detect button presses, releases and hold events.  
`learn_manager.py` - Execute learning workflow, timeouts and protocol selection.  
`remote_manager.py` - Manage remote definitions and active selection.  
`power_manager.py` - Derive battery state from measured voltage.

### /lib/storage

`storage.py` - Persist and restore application state data.  
`remotes.json` - Store remote definitions and learned commands.

## Mapping

| Feature                 | Primary Owner                                             |
| ----------------------- | --------------------------------------------------------- |
| Use Remote              | remote_manager.py + ir_transmitter.py                     |
| Select Active Remote    | remote_manager.py                                         |
| Display Status          | display_manager.py + screen_builder.py + power_manager.py |
| Enter Learning Mode     | device_manager.py                                         |
| Exit Learning Mode      | device_manager.py                                         |
| Learn Button            | learn_manager.py                                          |
| Change Receive Protocol | learn_manager.py                                          |
| Persist Learned Remotes | storage.py                                                |
| Factory Reset           | device_manager.py + storage.py                            |

## Implementation Plan

Drivers > Core > Storage > Display > Managers > main

### TDD

| Folder   | File                 | TDD Required | Comment                                                                                                                        |
| -------- | -------------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| drivers  | /ir_rx               | No           | Module implemented by [peterhinch](https://github.com/peterhinch/micropython_ir)                                               |
| drivers  | /ir_tx               | No           | Module implemented by [peterhinch](https://github.com/peterhinch/micropython_ir)                                               |
| drivers  | hardware.py          | No           | Hardware pin configuration only                                                                                                |
| drivers  | epdin54_v2.py        | No           | Low-level display hardware driver implemented by [joshnuss](https://gist.github.com/joshnuss/9ebc092d1c21b9dbc68e9d3020848146) |
| drivers  | battery.py           | No           | Direct ADC hardware access only                                                                                                |
| drivers  | ir_receiver.py       | No           | Thin wrapper around IR library                                                                                                 |
| drivers  | ir_transmitter.py    | No           | Thin wrapper around IR library                                                                                                 |
| core     | event_bus.py         | Yes          | Critical publish/subscribe behaviour                                                                                           |
| core     | state.py             | Yes          | Shared state and operating mode rules                                                                                          |
| core     | protocol_registry.py | Yes          | Protocol lookup and mapping behaviour                                                                                          |
| core     | config.py            | No           | Constants and configuration only                                                                                               |
| core     | types.py             | No           | Data structure definitions only                                                                                                |
| storage  | storage.py           | Yes          | Persistence and restore behaviour                                                                                              |
| storage  | remotes.json         | No           | Data file only                                                                                                                 |
| display  | screen_builder.py    | Yes          | Framebuffer generation and presentation logic                                                                                  |
| display  | battery_icon.py      | Yes          | Battery state to icon conversion                                                                                               |
| managers | display_manager.py   | Yes          | Display refresh and screen selection behaviour                                                                                 |
| managers | device_manager.py    | Yes          | Mode transitions and reset rules                                                                                               |
| managers | button_manager.py    | Yes          | Button timing and state logic                                                                                                  |
| managers | learn_manager.py     | Yes          | Complex learning workflow and protocol selection                                                                               |
| managers | remote_manager.py    | Yes          | Remote selection and command rules                                                                                             |
| managers | power_manager.py     | Yes          | Battery voltage to power state rules                                                                                           |
| root     | main.py              | No           | Application composition and startup, tested through [System Tests](#system-tests)                                              |

### System Tests

- The remote works as described by the feature files.
- Button press to IR transmission under 100 ms.
- Quiescent drain must not be higher than 0.5 mA in the dormant state.
- Quiescent drain should not be higher than 0.1 mA in the dormant state.
- Remote definitions must survive battery replacement.
- Common user operations should require 1 press.
- Users must always have a method of recovering from accidental configuration or corrupted data.
- The device should be capable of recovering to a functional default state.
