---
title: MrxVerifyManager
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [achievement, target]
verified: true
verified_note: fixed fabricated Events section (no Event.* in source); added nCount to Instance pattern; noted tChangedCallback is populated by AddCallback but never read/invoked anywhere in this file
---

# MrxVerifyManager

*Module: mrxverifymanager.lua*

## Overview
The `MrxVerifyManager` module is responsible for managing and tracking the status of various targets in the game. It handles adding, updating, and removing targets, as well as checking achievements related to target completion. This module also manages callbacks for target status changes and maintains statistics on killed and captured targets.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxAchievements`

## Instance pattern
This is a stateless manager/utility module (module-level globals, no `Create`/`uGuid`/`tInstance` pattern — `Activated()` here is just a plain function, not the `OnActivate`/`Awake` world-object lifecycle). It tracks the following key fields:
- `tTargetListStatus`: A nested table that stores the status of each target, categorized by faction (`All`, `Chi`, `Civ`, `Gur`, `Oil`, `Pir`, `Pmc`, `Vza`).
- `sSolanoStatus`: The status of the Solano target ("alive", "killed", or "captured").
- `tChangedCallback`: A list of callbacks registered via `AddCallback`. Populated but never read or invoked anywhere in this file — no call site iterates it, so it appears to be dead code in this module (or consumed by code outside the decompiled corpus).
- `tTargetGuidList`: A mapping of GUIDs to target names for quick lookup.
- `nKilled` and `nCaptured`: Counters for the number of killed and captured targets, recomputed by `UpdateStats()`.
- `nCount`: Cached total target count, computed once by `GetTotal()` and reused on subsequent calls (starts at `0`, meaning `0 == "not yet computed"` — the count is never legitimately zero since `tTargetListStatus` is pre-populated with dozens of static keys).

## Functions
### `LoadSingleton(tSaveData)`
Loads saved data into the module. If no save data is provided, it does nothing. It logs a debug message and updates the target list status and Solano status from the save data.

### `SaveSingleton()`
Saves the current state of the module to a table. It logs a debug message and returns a table containing the target list status and Solano status.

### `Activated()`
Builds the GUID list for targets when the module is activated.

### `AddTarget(sTargetName, sStatus)`
Adds a new target with the specified name and status. If no status is provided, it defaults to "alive". It updates the target list status and calls functions to update statistics and check achievements.

### `UpdateTarget(sTargetName, sStatus)`
Updates the status of an existing target. If the target's GUID is provided instead of its name, it converts it to the target name. It updates the target list status and calls functions to update statistics and check achievements.

### `_CheckJusticeAchievement()`
Checks if the "Justice for All" achievement should be granted based on the current status of targets. If the conditions are met, it grants the achievement and logs a debug message.

### `CheckTechnoVikingAchievement()`
Checks if the Techno Viking achievement conditions are met. It returns true if the conditions are met, otherwise false.

### `_FindFactionFromName(sName)`
Finds the faction abbreviation associated with a target name by searching through the target list status.

### `BuildGuidList()`
Builds a mapping of GUIDs to target names for quick lookup. It logs the old and new count of targets in the list.

### `FindTargetFromGuid(uGuid)`
Finds the target name associated with a GUID. If the target is not found, it rebuilds the GUID list and tries again.

### `AddCallback(sTargetName, fCallback, tArgs)`
Adds a callback function to be executed when a target's status changes. It converts the target's GUID to its name if necessary and inserts the callback into the `tChangedCallback` table.

### `UpdateStats()`
Updates the counters for killed and captured targets by iterating through the target list status.

### `GetStatus(sTargetName)`
Retrieves the current status of a target by name. If the target's GUID is provided instead of its name, it converts it to the target name.

### `GetKilled()`
Returns the number of killed targets by updating statistics first.

### `GetCaptured()`
Returns the number of captured targets by updating statistics first.

### `CountCompleted(tTargets)`
Counts the number of completed (killed or captured) targets in a given list of targets.

### `GetCompletedTotal()`
Returns the total number of completed (killed or captured) targets by updating statistics first.

### `GetTotalFactionVZA()`
Returns the total number of targets for the VZA faction. Currently returns 0.

### `GetCompletedVZA()`
Returns the number of completed targets for the VZA faction as a string. Currently returns "0".

### `GetTotalFactionPMC()`
Returns the total number of targets for the PMC faction by counting entries in the target list status.

### `GetCompletedPMC()`
Returns the number of completed targets for the PMC faction by calling `CountCompleted`.

### `GetTotalFactionPIR()`
Returns the total number of targets for the PIR faction by counting entries in the target list status.

### `GetCompletedPIR()`
Returns the number of completed targets for the PIR faction by calling `CountCompleted`.

### `GetTotalFactionOIL()`
Returns the total number of targets for the OIL faction by counting entries in the target list status.

### `GetCompletedOIL()`
Returns the number of completed targets for the OIL faction by calling `CountCompleted`.

### `GetTotalFactionGUR()`
Returns the total number of targets for the GUR faction by counting entries in the target list status.

### `GetCompletedGUR()`
Returns the number of completed targets for the GUR faction by calling `CountCompleted`.

### `GetTotalFactionCIV()`
Returns the total number of targets for the CIV faction. Currently returns 0.

### `GetCompletedCIV()`
Returns the number of completed targets for the CIV faction as a string. Currently returns "0".

### `GetTotalFactionCHI()`
Returns the total number of targets for the CHI faction by counting entries in the target list status.

### `GetCompletedCHI()`
Returns the number of completed targets for the CHI faction by calling `CountCompleted`.

### `GetTotalFactionALL()`
Returns the total number of targets for the ALL faction by counting entries in the target list status.

### `GetCompletedALL()`
Returns the number of completed targets for the ALL faction by calling `CountCompleted`.

### `GetTotal()`
Returns the total number of targets across all factions. It caches the count to avoid recalculating it repeatedly.

### `SetKilledIfNotSet(sTargetName)`
Sets the status of a target to "captured" if its current status is not set or is "alive". It updates statistics and checks achievements.

### `SetSolanoVerified()`
Updates the status of the Solano target based on whether any targets have been killed. It sets the Solano status accordingly, updates the target list status, and checks achievements.

## Events
No `Event.*` calls appear anywhere in this file. `Activated()` (line 90) is presumably invoked by native/engine code (name suggests an activation hook) but has no visible `Event.Create` wiring in this module. All other lifecycle here (target status updates, achievement checks) is driven by direct function calls, not engine events.

## Notes for modders
- Use `AddTarget` and `UpdateTarget` to manage target statuses.
- Customize target properties by updating fields in `tTargetListStatus`.
- Be aware that achievements are automatically checked and granted based on target status changes.
- Ensure that callbacks are added correctly using `AddCallback` to handle custom logic when targets change.