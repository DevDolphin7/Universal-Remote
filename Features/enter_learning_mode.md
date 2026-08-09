# Enter Learning Mode

## Purpose

Allow the user to transition from Normal Mode into Learning Mode so that buttons can be programmed or updated using an existing infrared remote without requiring a computer connection.

## Preconditions

- The remote is powered on.
- The remote is operating in Normal Mode.

## User Interaction

- The user presses and holds the MODE button.
- The MODE button remains pressed continuously for 2 seconds.
- The user releases the MODE button.

## Behaviour

### Entering Learning Mode

When the MODE button has been held continuously for 2 seconds:

- The remote enters Learning Mode.
- The display changes from the normal display screen to the learning screen.
- The currently selected remote remains selected.
- The currently selected receive protocol remains active.
- The current receive protocol is displayed on screen.
- No button is selected for learning.
- The remote is not yet waiting for an IR transmission.

### State Preservation

Entering Learning Mode must not:

- Modify any existing remote definitions.
- Modify any stored button definitions.
- Change the selected remote.
- Change the active receive protocol.
- Create a new remote.
- Transmit any IR command.

### Add New Selection

If the selected remote is "Add New":

- Learning Mode is entered normally.
- "Add New" remains selected.
- No remote is created during entry into Learning Mode.
- Remote creation can only occur during a later successful learning operation.

## Success Criteria

- The user can reliably enter Learning Mode by holding MODE for 2 seconds.
- The learning screen is displayed.
- The selected remote remains unchanged.
- The current receive protocol is displayed.
- The remote is ready to begin the Learn Button workflow.
- No configuration is changed merely by entering Learning Mode.

## Edge Cases

### MODE Released Before Hold Threshold

If MODE is released before 2 seconds have elapsed:

- Learning Mode is not entered.
- The MODE press is processed as a normal remote selection action.
- The next remote in the list becomes selected.
- The display updates to show the newly selected remote.

### Existing Empty Remote

If the selected remote contains no learned button definitions:

- Learning Mode is entered normally.
- The remote remains available for programming.

### Add New Selected

If "Add New" is selected when Learning Mode is entered:

- Learning Mode is entered normally.
- No remote is created until a successful learn operation occurs.

## Notes

- This feature is responsible only for the transition from Normal Mode to Learning Mode.
- Learning a button is defined by the **Learn Button** feature.
- Changing the receive protocol is defined by the **Change Receive Protocol** feature.
- Leaving Learning Mode is defined by the **Exit Learning Mode** feature.
- Screen layout details are intentionally excluded from this feature and should be specified elsewhere if required.
