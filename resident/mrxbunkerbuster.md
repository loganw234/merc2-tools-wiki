---
title: MrxBunkerBuster
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxLaserGuidedBomb
tags: [support, bomb]
verified: true
verified_note: corrects the Instance pattern section (class-factory, not per-uGuid)
---

# MrxBunkerBuster

*Module: mrxbunkerbuster.lua*

## Overview
The `MrxBunkerBuster` module is responsible for managing the behavior of a bunker buster support weapon in the game. It inherits from `MrxLaserGuidedBomb` and extends its functionality to handle specific behaviors related to bunker destruction, including visual effects and building demolition.

## Inheritance
- Inherits from: `MrxLaserGuidedBomb`
- Imports: `MrxSupportDesignatorLaser`

## Instance pattern
**Same class-factory pattern as [`MrxLaserGuidedBomb`](mrxlaserguidedbomb)/[`MrxSupport`](mrxsupport), not
per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new table via `setmetatable`/`__index`, exactly like
its parent chain. No `OnActivate`/`Awake`, no `tInstance` registry. It tracks the following key fields:
- `tVOCues`: A table of sound cues associated with the support weapon.
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `oDesignator`: An instance of `MrxSupportDesignatorLaser` used for designating targets.
- `uPlayerGuid`: The GUID of the player who owns the support weapon.
- `sRecruit`: The recruit type required to use the support weapon.
- `sModuleName`: The name of the module (`MrxBunkerBuster`).
- `sDeliveryVehicle`: The delivery vehicle for the bomb.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the bunker buster support weapon using the module's prototype. It initializes various fields such as the designator, owner, recruit type, and bomb details.

### `BombExplodes(self)`
Handles the explosion of the bunker buster bomb. It logs debug information, spawns initial explosions, kills the spawned bomb, and schedules subsequent ground explosions and a final explosion using timers.

### `FinalExplosion(self, nBombX, nBombY, nBombZ)`
Manages the final stages of the bomb explosion. Depending on whether the bomb is a standard bunker buster or a nuclear one, it spawns appropriate visual effects and triggers after-shock events. It also posts an event to indicate that the area has been "nuked" if applicable.

### `GroundExplosion(radius, density, nBombX, nBombY, nBombZ)`
Spawns ground shockwave effects around the bomb's impact point using the provided radius and density parameters.

### `AfterShock(self, nRadius, nBombX, nBombY, nBombZ)`
Handles the after-shock effects of the bomb explosion. It collects buildings within a specified radius, calculates random delays for demolishing them, and schedules demolition events using timers.

### `Demolish(building)`
Demolishes a building by spawning an explosion effect at its position.

## Events
- Listens for custom event `BombExplodes` to handle the bomb's explosion sequence.
- Listens for custom event `FinalExplosion` to manage the final stages of the bomb explosion.
- Listens for custom event `GroundExplosion` to spawn ground shockwave effects.
- Listens for custom event `AfterShock` to handle after-shock effects and building demolition.

## Notes for modders
- Ensure that the `Create` function is called appropriately to initialize the bunker buster support weapon.
- Customize bomb behavior by modifying fields such as `sBomb`, `uBomb`, and `tVOCues`.
- Be aware of the impact radius and density parameters in `GroundExplosion` to adjust visual effects.
- Use the `AfterShock` function to manage building demolition and after-shock events.