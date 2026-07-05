---
title: MrxSmartBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, smart bomb]
verified: true
verified_note: 'deeper pass: documented the SpawnTargettedOrdnance("Smart Bomb Projectile") guided drop and the radar blip, flagged the sBomb="Laser Guided Bomb Projectile" field as misleading/unused (the fired template is a literal), and that BombExplodes deletes the beacon target object; cross-linked Airstrike/MrxSupport'
---

# MrxSmartBomb

*Module: mrxsmartbomb.lua*

## Overview
`MrxSmartBomb` is a **beacon-guided** bomb: the player plants a beacon, a jet flies over, and it drops a
homing **"Smart Bomb Projectile"** via [`Airstrike.SpawnTargettedOrdnance`](../namespaces/airstrike) that
tracks the beacon's guid. The falling bomb is blipped on the radar in red, and on detonation the beacon
target object itself is removed. Extends [`MrxSupport`](mrxsupport) and uses
[`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oDesignator`: The designator beacon used for targeting.
- `uOwner`: The GUID of the player who owns this support instance.
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `uJet`: The GUID of the aircraft delivering the bomb.
- `uSpawnedBomb`: The GUID of the spawned bomb.

## Module constants & templates
- The **actually-fired** ordnance template is the literal `"Smart Bomb Projectile"` in `DropBomb`.
- `Create` also sets `self.sBomb = "Laser Guided Bomb Projectile"` / `self.uBomb = Pg.GetGuidByName(...)`,
  but **neither field is read anywhere in this file** — `DropBomb` ignores them and passes the literal above.
  Treat `sBomb`/`uBomb` here as misleading dead fields (a likely copy-paste from
  [MrxLaserGuidedBomb](mrxlaserguidedbomb), which *does* use them).
- Radar blip color: red `{255, 0, 0}` (via the inherited `BlipAircraft`).

## Functions
### `Create(self, uPlayerGuid)`
Class-factory constructor. Builds a [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon), sets owner /
recruit `"Pilot"` / module name, and sets the (unused) `sBomb`/`uBomb` fields. Note it does **not** set a
delivery vehicle — `DesignationCallback` uses `self.uDeliveryVehicle` from the prototype/parent.

### `DesignationCallback(self)`
Picks a random 360° approach angle, computes spawn (300 back, alt 25) and target (100 out, alt 80) points,
flies the jet with `Airstrike.Flyby(self.uDeliveryVehicle, …, nTargetY + 150, 50, DropBomb, {self})` (note
the +150 altitude offset and the slow speed `50`), and plays a Misha VO from a nine-cue pool.

### `DropBomb(self)`
Reads the beacon target (`uGuid`, `uTarget`) and jet position, and fires the **guided** bomb:
```lua
self.uSpawnedBomb = Airstrike.SpawnTargettedOrdnance("Smart Bomb Projectile", nX, nY, nZ,
  nVX, nVY, nVZ, uGuid, "impact", uTarget, self.uOwner, BombExplodes, {self})
```
then `BlipAircraft(self.uSpawnedBomb, {255,0,0})` to mark the descending bomb red on radar. Velocity is the
**unscaled** normalized vector (no speed multiplier).

### `BombExplodes(self)`
Detonation callback. Prints a debug line, then — if the beacon `uGuid` exists and `Player.IsLocal(self.uOwner)`
— calls `Object.Remove(uGuid)` to delete the beacon object so it doesn't linger after the strike.

## Events
- **No `Event.Create` subscriptions.** `DesignationCallback`/`DropBomb`/`BombExplodes` are wired by the parent
  designation flow and the `Airstrike.Flyby`/`SpawnTargettedOrdnance` callbacks — not event handlers.

## Notes for modders
- **To change what this weapon drops, edit the `"Smart Bomb Projectile"` literal in `DropBomb`** (a plain
  global) — do **not** bother setting `sBomb`/`uBomb`, which this module ignores.
- This is a rare example of a **guided** support bomb (`SpawnTargettedOrdnance` with a `uTarget`), so the bomb
  actually homes on the beacon rather than following a fixed ballistic arc — see the
  [Airstrike namespace](../namespaces/airstrike) for the targetted-vs-ballistic distinction.
- `BombExplodes` deleting the beacon is host+owner-gated (`Player.IsLocal`); on other clients the object is
  left to sync normally.