---
title: MrxDaisyCutter
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: 'deeper pass: separated the module-level local defaults (sProjectileName/sExplosionName/sDeliveryVehicle) from the settable instance fields, flagged the unused nSpeedScale and dead sExplosionName, documented the CreateDebris distance/client gate; parent of MrxMOAB; cross-linked Airstrike/MrxSupport'
---

# MrxDaisyCutter

*Module: mrxdaisycutter.lua*

## Overview
`MrxDaisyCutter` drops a single guided **"Daisy Cutter Projectile"** from a C-130 onto a smoke-marked target,
then kicks off a delayed dust-fall effect near the impact. It's a thin subclass of [`MrxSupport`](mrxsupport)
and is itself the **parent of [MrxMOAB](mrxmoab)** (which reuses this whole drop pipeline with a different
projectile). The screen-flash grade is the separate
[Airstrike_Atmosphere_Daisycutter](airstrike_atomsphere_daisycutter) object.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke), [`MrxUtil`](mrxutil)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who owns this support operation.
- `sDeliveryVehicle`: The name of the delivery vehicle used ("Support Vehicle (C130)").
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sBomb`: The name of the bomb projectile ("Daisy Cutter Projectile").
- `uBomb`: The GUID of the bomb projectile.
- `uJet`: The GUID of the aircraft performing the flyby.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Module constants & tunables
Three **module-level `local`s** hold the *defaults* (unreachable from outside — see the
[function-override deep dive](../deep-dives/function-override)):
- `sProjectileName = "Daisy Cutter Projectile"`
- `sExplosionName = "Explosion (Daisy Cutter)"` — **declared but never used** (dead constant).
- `sDeliveryVehicle = "Support Vehicle (C130)"`

`Create` copies these onto the instance as `self.sBomb`/`self.uBomb`/`self.sDeliveryVehicle`/
`self.uDeliveryVehicle`, and `DropBomb` fires `Airstrike.SpawnOrdnance(self.uBomb, …)`. So the **instance
fields** are the real customization surface — reassign `oInstance.uBomb` / `oInstance.uDeliveryVehicle`
before firing rather than trying to touch the `local` defaults.

{: .warning }
> `DropBomb` declares `local nSpeedScale = 20` but then passes the **unscaled** normalized vector
> (`nVectorX, nVectorY, nVectorZ`) to `SpawnOrdnance` — the `nSpeedScale` is never applied. This looks like a
> decompiled-source bug; the daisy cutter's projectile therefore launches at unit speed, relying on the
> template's own physics rather than the intended ×20 boost.

## Functions
### `Create(self, uPlayerGuid)`
Class-factory constructor. Builds a smoke designator with `_NoValidation` + `"basic"` AA test, sets owner /
recruit `"Fiona"` / module name, and copies the projectile and delivery-vehicle defaults onto the instance.

### `DesignationCallback(self)`
Computes spawn (300 behind, alt 100) and target (at camera, alt 100) via `Pg.FindPointFromCamera`, flies the
C-130 with `Airstrike.Flyby(self.uDeliveryVehicle, …, 80, DropBomb, {self})`, and plays an (empty) VO via
[`MrxSupport.PlayAirstrikeVO`](mrxsupport).

### `DropBomb(self)`
Reads jet + designator target, normalizes the direction, and spawns the projectile with
`Airstrike.SpawnOrdnance(self.uBomb, …, uTarget, "impact", self.uOwner, BombExplodes, {self})` (see the
unscaled-velocity warning above).

### `BombExplodes(self)`
Detonation callback — schedules `CreateDebris` **1.5 s** later via `Event.TimerRelative`.

### `CreateDebris(self)`
Draws a `Graphics.Effect.Terrain("global_particle_dustfall", 20, 0.005, …)` dust cloud at the *local
player's* feet — **but only if** this is not a network client and the local hero is within **150 units** of
the target (`MrxUtil.GetDistanceToObject(...) > 150` early-returns). A purely cosmetic, host-side, near-player
effect.

## Events
- **No `Event.Create` subscriptions.** The only `Event.*` use is the `Event.TimerRelative` that delays
  `CreateDebris` by 1.5 s. The other functions are wired by the parent designation flow and the
  `Airstrike.Flyby`/`Airstrike.SpawnOrdnance` callbacks.

## Notes for modders
- **To change the bomb, reassign the instance field `uBomb` (and `sBomb`) — not the `local`
  `sProjectileName`.** [MrxMOAB](mrxmoab) does exactly this: it inherits this module and just points
  `sBomb`/`uBomb` at `"MOAB Projectile"`.
- The `nSpeedScale = 20` in `DropBomb` is dead code (see warning) — if you override `DropBomb` to give the
  projectile a real launch velocity, that's the value the original author appears to have intended.
- `CreateDebris` is host-only and gated to a **150-unit** radius; on a dedicated client or a far-away player
  it does nothing. Keep that in mind if you're relying on it for gameplay feedback.