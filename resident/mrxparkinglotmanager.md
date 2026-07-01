---
title: MrxParkingLotManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [parking lot, tutorial, vehicle]
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
- Listens for `Event.ObjectInSeat` to call `_TrackVehicle` when a vehicle enters or leaves a seat.
- Listens for `Event.ScriptEvent` with the name "parkingLotStart" to call `_MoveVehicle` when a parking lot start event is triggered.
- Listens for custom events related to vehicle state changes (`eMarkEnter`, `eMarkDeath`, `eMarkHibernation`) to unmark vehicles as needed.
- Listens for tutorial-related timers (`eTutorial`) to manage the display of tutorial messages.

## Notes for modders
- Ensure that `Setup` and `Cleanup` are called appropriately to manage the lifecycle of parking lot events and state.
- Customize vehicle selection criteria by modifying the conditions in `_TrackVehicle` and `_GetLastVehicle`.
- Adjust tutorial timing and content by changing `kfTutorialTime` and the messages passed to `MrxTutorialManager.ShowMessage`.
- Be aware that network synchronization (`Net.IsServer`) may affect multiplayer behavior when managing world markers and radar objectives.