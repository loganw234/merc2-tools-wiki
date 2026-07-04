---
title: MrxFuelAirBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxFuelAirBomb

*Module: mrxfuelairbomb.lua*

## Overview
The `MrxFuelAirBomb` module is responsible for managing the deployment and detonation of fuel air bombs as a support action in the game. It inherits from the `MrxSupport` module and utilizes designator functionalities to target and deploy the bomb.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSmoke`, `MrxSupportDesignatorLaser`, `MrxSupportDesignatorSatellite`

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who owns this support action.
- `sRecruit`: The type of recruit required for this support action, set to "Pilot".
- `oDesignator`: The designator used to target the bomb drop location.
- `sModuleName`: The name of the module, set to "MrxFuelAirBomb".
- `sDeliveryVehicle`: The name of the delivery vehicle used for the airstrike.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uJet`: The GUID of the jet performing the flyby.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new instance of the `MrxFuelAirBomb` support action. It sets up the designator with specific properties and initializes the module's fields with the provided player GUID.

### `DesignationCallback(self)`
Handles the designation callback for placing the fuel air bomb. It calculates the spawn and launch points, retrieves the target coordinates from the designator, and initiates the flyby of the delivery vehicle towards the target location. It also plays a voice-over for the airstrike.

### `DropBomb(self)`
Drops the fuel air bomb at the designated target location. It calculates the direction vector from the jet to the target, normalizes it, and spawns the bomb projectile with an appropriate speed.

### `BombExplodes(self, sTrigger)`
Handles the explosion of the dropped bomb. It retrieves the current position of the bomb, calculates the direction vector towards the target, spawns explosion particles, and schedules the ignition sequence.

### `Test(nVZ, nVY, nVZ, nTargetX, nTargetY, nTargetZ)`
A test function that spawns a fuel air bomb particle at the specified target location. This is likely for debugging purposes.

### `Ignition(nBombX, nBombY, nBombZ, nTargetX, nTargetY, nTargetZ, nVectorX, nVectorY, nVectorZ)`
Handles the ignition sequence of the bomb. It spawns light and debris particles at the target location, schedules the fireball effect, and plays a sound cue for the explosion.

### `Fireball(nBombX, nBombY, nBombZ, nTargetX, nTargetY, nTargetZ, nVectorX, nVectorY, nVectorZ)`
Handles the fireball effect of the bomb. It spawns explosion particles at the bomb's position and ground shockwave particles towards the target location.

## Events
- Listens for custom event `DesignationCallback` to handle the designation of the bomb drop location.
- Listens for custom event `DropBomb` to handle the actual dropping of the bomb.
- Listens for custom event `BombExplodes` to handle the explosion of the bomb.
- Listens for custom event `Ignition` to handle the ignition sequence of the bomb.
- Listens for custom event `Fireball` to handle the fireball effect of the bomb.

## Notes for modders
- Ensure that the designator is properly set up and validated before attempting to drop the bomb.
- Customize the delivery vehicle and other properties as needed for different game scenarios.
- Be aware of the timing and sequence of events, especially during the ignition and explosion phases.
- Use the `Test` function for debugging purposes to visualize the bomb placement.