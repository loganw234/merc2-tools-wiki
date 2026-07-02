---
title: MoonPatrol
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, ai]
---

# MoonPatrol

*Module: moonpatrol.lua*

## Overview
The `MoonPatrol` module manages the behavior of a moon patrol vehicle in the game. It handles events related to the vehicle's activation, deactivation, and player interaction, including jump mechanics and visual effects.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tEvents`: A table to store event handles for each instance.
- `NETEVENT_STARTEMITTERS` and `NETEVENT_STOPEMITTERS`: Constants for network events related to starting and stopping emitters.

## Functions
### `NetEventCallback(eventId, tArgs)`
Handles custom network events. It starts or stops emitters based on the event ID.

### `Init()`
Initializes the module by setting up an empty table for storing event handles.

### `Deinit()`
Deinitializes the module by clearing the event handles table.

### `OnActivate(uGuid, args)`
Called when the vehicle instance is activated. It triggers the `OnExit` function immediately.

### `OnDeath(uGuid)`
Called when the vehicle's underlying object dies. It deactivates the vehicle instance.

### `OnDeactivate(uGuid, args)`
Called when the vehicle instance is deactivated. It cleans up all registered events and removes them from the `tEvents` table.

### `OnEnter(uDriver, uGuid)`
Called when a player enters the vehicle's seat. It sets up events to handle player exit and co-op player session changes.

### `OnExit(uDriver, uGuid)`
Called when a player exits the vehicle's seat. It resets jump mechanics and stops emitters. If networking is active, it sends a network event to stop emitters on other clients.

### `StartEmitters(uGuid)`
Starts particle effects for the vehicle's exhaust system.

### `StopEmitters(uGuid)`
Stops particle effects for the vehicle's exhaust system.

### `OnJump(uGuid)`
Handles the jump action. It applies an impulse to the vehicle, starts emitters, and sets up a timer event to wait for landing.

### `WaitForLanding(uGuid)`
Called after the jump duration. It stops emitters and waits for the vehicle to land before resetting jump mechanics.

### `ResetJump(uGuid)`
Resets jump mechanics by setting up an event to handle the player pressing the jump button.

### `Deactivated(uGuid, tListOfObjects)`
Closes the gate of the vehicle and sets up a proximity event to reactivate it when nearby objects are detected.

## Events
- Listens for `Event.ObjectInSeat` to call `OnEnter` or `OnExit` based on player entry/exit.
- Listens for `Event.ScriptEvent` with `"mpPlayerLeft"` to handle co-op player session changes and trigger `OnExit`.
- Listens for `Event.TimerRelative` to wait for landing after a jump.
- Listens for `Event.ObjectIsGrounded` to reset jump mechanics when the vehicle lands.

## Notes for modders
- Ensure that `OnActivate`, `OnDeactivate`, and related functions are called appropriately to manage the vehicle's lifecycle.
- Customize jump mechanics by modifying the impulse values or emitter effects in `StartEmitters` and `StopEmitters`.
- Be aware of network synchronization (`Net.SendCustomEvent`) when extending this module for multiplayer support.