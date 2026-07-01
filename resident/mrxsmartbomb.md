---
title: MrxSmartBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, smart bomb]
---

# MrxSmartBomb

*Module: mrxsmartbomb.lua*

## Overview
The `MrxSmartBomb` module is responsible for handling the functionality of the Smart Bomb support type in the game. It manages the designation process, spawning the bomb, and handling its explosion effects.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorBeacon`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oDesignator`: The designator beacon used for targeting.
- `uOwner`: The GUID of the player who owns this support instance.
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `uJet`: The GUID of the aircraft delivering the bomb.
- `uSpawnedBomb`: The GUID of the spawned bomb.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the Smart Bomb support using the module's prototype. Initializes the designator beacon, sets the owner, recruit type, module name, and bomb details.

### `DesignationCallback(self)`
Handles the designation process for the Smart Bomb. Generates a random angle, finds spawn and target points relative to the camera, and initiates an airstrike with the bomb. Plays voice-over announcements for the airstrike.

### `DropBomb(self)`
Spawns the Smart Bomb projectile at the calculated position and direction. Blips the spawned bomb on the radar with a red color.

### `BombExplodes(self)`
Handles the explosion of the Smart Bomb. Prints a debug message, retrieves the target coordinates, and removes the target object if it exists and the player is local.

## Events
- Listens for custom event `DesignationCallback` to handle the designation process.
- Listens for custom event `DropBomb` to spawn the bomb.
- Listens for custom event `BombExplodes` to handle the bomb's explosion effects.

## Notes for modders
- Ensure that `Create` is called appropriately to initialize a new Smart Bomb support instance.
- Customize the bomb details by setting fields like `sBomb` and `uBomb`.
- Be aware of the voice-over announcements played during the airstrike process.