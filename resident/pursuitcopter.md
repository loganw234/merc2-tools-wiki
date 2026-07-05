---
title: PursuitCopter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle, support]
verified: true
verified_note: added missing Event.TimerRelative to Events section, clarified Create resolves via inherited VehicleBlippable/Inheritable chain (not defined locally)
---

# PursuitCopter

*Module: pursuitcopter.lua*

## Overview
The `PursuitCopter` module represents a pursuit helicopter that lands near the player and deploys passengers. It is part of the support system in the game, designed to provide reinforcements or additional forces during missions.

## Inheritance
- Inherits from: `VehicleBlippable`
- Imports: `MrxSupport`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`), but `pursuitcopter.lua` itself defines no `Create`
— it inherits one through the chain `VehicleBlippable` → `OrientedBlippable` → `Blippable` →
`Inheritable`, none of which override `Create` after `Inheritable`, so `self:Create(uGuid, uRuntimeOwner)`
(called from `FoundPosition`, line 76) resolves all the way to `Inheritable.Create` — the standard
`setmetatable`/`tInstance[uGuid]` factory described on [Resident Modules](index). Module-level (not
per-instance) state:
- `tCopters`: a table (used as a queue) of GUIDs for copters currently mid-LZ-search.
- `tRetries`: retry counts, keyed by `uGuid`.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, uRuntimeOwner, iArg)`
Creates a new per-instance table for the object using the module's prototype and attempts to find a landing zone for the pursuit copter.

### `FoundPosition(bFound, x, y, z)`
A callback function that handles the result of finding a landing zone. If a valid LZ is found, it sets up a landing goal; otherwise, it retries or sends the copter home if too many attempts fail.

Exact retry behavior, read directly from source: **3 attempts**, tracked per-`uGuid` in `tRetries`. Each
failed attempt also nudges the pilot 50 units toward the player (`Ai.Goal({Goal = "MoveTo", ...})`)
before trying again 3 seconds later. On both "no LZ found at all" and "3 retries exhausted," it calls
`MrxSupport.GoHome(self, uGuid)` — the same fallback used elsewhere in the support-delivery system for
"couldn't complete the delivery, send the vehicle away" (see [Support & Airstrikes](cat-support-airstrikes)).

### `AllOut(self, uGuid, nState)`
Handles the outcome of the landing goal. If successful, it deploys passengers; if not, it sends the copter home.

### `FindLZ(uGuid)`
Attempts to find a suitable landing zone for the pursuit copter using AI functions and sets up a callback to handle the result.

## Events
- `Event.ObjectHibernation` (in `OnActivate`) — fires `Start` once the object leaves hibernation.
- `Event.TimerRelative` (in `FindLZ`, on retry) — schedules another `FindLZ` attempt 3 seconds later when
  `Ai.TestDropZone` fails to find a valid landing zone.
- `FoundPosition` and `AllOut` are not `Event.*` registrations themselves — they're passed as bare
  `Callback` fields to `Ai.TestDropZone` and `Ai.Goal`/`Ai.Deploy` respectively, which are native AI
  functions, not the `Event.Create` mechanism.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the copter's lifecycle.
- Customize the number of retries or landing zone parameters by modifying the `tRetries` table or adjusting the `FindLZ` function.
- Be aware that network synchronization may affect multiplayer behavior, especially if multiple pursuit copters are active simultaneously.