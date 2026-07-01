---
title: MrxDaisyCutter
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
---

# MrxDaisyCutter

*Module: mrxdaisycutter.lua*

## Overview
The `MrxDaisyCutter` module is responsible for managing the Daisy Cutter support operation in the game. It handles the designation, delivery, and explosion of Daisy Cutter projectiles using an aerial vehicle (C130). The module integrates with the MrxSupport system to manage player ownership and designator functionality.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSmoke`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uOwner`: The GUID of the player who owns this support operation.
- `sDeliveryVehicle`: The name of the delivery vehicle used ("Support Vehicle (C130)").
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sBomb`: The name of the bomb projectile ("Daisy Cutter Projectile").
- `uBomb`: The GUID of the bomb projectile.
- `uJet`: The GUID of the aircraft performing the flyby.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the Daisy Cutter support operation. Initializes the designator with validation and AATestLevel settings, sets the owner, recruit, module name, delivery vehicle, and bomb details.

### `DesignationCallback(self)`
Called when the designation is complete. Calculates spawn and target points using the camera position, initiates a flyby with the C130 aircraft, and schedules the bomb drop.

### `DropBomb(self)`
Drops the Daisy Cutter bomb from the aircraft. Retrieves the current position of the aircraft and the designated target, calculates the normalized vector towards the target, spawns the bomb projectile, and sets up the explosion callback.

### `BombExplodes(self)`
Called when the bomb explodes. Creates a timer event to trigger debris creation after a delay.

### `CreateDebris(self)`
Creates debris effects at the bomb's impact location if the player is nearby or on the client side. Uses particle effects to simulate dustfall.

## Events
- Listens for custom events triggered by designator and bomb operations (not explicitly listed in the provided code).

## Notes for modders
- Ensure that `Create` is called with a valid player GUID to initialize the support operation.
- Customize the delivery vehicle and bomb details by modifying the `sDeliveryVehicle` and `sBomb` fields.
- Be aware of network synchronization (`Net.IsClient`) when creating debris effects to avoid client-server discrepancies.