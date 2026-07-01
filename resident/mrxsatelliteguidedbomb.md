---
title: MrxSatelliteGuidedBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, satellite]
---

# MrxSatelliteGuidedBomb

*Module: mrxsatelliteguidedbomb.lua*

## Overview
The `MrxSatelliteGuidedBomb` module is responsible for managing the guided bomb support system in the game. It handles the creation, cost setting, and execution of satellite-guided bombs through a mini-game interface.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSatellite`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `nCost`: The cost of using the guided bomb.
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `sDeliveryVehicle`: The name of the delivery vehicle.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uOwner`: The GUID of the player who owns this support instance.
- `uJet`: The GUID of the aircraft used for the airstrike.
- `tBombs`: A table to store bomb instances.
- `uTarget`: The GUID of the target.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the guided bomb support system. Initializes the designator with default settings and sets up the owner and delivery vehicle information.

### `SetCost(self, nCost)`
Sets the cost of using the guided bomb and updates the designator's cost accordingly.

### `DesignationCallback(self)`
Handles the callback from the mini-game interface after the player has designated a target. Spawns an aircraft to deliver the bomb and plays voice-over messages for the airstrike.

### `DropBomb(self)`
Drops the bomb at the designated target location. Calculates the direction vector, spawns the bomb, and blips it on the radar.

### `BombExplodes(self, nIndex)`
Handles the explosion of a bomb instance. Retrieves the position of the exploded bomb.

### `FinalExplosion(self)`
Handles the final explosion logic after all bombs have been dropped. Retrieves the position of the final bomb.

## Events
- Listens for mini-game designation events to call `DesignationCallback`.
- Listens for bomb explosion events to call `BombExplodes`.

## Notes for modders
- Ensure that `SetCost` is called appropriately to manage the cost of using the guided bomb.
- Customize the delivery vehicle and bomb projectile by setting fields like `sDeliveryVehicle` and `sBomb`.
- Be aware that network synchronization may affect multiplayer behavior when using this support system.