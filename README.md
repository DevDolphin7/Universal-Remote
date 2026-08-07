# Universal Remote

## Overview

Universal Remote is a handheld programmable infrared (IR) remote built using a Raspberry Pi Pico 2W, e-paper display, an IR Rx and Tx breakout board, buttons and 2 x AA batteries.

The device is designed to replace my broken TV remote, whilst allowing every functional button to be reprogrammed from other IR remotes without requiring a computer connection. This means it can control other IR devices as well, because I was interested to see if I could do it!

The primary goals of the project are:

- Simple everyday operation.
- Fast button response.
- Long battery life.
- Persistent storage of learned remotes.
- Easy in-device reprogramming.
- Minimal user interface complexity.

---

# Physical Layout

The remote contains ten physical buttons.

## Navigation Buttons

A central five-button directional pad:

- NAV_UP
- NAV_DOWN
- NAV_LEFT
- NAV_RIGHT
- NAV_OK

## Device Control Buttons

Two pairs of programmable buttons positioned either side of the navigation pad:

Left side:

- VOL_UP
- VOL_DOWN

Right side:

- CH_UP
- CH_DOWN

## Mode Button

A dedicated MODE button positioned beneath the display.

The MODE button is responsible for:

- Cycling between configured remotes.
- Entering learning mode.
- Exiting learning mode.
- Switching IR receive protocols whilst in learning mode.

---

# Normal Operating Mode

When powered on, the remote operates in Normal Mode.

The display shows:

- Main menu of stored remotes.
- Active remote name.
- Current IR protocol.
- Battery percentage.
- Battery icon.

Pressing any of the nine programmable buttons causes the configured IR command to be transmitted.

If a button has both a press command and release command configured:

- Pressing the button transmits the press command.
- Releasing the button transmits the release command.

This supports devices that require separate press and release events.

---

# Remote Selection

A short press of MODE cycles through the available remotes.

Example:

TV
→ Soundbar
→ Media Centre
→ Remote 4
→ Add New
→ TV

The currently selected remote becomes the active remote for all button transmissions.

---

# Learning Mode

Learning mode allows any programmable button to be updated using an existing IR remote.

## Entering Learning Mode

The user enters learning mode by holding MODE for two seconds.

The display switches to the learning screen.

---

## Learning a Button

Whilst in learning mode:

1. The user presses the button they wish to programme.
2. The display indicates that the remote is ready to receive a signal.
3. The user transmits an IR signal from the original remote.
4. The received protocol, address and command are captured.
5. The button definition is updated and saved.
6. The display confirms successful learning.

This workflow is intended to make updating a single button as quick as possible.

---

## Learning Press and Release Commands

Some remotes send two commands:

- Button press
- Button release

If two commands are received within 200 milliseconds:

- First command becomes the press command.
- Second command becomes the release command.

If only a single command is received within 200 millisecond:

- The command becomes the press command.
- No release command is stored.

When transmitting:

- Press transmits the press command.
- Release transmits the release command if one exists.
- Press and hold transmits the press command every 160 milliseconds.

---

## Protocol Selection

Whilst in learning mode:

- A short press of MODE cycles the active receive protocol.

Example:

NEC
→ Sony
→ Philips
→ MCE
→ NEC

The display always shows the currently selected receive protocol.

---

## Leaving Learning Mode

The user exits learning mode by holding MODE for two seconds.

The display returns to Normal Mode.

---

# Creating New Remotes

One entry in the remote list is always:

Add New

Selecting this entry and learning a button creates a new remote.

New remotes are automatically named:

Remote 1  
Remote 2  
Remote 3  
...

Names are assigned sequentially and are not user editable.

---

# Persistence

All learned remotes are stored permanently in non-volatile storage.

Configured remotes should survive:

- Power loss.
- Device restart.
- Battery replacement.

---

# Factory Reset

The remote provides a recovery mechanism to return to a known state.

Factory reset is activated by holding:

MODE + NAV_OK

for ten seconds, while in Normal Mode.

The factory reset process:

- Removes all learned remotes.
- Restores default data.
- Returns the remote to its initial state.

---

# Planned Feature Files

The system behaviour will be defined through the following feature files:

1. Use Remote
2. Select Active Remote
3. Display Status
4. Enter Learning Mode
5. Exit Learning Mode
6. Learn Button
7. Change Receive Protocol
8. Add New Remote
9. Persist Learned Remotes
10. Factory Reset

These feature files will act as the primary source of behavioural requirements.

---

# System Constraints

## Responsiveness

Button interactions should feel instantaneous to the user.

Target:

- Button press to IR transmission under 100 ms.

---

## Battery Life

The remote must achieve a minimum battery life of 6 monthd using two AA batteries under normal usage.
> Quiescent drain must not be higher than 0.5 mA in the dormant state.

The remote should achieve a minimum battery life of two years using two AA batteries under normal usage.
> Quiescent drain should not be higher than 0.1 mA in the dormant state.

---

## Persistent Storage

Remote definitions must survive:

- Power loss.
- Battery replacement.
- Device restart.

---

## Simplicity

Common user operations should require the minimum practical number of interactions.

Particular emphasis should be placed on making button learning fast and intuitive.

---

## Recovery

Users must always have a method of recovering from accidental configuration or corrupted data.

---

## Storage Integrity

The device should be capable of recovering to a functional default state.

---

# Future Development

This document describes product behaviour only.

The implementation architecture is intentionally not defined here and may evolve as feature files are created and tested.

Feature files remain the authoritative definition of behaviour.

---

# Hardware
- [Raspberry Pi Pico 2W](https://www.raspberrypi.com/products/raspberry-pi-pico-2/)
- [Wave share 200x200, 1.54inch E-Ink display module, SKU 12955](https://www.waveshare.com/1.54inch-e-paper-module.htm)
