# Exit Learning Mode

## Purpose

Allow the user to leave Learning Mode and return to Normal Mode without modifying remote definitions or creating additional configuration changes.

## Preconditions

- The remote is powered on.
- The remote is operating in Learning Mode.

## User Interaction

- The user presses and holds the MODE button.
- The MODE button remains pressed continuously for 2 seconds.
- The user releases the MODE button.

## Behaviour

### Exiting Learning Mode

When the MODE button has been held continuously for 2 seconds:

- The remote exits Learning Mode.
- The display changes from the learning screen to the normal display screen.
- The previously selected menu item remains selected.
- The current receive protocol remains unchanged.
- Any remote definitions previously learned during the session remain stored.
- The remote becomes ready to transmit commands using the selected remote.

### State Preservation

Exiting Learning Mode must not:

- Modify any existing remote definitions.
- Modify any stored button definitions.
- Change the selected remote.
- Change the active receive protocol.
- Create a new remote.
- Delete a remote.
- Transmit any IR command.

### Return To Normal Mode

After exiting Learning Mode:

- The remote menu is displayed.
- The selected menu item is displayed.
- The protocol associated with the selected menu item is displayed.
- The battery icon is displayed.
- Normal remote operation is restored.

## Success Criteria

- The user can reliably exit Learning Mode by holding MODE for 2 seconds.
- The normal display screen is shown.
- The selected menu item remains unchanged.
- The active receive protocol remains unchanged.
- Previously learned data remains available.
- The remote is immediately available for normal operation.

## Edge Cases

### MODE Released Before Hold Threshold

If MODE is released before 2 seconds have elapsed:

- Learning Mode is not exited.
- The MODE press is processed as a normal receive protocol selection action.
- The next receive protocol becomes active.
- The display updates to show the newly selected receive protocol.

### Waiting For IR Transmission

If the remote is currently waiting for an IR transmission when Learning Mode is exited:

- The receive operation is cancelled.
- No button definition is modified.
- The remote returns to Normal Mode.

### Add New Selected

If "Add New" is selected when Learning Mode is exited:

- Learning Mode exits normally.
- "Add New" remains selected.
- Exiting Learning Mode does not create a remote, this is defined by the Learn Button feature.

### Empty Learned Remote List

If no learned remotes exist when Learning Mode is exited:

- The remote returns to Normal Mode.
- "Add New" remains selected.

## Notes

- This feature is responsible only for the transition from Learning Mode to Normal Mode.
- Learning a button is defined by the **Learn Button** feature.
- Changing the receive protocol is defined by the **Change Receive Protocol** feature.
- Entering Learning Mode is defined by the **Enter Learning Mode** feature.
- Display layout details are intentionally excluded from this feature and should be specified elsewhere if required.
