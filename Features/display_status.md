# Display Status

## Purpose

Provide the user with clear information about the current state of the remote whilst operating in Normal Mode.

The display enables the user to:

- Identify the currently selected menu item.
- View available remote definitions.
- View the protocol associated with the selected menu item.
- View battery status.

---

## Preconditions

- The device is powered on.
- The device is in Normal Mode.

---

## Display Contents

The display shall show:

- Remote menu.
- Selected menu item.
- Selected remote protocol.
- Battery icon.

---

## Remote Menu

The remote menu shall contain:

- All learned remote definitions.
- A permanent Add New entry.

The menu shall indicate which item is currently selected.

Example:

-> TV  
   Soundbar  
   Media Centre  
   Add New  

---

## Selected Menu Item

The currently selected menu item shall be visually distinct from all other menu items.

The selected item may be:

- A learned remote.
- The Add New entry.

Only one menu item may be selected at any time.

---

## Remote Protocol

When a learned remote is selected:

- The protocol associated with that remote shall be displayed.

Example values:

- NEC
- Sony
- Philips
- MCE

When a different remote is selected:

- The displayed protocol shall update to match the newly selected remote.

The displayed protocol shall match the protocol used when transmitting commands for the selected remote.

### Add New

When Add New is selected:

- NEC shall be displayed.

---

## Battery Icon

The display shall show a battery icon.

The battery icon shall visually represent the current battery level.

The icon shall indicate:

- Full battery.
- High battery.
- Medium battery.
- Low battery.
- Critically low battery.

The exact visual representation is implementation defined.

---

## Behaviour

### Device Startup

When the device starts:

1. The display is updated to reflect the current system state.
2. The selected menu item is shown.
3. The selected remote protocol is shown.
4. The battery icon is shown
