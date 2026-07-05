---
title: MrxSatClusterBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, satellite]
verified: true
verified_note: 'deeper pass: documented the four-ring ConeSpawn spread (10/15/30/50° × 4/4/6/6), the satellite minigame sectors + SetCost(0), the "distance" detonation trigger, and that the declared tVOCues is never actually played here; cross-linked Airstrike/MrxClusterBomb/MrxSupport'
---

# MrxSatClusterBomb

*Module: mrxsatclusterbomb.lua*

## Overview
`MrxSatClusterBomb` is the **satellite-targeted** cluster bomb: same two-projectile idea as
[MrxClusterBomb](mrxclusterbomb) (a `"Cluster Bomb Projectile"` shell that scatters
`"Cluster Bomblet Projectile"` submunitions on detonation), but designated through a satellite mini-game
instead of ground smoke — and it fires a **wider four-ring** spread rather than two. Extends
[`MrxSupport`](mrxsupport) and uses [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(oSelf, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oDesignator`: The designator satellite used for targeting.
- `uOwner`: The GUID of the player who owns this support system.
- `sDeliveryVehicle`: The name of the delivery vehicle.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uJet`: The GUID of the jet used for delivering the bombs.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Module constants & templates
- `tVOCues` — three `"Misha-None-Freeplay-Support-*"` lines (03/14/25) declared at module scope, **but this
  file never calls `PlayAirstrikeVO`, so they're not actually played here** (unlike its ground sibling
  [MrxClusterBomb](mrxclusterbomb)).
- Ordnance: `"Cluster Bomb Projectile"` (shell, `nSpeedScale = 35`) → `"Cluster Bomblet Projectile"`
  (submunitions, `nSpeed = 20`). Shell detonation trigger: `"distance"` with `nDistance = nSpawnY - nTargetY - 15`.
- Satellite designator config: `SetMinigameSectors({{45,135},{225,315}})` and `SetCost(0)` — **this strike is
  free** (no support-resource cost).

## Functions
### `Create(oSelf, uPlayerGuid)`
Class-factory constructor (uses `oSelf` as the prototype name). Builds a satellite designator with
`_NoValidation`, the two minigame sectors above and `SetCost(0)`, sets owner / recruit `"Pilot"` / module
name, and copies the delivery-vehicle fields.

### `DesignationCallback(oSelf)`
Runs after the satellite mini-game. Computes spawn/target points from the camera and flies the jet with
`Airstrike.Flyby(…, 100, DropBomb, {oSelf, nTargetX, nTargetY, nTargetZ})`. (No VO call — see the note above.)

### `DropBomb(oSelf, nTargetX, nTargetY, nTargetZ)`
Reads the jet position and the current designator target, computes `nDistance = nSpawnY - nTargetY - 15`,
and fires the shell with `Airstrike.SpawnOrdnance("Cluster Bomb Projectile", …, "distance", nDistance,
oSelf:GetOwner(), BombExplodes, {oSelf})`.

### `BombExplodes(oSelf)`
Detonation callback. Aims a normalized vector at the target and fires **four** forward cones of bomblets
(vs the ground cluster bomb's two):
```lua
Airstrike.ConeSpawn("Cluster Bomblet Projectile", …, 10, 20, 4)   -- 10° / speed 20 / 4 bomblets
Airstrike.ConeSpawn("Cluster Bomblet Projectile", …, 15, 20, 4)   -- 15° / 4
Airstrike.ConeSpawn("Cluster Bomblet Projectile", …, 30, 20, 6)   -- 30° / 6
Airstrike.ConeSpawn("Cluster Bomblet Projectile", …, 50, 20, 6)   -- 50° / 6
```
~20 submunitions across four escalating rings out to a 50° cone — a broader footprint than the ground variant.

## Events
- **No `Event.Create` subscriptions.** `DesignationCallback`/`DropBomb`/`BombExplodes` are wired by the
  parent designation flow and the `Airstrike.Flyby`/`Airstrike.SpawnOrdnance` callbacks — not event handlers.

## Notes for modders
- **The four `Airstrike.ConeSpawn` calls (`angle, speed, count`) are the spread lever** — widen the angles
  (10/15/30/50) or raise the counts (4/4/6/6) in an override of `BombExplodes` (a plain global) for a bigger
  saturation pattern; compare the two-ring [MrxClusterBomb](mrxclusterbomb).
- **`SetCost(0)` makes this strike free** — flip it to a nonzero cost (or set `SetCost` in an override of
  `Create`) if you want it to consume support resources.
- `SetMinigameSectors({{45,135},{225,315}})` defines the satellite-aiming mini-game's valid arcs; adjust for
  an easier/harder designation.