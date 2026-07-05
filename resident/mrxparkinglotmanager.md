---
title: MrxParkingLotManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [parking lot, tutorial, vehicle]
verified: true
verified_note: found likely bug in _TrackVehicle (references undeclared global uVeh instead of parameter uVehicle); corrected Events section to name all real Event.* constants (ObjectDeath, ObjectHibernation, TimerRelative were missing).
---

# MrxParkingLotManager

*Module: mrxparkinglotmanager.lua*

## Overview
The `MrxParkingLotManager` module is responsible for managing parking lots in the game. It tracks vehicles entering and leaving seats, handles vehicle movement to designated parking points, and manages tutorial messages related to parking lot interactions.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxTutorialManager`, `MrxUtil`, `MrxGui`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `_tParkingLotCandidates`: A table of candidate vehicles for parking.
- `_uNewParkingLotVeh`: The GUID of the vehicle currently being parked.
- `_uWorldMarker`: The world marker used to indicate the parking location.
- `_uParkingLotVeh`: The GUID of the vehicle currently marked for parking.
- `eParkingLotTracker`: An event handle for tracking vehicles entering seats.
- `eParkingLotTriggered`: An event handle for handling parking lot start events.
- `eMarkEnter`, `eMarkDeath`, `eMarkHibernation`: Event handles for managing vehicle state changes.
- `eTutorial`: An event handle for managing tutorial messages.

## Functions
### `Setup()`
Initializes the module by setting up persistent event listeners for tracking vehicles entering seats and handling parking lot start events. It also initializes the list of parking lot candidates.

### `Cleanup()`
Cleans up all event listeners and unmarks any currently marked vehicle, ensuring a clean shutdown of the module.

### `MarkLastVehicle()`
Unmarks any currently marked vehicle and marks the last vehicle in the parking lot candidates list as the new marked vehicle.

### `_TrackVehicle(uChar, uVehicle)`
Adds a vehicle to the list of parking lot candidates if it is alive and not a boat or emplaced weapon. If the candidate list exceeds the limit (`kiParkingLotLimit`), the oldest candidate is removed.

**Likely bug, confirmed in source:** the boat/emplaced-weapon check reads `Object.HasLabel(uVeh, "Boat")` / `Object.HasLabel(uVeh, "Emplacedweapon")` — but the function's parameter is named `uVehicle`, not `uVeh`. `uVeh` is never assigned anywhere in this file, so it's an undeclared global (`nil` unless some other loaded module happens to set a global of that exact name). In practice this means the boat/emplaced-weapon exclusion check almost certainly never filters the vehicle actually passed in — `Object.HasLabel(nil, ...)` — so boats and emplaced weapons likely get added to the candidate list despite the apparent intent to exclude them.

### `_MoveVehicle(tData)`
Moves the last vehicle in the parking lot candidates list to a designated parking point based on its type (normal or helicopter). It also cleans up any remaining vehicles in the candidate list after moving the selected one.

### `_GetLastVehicle(uRefPos, uHeliPos)`
Retrieves the last vehicle from the parking lot candidates list that is alive and not currently occupied by a driver. The selection criteria include proximity to reference points and helicopter-specific conditions.

### `_MarkVehicle(uGuid)`
Marks a vehicle with a world blip and radar objective, indicating its position on the map. It also sets up event listeners for managing changes in the vehicle's state (entering seat, death, hibernation) and shows tutorial messages related to parking lot interactions.

### `_UnmarkVehicle()`
Removes any existing world marker and radar objective associated with a marked vehicle, deletes event listeners for managing vehicle state changes, and hides any active tutorial messages.

### `_ShowTutorial1()`
Shows the first tutorial message related to parking lots and sets up a timer to show the second tutorial message after `kfTutorialTime` seconds.

### `_ShowTutorial2()`
Shows the second tutorial message related to parking lots and sets up a timer to hide the tutorial messages after another `kfTutorialTime` seconds.

### `_HideTutorial()`
Hides any active tutorial messages and deletes the event listener for managing tutorial timers.

## Events
- `Event.ObjectInSeat` (persistent, via `Setup`) — filters on `Player.GetAnyCharacter(), 0, "d", "xo"`, calls `_TrackVehicle` when a vehicle is entered/exited.
- `Event.ScriptEvent` named `"parkingLotStart"` (persistent, via `Setup`) — calls `_MoveVehicle`.
- `Event.ObjectInSeat` again (non-persistent, via `_MarkVehicle`, handle `eMarkEnter`) — filters on `Player.GetAnyCharacter(), uGuid, "a", "ei"`, calls `_UnmarkVehicle`.
- `Event.ObjectDeath` (via `_MarkVehicle`, handle `eMarkDeath`) — calls `_UnmarkVehicle` if the marked vehicle dies.
- `Event.ObjectHibernation` filtered on `"hibernated"` (via `_MarkVehicle`, handle `eMarkHibernation`) — calls `_UnmarkVehicle`.
- `Event.TimerRelative` (via `_ShowTutorial1`/`_ShowTutorial2`, handle `eTutorial`) — chains `_ShowTutorial1` → `_ShowTutorial2` → `_HideTutorial`, each `kfTutorialTime` seconds apart.

## Notes for modders
- Ensure that `Setup` and `Cleanup` are called appropriately to manage the lifecycle of parking lot events and state.
- Customize vehicle selection criteria by modifying the conditions in `_TrackVehicle` and `_GetLastVehicle`.
- Adjust tutorial timing and content by changing `kfTutorialTime` and the messages passed to `MrxTutorialManager.ShowMessage`.
- Be aware that network synchronization (`Net.IsServer`) may affect multiplayer behavior when managing world markers and radar objectives.
- See the confirmed `uVeh`/`uVehicle` typo bug noted under `_TrackVehicle` above — if you're patching this module, that's the first thing to fix.