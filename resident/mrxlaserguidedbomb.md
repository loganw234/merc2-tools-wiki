---
title: MrxLaserGuidedBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, bomb]
---

# MrxLaserGuidedBomb

*Module: mrxlaserguidedbomb.lua*

## Overview
The `MrxLaserGuidedBomb` module is responsible for managing the deployment and behavior of a laser-guided bomb support system. It inherits from `MrxSupport` and utilizes additional modules such as `MrxSupportDesignatorLaser` and `MrxUtil`. This module handles the designation, dropping, and explosion effects of the bomb.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorLaser`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `sDeliveryVehicle`: The name of the delivery vehicle.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `tVOCues`: Voice-over cues for the support system.
- `uOwner`: The GUID of the player who owns the support system.
- `uJet`: The GUID of the aircraft used to deliver the bomb.
- `uTarget`: The GUID of the target designated by the laser designator.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the laser-guided bomb support system. Initializes the designator, owner, recruit, module name, delivery vehicle, bomb, and voice-over cues.

### `DesignationCallback(self)`
Called when the designation process is complete. Spawns an aircraft to deliver the bomb and sets up a timer to play voice-over cues.

### `DropBomb(self)`
Drops the bomb at the designated target location. Calculates the spawn position and vector for the bomb, spawns it with a randomized offset, and blips it on the radar.

### `BombExplodes(self)`
Called when the bomb explodes. Sets up a timer to create debris effects.

### `CreateDebris(self)`
Creates debris effects around the bomb's impact point if the player is within range. Uses particle effects to simulate dustfall.

## Events
- Listens for custom event (not specified in the provided code) to trigger the designation process.
- Listens for `Event.TimerRelative` to play voice-over cues and create debris effects.

## Notes for modders
- Ensure that the designator is properly set up before calling `DesignationCallback`.
- Customize the bomb's delivery vehicle, projectile, and voice-over cues by modifying the respective fields.
- Be aware of network synchronization (`Net.IsClient`) when creating debris effects to ensure they are only played on the client side.