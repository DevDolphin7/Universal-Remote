# Learn Button

## Purpose

Allow the user to program or update a button definition using an infrared signal received from another remote control.

The feature supports:

- Updating existing button definitions.
- Creating new button definitions.
- Capturing button press commands.
- Capturing button release commands when present.
- Updating the protocol associated with a remote.
- Creating a new remote when learning against the Add New menu item.

## Preconditions

- The remote is powered on.
- The remote is operating in Learning Mode.
- A menu item is selected.
- A receive protocol is selected.

## User Interaction

- The user presses one of:
  - NAV_UP
  - NAV_DOWN
  - NAV_LEFT
  - NAV_RIGHT
  - NAV_OK
  - VOL_UP
  - VOL_DOWN
  - CH_UP
  - CH_DOWN

- The selected button becomes ready for learning.
- The user transmits an IR command using the original remote.

## Behaviour

### Selecting A Button

When a programmable button is pressed whilst in Learning Mode:

- The button becomes the target button for learning.
- Any previously selected target button is cleared.
- The display indicates that the remote is waiting for an IR transmission.
- The active receive protocol is used to decode incoming signals.

### Receiving A Command

When a valid IR command is received:

- The received protocol data is decoded.
- The command is temporarily stored.
- The system waits up to 200 milliseconds for a second command.

### Learning Press And Release Commands

If a second valid command is received within 200 milliseconds:

- The first command becomes the press command.
- The second command becomes the release command.

If no second valid command is received within 200 milliseconds:

- The first command becomes the press command.
- No release command is stored.

### Updating Existing Buttons

If the selected menu item is an existing remote:

- The target button definition is updated.
- Any previous definition for that button is replaced.
- The remote protocol is updated to match the currently active receive protocol.
- The updated remote definition is saved to persistent storage.

### Creating A New Remote

If the selected menu item is Add New:

- A new remote is created.
- The learned button becomes the first button definition within that remote.
- The remote protocol is set to the currently active receive protocol.
- The remote is assigned the next available sequential name.
- The remote definition is saved to persistent storage.
- The newly created remote becomes selected.

Example:

- Remote 1
- Remote 2
- Add New

After successful learning:

- Remote 1
- Remote 2
- Remote 3
- Add New

Remote 3 becomes selected.

### Subsequent Learning On Newly Created Remotes

After a new remote has been created:

- The remote remains selected.
- Future learn operations update the existing remote.
- Additional learn operations do not create further remotes unless Add New is explicitly selected.

### Successful Learning

Following a successful learn operation:

- The learned data is saved.
- The selected button is cleared.
- No button remains selected for learning.
- The display indicates successful learning.
- The remote remains in Learning Mode.
- The current receive protocol remains unchanged.
- The same menu item remains selected unless a new remote was created.

### Learning Timeout

If no valid IR command is received within 30 seconds:

- The learn operation is cancelled.
- The selected button is cleared.
- No button definition is modified.
- The display returns to the Learning Mode idle state.

## Success Criteria

### Learn Single Command

Given:

- A button is selected for learning.
- A valid IR command is received.

When:

- No second command is received within 200 milliseconds.

Then:

- A press command is learned.
- No release command is stored.
- The button definition is saved.
- The selected button is cleared.

### Learn Press And Release Commands

Given:

- A button is selected for learning.

When:

- Two valid IR commands are received within 200 milliseconds.

Then:

- The first command becomes the press command.
- The second command becomes the release command.
- Both commands are saved.
- The selected button is cleared.

### Update Existing Button

Given:

- The selected remote already contains a definition for the button.

When:

- Learning completes successfully.

Then:

- The previous definition is replaced.
- The remote protocol is updated to match the active receive protocol.
- The new definition is saved.

### Create New Remote

Given:

- Add New is selected.

When:

- Learning completes successfully.

Then:

- A new remote is created.
- The learned button is stored.
- The remote protocol is stored.
- The new remote becomes selected.

## Edge Cases

### Different Button Selected Before Learning Completes

Given:

- A button has been selected for learning.
- No valid IR command has yet been received.

When:

- The user presses a different programmable button.

Then:

- The previously selected button is cleared.
- The newly pressed button becomes the target button for learning.
- The display updates to show the new learning target.
- The system continues waiting for an IR transmission.

### No Command Received

Given:

- A button has been selected for learning.

When:

- No valid IR transmission is received within 30 seconds.

Then:

- Learning is cancelled.
- The selected button is cleared.
- No configuration is modified.

### Invalid IR Transmission

Given:

- A button has been selected for learning.

When:

- An invalid or undecodable IR transmission is received.

Then:

- The transmission is ignored.
- The system continues waiting for a valid command.
- The timeout period continues.

### Learning Cancelled By Exiting Learning Mode

Given:

- A button has been selected for learning.
- The system is waiting for an IR transmission.

When:

- The user exits Learning Mode.

Then:

- The learn operation is cancelled.
- The selected button is cleared.
- No button definition is modified.
- No remote is created.

### Existing Button Overwritten

Given:

- A button already contains a stored definition.

When:

- Learning completes successfully.

Then:

- The previous definition is permanently replaced.

### First Learned Remote

Given:

- No learned remotes exist.
- Add New is selected.

When:

- Learning completes successfully.

Then:

- Remote 1 is created.
- Remote 1 becomes selected.
- Add New remains available.

## Notes

- This feature is responsible for learning and storing button definitions.
- This feature is responsible for updating the protocol associated with a remote.
- This feature is responsible for creating new remotes when Add New is selected.
- A remote may only use a single protocol.
- Protocols are associated with remotes, not individual buttons.
- Exiting Learning Mode does not create a remote, this is defined by this feature.
- Entering Learning Mode is defined by the **Enter Learning Mode** feature.
- Exiting Learning Mode is defined by the **Exit Learning Mode** feature.
- Receive protocol selection is defined by the **Change Receive Protocol** feature.
- Display layout details are intentionally excluded from this feature and should be specified elsewhere if required.
