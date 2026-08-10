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

| File                   | TDD required | Comment               |
| ---------------------- | ------------ | --------------------- |
| `/ir_rx`               | No           | Implemented elsewhere |
| `/ir_tx`               | No           | Implemented elsewhere |
| `hardware.py`          | No           | States GPIO pins      |
| `epd.py`               | No           |
| `epdin54_v2.py`        | No           |
| `battery_manager.py`   | No           |
| `ir_receiver.py`       | No           |
| `ir_transmitter.py`    | No           |
| `protocol_registry.py` | No           |
