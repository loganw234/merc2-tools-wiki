---
title: MrxApcDrop
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [support, mission]
verified: true
verified_note: 'deeper pass: re-confirmed the DropCallback nil-call bug and class-factory pattern; corrected the Events section (ObjectDeath is the only real subscription; the _DropCallback chain is Ai.Goal/Ai.Deploy callbacks, not "custom events") and surfaced the inDestType/outDestType/config-field reference'
---

# MrxApcDrop

*Module: mrxapcdrop.lua*

## Overview
The `MrxApcDrop` module is a generic helper for mission scripts that involves flying in an APC (Armored Personnel Carrier), deploying a squad of passengers, and then flying out. It is config-driven and can handle different types of destinations (path, object, or coordinate) with customizable speeds.

## Inheritance
- Inherits from: `none` — base/utility module
- Imports: `MrxUtil`

## Instance pattern
This is a stateless manager/utility module that does not follow the per-instance pattern. It manages the lifecycle of an APC drop operation without maintaining persistent state across activations.

## Functions
### `Create(srcObj, tConfig)`
Initializes and starts the APC drop operation based on the provided configuration. It sets up AI goals for moving to the destination, deploying passengers, and flying out. If the vehicle is not alive, it logs an error message and returns early.

**Not mentioned above but confirmed in source:** if `tConfig.inDest` is falsy (no `inDest` configured), `Create`
skips the AI-goal setup entirely and instead calls `self:DropCallback()` immediately. This looks like a bug in
the game's own code — only `_DropCallback` (with a leading underscore) is actually defined anywhere in this
module, so that call would fail with an "attempt to call a nil value" error. This path is likely dead/never
exercised in practice, since every real caller apparently always supplies `inDest`.

### `Cancel(self)`
Cancels any ongoing events related to the APC drop operation, such as death events and exit delays.

### `_DropCallback(self)`
A private callback function that handles the deployment of passengers from the APC. It retrieves the riders and sets up a new AI goal for deploying them.

### `_DropCallback2(self)`
Another private callback function that handles the post-deployment actions, including taking off if it's a helicopter and moving to the out destination. It also commands the squad to move within a boundary around the target.

### `_CommandSquad(self)`
A private function that adds the deployed passengers to a specified squad and issues a command for them to move within a boundary around the target. It also calls any provided callback function once the operation is complete.

### `_GetGuidIfString(param)`
A helper function that converts a string parameter into a GUID using `Pg.GetGuidByName`. If the parameter is not a string, it returns the parameter as-is.

## Events
- **`Event.ObjectDeath`** (on the driver) is the only real subscription — stored as `self.eDeath`, fires
  `Cancel` if the driver dies mid-drop. It's registered only when `inDest` is supplied.
- `_DropCallback` and `_DropCallback2` are **not** events — they're passed as `Callback` fields to `Ai.Goal`
  / `Ai.Deploy` and run when those AI orders complete. (For a helicopter vehicle the move `Callback` is
  cleared and `_DropCallback` is instead wired to a separate `HeliLand` goal.)

## Notes for modders
- **Config table (`tConfig`) fields**, read in `Create`: `uVehicle` (required, must be alive),
  `inDest`/`inDestType`, `outDest`/`outDestType`, `inSpeed`/`outSpeed`, `squadName`, `squadTarget`,
  `squadOrder`, `fDropDoneCallback`, `MaintainRotorSpeed`. `inDestType`/`outDestType` each select the AI goal:
  `"path"` → `PathMove`, `"object"` → `MoveTo`, `"coord"` → `MoveToPos` (an unrecognized value just logs a
  warning and issues no move).
- **Defaults**: `inSpeed`/`outSpeed` default to `0.8` (via `MrxUtil.SetDefault`); the squad
  `MoveWithinBoundary` radius is `8`.
- **Pass strings or GUIDs**: `inDest`/`outDest`/`squadTarget` accept either — `_GetGuidIfString` resolves
  names through `Pg.GetGuidByName`, so you don't need to pre-resolve them.
- **Bug to avoid triggering**: omitting `inDest` sends `Create` down a `self:DropCallback()` path that calls
  a function that doesn't exist (only `_DropCallback` is defined) — see the note under `Create`. Always
  supply `inDest`.
- `fDropDoneCallback(uVehicle, tRiders)` fires once the squad has been commanded — use it to chain follow-up
  logic. This is a stateless helper: each `Create` call is an independent drop.