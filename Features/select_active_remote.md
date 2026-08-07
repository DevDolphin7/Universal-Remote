# Select Active Remote

## Purpose

Allow the user to choose which menu item is active.

The selected item determines:

- Which remote is used when transmitting commands.
- Which remote is modified when learning commands.

---

## Preconditions

- The device is powered on.
- The device is in Normal Mode.

---

## User Interaction

The user performs a short press of the MODE button.

---

## Behaviour

### Cycling Selection

When the MODE button is pressed:

1. The next item in the remote menu becomes selected.
2. When the final menu item is reached, selection wraps to the first item.
3. The display updates to show the newly selected item.

Example:

TV
→ Soundbar
→ Media Centre
→ Add New
→ TV

---

## Menu Contents

The menu shall contain:

- All learned remote definitions.
- A permanent Add New entry.

The Add New entry shall always be present.

---

## Selected Item

The system shall always maintain a selected menu item.

A selected item may be:

- A learned remote.
- The Add New entry.

There shall never be a state where no menu item is selected.

---

## Persistence

When selection changes:

1. The newly selected item is stored in non-volatile storage.

When the device starts:

1. The previously selected item is restored.

If the previously selected item cannot be restored:

1. The first available menu item becomes selected.

---

## Initial State

When the device is started for the first time:

### If learned remotes exist

The first learned remote is selected.

### If no learned remotes exist

The Add New entry is selected.

---

## Factory Reset Recovery

Following a factory reset:

1. All learned remotes are removed.
2. The Add New entry remains available.
3. The Add New entry becomes selected.

---

## Success Criteria

### Select Next Remote

Given:

- TV is selected.
- Soundbar exists.

When:

- MODE is pressed.

Then:

- Soundbar becomes selected.

### Wrap Around

Given:

- Add New is selected.

When:

- MODE is pressed.

Then:

- The first menu item becomes selected.

### Restore Previous Selection

Given:

- Soundbar is selected.

When:

- The device restarts.

Then:

- Soundbar remains selected.

### No Learned Remotes

Given:

- No learned remotes exist.

When:

- The device starts.

Then:

- Add New is selected.

---

## Edge Cases

### Selected Remote Removed

Given:

- A remote is selected.
- That remote no longer exists.

When:

- The device starts.

Then:

- The first available menu item becomes selected.

### Empty Remote List

Given:

- No learned remotes exist.

When:

- MODE is pressed.

Then:

- Add New remains selected.

---

## Requirements

- Selection changes should feel instantaneous to the user.
- Menu navigation must not affect stored remote definitions.
- Selection state must survive power loss, restart and battery replacement.
- The user must be able to reach any menu item using only repeated MODE button presses.

---

## Notes

This feature defines menu navigation and selection behaviour only.

It does not define:

- Display layout.
- Learning behaviour.
- New remote creation.
- Storage implementation.
