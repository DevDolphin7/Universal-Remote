# Architecture

`main.py` - Initialise system and start application loop.

## /lib/core

`event_bus.py` - Publish and subscribe to application events.  
`config.py` - Store application constants and configuration values.  
`types.py` - Define shared application data structures and types.

## /lib/drivers

`/ir_rx`  
`/ir_tx`  
`hardware.py` - Create and expose hardware interface instances.  
`epd.py` - Render display contents to e-paper screen.  
`epdin54_v2.py` - Low-level Waveshare e-paper hardware driver.  
`battery_manager.py` - Measure battery voltage and derive level.  
`ir_receiver.py` - Receive raw infrared transmissions from hardware.  
`ir_transmitter.py` - Send infrared commands using active protocol.  
`protocol_registry.py` - Register and retrieve supported IR protocols.

## lib/managers

`device_manager.py` - Coordinate high-level application state and workflows.  
`button_manager.py` - Detect button presses, releases and hold events.  
`learn_manager.py` - Execute button learning workflow and timeouts.  
`remote_manager.py` - Manage remote definitions and active selection.

## /lib/storage

`storage.py` - Persist and restore application state data.  
`remotes.json` - Store remote definitions and learned commands.

# Mapping

| Feature                 | Primary Owner                             |
| ----------------------- | ----------------------------------------- |
| Use Remote              | `remote_manager.py` + `ir_transmitter.py` |
| Select Active Remote    | `remote_manager.py`                       |
| Display Status          | `epd.py`                                  |
| Enter Learning Mode     | `device_manager.py`                       |
| Exit Learning Mode      | `device_manager.py`                       |
| Learn Button            | `learn_manager.py`                        |
| Change Receive Protocol | `learn_manager.py`                        |
| Persist Learned Remotes | `storage.py`                              |
| Factory Reset           | `device_manager.py` + `storage.py`        |

# Implementation Plan

Drivers > Core > Storage > Managers > main

## Testing

| Folder | File | TDD Required | Comment |
|----------|----------|----------|----------|
| drivers | /ir_rx | No | Implemented elsewhere |
| drivers | /ir_tx | No | Implemented elsewhere |
| drivers | hardware.py | No | Hardware pin configuration only |
| drivers | epd.py | No | Primarily visual display rendering |
| drivers | epdin54_v2.py | No | Third-party hardware driver |
| drivers | battery_manager.py | No | Simple voltage conversion logic |
| drivers | ir_receiver.py | No | Thin wrapper around IR library |
| drivers | ir_transmitter.py | No | Thin wrapper around IR library |
| drivers | protocol_registry.py | No | Static protocol lookup data |
| core | event_bus.py | Yes | Critical publish/subscribe behaviour |
| core | config.py | No | Constants and configuration only |
| core | types.py | No | Data structure definitions only |
| storage | storage.py | Yes | Persistence and restore behaviour |
| storage | remotes.json | No | Data file only |
| managers | device_manager.py | Yes | Mode transitions and reset rules |
| managers | button_manager.py | Yes | Button timing and state logic |
| managers | learn_manager.py | Yes | Complex learning workflow |
| managers | remote_manager.py | Yes | Remote selection and command rules |
| root | main.py | No | Application composition and startup |
