---
title: MrxLaserGuidedBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, bomb]
verified: true
verified_note: 'deeper pass: documented the SpawnTargettedOrdnance(self.uBomb) ×80 guided drop with ±25 target scatter, the module-global sBomb/uBomb (overridable, unlike the locals in sibling modules), and the host+150-unit debris gate; noted it is the base class of MrxBunkerBuster; cross-linked Airstrike/MrxSupport'
---

# MrxLaserGuidedBomb

*Module: mrxlaserguidedbomb.lua*

## Overview
`MrxLaserGuidedBomb` is the base laser-guided bomb support: a jet drops a homing **"Laser Guided Bomb
Projectile"** that tracks the laser-designated target via
[`Airstrike.SpawnTargettedOrdnance`](../namespaces/airstrike), with a small random scatter so repeat strikes
don't land in the exact same spot. It's also the **parent of [MrxBunkerBuster](mrxbunkerbuster)** — the
bunker buster reuses this drop pipeline and only overrides `BombExplodes`. Extends [`MrxSupport`](mrxsupport)
and uses [`MrxSupportDesignatorLaser`](mrxsupportdesignatorlaser).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorLaser`](mrxsupportdesignatorlaser), [`MrxUtil`](mrxutil)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `sDeliveryVehicle`: The name of the delivery vehicle.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `tVOCues`: Voice-over cues for the support system.
- `uOwner`: The GUID of the player who owns the support system.
- `uJet`: The GUID of the aircraft used to deliver the bomb.
- `uTarget`: The GUID of the target designated by the laser designator.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Module constants & templates
- `sBomb = "Laser Guided Bomb Projectile"` and `uBomb = Pg.GetGuidByName(...)` are **module-level globals**
  (not `local`), so — unlike the daisy-cutter/MOAB `local` defaults — they can be reassigned from an external
  script *and* they're copied onto each instance in `Create`. `DropBomb` fires `self.uBomb`, so setting the
  instance field is the clean per-strike override.
- Velocity multiplier: `×80` (applied inline in `DropBomb`, not a named constant).
- Target scatter: each of X/Y/Z is nudged by `math.randf()*25 - math.randf()*25` (roughly ±25 units) before
  aiming — the "don't stack perfectly" jitter.

## Functions
### `Create(self, uPlayerGuid)`
Class-factory constructor. Builds a [`MrxSupportDesignatorLaser`](mrxsupportdesignatorlaser), sets owner /
recruit `"Pilot"` / module name, and copies delivery-vehicle, bomb (`sBomb`/`uBomb`) and `tVOCues` fields
onto the instance.

### `DesignationCallback(self)`
Computes spawn (300 back, alt 100) and target (100 back, alt 80) points, flies the jet with
`Airstrike.Flyby(self.uDeliveryVehicle, …, 120, DropBomb, {self})`, and schedules a Misha VO (six-cue pool)
2 s later via `Event.TimerRelative`.

### `DropBomb(self)`
Reads the laser target, applies the ±25 random scatter, re-aims at the target object's actual position, and
fires the **guided** bomb:
```lua
self.uSpawnedBomb = Airstrike.SpawnTargettedOrdnance(self.uBomb, nX, nY, nZ,
  nVX*80, nVY*80, nVZ*80, uGuid, "impact", 1, self:GetOwner(), self.BombExplodes, {self})
```
then `BlipAircraft(self.uSpawnedBomb, {255,0,0})` to mark it red on radar. Note it passes `self.BombExplodes`
(the instance's own override, so subclasses like the bunker buster get their version called).

### `BombExplodes(self)`
Detonation callback — schedules `CreateDebris` **1.5 s** later via `Event.TimerRelative`. (Subclasses
override this: [MrxBunkerBuster](mrxbunkerbuster) replaces it with its multi-stage demolition chain.)

### `CreateDebris(self)`
Draws a `Graphics.Effect.Terrain("global_particle_dustfall", 20, 0.005, …)` dust cloud at the local player's
feet — **only if** not a network client and the local hero is within **150 units** of the target
(`MrxUtil.GetDistanceToObject(...) > 150` early-returns). Host-side, near-player cosmetic only. (Same code as
[MrxDaisyCutter](mrxdaisycutter)'s `CreateDebris`.)

## Events
- **No `Event.Create` subscriptions.** The only `Event.*` use is `Event.TimerRelative` scheduling (the 2 s VO
  delay and the 1.5 s `CreateDebris` delay). `DesignationCallback`/`DropBomb`/`BombExplodes` are wired by the
  parent designation flow and the `Airstrike.Flyby`/`SpawnTargettedOrdnance` callbacks.

## Notes for modders
- **`sBomb`/`uBomb` are the intended override point and are genuinely reachable** (module globals, not
  `local`) — reassign `oInstance.uBomb` before a strike to drop a different projectile. This is the pattern
  [MrxBunkerBuster](mrxbunkerbuster) uses to select standard vs nuclear.
- `BombExplodes` is dispatched as `self.BombExplodes`, so **overriding it on a subclass/instance actually
  takes effect** — this is how the bunker buster injects its demolition sequence without touching `DropBomb`.
- The ±25 scatter and `×80` velocity are hardcoded in `DropBomb` (a plain global) — override the function to
  tighten accuracy or change the drop speed.
- `CreateDebris` is host-only and gated to a 150-unit radius; don't rely on it firing for remote clients or
  distant players.