---
title: MrxParkingLotManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [parking lot, tutorial, vehicle]
verified: true
verified_note: "deeper pass: re-confirmed the _TrackVehicle uVeh/uVehicle bug, the Events section, and Imports against source; surfaced the module constants (kiParkingLotLimit=8, kfTutorialTime=6, kiBlipSize=6), the blip/radar textures and tutorial message keys, and the parkingLotStart tData shape; made modder notes actionable"
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

## Module constants & tunables
| Constant | Value | Meaning |
|---|---:|---|
| `kiParkingLotLimit` | `8` | Max tracked candidate vehicles; adding a 9th drops the oldest. |
| `kfTutorialTime` | `6` | Seconds between the two parking-lot tutorial steps, and before auto-hide. |
| `kiBlipSize` | `6` | Radar objective width/height (animated up to `×1.2`). |

Other hard-coded strings worth knowing: the world marker icon is `"HUD_PMC_Fiona"` (primary-objective RGB from
[`MrxUtil.GetPrimaryObjectiveRgb`](mrxutil)), the radar texture is `"MiniMap_Icon_Faction_PMC"`, and the two
tutorial messages are `"[TUTORIAL.ParkingLot.First]"` / `"[TUTORIAL.ParkingLot.Second]"` (shown via
[`MrxTutorialManager.ShowMessage`](mrxtutorialmanager) under the identifier `"parkingLot"`).

The `"parkingLotStart"` script event that triggers `_MoveVehicle` carries
`tData = {uRefPoint, uNormalPoint, uHeliPoint}` — it's posted by [`MrxHq.ExitEnd`](mrxhq) when leaving an HQ.

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
- **Tune the feature** via the three `ki*`/`kf*` constants above — candidate count, tutorial pacing, blip size.
- **Selection distances are hard-coded** in `_GetLastVehicle`: a candidate qualifies within `65` units of the
  reference point, or (if it has the `"helicopter"` label) within `15` units of the heli point, and only if it
  has no driver. Edit those thresholds to change which parked vehicle gets moved.
- `_MoveVehicle` **removes every other candidate** in the list after picking one — so leftover vehicles near an
  HQ parking lot are despawned on exit, not just repositioned.

{: .warning }
> Confirmed source bug in `_TrackVehicle`: the boat/emplaced-weapon exclusion tests `Object.HasLabel(uVeh, ...)`
> but the parameter is `uVehicle`; `uVeh` is an undeclared (nil) global here, so the check never filters the
> vehicle actually passed in — boats and emplaced weapons get added to the candidate list despite the intent to
> skip them. Fix the identifier to `uVehicle` if you're patching this module.