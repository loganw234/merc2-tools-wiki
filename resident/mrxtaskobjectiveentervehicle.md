---
title: MrxTaskObjectiveEnterVehicle
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, vehicle]
---

# MrxTaskObjectiveEnterVehicle

*Module: mrxtaskobjectiveentervehicle.lua*

## Overview
The `MrxTaskObjectiveEnterVehicle` module is a task objective that requires the player to enter a specified vehicle. It handles setting up events for vehicle entry and death, managing target data, and providing descriptions and icons for the task.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: None

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tTargets`: A table containing target data, including events and status.
- `_bUseAllChars`: A boolean indicating whether all characters should be used for vehicle entry.
- `_uTgtObjFilter`: A filter for identifying target vehicles.

## Functions
### `Activated(self, tConfig)`
Called when the task objective is activated. It sets up default player configuration, retrieves target vehicles, and initializes events for each vehicle.

### `Cleanup(self)`
Cleans up all target events and calls the base class's cleanup method to ensure proper resource management.

### `_SetupEvents(self, uGuid)`
Sets up events for a specific vehicle, including handling its death and entry by the player. It configures whether any seat can be used and sets up appropriate event listeners.

### `_CleanupTargetEvents(self, tTargetData)`
Cleans up all events associated with a target vehicle to prevent memory leaks and ensure proper event management.

### `_OnStatusChange(self, sStatusType, uGuid)`
Handles changes in the status of a target vehicle (e.g., death). It calls any configured status change callback, cleans up target events, updates the target status, and cancels the task part.

### `_TargetEntered(self, uChar, uVehicle)`
Called when a player enters a target vehicle. It checks if all characters are using the vehicle (if applicable), cleans up target events, removes the target, and completes the task part.

### `_GetShortDescription(self)`
Returns a short description of the task objective, including the name of the target vehicle. If no specific vehicle is found, it returns a generic description.

### `_GetTargetRadarIcon()`
Returns the radar icon for the task objective, which is used in the game's radar system to indicate the type of objective.

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA (Personal Digital Assistant) icon for the task objective. The optional parameter determines whether a different icon should be returned.

### `_GetTargetGameSpaceIcon()`
Returns the game space icon for the task objective, which is used in the HUD (Heads-Up Display) to indicate the type of objective.

## Events
- Listens for `Event.ObjectDeath` to handle vehicle death.
- Listens for `Event.ObjectInSeat` to detect when a player enters a vehicle seat.

## Notes for modders
- Ensure that the task objective is properly activated and cleaned up to manage events and resources effectively.
- Customize the target vehicle filter (`_uTgtObjFilter`) to specify which vehicles should be considered for the task.
- Use the `_GetShortDescription` function to provide a clear description of the task in the game interface.
- Be aware that network synchronization may affect multiplayer behavior, especially if multiple players are involved in entering the same vehicle.