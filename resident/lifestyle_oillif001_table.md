---
title: LifestyleOilLif001Table
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [lifestyle, vehicle]
verified: true
verified_note: added the module-load-time Debug.Printf, noted SetStaging's unused self param and lack of nil-guard on riders/count assumption; events section confirmed empty.
---

# LifestyleOilLif001Table

*Module: lifestyle_oillif001_table.lua*

## Overview
The `LifestyleOilLif001Table` module is responsible for initializing and managing the state of a specific vehicle asset model named "OilLif001 Table". It sets up two riders in the vehicle with predefined states related to an arm wrestling job.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state and operates globally on the specified vehicle asset model.

## Functions
### Module-load statement
`Debug.Printf("Adding asset model")` runs at module-load time — not inside any function — so it fires
once when this file is loaded/compiled by the engine, before `Init` is ever called.

### `Init()`
Called during the initialization phase of the game. Logs `"Init called"` and then calls `SetStaging()`
(with no arguments, despite `SetStaging` declaring a `self` parameter — see below).

### `SetStaging(self)`
Sets up the staging for the "OilLif001 Table" vehicle. Logs `"SetStaging Called"`, looks up the vehicle's
GUID via `Pg.GetGuidByName("OilLif001 Table")`, and iterates `Vehicle.GetRiders(stageTable)` with
`pairs`, assigning the first iterated rider to the global `iRider1` and every subsequent rider to the
global `iRider2` (so with more than two riders, `iRider2` ends up holding whichever rider `pairs`
enumerates last, silently overwriting earlier ones — the loop does not `break` after finding a second
rider). Then calls `Human.SetState(iRider1, "InVehicle", "lifestylejobPlayerArmwrestlingWinningloop01")`
and `Human.SetState(iRider2, "InVehicle", "lifestylejobOpponentArmwrestlingWinningloop01")`, and logs
`"At end of function"`. The declared `self` parameter is never read in the function body and `Init` never
passes an argument for it — dead parameter, always `nil` when called from `Init`. No `nil`-guard exists
if the vehicle has fewer than two riders (`iRider2`, or both, could be left `nil` and passed straight
into `Human.SetState`).

## Events
- Listens for none (no engine events are subscribed to or fired).

## Notes for modders
- Ensure that the vehicle asset model "OilLif001 Table" exists in the game world.
- The `SetStaging` function assumes there are exactly two riders in the vehicle, using an unguarded `pairs` loop
  with no `break` — with 0, 1, or 3+ riders the `iRider1`/`iRider2` assignment will be `nil` or wrong
  (see Functions above). If this is not the case, additional logic may be needed to handle different numbers of riders.
- The states set for the riders (`lifestylejobPlayerArmwrestlingWinningloop01` and `lifestylejobOpponentArmwrestlingWinningloop01`) are specific to the arm wrestling job scenario. Adjust these states as necessary for different scenarios.
- This module does not handle any lifecycle events (e.g., `OnActivate`, `OnDeactivate`). It is purely a one-time initialization script driven by `Init()`.
- `iRider1`/`iRider2` are left as plain globals (no `local`), so they're visible/overwritable from any other script in the environment.