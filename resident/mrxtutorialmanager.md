---
title: MrxTutorialManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [tutorial, manager]
verified: true
verified_note: "deeper pass: re-confirmed all functions/Events (no Event.* in file) against source; added the full _tTutorials catalog (22 tutorial keys -> WifTutorial* module names, the valid StartTutorial names) and noted the Sys.TutorialsEnabled() gate; made modder notes actionable"
---

# MrxTutorialManager

*Module: mrxtutorialmanager.lua*

## Overview
The `MrxTutorialManager` module is responsible for managing in-game tutorials. It handles the creation, activation, and completion of various tutorial modules, ensuring that players receive appropriate guidance based on their actions within the game.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module (module-level globals, no `Create`/`uGuid`/`tInstance` pattern). It tracks the following key fields:
- `_tTutorials`: A table containing data for each tutorial, including its module name and whether it has been completed.
- `_sCurrentActiveTutorial`: The identifier of the currently active tutorial.
- `_sCurrentMessage`: The text of the tutorial message currently displayed (set/cleared by `ShowMessage`/`HideMessage`).
- `_bMessageDisplayed`: Whether a tutorial message is currently showing.

## Tutorial catalog

`_tTutorials` is the master registry: each key is the **tutorial name** you pass to `StartTutorial` /
`GetTutorial`, mapping to the `WifTutorial*` module `Setup` dynamically imports. The 22 built-in tutorials:

| Name | Module | Name | Module |
|---|---|---|---|
| `Swimming` | `WifTutorialSwimming` | `Alarm` | `WifTutorialAlarm` |
| `WheeledVehicleBasic` | `WifTutorialWheeledVehicleBasic` | `AirstrikeInterrupt` | `WifTutorialAirstrikeInterrupt` |
| `Boats` | `WifTutorialBoat` | `HeliRepairPad` | `WifTutorialHeliRepairPad` |
| `Tanks` | `WifTutorialTank` | `TankHijack` | `WifTutorialTankHijack` |
| `Helicopters` | `WifTutorialHelicopter` | `CoopTether` | `WifTutorialCoopTether` |
| `C4` | `WifTutorialC4` | `APC` | `WifTutorialAPC` |
| `CollateralDamage` | `WifTutorialCollateralDamage` | `VehicleDisguise` | `WifTutorialVehicleDisguise` |
| `Trespass` | `WifTutorialTrespass` | `Collectibles` | `WifTutorialCollectibles` |
| `NoFuel` | `WifTutorialNoFuel` | `GateHonk` | `WifTutorialGateHonk` |
| `LowFuel` | `WifTutorialLowFuel` | `C4Switch` | `WifTutorialC4Switch` |
| `AlliesHonk` | `WifTutorialAlliesHonk` | `CoopRevive` | `WifTutorialCoopRevive` |

These are the exact strings other modules pass, e.g. [`MrxPmc`](mrxpmc) fires `StartTutorial("NoFuel")` /
`"LowFuel"`, [`MrxFactionManager`](mrxfactionmanager) fires `"CollateralDamage"`.

## Functions
### `Reset()`
Resets the tutorial system by clearing the current active tutorial and destroying events associated with all tutorials. Also hides any displayed messages.

### `Setup()`
Sets up the tutorial system by resetting it and then initializing each tutorial that has not been completed. It dynamically imports each tutorial module and creates an instance of it, setting up activation criteria.

### `BeginCustomTutorial(sIdentifierName, bDontNetSync)`
Begins a custom tutorial if tutorials are enabled and no other tutorial is currently active. Sets the current active tutorial to the specified identifier name.

### `EndCustomTutorial(sIdentifierName, bDontNetSync)`
Ends a custom tutorial if it matches the current active tutorial. Hides any displayed messages and clears the current active tutorial.

### `StartTutorial(sTutorialName, bDontNetSync)`
Activates a specific tutorial if it has not been completed and its instance exists.

### `SetCurrentTutorial(oTutorial, bDontNetSync)`
Sets the current tutorial by displaying its message. Returns false if tutorials are disabled or if a message is already displayed.

### `UpdateCurrentTutorial(oTutorial, bDontNetSync)`
Updates the current tutorial by displaying its message. Returns false if the tutorial name does not match the current active tutorial.

### `HideCurrentTutorial(oTutorial, bComplete, bDontNetSync)`
Hides the current tutorial and marks it as complete in the save data. Returns true if successful.

### `GetTutorial(sTutorial)`
Retrieves the instance of a specific tutorial.

### `DestroyTutorial(oTutorial)`
Destroys a tutorial by removing its module and clearing its instance.

### `ShowMessage(sMessage, bDontNetSync, sIdentifierName)`
Displays a tutorial message. If networking is enabled and not disabled, it sets the tutorial message on the server. Returns false if the same message is already displayed or if another tutorial is active.

### `HideMessage(bDontNetSync, sIdentifierName)`
Hides the current tutorial message. If networking is enabled and not disabled, it clears the tutorial message on the server.

### `SaveSingleton()`
Saves the state of completed tutorials by returning a list of their names.

### `LoadSingleton(tSaveData)`
Loads the saved data for completed tutorials, marking them as complete in the module's internal state.

## Events
No `Event.*` calls appear anywhere in this file. Tutorial activation/completion is driven entirely by direct function calls (`Setup`, `StartTutorial`, `SetCurrentTutorial`, `HideCurrentTutorial`, etc.) from other modules (individual `WifTutorial*` modules), not by engine events raised here. Networking uses `Net.SetTutorialMessage`/`Net.IsServer` directly, not the `Event` system.

## Notes for modders
- **Trigger a built-in tutorial** with `MrxTutorialManager.StartTutorial(<name>)` using a key from the catalog
  above. It no-ops if that tutorial is already `bComplete` or its instance hasn't been imported yet.
- **Everything is gated by `Sys.TutorialsEnabled()`** — `BeginCustomTutorial`, `SetCurrentTutorial`, and
  `ShowMessage` all early-out when tutorials are off. If your tutorial calls silently do nothing, that setting
  is the first suspect.
- **Only one tutorial message shows at a time**: `ShowMessage` refuses to display if the same message is
  already up, or if a different `_sCurrentActiveTutorial` owns the slot. `_bMessageDisplayed` /
  `_sCurrentMessage` track this.
- **Add a custom tutorial** by inserting a `{sModuleName = "YourModule"}` entry into `_tTutorials` before
  `Setup` runs (subclass [`MrxTutorial`](mrxtutorial) for the module). `SaveSingleton`/`LoadSingleton` persist
  only the set of completed tutorial names.
- Message text/network flows through `Hud.Tutorial:SetText` and (server, unless `bDontNetSync`)
  `Net.SetTutorialMessage`.