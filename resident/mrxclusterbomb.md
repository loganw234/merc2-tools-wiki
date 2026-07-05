---
title: MrxClusterBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: 'deeper pass: documented the two-projectile design (Cluster Bomb Projectile → ConeSpawn of Cluster Bomblet Projectile), the "obstructed"/30 detonation trigger, the two cone rings (15/10 and 30/20) and red-smoke designator; cross-linked Airstrike/MrxSupport'
---

# MrxClusterBomb

*Module: mrxclusterbomb.lua*

## Overview
`MrxClusterBomb` drops a single **"Cluster Bomb Projectile"** from a jet; when that shell detonates,
`BombExplodes` scatters a spray of **"Cluster Bomblet Projectile"** submunitions in two forward cones via
[`Airstrike.ConeSpawn`](../namespaces/airstrike). Extends [`MrxSupport`](mrxsupport) and marks the target
with a **red** [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke). The screen-flash grade is the
separate [AirstrikeAtomsphereClusterbomb](airstrike_atomsphere_clusterbomb) object.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oDesignator`: The designator object used for marking targets.
- `sDeliveryVehicle`: The name of the delivery vehicle used to drop the bomb.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uJet`: The GUID of the jet performing the flyby.
- `uSpawnedBomb`: The GUID of the spawned cluster bomb projectile.
- `uOwner`: The GUID of the player who owns this support system.

## Module constants & templates
- Ordnance templates (literals in the firing code): `"Cluster Bomb Projectile"` (the shell) and
  `"Cluster Bomblet Projectile"` (the submunitions). See the
  [Airstrike namespace](../namespaces/airstrike) for the confirmed template-name list.
- `nSpeedScale = 35` (shell velocity), `nSpeed = 20` (bomblet velocity).
- Detonation trigger for the shell: `"obstructed"` with param `30` — detonates on obstruction (vs the
  bombing-run's `"impact"`).

## Functions
### `Create(self, uPlayerGuid)`
Class-factory constructor. Builds a smoke designator, sets its color to `"red"`, AA test level `"basic"`,
and validation `_NoValidation`; sets owner, recruit `"Pilot"`, module name, and copies the delivery-vehicle
fields onto the instance.

### `DesignationCallback(self)`
Picks a randomized approach angle (`300 + math.randi(120)`), computes spawn/target points from the camera at
that angle, flies the jet with `Airstrike.Flyby(self.uDeliveryVehicle, …, 100, DropBomb, {self})`, and
schedules a Misha VO (cues 03/14/25) 2 s later.

### `DropBomb(self)`
Reads jet + designator target, normalizes the direction, and spawns the shell:
```lua
self.uSpawnedBomb = Airstrike.SpawnOrdnance("Cluster Bomb Projectile", nX, nY, nZ,
  nVX*35, nVY*35, nVZ*35, "obstructed", 30, self:GetOwner(), BombExplodes, {self})
```

### `BombExplodes(self)`
Detonation callback. From the shell's position, aims a normalized vector at the current designator target and
fires **two forward cones** of bomblets:
```lua
Airstrike.ConeSpawn("Cluster Bomblet Projectile", …, 15, nSpeed, 10)  -- 15° cone, speed 20, 10 bomblets
Airstrike.ConeSpawn("Cluster Bomblet Projectile", …, 30, nSpeed, 20)  -- 30° cone, speed 20, 20 bomblets
```
So a single strike scatters ~30 submunitions — a tight inner ring plus a wider outer ring.

## Events
- **No `Event.Create` subscriptions.** The only scheduling is the `Event.TimerRelative` that delays the VO by
  2 s. `DesignationCallback`/`DropBomb`/`BombExplodes` are wired by the parent designation flow and the
  `Airstrike.Flyby`/`Airstrike.SpawnOrdnance` callbacks — not event handlers.

## Notes for modders
- **The two `Airstrike.ConeSpawn` calls are the real "make it deadlier / wider" lever.** Their trailing
  three args are `(coneAngleDeg, speed, count)` — bump the counts (10/20) or angles (15/30) in an override of
  `BombExplodes` (a plain global) for a denser or wider spread. Compare
  [MrxSatClusterBomb](mrxsatclusterbomb), which fires **four** rings instead of two.
- Swap the submunition by changing the `"Cluster Bomblet Projectile"` template string; swap the delivered
  shell via the `"Cluster Bomb Projectile"` literal in `DropBomb`.
- The designator uses **red** smoke (`SetSmokeColor("red")`) with no AA/validity gating (`_NoValidation`).