---
title: MrxCruiseMissile
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, missile]
verified: true
verified_note: "deeper pass: surfaced module-level template locals, documented the Airstrike.Flyby jet -> DropBomb -> SpawnTargettedOrdnance homing chain; noted the local-vs-instance sBomb duplication; cross-linked Airstrike/beacon"
---

# MrxCruiseMissile

*Module: mrxcruisemissile.lua*

## Overview
`MrxCruiseMissile` flies a delivery jet on a beacon-designated run, then launches a single *homing* cruise missile at the marked target. It inherits from [`MrxSupport`](mrxsupport) and uses [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon) to designate.

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorBeacon`](mrxsupportdesignatorbeacon)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `sDeliveryVehicle`: The name of the delivery vehicle used for cruise missiles.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `uOwner`: The GUID of the player who owns the missile support.
- `uJet`: The GUID of the jet used for the bombing run.
- `uSpawnedBomb`: The GUID of the spawned bomb projectile.

## Functions
### `Create(self, uPlayerGuid)`
Creates a new per-instance table for the cruise missile support using the module's prototype. Initializes the designator beacon, sets the owner and recruit, and configures the delivery vehicle and bomb details.

### `DesignationCallback(self)`
Runs on beacon-designation complete. Computes a spawn point behind the camera and an approach path offset toward the target, then flies the jet in with [`Airstrike.Flyby`](../namespaces/airstrike) (template `"Support Vehicle (Cruise Missile)"`), passing `DropBomb` as the arrival callback and storing the jet handle in `self.uJet`. Ends with a faction-branched VO (keyed off the **delivery vehicle's** labels — Allied/China/else Fiona) via [`MrxVoSequence.Start`](mrxvosequence).

### `DropBomb(self)`
Fires when the jet reaches its launch point. Removes the jet (`Object.Remove(self.uJet)`), computes a normalized heading toward the beacon, and launches a **homing** missile with [`Airstrike.SpawnTargettedOrdnance`](../namespaces/airstrike) — `"Cruise Missile Projectile"`, target `uGuid` from the beacon, `"impact"` detonation, callback `BombExplodes`. Stores it in `self.uSpawnedBomb`.

### `BombExplodes(self)`
On impact: removes the beacon object if `Player.IsLocal(self.uOwner)`. (The actual explosion visual is on the ordnance template, not spawned here — this callback only cleans up the beacon. `sExplosionName` is declared but unused in the current source.)

## Events
No event subscriptions. `DesignationCallback` is the beacon's completion callback (via [`MrxSupport:Commence`](mrxsupport)); `DropBomb` is the flyby-arrival callback; `BombExplodes` is the ordnance-impact callback. No `Event.Create`/`TimerRelative` anywhere in this module.

## Module constants & tunables
The names live in **two** places — a real quirk:
- Module-level `local`s (top of file): `sProjectileName = "Cruise Missile Projectile"`, `sExplosionName = "Explosion (Cruise Missile)"` (unused), and `local sBomb`/`local uBomb = "Support Vehicle (Cruise Missile)"`.
- Per-instance fields set in `Create`: `self.sBomb`/`self.uBomb` (from `self.sBomb`, which starts `nil` unless a subclass/config sets it), and `self.sDeliveryVehicle` defaulting to `"Fiona"`.
- The jet in `DesignationCallback` is spawned from a **hardcoded literal** `"Support Vehicle (Cruise Missile)"`, *not* from `self.sDeliveryVehicle` — so repointing `sDeliveryVehicle` does not change the jet here.

## Notes for modders
- `DesignationCallback`, `DropBomb`, `BombExplodes` are plain globals — override them to change the run. The homing missile is [`Airstrike.SpawnTargettedOrdnance`](../namespaces/airstrike); swap `sProjectileName` there (it's a `local`, so you must override the function, not reassign a field).
- Because the jet template is a literal, changing `self.sDeliveryVehicle` won't repaint the flyby aircraft — edit the `Airstrike.Flyby` call in `DesignationCallback` instead.
- The faction VO branch reads the **delivery vehicle's** labels, same pattern (and gotcha) as [`MrxArtillery`](mrxartillery).