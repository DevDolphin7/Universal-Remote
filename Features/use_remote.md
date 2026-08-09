# Use Remote

## Purpose

Allow the user to transmit commands from the currently selected remote using any of the nine programmable buttons.

This is the primary function of the device and should require no menu navigation or additional user interaction.

---

## Preconditions

- The device is powered on.
- The device is in Normal Mode.
- A remote is selected.
- The selected remote contains a definition for the pressed button.

---

## User Interaction

The user presses one of:

- NAV_UP
- NAV_DOWN
- NAV_LEFT
- NAV_RIGHT
- NAV_OK
- VOL_UP
- VOL_DOWN
- CH_UP
- CH_DOWN

---

## Behaviour

### Button Press

When a programmable button is pressed:

1. The button definition is retrieved from the selected remote.
2. The associated press command is transmitted using the configured protocol.
3. Transmission should begin within 100 milliseconds of the button press.

### Button Release

When a programmable button is released:

1. If a release command exists, the release command is transmitted after 160 milliseconds of button press transmission.
2. If no release command exists, no action occurs.

### Button Hold

When a programmable button remains held:

1. The press command continues to be transmitted.
2. Repeat transmissions occur every 160 milliseconds.
3. Repeat transmissions stop immediately when the button is released.
4. If a release command exists, it is transmitted when the button is released.

---

## Success Criteria

### Press Command

Given:

- A remote is selected.
- The button contains a learned press command.

When:

- The user presses the button.

Then:

- The command is transmitted.

### Release Command

Given:

- The button contains both a press and release command.

When:

- The button is released.

Then:

- The release command is transmitted.

### Hold Behaviour

Given:

- The button contains a press command.

When:

- The button is held.

Then:

- The command is retransmitted every 160 milliseconds.
- Retransmission stops when the button is released.
- If a release command exists, it is transmitted when the button is released.

---

## Edge Cases

### Undefined Button

Given:

- The selected remote does not contain a definition for the button.

When:

- The user presses the button.

Then:

- No IR transmission occurs.
- The device remains operational.

### Invalid Command Data

Given:

- A stored command cannot be transmitted.

When:

- The user presses the button.

Then:

- The transmission is ignored.
- The device remains operational.

---

## Requirements

- Button press to transmission latency must be less than 100 milliseconds.
- Behaviour must be identical across all supported IR protocols.
- Behaviour must be identical across all programmable buttons.
- The user must not need to navigate menus to use normal remote functionality.

---

## Notes

This feature describes user-facing behaviour only.

It does not define:

- Event architecture
- Storage format
- Display implementation
- Protocol implementation

These concerns are defined elsewhere.
