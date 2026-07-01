---
title: MrxClusterBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
---

# MrxClusterBomb

*Module: mrxclusterbomb.lua*

## Overview
The `MrxClusterBomb` module is responsible for managing the deployment and behavior of a cluster bomb support system in the game. It inherits from `MrxSupport` and utilizes the `MrxSupportDesignatorSmoke` module to handle designating targets with smoke markers.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSmoke`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oDesignator`: The designator object used for marking targets.
- `sDeliveryVehicle`: The name of the delivery vehicle used to drop the bomb.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uJet`: The GUID of the jet performing the flyby.
- `uSpawnedBomb`: The GUID of the spawned cluster bomb projectile.
- `uOwner`: The GUID of the player who owns this support system.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new instance of the `MrxClusterBomb` module. Initializes the designator with specific properties and sets up the delivery vehicle and owner information.

### `DesignationCallback(self)`
Called when the target designation is complete. Handles the logic for spawning the jet and setting up the airstrike, including playing voice-over announcements.

### `DropBomb(self)`
Handles the dropping of the cluster bomb projectile from the jet. Calculates the spawn and target positions, normalizes the vector, and spawns the bomb with appropriate velocity.

### `BombExplodes(self)`
Called when the cluster bomb explodes. Spawns multiple bomblets in a cone pattern around the explosion point to simulate the cluster bomb effect.

## Events
- Listens for custom event `DesignationCallback` to handle target designation completion.
- Listens for custom event `DropBomb` to handle the dropping of the bomb.
- Listens for custom event `BombExplodes` to handle the explosion of the bomb and spawn bomblets.

## Notes for modders
- Ensure that the delivery vehicle specified in `sDeliveryVehicle` is correctly set up in the game world.
- Customize the designator properties by modifying fields like smoke color, AA test level, and validation function.
- Be aware that the cluster bomb's behavior can be tuned by adjusting parameters such as spawn and target positions, vector normalization, and bomblet spawning patterns.