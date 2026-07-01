---
title: MrxStrategicMissile
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, missile]
---

# MrxStrategicMissile

*Module: mrxstrategicmissile.lua*

## Overview
The `MrxStrategicMissile` module is responsible for managing the launch and detonation of strategic missiles in the game. It inherits from the `MrxSupport` module and utilizes a designator beacon to target and deploy the missile.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorBeacon`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uOwner`: The GUID of the player who owns the missile.
- `uSpawnedBomb`: The GUID of the spawned missile projectile.
- `oDesignator`: The designator beacon used to target the missile.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the strategic missile using the module's prototype. Initializes the designator beacon and sets the owner, recruit, and module name.

### `DesignationCallback(self)`
Starts a voice sequence when the missile is designated. Calls `MissileLaunch` to launch the missile.

### `MissileLaunch(self)`
Spawns the missile projectile at a calculated position relative to the camera and sets up a timer for the bomb drop.

### `ActivateDelay(self, uProjectileGuid)`
Sets a timer to delay the bomb drop after the missile is launched.

### `DropBomb(self)`
Drops the bomb at the designated target location. Spawns the missile projectile and sets up the explosion callback.

### `BombExplodes(self)`
Handles the explosion of the dropped bomb. Logs target coordinates, spawns an explosion effect, kills the spawned bomb, removes the target if it exists, and spawns shrapnel in various directions.

## Events
- Listens for a custom event (not explicitly defined in the code) to call `DesignationCallback` when the missile is designated.
- Uses `Event.TimerRelative` to delay the bomb drop after the missile launch.

## Notes for modders
- Ensure that the designator beacon is properly set up and targeted before launching the missile.
- Customize the missile's behavior by modifying fields such as `sProjectileName`, `sShrapnelName`, and `sExplosionName`.
- Be aware of the network synchronization settings if using this module in multiplayer scenarios.