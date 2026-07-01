---
title: MrxCruiseMissile
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, missile]
---

# MrxCruiseMissile

*Module: mrxcruisemissile.lua*

## Overview
The `MrxCruiseMissile` module is responsible for managing the deployment and behavior of cruise missiles in the game. It extends the functionality provided by the `MrxSupport` module to handle specific aspects related to cruise missile support, such as designation, bombing runs, and explosions.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorBeacon`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `sDeliveryVehicle`: The name of the delivery vehicle used for cruise missiles.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `uOwner`: The GUID of the player who owns the missile support.
- `uJet`: The GUID of the jet used for the bombing run.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the cruise missile support using the module's prototype. Initializes the designator beacon, sets the owner and recruit, and configures the delivery vehicle and bomb details.

### `DesignationCallback(self)`
Called when the designation process is complete. Handles the calculation of spawn and target positions, spawns the jet for the bombing run, and starts a voice-over sequence based on the player's faction.

### `DropBomb(self)`
Handles the dropping of the bomb projectile from the jet. Calculates the vector towards the target, spawns the bomb, and sets up the explosion callback.

### `BombExplodes(self)`
Called when the bomb explodes. Removes the target object if it exists and logs a debug message indicating the explosion.

## Events
- Listens for custom event (not explicitly defined in this file) to trigger the designation process.
- Listens for custom event (not explicitly defined in this file) to handle the bombing run and bomb drop.

## Notes for modders
- Ensure that `Create` is called appropriately when initializing cruise missile support.
- Customize the delivery vehicle and bomb details by setting fields like `sDeliveryVehicle` and `sBomb`.
- Be aware of the voice-over sequences triggered based on the player's faction, which can be modified or extended as needed.