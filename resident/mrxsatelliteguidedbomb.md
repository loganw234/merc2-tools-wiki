---
title: MrxSatelliteGuidedBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, satellite]
verified: true
verified_note: "deeper pass: documented default cost (self.nCost or 1000), minigame sectors, Smart Bomb payload + inherited BlipAircraft; noted BombExplodes/FinalExplosion are effectively empty (no explosion spawned); cross-linked Airstrike/satellite; paired with the free MrxSurgicalStrike sibling"
---

# MrxSatelliteGuidedBomb

*Module: mrxsatelliteguidedbomb.lua*

## Overview
`MrxSatelliteGuidedBomb` is the **paid** satellite-designated precision bomb. The player targets through the satellite mini-game, a jet flies in and drops one `"Smart Bomb Projectile"` on the mark. The free/easier variant is [`MrxSurgicalStrike`](mrxsurgicalstrike) (same code, `SetCost(0)`, wider sectors). Inherits from [`MrxSupport`](mrxsupport); designates with [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `nCost`: The cost of using the guided bomb.
- `sBomb`: The name of the bomb projectile.
- `uBomb`: The GUID of the bomb projectile.
- `sDeliveryVehicle`: The name of the delivery vehicle.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `uOwner`: The GUID of the player who owns this support instance.
- `uJet`: The GUID of the aircraft used for the airstrike.
- `tBombs`: A table to store bomb instances.
- `uTarget`: The GUID of the target.

## Functions
### `Create(self, uPlayerGuid)`
Builds the instance. Creates a [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite), sets its cost to `self.nCost or 1000` (default **1000**), and mini-game sectors `{{135,225},{-45,45}}` (two broad bands). Copies `sDeliveryVehicle`/`sBomb` from the prototype; module-level `sBomb = "Smart Bomb Projectile"`, module name `"MrxSatelliteGuidedBomb"`.

### `SetCost(self, nCost)`
Updates both the designator's cost and `self.nCost`. This is the money knob — call before `Create` (or override the default) to change what the strike costs.

### `DesignationCallback(self)`
Runs on satellite-designation complete. Flies the delivery jet in with [`Airstrike.Flyby`](../namespaces/airstrike) (`self.uDeliveryVehicle`, callback `DropBomb`, jet in `self.uJet`), then plays a random Misha freeplay-support line via [`MrxSupport.PlayAirstrikeVO`](mrxsupport).

### `DropBomb(self)`
Reads the target, computes a normalized heading, and drops one bomb with [`Airstrike.SpawnOrdnance`](../namespaces/airstrike) using `self.uBomb` at velocity scale `110`, `"impact"` detonation, callback `BombExplodes` with index `1` (stored in `self.tBombs[1]`). Then red-blips the bomb on the radar via `BlipAircraft` (inherited from [`MrxSupport`](mrxsupport)). (`self.uTarget = uGuid` reads an unassigned `uGuid`, so it becomes `nil` — a decompile artifact.)

### `BombExplodes(self, nIndex)`
Impact callback. **Reads the bomb's position but does nothing with it** — no explosion is spawned here (the detonation visual/damage is on the ordnance template). Effectively a no-op in this module; contrast [`MrxSurgicalStrike`](mrxsurgicalstrike), whose `BombExplodes` adds an `"Explosion (Grenade)"`.

### `FinalExplosion(self)`
Reads `self.uBomb`'s position and does nothing else. Dead/no-op as written; nothing calls it.

## Events
No event subscriptions. `DesignationCallback` is the satellite designator's completion callback (via [`MrxSupport:Commence`](mrxsupport)); `DropBomb`/`BombExplodes` are flyby-arrival and ordnance-impact callbacks. No `Event.Create`/`TimerRelative`.

## Module constants & tunables
- `sBomb = "Smart Bomb Projectile"` — module-level global (settable per-instance).
- Default cost: **1000** (`self.nCost or 1000` in `Create`; also settable via `SetCost`).
- Mini-game sectors: `{{135,225},{-45,45}}`.
- Bomb velocity scale: `110`.

## Notes for modders
- `SetCost` (or the `self.nCost or 1000` default) is the price lever; set it to `0` and widen the sectors and you've essentially reproduced [`MrxSurgicalStrike`](mrxsurgicalstrike).
- `sBomb` is a non-`local` global, so reassign `oInstance.sBomb` to change the payload before firing (see [Airstrike](../namespaces/airstrike#notes-for-modders)).
- Since this module's `BombExplodes` spawns no explosion, if you want an on-impact effect, add a [`Pg.Spawn`](../namespaces/pg) there (as the surgical-strike sibling does).