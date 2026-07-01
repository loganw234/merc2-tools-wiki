---
title: SpyHunter
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, boost]
---

# SpyHunter

*Module: spyhunter.lua*

## Overview
The `SpyHunter` module manages the behavior of the Spy Hunter vehicle in the game. It handles player entry and exit events, jump mechanics, boost meter display, and network synchronization for particle effects and sound cues.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module that tracks event handlers for each Spy Hunter instance. It uses the following key fields:
- `tEvents`: A table to store event handles for each Spy Hunter instance.
- `gbEnableBoostMeter`: A boolean flag to enable or disable the boost meter display.

## Functions
### `Init()`
Initializes the module by setting up an empty table `tEvents` to store event handlers.

### `Deinit()`
Deinitializes the module by clearing the `tEvents` table.

### `OnActivate(uGuid, args)`
Called when a Spy Hunter instance is activated. It initializes the event table for the instance and sets up initial events.

### `OnDeactivate(uGuid, args)`
Called when a Spy Hunter instance is deactivated. It cleans up all registered events for the instance.

### `OnEnter(uDriver, uGuid)`
Called when a player enters the Spy Hunter vehicle. It sets up events to handle exit and multiplayer player left scenarios, and starts the cool check process.

### `CoolCheck(uGuid)`
Checks if the Spy Hunter is ready for a jump. If it is, it resets the jump; otherwise, it schedules another check in 0.5 seconds.

### `OnExit(uDriver, uGuid)`
Called when a player exits the Spy Hunter vehicle. It stops any ongoing boost effects and sets up an event to handle re-entry.

### `NetEventCallback(eventId, tArgs)`
Handles network events related to boost particle effects and sound cues. It calls appropriate functions based on the event ID.

### `GetDriverGuid(uGuid)`
Retrieves the GUID of the driver controlling the Spy Hunter vehicle.

### `DisplayBoost(uGuid)`
Displays the boost meter on the HUD based on the current boost level.

### `ResetJump(uGuid)`
Resets the jump mechanics for the Spy Hunter, starting the boost effect and setting up the jump event handler.

### `NetSafeSmokeStop(uGuid)`
Stops the smoke particle effect safely by stopping the emitter.

### `SetupBoost(uGuid)`
Sets up the boost mechanics for the Spy Hunter, including starting the boost effect and sending a network event if active.

### `NetSafeSetupBoost(uGuid)`
Starts the boost particle effect safely by setting up the emitter.

### `OnJump(uGuid)`
Handles the jump mechanics for the Spy Hunter. It applies impulses based on the current jump stage and schedules the next jump or stops the boost if all jumps are completed.

### `StopBoost(uGuid)`
Stops the boost mechanics for the Spy Hunter, including stopping the boost effect and sending a network event if active.

### `NetSafeStopBoost(uGuid)`
Stops the boost particle effect safely by stopping the emitter.

### `NetSafeSmokeStart(uGuid)`
Starts the smoke particle effect safely by setting up the emitter.

### `DontSmoke(uGuid)`
Stops the smoke particle effect and sends a network event if active.

### `IsCool(uGuid)`
Marks the Spy Hunter as ready for another jump and resets it if there is a driver.

### `CoolDown(uGuid)`
Starts the cooldown process after a boost, including setting up smoke effects and sending network events if active. It also updates the boost meter display if enabled.

## Events
- Listens for `Event.ObjectInSeat` to handle player entry and exit.
- Listens for `Event.ScriptEvent` with `"mpPlayerLeft"` to handle multiplayer player left scenarios.
- Listens for `Event.TimerRelative` to schedule cool checks and cooldowns.
- Listens for custom network events (`NETEVENT_STARTEMITTERS`, `NETEVENT_STOPEMITTERS`, `NETEVENT_STARTEMITTERSMOKE`, `NETEVENT_STOPEMITTERSMOKE`) to manage particle effects and sound cues.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage Spy Hunter lifecycle.
- Use `DisplayBoost` to control the visibility of the boost meter on the HUD.
- Customize jump mechanics by modifying impulse values in `OnJump`.
- Be aware that network synchronization (`Net.SendCustomEvent`) may affect multiplayer behavior.