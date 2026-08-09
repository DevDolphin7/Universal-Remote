# Factory Reset

## Purpose

Allow the user to return the remote to a known default state by removing all learned configuration data.

Factory Reset provides a recovery mechanism when:
- The user wishes to remove all learned remotes.
- Stored configuration becomes unusable.
- The system needs to recover from corrupt persisted data.

## Preconditions

- The remote is powered on.
- The remote is operating in Normal Mode.
- The remote is not operating in Learning Mode.

## User Interaction

- The user presses and holds MODE and NAV_OK simultaneously.
- MODE and NAV_OK remain pressed continuously for 10 seconds.
- No other button is pressed during the hold period.
- The user releases the buttons.

## Behaviour

### Factory Reset Availability

Factory Reset may only be initiated whilst the remote is operating in Normal Mode.

The Factory Reset button combination shall be ignored when:
- The remote is operating in Learning Mode.
- The remote is waiting for an IR transmission.
- A button learning operation is in progress.

### Performing A Factory Reset

When MODE and NAV_OK have been held continuously for 10 seconds:

- All learned remotes are permanently deleted.
- All learned button definitions are permanently deleted.
- All stored remote protocol associations are deleted.
- All stored remote addresses are deleted.
- The selected menu item is reset.
- The active receive protocol is reset to NEC.
- The remote returns to its default state.

### Post Reset State

After a successful Factory Reset:

- No learned remotes exist.
- The Add New menu item remains available.
- Add New becomes the selected menu item.
- NEC becomes the active receive protocol.
- The display updates to show the Normal Mode screen.
- The display shows Add New as the selected menu item.
- NEC is displayed as the protocol associated with Add New.
- The remote remains fully operational.

### Persistence

Following a successful Factory Reset:

- The reset state is saved to non-volatile storage.
- Deleted remote definitions must not be restored following power loss.
- Deleted remote definitions must not be restored following device restart.
- Deleted remote definitions must not be restored following battery replacement.
- NEC remains the active receive protocol after restart.

## Success Criteria

### Remove Learned Remotes

Given:
- One or more learned remotes exist.

When:
- Factory Reset completes successfully.

Then:
- All learned remotes are removed.
- Add New remains available.

### Reset Selection

Given:
- A learned remote is selected.

When:
- Factory Reset completes successfully.

Then:
- Add New becomes selected.

### Reset Receive Protocol

Given:
- A receive protocol other than NEC is active.

When:
- Factory Reset completes successfully.

Then:
- NEC becomes the active receive protocol.

### Reset Persists Across Restart

Given:
- Factory Reset has completed successfully.

When:
- The device restarts.

Then:
- No learned remotes exist.
- Add New remains selected.
- NEC remains the active receive protocol.

## Edge Cases

### Attempted During Learning Mode

Given:
- The remote is operating in Learning Mode.

When:
- The user presses and holds MODE and NAV_OK.

Then:
- Factory Reset is not performed.
- No stored data is modified.
- Learning Mode continues operating normally.

### Buttons Released Before Hold Threshold

Given:
- The remote is operating in Normal Mode.

When:
- MODE and NAV_OK are released before 10 seconds have elapsed.

Then:
- Factory Reset is not performed.
- No stored data is modified.
- The remote continues operating normally.

### Additional Button Pressed During Hold

Given:
- MODE and NAV_OK are being held.

When:
- Any other button is pressed before the 10 second threshold is reached.

Then:
- The reset attempt is cancelled.
- No stored data is modified.
- Factory Reset is not performed.
- The user must restart the full button combination to initiate another reset attempt.

### No Learned Remotes

Given:
- No learned remotes exist.

When:
- Factory Reset completes successfully.

Then:
- The operation completes normally.
- Add New remains selected.
- NEC becomes the active receive protocol.

### Power Loss During Factory Reset

Given:
- A Factory Reset operation is in progress.

When:
- Power is lost before the operation completes.

Then:
- The device must recover to a valid operational state.
- Recovery behaviour is implementation defined.
- Previously stored data may be retained if reset completion cannot be verified.

### Corrupt Stored Data

Given:
- Stored configuration data cannot be successfully loaded.

When:
- Recovery requires a Factory Reset.

Then:
- The device returns to the default state.
- Add New becomes selected.
- NEC becomes the active receive protocol.
- The device remains operational.

## Notes

- Factory Reset is responsible for removing all learned configuration data.
- Factory Reset is responsible for restoring the default receive protocol.
- Factory Reset may only be initiated from Normal Mode.
- Factory Reset does not modify firmware.
- Factory Reset does not modify hardware configuration.
- Add New is a permanent menu item and cannot be removed.
- Remote creation is defined by the Learn Button feature.
- Menu selection behaviour is defined by the Select Active Remote feature.
- Persistence behaviour is defined by the Persist Learned Remotes feature.
- Display behaviour is defined by the Display Status feature.
