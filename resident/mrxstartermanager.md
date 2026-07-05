---
title: MrxStarterManager
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, manager]
verified: true
verified_note: 'deeper pass: re-confirmed all functions and the corrected Events section (no Event.*; the
  attitude listener is MrxFactionManager.CreatePersistentAttitudeChangeEvent, not engine Event.*); confirmed
  RequestStarter is the memoized accessor over CreateStarter and that CreateStarter auto-sets HeliPilot/
  Mechanic/JetPilot recruited flags by starter ID; MrxHqManager still an unused import.'
---

# MrxStarterManager

*Module: mrxstartermanager.lua*

## Overview
The `MrxStarterManager` module is responsible for managing game starters, which are likely key mission or support elements in the game. It handles the creation, activation, deactivation, and destruction of these starters, as well as their associated briefings and fanfare displays.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxFactionManager`, `MrxHqManager`, `MrxStarter`, `MrxSupportData`, `WifStarterData`. Note:
  `MrxHqManager` is imported at the top of the file but has no further reference anywhere in source —
  appears to be a dead/unused import.

## Instance pattern
This is a stateless manager utility module. It tracks the following key fields:
- `_tStarters`: A table that holds all active starters, indexed by their names.

## Functions
### `Init()`
Initializes the module by setting up a persistent faction attitude change event listener. This event triggers a refresh of briefing room displays for all starters when the PMC faction's attitude changes. It also initializes support data by setting recruited statuses for heli pilot, mechanic, and jet pilot to false.

### `GetStarter(sName)`
Retrieves an active starter by its name from the `_tStarters` table.

### `GetStarters()`
Returns the entire `_tStarters` table containing all active starters.

### `RequestStarter(sName, bFanfareDisplayed)`
Requests a starter by its name. If the starter already exists, it returns the existing instance; otherwise, it creates a new one using `CreateStarter`.

### `CreateStarter(sName, bFanfareDisplayed)`
Builds a fresh [`MrxStarter`](mrxstarter) from `WifStarterData[sName]` (`MrxStarter:Create(tStarterData)`),
optionally marks its fanfare shown, `Activate`s it, and stores it in `_tStarters[sName]`. If the starter is a
PMC recruit, it flips the matching [`MrxSupportData`](mrxsupportdata) recruited flag by starter ID:
`"HelPmcBoss"` → heli pilot, `"MecPmcBoss"` → mechanic, `"JetPmcBoss"` → jet pilot. Prefer `RequestStarter`
(which memoizes) over calling this directly — calling `CreateStarter` twice for the same name overwrites the
first instance in `_tStarters`.

### `DestroyStarter(sName)`
Destroys a starter by its name by deactivating it and removing it from the `_tStarters` table.

### `DestroyAllStarters()`
Deactivates and removes all starters from the `_tStarters` table.

### `GetStarterIndexFromName(sStarterName)`
Retrieves the index of a starter by its name from the `WifStarterData._sStarters` list. Logs a warning if the starter name is not found.

### `GetStarterNameFromIndex(nStarterIndex)`
Retrieves the name of a starter by its index from the `WifStarterData._sStarters` list. Logs a warning if the starter index is not found.

### `SaveSingleton()`
Saves the state of all active starters, including whether fanfare and card displays have been shown, as well as their intros and old briefings.

### `LoadSingleton(tSaveData)`
Loads the saved state of starters from the provided save data. It recreates each starter with its saved status and updates its internal state accordingly.

## Events
No `Event.*` references anywhere in this file — this module does not use the engine's `Event.Create`
system directly. `Init()` registers a callback via `MrxFactionManager.CreatePersistentAttitudeChangeEvent(
{nil, "Pmc", nil, nil}, function() ... end)` — that's `MrxFactionManager`'s own event-registration API
(imported, not defined here), fired whenever the PMC faction's attitude changes. The anonymous callback
loops `_tStarters` and calls `oStarter:RefreshBriefingRoomDisplay()` on each.

## Notes for modders
- Ensure that starters are requested and destroyed appropriately using `RequestStarter` and `DestroyStarter`.
- Use `SaveSingleton` and `LoadSingleton` to manage the persistent state of starters.
- Be aware of the dependencies on imported modules like `MrxFactionManager`, `MrxSupportData`, and `WifStarterData`.
- `Init()` unconditionally resets `MrxSupportData`'s heli-pilot/mechanic/jet-pilot recruited flags to
  `false` — calling `Init()` again after starters already exist will not un-recruit existing starter
  instances, but will reset the recruited-flag state that gates equipping those support items elsewhere.