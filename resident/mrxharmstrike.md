---
title: MrxHARMStrike
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxHARMStrike

*Module: mrxharmstrike.lua*

## Overview
The `MrxHARMStrike` module is a support system for initiating and managing HARM (High-speed Anti-Radiation Missile) strikes. It extends the base `MrxSupport` class to provide functionality for designating targets, deploying an aircraft, and launching missiles at enemy vehicles.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorBeacon`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(oSelf, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who initiated the support.
- `uJet`: The GUID of the aircraft used for the strike.
- `oDesignator`: An instance of `MrxSupportDesignatorBeacon` used for target designation.

## Functions
### `Create(oSelf, uPlayerGuid)`
Creates a new per-instance table for the HARM strike support system. Initializes the designator beacon, sets the owner and recruit, and assigns the module name.

### `DesignationCallback(oSelf)`
Called when the target is designated. Calculates the spawn point and target position, normalizes vectors, and spawns an aircraft to perform the strike. Triggers sound cues for confirmation and aircraft flyby.

### `Strike(oSelf)`
Executes the HARM strike by finding nearby enemy vehicles within a 200-unit radius. For each vehicle with a driver, schedules a missile launch with a delay based on its index in the list of targets.

### `BombExplodes(uBomb)`
Called when a bomb explodes. Logs a debug message indicating a direct hit.

### `LaunchMissile(oSelf, uTarget)`
Calculates the vector from the aircraft to the target vehicle, normalizes it, and spawns a targeted ordnance (missile) towards the target. Registers a callback for when the bomb explodes.

## Events
- Listens for custom event `DesignationCallback` to initiate the strike after target designation.
- Listens for custom event `LaunchMissile` to launch missiles at designated targets.

## Notes for modders
- Ensure that the `Create` function is called with a valid player GUID to properly initialize the support system.
- Customize the designator beacon and missile behavior by modifying fields such as `nTargetXOffset`, `nTargetZOffset`, and missile speed.
- Be aware that network synchronization may affect multiplayer behavior, especially when dealing with multiple players initiating strikes simultaneously.