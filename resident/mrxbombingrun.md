---
title: MrxBombingRun
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, bombing run]
verified: true
verified_note: 'deeper pass: documented the exact SpawnOrdnance call (two "Bomb" ordnance, nSpeedScale 33), the local sProjectileName/sExplosionName constants (sExplosionName is dead), the smoke designator + VO cues; flagged BombExplodes as an empty stub; cross-linked Airstrike/MrxSupport'
---

# MrxBombingRun

*Module: mrxbombingrun.lua*

## Overview
`MrxBombingRun` is the [support](mrxsupport) weapon that flies a jet over a smoke-marked target and drops a
pair of unguided **"Bomb"** ordnance on it. It extends [`MrxSupport`](mrxsupport), uses a red-smoke
[`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke) to pick the target, and spawns the actual bombs
through [`Airstrike.SpawnOrdnance`](../namespaces/airstrike). The airstrike-flash screen grade for this
weapon is a separate object — see [AirstrikeAtomsphereBombrun](airstrike_atomsphere_bombrun).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `sDeliveryVehicle`: Name of the delivery vehicle used for the bombing run.
- `uDeliveryVehicle`: GUID of the delivery vehicle.
- `uOwner`: GUID of the player who initiated the bombing run.
- `uJet`: GUID of the aircraft performing the bombing run.
- `uSpawnedBomb`: GUID of the bomb dropped during the bombing run.

## Module constants
Both are module-level **`local`** — set at file scope, unreachable from outside (see the
[Overriding a Function deep dive](../deep-dives/function-override) on why `local` can't be reassigned):
- `sProjectileName = "Bomb"` — the ordnance template passed to `Airstrike.SpawnOrdnance`.
- `sExplosionName = "Explosion (Bombing Run)"` — **declared but never referenced anywhere in the file**
  (dead constant; the "Bomb" template handles its own detonation FX).

## Functions
### `Create(self, uPlayerGuid)`
Class-factory constructor. Builds a `MrxSupportDesignatorSmoke`, sets its AA test level to `"basic"` and
its validation function to `_NoValidation` (inherited from the parent chain — no AA/validity gating), then
sets owner, recruit `"Pilot"`, module name, and copies `sDeliveryVehicle`/`uDeliveryVehicle` onto the
instance.

### `DesignationCallback(self)`
Runs once the smoke target is placed. Computes a spawn point 300 units *behind* the camera and a fly-to
point at the camera via `Pg.FindPointFromCamera`, launches the jet with
`Airstrike.Flyby(self.uDeliveryVehicle, …, 200, DropBomb, {self})` (speed `200`, `DropBomb` as the
over-target callback), stores it as `self.uJet`, and plays a Misha VO line via
[`MrxSupport.PlayAirstrikeVO`](mrxsupport) from a pool of four `"Misha-None-Freeplay-Support-*"` cues.

### `DropBomb(self)`
Fired by `Airstrike.Flyby` when the jet is over the target. Reads the jet position and the designator
target, builds a normalized direction, scales it by `nSpeedScale = 33`, and spawns **two** `"Bomb"`
ordnance — the second offset by `+3/+4/+3` in position and `-2` on each velocity component so they don't
overlap:
```lua
self.uSpawnedBomb = Airstrike.SpawnOrdnance(sProjectileName, nSpawnX, nSpawnY, nSpawnZ,
  nVX*33, nVY*33, nVZ*33, uTarget, "impact", nil, self:GetOwner(), BombExplodes, {self})
```
Note both assignments write the same `self.uSpawnedBomb`, so only the **second** bomb's guid is retained.

### `BombExplodes(self, uBomb)`
Detonation callback registered with each `SpawnOrdnance`. **Empty stub** — the "Bomb" template's own
effects do all the work; there is no scripted post-blast logic here (unlike the daisy-cutter/bunker-buster
variants, which chain debris and demolition off this callback).

## Events
- **No `Event.Create` subscriptions.** `DesignationCallback`/`DropBomb`/`BombExplodes` are engine/callback
  entry points wired up by the parent [`MrxSupport`](mrxsupport) designation flow and by
  `Airstrike.Flyby`/`Airstrike.SpawnOrdnance`, not `Event.*` handlers.

## Notes for modders
- **`sProjectileName` and `nSpeedScale` are the two "change the bomb" levers, but `sProjectileName` is a
  `local`** — you can't reassign it from outside; override the whole `DropBomb` function instead (it's a
  plain global) and pass a different template string (e.g. `"Fuel Air Bomb Projectile"`) to
  `Airstrike.SpawnOrdnance`. See the [Airstrike namespace](../namespaces/airstrike) for the confirmed
  template names.
- `BombExplodes` is a plain global and a genuinely empty stub — a clean place to hook post-blast behavior
  (spawn extra explosions, damage buildings, etc.) without touching the drop logic.
- The `sExplosionName` constant is dead; don't rely on it doing anything.