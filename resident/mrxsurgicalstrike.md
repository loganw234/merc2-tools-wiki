---
title: MrxSurgicalStrike
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
---

# MrxSurgicalStrike

*Module: mrxsurgicalstrike.lua*

## Overview
The `MrxSurgicalStrike` module is a specialized support system for surgical airstrikes. It extends the base `MrxSupport` module to provide functionality for designating targets, launching guided bombs, and handling bomb explosions.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSatellite`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oDesignator`: The designator satellite used for target designation.
- `uOwner`: The GUID of the player who owns this support system.
- `sRecruit`: The recruit type required for this support.
- `sModuleName`: The name of the module.
- `sDeliveryVehicle`: The delivery vehicle used for the airstrike.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sBomb`: The bomb projectile used.
- `uBomb`: The GUID of the bomb projectile.
- `uJet`: The GUID of the jet performing the airstrike.
- `uTarget`: The GUID of the target.
- `tBombs`: A table to track spawned bombs.

## Functions
### `Create(oSelf, uPlayerGuid)`
Creates a new instance of the `MrxSurgicalStrike` support system. Initializes the designator satellite, sets its cost to 0, and configures the minigame sectors for target designation. Sets the owner, recruit type, module name, delivery vehicle, bomb projectile, and other relevant fields.

### `DesignationCallback(oSelf)`
Called when the target is designated. Spawns a jet at a calculated position, launches it towards the target, and plays voice-over announcements for the airstrike.

### `DropBomb(oSelf)`
Drops a guided bomb from the jet towards the designated target. Normalizes the vector between the spawn point and the target, spawns the bomb with an initial velocity, and sets up a callback for when the bomb explodes.

### `BombExplodes(oSelf, nIndex)`
Called when a bomb explodes. Spawns an explosion effect at the bomb's position.

### `FinalExplosion(oSelf)`
Handles the final explosion of the bomb, spawning a more powerful explosion effect.

## Events
- Listens for custom events related to target designation and bomb explosions (not explicitly detailed in this module).

## Notes for modders
- Ensure that the `Create` function is called with the correct player GUID to initialize the support system properly.
- Customize the delivery vehicle, bomb projectile, and other fields as needed for different configurations.
- Be aware of the voice-over announcements played during the airstrike and adjust them if necessary.
- The module relies on the `MrxSupportDesignatorSatellite` for target designation, so ensure that this module is imported and configured correctly.