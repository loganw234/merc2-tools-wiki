---
title: MrxTaskObjectiveEnterVehicle
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, vehicle]
verified: true
verified_note: deeper pass — confirmed the per-target Event.ObjectDeath + Event.ObjectInSeat wiring (seat "d" default, "a" when bUseAnySeat; persistent all-chars path when uPlayer == GetAllCharacters); documented uPlayer/bUseAnySeat config levers and the dynamic _GetShortDescription (pilot vs enter label)
---

# MrxTaskObjectiveEnterVehicle

*Module: mrxtaskobjectiveentervehicle.lua*

## Overview
The `MrxTaskObjectiveEnterVehicle` module is a task objective that requires the player to enter a specified vehicle. It handles setting up events for vehicle entry and death, managing target data, and providing descriptions and icons for the task.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: None

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page for the general mechanism), identified by name/lineage
rather than a world-object GUID. Key fields:
- `_tTargets`: A table containing target data, including events and status.
- `_bUseAllChars`: A boolean indicating whether all characters should be used for vehicle entry.
- `_uTgtObjFilter`: A filter for identifying target vehicles.

## Functions
### `Activated(self, tConfig)`
Called when the task objective is activated. It sets up default player configuration, retrieves target vehicles, and initializes events for each vehicle.

### `Cleanup(self)`
Cleans up all target events and calls the base class's cleanup method to ensure proper resource management.

### `_SetupEvents(self, uGuid)`
Per vehicle, creates an `Event.ObjectDeath` (→ `_OnStatusChange "destroyed"`) and an `Event.ObjectInSeat`
(→ `_TargetEntered`). Seat is `"d"` (driver) by default, or `"a"` (any) when config `bUseAnySeat` is set.
When `uPlayer == Player.GetAllCharacters()` it sets `_bUseAllChars` and uses a **persistent** seat event
requiring *every* player to be in the vehicle; otherwise it uses a one-shot seat event for `tConfig.uPlayer`.

### `_CleanupTargetEvents(self, tTargetData)`
Cleans up all events associated with a target vehicle to prevent memory leaks and ensure proper event management.

### `_OnStatusChange(self, sStatusType, uGuid)`
Handles changes in the status of a target vehicle (e.g., death). It calls any configured status change callback, cleans up target events, updates the target status, and cancels the task part.

### `_TargetEntered(self, uChar, uVehicle)`
Called when a player enters a target vehicle. It checks if all characters are using the vehicle (if applicable), cleans up target events, removes the target, and completes the task part.

### `_GetShortDescription(self)` *(instance override)*
Unlike most subclasses' static version, this builds the label from the first target vehicle's localized
name: `"[ContextAction.PilotVehicleName:<name>]"` if the vehicle has the `"helicopter"` label, else
`"[ContextAction.EnterVehicleName:<name>]"`; falls back to `"[Generic.ObjectiveEnterVehicle]"` when no name
is available.

### `_GetTargetRadarIcon()`
Returns the radar icon for the task objective, which is used in the game's radar system to indicate the type of objective.

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA (Personal Digital Assistant) icon for the task objective. The optional parameter determines whether a different icon should be returned.

### `_GetTargetGameSpaceIcon()`
Returns the game space icon for the task objective, which is used in the HUD (Heads-Up Display) to indicate the type of objective.

## Events
Created **per target vehicle** in `_SetupEvents` (stored in `_tTargets[uGuid].tEvents`):
- **`Event.ObjectDeath`** → `_OnStatusChange` (`"destroyed"`) — a destroyed target vehicle cancels the part.
- **`Event.ObjectInSeat`** → `_TargetEntered` — one-shot for a specific `uPlayer`, or **persistent** in the
  all-characters mode (only completes once *all* players are aboard).

Inherits [`MrxTaskObjective`](mrxtaskobjective)'s `Event.TimerRelative` initial-notes timer. It uses no
world/HUD-lifecycle callbacks.

## Notes for modders
- **`uPlayer`** (config) selects who must enter — defaults to `Player.GetAnyCharacter()` (any one player).
  Set it to `Player.GetAllCharacters()` to require the whole co-op team in the vehicle at once.
- **`bUseAnySeat`** lets riding in any seat count; without it, only the driver seat completes the objective.
- Reuses the base **action** art (radar `"objective_action"`, world `"HUD_objective_action"`, PDA
  `"icon_action_1_mc"`/`"_2_mc"`).