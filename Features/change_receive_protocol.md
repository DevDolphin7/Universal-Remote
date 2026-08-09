## Change Receive Protocol

### Purpose

Allow the user to select which infrared receive protocol is used whilst in Learning Mode.

The selected receive protocol determines:

- How incoming IR transmissions are decoded during learning.
- Which transmit protocol becomes associated with a remote following a successful learn operation.

### Preconditions

- The remote is powered on.
- The remote is operating in Learning Mode.

### User Interaction

- The user performs a short press of the MODE button whilst in Learning Mode.

### Behaviour

#### Cycling Receive Protocols

When the MODE button is pressed:

- The next receive protocol becomes active.
- The display updates to show the newly selected protocol.
- When the final protocol is reached, selection wraps to the first protocol.

Example:

NEC  
→ Sony  
→ Philips  
→ MCE  
→ NEC

#### Active Receive Protocol

The active receive protocol:

- Determines how incoming IR transmissions are decoded.
- Is used for all subsequent learn operations.
- Remains active until another protocol is selected.
- Remains active when learning completes successfully.
- Remains active when a learn operation times out.
- Remains active when entering Learning Mode.
- Remains active when leaving Learning Mode.

#### Receive And Transmit Protocol Relationship

A receive protocol corresponds to a matching transmit protocol.

When learning completes successfully:

- The active receive protocol becomes associated with the target remote.
- The matching transmit protocol becomes associated with the target remote.
- Future remote transmissions use that protocol.
- Protocol storage behaviour is defined by the Learn Button feature.

Example:

- Sony receive protocol successfully decodes a learned command.
- The remote is stored as a Sony remote.
- Future transmissions from that remote use the Sony transmit protocol.

#### Learn Button Integration

When a button is selected for learning:

- The currently active receive protocol is used to decode incoming IR signals.

When learning completes successfully:

- The protocols associated with the target remote are updated to match the active receive protocol and matching transmit protocol.

#### Display Behaviour

Whenever the active receive protocol changes:

- The displayed protocol updates immediately.
- The display always reflects the currently active receive protocol.

### Success Criteria

#### Select Next Protocol

Given:

- NEC is active.

When:

- MODE is pressed.

Then:

- Sony becomes active.
- Sony is displayed.

#### Wrap Around

Given:

- MCE is active.

When:

- MODE is pressed.

Then:

- NEC becomes active.
- NEC is displayed.

#### Learn Using Selected Protocol

Given:

- Sony is the active receive protocol.
- A button is selected for learning.

When:

- A valid Sony transmission is received.

Then:

- The transmission is decoded using the Sony protocol.

#### Protocol Persists During Learning Session

Given:

- Philips is active.

When:

- Learning completes successfully.

Then:

- Philips remains the active receive protocol.

#### Remote Protocol Updated Following Learning

Given:

- NEC is active.
- TV Remote is selected.

When:

- Learning completes successfully.

Then:

- TV Remote becomes associated with NEC.
- Future transmissions from TV Remote use NEC.

### Edge Cases

#### MODE Held For 2 Seconds

Given:

- The remote is operating in Learning Mode.

When:

- MODE is held continuously for 2 seconds.

Then:

- The protocol is not changed.
- The remote exits Learning Mode.
- Exit behaviour is defined by the Exit Learning Mode feature.

#### Protocol Changed Whilst Waiting For IR Transmission

Given:

- A button has been selected for learning.
- The system is waiting for an IR transmission.

When:

- MODE is pressed.

Then:

- The selected button remains selected.
- The active receive protocol changes.
- The display updates to show the new protocol.
- The learning timeout is reset.
- Subsequent received transmissions are decoded using the newly selected protocol.

#### Unsupported Transmission

Given:

- NEC is the active receive protocol.

When:

- A transmission using a different protocol is received.

Then:

- The transmission is treated as invalid.
- No button definition is modified.
- The system continues waiting for a valid transmission.
- The timeout period continues.

### Notes

- This feature is responsible for selecting the active receive protocol.
- This feature indirectly determines which transmit protocol becomes associated with a remote after successful learning.
- Protocol association with a remote is finalised by the Learn Button feature.
- This feature does not define how protocol decoding is implemented.
- This feature does not define how protocol transmission is implemented.
- This feature does not define how button learning is performed.
- Learning behaviour is defined by the Learn Button feature.
- Entering Learning Mode is defined by the Enter Learning Mode feature.
- Exiting Learning Mode is defined by the Exit Learning Mode feature.
- The display must always show the currently active receive protocol whilst in Learning Mode.
