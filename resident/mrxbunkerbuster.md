---
title: MrxBunkerBuster
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxLaserGuidedBomb
tags: [support, bomb]
verified: true
verified_note: 'deeper pass: documented the standard-vs-nuclear FinalExplosion branch, the multi-stage timer chain (0.5/1/1.5/2.75s) and its exact particle/explosion template strings, the AfterShock random-demolition loop, and the "Nuked"/"Busted" Event.Post signals; cross-linked MrxLaserGuidedBomb/Airstrike'
---

# MrxBunkerBuster

*Module: mrxbunkerbuster.lua*

## Overview
`MrxBunkerBuster` is the laser-guided "penetrator" support weapon: it reuses the whole drop/guidance
pipeline of its parent [`MrxLaserGuidedBomb`](mrxlaserguidedbomb) and only overrides `BombExplodes` to play
a dramatic **multi-stage** detonation — staged ground shockwaves, a big final blast, then a randomized wave
of nearby-building demolition. It has two modes selected purely by which projectile guid was loaded: a
standard `"Bunker Buster Projectile"` and a `"Nuclear Bunker Buster Projectile"` (the tactical-nuke path,
which fires the [tact-nuke screen grade](airstrike_atomsphere_tactnuke)).

## Inheritance
- Inherits from: [`MrxLaserGuidedBomb`](mrxlaserguidedbomb) → [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorLaser`](mrxsupportdesignatorlaser)

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

## Module constants & templates
Set at file scope (module-level globals, not `local`):
- `sBomb = "Bunker Buster Projectile"` and `uBomb = Pg.GetGuidByName("Bunker Buster Projectile")`.
- `tVOCues` — three `"Misha-None-Freeplay-Support-*"` lines (02/12/20).

Explosion/particle template strings spawned by the detonation chain (all via `Pg.Spawn` /
`MrxUtil.SpawnObject` / `Graphics.Effect.Terrain`, so all editable only as engine assets):
- `"Explosion (Bunker Buster Stage 1)"`, `"Explosion (Bunker Buster Stage 2)"`,
  `"Explosion (Airstike Bomb Final Strike)"` (note the engine's own `Airstike` typo).
- `"global_particle_exp_shockwave_ground_bunkerbuster"` (ground shockwave).
- Nuclear branch: `"global_particle_airstrike_tactnuke"` and
  `"global_particle_exp_shockwave_ground_tactnuke"` (spawned at named location `"loc_shockwave"`).

## Functions
### `Create(self, uPlayerGuid)`
Class-factory constructor. Builds a [`MrxSupportDesignatorLaser`](mrxsupportdesignatorlaser), sets owner /
recruit `"Pilot"` / module name, copies delivery-vehicle and bomb fields onto the instance, and — notably —
copies `self.BombExplodes` onto the instance so the parent's `DropBomb` (inherited from
[`MrxLaserGuidedBomb`](mrxlaserguidedbomb)) calls *this* module's override.

### `BombExplodes(self)`
Override of the parent stub. Reads `self.uSpawnedBomb`'s position, spawns `"Explosion (Bunker Buster Stage
1)"`, kills the bomb object, then schedules a staged shockwave chain via `Event.Create(Event.TimerRelative, …)`:
`GroundExplosion` at **+0.5 s (r=20), +1 s (r=45), +1.5 s (r=65)**, and `FinalExplosion` at **+2.75 s**.

### `FinalExplosion(self, nBombX, nBombY, nBombZ)`
Branches on which projectile guid `self.uBomb` holds:
- **Standard** (`"Bunker Buster Projectile"`): spawns `"Explosion (Bunker Buster Stage 2)"`, then schedules
  `AfterShock` with radius **50** at +2 s.
- **Nuclear** (`"Nuclear Bunker Buster Projectile"`): spawns the tact-nuke particle, spawns the ground
  shockwave at `"loc_shockwave"` at +1 s, schedules `AfterShock` radius **80** at +2 s, and `Event.Post("Nuked", {x,y,z})` at +2 s so other systems can react to a nuke detonation.

### `GroundExplosion(radius, density, nBombX, nBombY, nBombZ)`
Draws a terrain shockwave decal with `Graphics.Effect.Terrain("global_particle_exp_shockwave_ground_bunkerbuster", radius, density, nBombX, 0, nBombZ)`. Called from the timer chain with escalating radii.

### `AfterShock(self, nRadius, nBombX, nBombY, nBombZ)`
Posts `Event.Post("Busted", {x,y,z})`, collects buildings in range with
`Pg.FastCollectBuildings(nBombX, nBombY, nBombZ, nRadius)`, and for each schedules a `Demolish` after a
random `math.randf()`-based delay — so buildings topple in a staggered wave rather than all at once.

### `Demolish(building)`
Spawns `"Explosion (Airstike Bomb Final Strike)"` at a building's position (guarded by a position check).

## Events
- **No `Event.Create` subscriptions.** All `Event.*` use is either **`Event.TimerRelative` scheduling**
  (the staged 0.5/1/1.5/2.75/+2 s chain above) or **`Event.Post`** broadcasts: `"Nuked"` (nuclear branch)
  and `"Busted"` (every AfterShock). Modules elsewhere can subscribe to those two signals.
- `BombExplodes`/`FinalExplosion`/`GroundExplosion`/`AfterShock`/`Demolish` are plain functions invoked via
  the timer chain and the inherited drop pipeline — they are not event handlers.

## Notes for modders
- **Radius/timing are the real levers, and they're plain numeric literals in the timer chain** — override
  `BombExplodes` or `AfterShock` (both plain globals) to change the shockwave radii (20/45/65), the demolish
  radius (50 / 80 nuclear), or the stage timings.
- **The standard-vs-nuclear split keys entirely off `self.uBomb`** (the guid of `"Bunker Buster Projectile"`
  vs `"Nuclear Bunker Buster Projectile"`). Set `uBomb` to the nuclear projectile's guid before firing to
  get the nuke path (bigger radius + tact-nuke FX + `"Nuked"` broadcast).
- Listen for the `Event.Post("Nuked", …)` / `Event.Post("Busted", …)` broadcasts if you want your own mod to
  react to a bunker-buster/nuke detonation.
- The staged demolition uses `Pg.FastCollectBuildings` — buildings outside `nRadius` of the impact are never
  touched.