---
title: MrxSatClusterBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, satellite]
---

# MrxSatClusterBomb

*Module: mrxsatclusterbomb.lua*

## Overview
The `MrxSatClusterBomb` module represents the support system for deploying cluster bombs via a satellite. It handles the creation, designation, and detonation of these bombs, providing a mini-game interface for players to target their deployment.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSatellite`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oDesignator`: The designator satellite used for targeting.
- `uOwner`: The GUID of the player who owns this support system.
- `sDeliveryVehicle`: The name of the delivery vehicle.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uJet`: The GUID of the jet used for delivering the bombs.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Functions
### `Create(oSelf, uPlayerGuid)`
Creates a new instance of the `MrxSatClusterBomb` support system. Initializes the designator satellite with validation function and sets up the necessary properties such as owner, recruit, module name, delivery vehicle, and cost.

### `DesignationCallback(oSelf)`
Called when the player completes the designation mini-game. Spawns a jet to deliver the bombs from the designated spawn point to the target point.

### `DropBomb(oSelf, nTargetX, nTargetY, nTargetZ)`
Drops the cluster bomb at the specified target coordinates. Calculates the direction and speed for the bomb projectile and spawns it accordingly.

### `BombExplodes(oSelf)`
Handles the explosion of the dropped bomb. Spawns multiple bomblets in a cone pattern around the bomb's position to simulate the cluster effect.

## Events
- Listens for custom events related to designation and delivery (not explicitly detailed in the provided code).

## Notes for modders
- Ensure that `Create` is called with the correct player GUID to properly initialize the support system.
- Customize the designator sectors by modifying the `SetMinigameSectors` function call.
- Adjust the bomb's speed and spawn distance by changing the parameters in the `DropBomb` function.
- Be aware of network synchronization settings if extending this module for multiplayer use.