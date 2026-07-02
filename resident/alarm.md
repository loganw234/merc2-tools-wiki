---
title: Alarm
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [alarm, building]
---

# Alarm

*Module: alarm.lua*

## Overview
The `Alarm` module manages the activation and deactivation of alarms for occupied buildings within a 100-meter radius. It triggers an alarm when any building is occupied and auto-checks every 8 seconds, self-muting after 60 seconds if no buildings remain occupied.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `DangerousBuilding`, `MrxTutorialManager`

## Instance pattern
This module does not follow the per-instance object pattern. It maintains global state in tables like `tEvents` and `tLights`.

## Functions
### `NetEventCallback(nEventType, tArgs)`
Handles network events for alarm activation and deactivation by calling `NetSafeAlarmActivated` or `NetSafeAlarmDeactivated` based on the event type.

### `OnActivate(uGuid, iArg)`
Called when the alarm object is activated. Sets up initial state and schedules an event to call `Awake` once the object leaves hibernation.

### `SendPlayerJoinEventsAlarm(uGuid)`
Sends a network event to activate the alarm if it was previously active.

### `OnDeath(uGuid)`
Calls `OnDeactivate` when the alarm object dies.

### `OnDeactivate(uGuid)`
Cleans up all events and state associated with the alarm object.

### `SetupActivationEvents(uGuid)`
Sets up context actions and events for activating the alarm, including handling player joins.

### `SetupDeactivationEvents(uGuid)`
Sets up context actions and events for deactivating the alarm.

### `OnUse(uGuid, bEnabled)`
Handles the use of the alarm by either activating or deactivating it based on the `bEnabled` flag.

### `MuteAlarm(uGuid)`
Stops the alarm sound after 60 seconds if no buildings are occupied.

### `AlarmActivated(uGuid)`
Activates the alarm, turns on nearby occupied buildings, plays sounds, and sets up a check event to monitor building occupancy.

### `CheckAlarm(uGuid)`
Checks for any occupied buildings within the radius. If none are found, it deactivates the alarm.

### `AlarmDeactivated(uGuid)`
Deactivates the alarm, stops sounds, and resets parts of the alarm object.

### `NetSafeAlarmActivated(uGuid)`
Safely activates the alarm by ensuring the object is awake before proceeding with activation logic.

### `NetSafeAlarmDeactivated(uGuid)`
Safely deactivates the alarm by stopping sounds and resetting parts of the alarm object.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for custom event `mpPlayerJoin` to send player join events.
- Listens for network events `NETEVENT_ALARMACTIVATE` and `NETEVENT_ALARMDEACTIVATE` to handle alarm activation and deactivation.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the alarm lifecycle.
- Customize the alarm behavior by modifying the constants like building collect radius, recheck interval, and mute duration.
- Be aware of network synchronization as it affects multiplayer behavior.