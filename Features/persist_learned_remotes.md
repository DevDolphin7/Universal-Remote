# Persist Learned Remotes

## Purpose

Ensure that all learned remote definitions and user selections are retained across power loss, device restart and battery replacement.

The persistence system shall:
- Store learned remote definitions.
- Store learned button definitions.
- Store remote protocol associations.
- Store remote addresses.
- Store the currently selected menu item.
- Restore stored data when the device starts.

## Preconditions

- Non-volatile storage is available.

## User Interaction

The user does not directly interact with this feature.

Persistence occurs automatically when:
- A remote is created.
- A remote is modified.
- A menu selection changes.

Stored information is restored automatically when the device starts.

## Behaviour

### Stored Data

The system shall persist the complete state required to restore learned remotes.

For each remote:

- Remote name.
- Receive protocol.
- Transmit protocol.
- Remote address.
- Learned button definitions.

For each learned button:

- Press command.
- Release command if present.

The system shall also persist:

- The currently selected menu item.

### Automatic Saving

When a learning operation completes successfully:

- Updated remote data is written to non-volatile storage.

When a new remote is created:

- The complete remote definition is written to non-volatile storage.

When the selected menu item changes:

- The selected item is written to non-volatile storage.

Persistence shall occur automatically without requiring additional user action.

### Startup Recovery

When the device starts:

- Stored remote definitions are loaded.
- Stored remote names are restored.
- Stored receive protocols are restored.
- Stored transmit protocols are restored.
- Stored addresses are restored.
- Stored button definitions are restored.
- The previously selected menu item is restored.

The device shall return to the same operational state that existed before power loss.

### Power Loss

Loss of power shall not:

- Delete stored remotes.
- Delete stored button definitions.
- Reset protocol associations.
- Reset stored addresses.
- Reset the selected menu item.

After power is restored:

- Previously stored data shall remain available.

### Battery Replacement

Removing and replacing batteries shall have the same behaviour as a normal power cycle.

Stored data shall remain available after battery replacement.

### Data Integrity

The system shall never intentionally overwrite stored data unless:

- A button is relearned.
- A remote is created.
- The selected menu item changes.
- A factory reset is performed.

Existing stored data shall remain unchanged during normal remote operation.

## Success Criteria

### Restore Existing Remote

Given:

- TV Remote exists.
- The device is powered off.

When:

- The device starts.

Then:

- TV Remote exists.
- The stored address is restored.
- The stored receive protocol is restored.
- The stored transmit protocol is restored.
- All learned button definitions are available.
- The remote may be used normally.

### Restore Selected Menu Item

Given:

- Soundbar is selected.

When:

- The device restarts.

Then:

- Soundbar remains selected.

### Newly Learned Button Persists

Given:

- A button is successfully learned.

When:

- The device restarts.

Then:

- The learned button definition remains available.

### New Remote Persists

Given:

- A new remote is successfully created.

When:

- The device restarts.

Then:

- The remote remains available.
- The stored address remains available.
- The stored protocols remain available.

## Edge Cases

### No Learned Remotes

Given:

- No learned remotes exist.

When:

- The device starts.

Then:

- Add New is selected.

### Interrupted Learning Operation

Given:

- A learning operation is in progress.

When:

- Power is lost before learning completes.

Then:

- The previously stored configuration remains valid.
- No partially learned button is stored.
- No partially created remote is stored.

### Corrupt Stored Data

Given:

- Stored data cannot be successfully loaded.

When:

- The device starts.

Then:

- The device recovers to a valid default state.
- The device remains operational.
- Recovery behaviour is defined by the Factory Reset feature.

### Missing Selected Remote

Given:

- The stored selected menu item cannot be restored.

When:

- The device starts.

Then:

- The first available menu item becomes selected.

## Notes

- Persistence must survive power loss.
- Persistence must survive device restart.
- Persistence must survive battery replacement.
- Remote addresses are persisted as part of the remote definition.
- Receive and transmit protocols are persisted independently.
- The exact storage implementation is not defined by this feature.
- File formats are intentionally implementation defined.
- Remote creation is defined by the Learn Button feature.
- Menu selection is defined by the Select Active Remote feature.
- Factory reset behaviour is defined by the Factory Reset feature.
- Recovery mechanisms should prioritise restoring a functional device over preserving corrupt data.
