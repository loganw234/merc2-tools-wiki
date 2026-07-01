---
title: MrxRocketArtillery
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, artillery]
---

# MrxRocketArtillery

*Module: mrxrocketartillery.lua*

## Overview
The `MrxRocketArtillery` module is responsible for managing the rocket artillery support system in the game. It inherits from `MrxSupport` and integrates with other modules like `MrxSupportDesignatorSatellite`, `MrxVoSequence`, and `MrxUtil` to handle the designation, targeting, and firing of rocket artillery projectiles.

## Inheritance
- Inherits from: `MrxSupport`
- Imports: `MrxSupportDesignatorSatellite`, `MrxVoSequence`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `oDesignator`: The designator satellite used for targeting.
- `uOwner`: The GUID of the player who owns this support system.
- `sRecruit`: The recruit name associated with this support system.
- `sModuleName`: The module name, set to "MrxRocketArtillery".

## Functions
### `Create(self, uPlayerGuid)`
Creates a new instance of the rocket artillery support system. It initializes the designator satellite with specific mini-game sectors and sets up the owner, recruit, and module name.

### `DesignationCallback(self)`
Handles the designation callback for the rocket artillery. It calculates the target position, determines the vectors for width and height adjustments, and spawns multiple rocket projectiles in a spread pattern. It also starts a voice sequence to announce the incoming attack.

### `TriggerFallingMissile(tData, uPlayer)`
Triggers the falling missile by spawning an ordnance at the calculated target position. It uses the `Airstrike.SpawnOrdnance` function to create the projectile and sets up a delay for activation.

## Events
- Listens for custom events related to designation and triggering of missiles.

## Notes for modders
- Ensure that the designator satellite is properly initialized with the correct mini-game sectors.
- Customize the target spread by adjusting `nWidth`, `nHeight`, and `nShells` in the `DesignationCallback` function.
- Be aware that the voice sequence announcement can be customized by modifying the list of voice files in `MrxVoSequence.Start`.
- The module relies on network synchronization for multiplayer behavior, so ensure that the ordnance spawning respects this.