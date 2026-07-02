---
title: PursuitCopter
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: VehicleBlippable
tags: [vehicle, support]
---

# PursuitCopter

*Module: pursuitcopter.lua*

## Overview
The `PursuitCopter` module represents a pursuit helicopter that lands near the player and deploys passengers. It is part of the support system in the game, designed to provide reinforcements or additional forces during missions.

## Inheritance
- Inherits from: `VehicleBlippable`
- Imports: `MrxSupport`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tCopters`: A table to keep track of active pursuit copters.
- `tRetries`: A table to count the number of retries for finding a landing zone.

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
"couldn't complete the delivery, send the vehicle away" (see [Support & Airstrikes](../cat-support-airstrikes)).

### `AllOut(self, uGuid, nState)`
Handles the outcome of the landing goal. If successful, it deploys passengers; if not, it sends the copter home.

### `FindLZ(uGuid)`
Attempts to find a suitable landing zone for the pursuit copter using AI functions and sets up a callback to handle the result.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- Uses custom event callbacks (`FoundPosition`, `AllOut`) to manage the lifecycle of finding a landing zone and deploying passengers.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the copter's lifecycle.
- Customize the number of retries or landing zone parameters by modifying the `tRetries` table or adjusting the `FindLZ` function.
- Be aware that network synchronization may affect multiplayer behavior, especially if multiple pursuit copters are active simultaneously.