---
title: MrxSurgicalStrike
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: "deeper pass: flagged that SetModuleName is 'MrxSatelliteGuidedBomb' (not SurgicalStrike), documented the free satellite (SetCost 0)/minigame sectors, the Smart Bomb payload + Explosion (Grenade) burst, and the dead FinalExplosion; cross-linked Airstrike/satellite"
---

# MrxSurgicalStrike

*Module: mrxsurgicalstrike.lua*

## Overview
`MrxSurgicalStrike` is a **free** satellite-designated precision bomb — effectively a no-cost variant of [`MrxSatelliteGuidedBomb`](mrxsatelliteguidedbomb) (it even shares that module's name; see the warning below). The player targets through the satellite mini-game, a jet flies in and drops one `"Smart Bomb Projectile"` on the mark. It inherits from [`MrxSupport`](mrxsupport) and designates with [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(oSelf, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `oDesignator`: The designator satellite used for target designation.
- `uOwner`: The GUID of the player who owns this support system.
- `sRecruit`: The recruit type required for this support.
- `sModuleName`: The name of the module.
- `sDeliveryVehicle`: The delivery vehicle used for the airstrike.
- `uDeliveryVehicle`: The GUID of the delivery vehicle.
- `sBomb`: The bomb projectile used.
- `uBomb`: The GUID of the bomb projectile.
- `uJet`: The GUID of the jet performing the airstrike.
- `uTarget`: The GUID of the target.
- `tBombs`: A table to track spawned bombs.

## Functions
### `Create(oSelf, uPlayerGuid)`
Builds the instance. Creates a [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite), calls `oDesignator:SetCost(0)` (**free** — the defining difference from the paid [`MrxSatelliteGuidedBomb`](mrxsatelliteguidedbomb)), sets mini-game sectors `{{45,90},{152,203},{270,315}}` (wider/easier bands than the paid version), recruit `"Pilot"`, and copies `sDeliveryVehicle`/`sBomb` from the prototype. The module-level default `sBomb = "Smart Bomb Projectile"`.

{: .warning }
> `Create` calls `oNewSupport:SetModuleName("MrxSatelliteGuidedBomb")`, **not** `"MrxSurgicalStrike"`. The module identifies itself to the network/support layer as the guided-bomb module. This is almost certainly a copy-paste from [`MrxSatelliteGuidedBomb`](mrxsatelliteguidedbomb) that was never renamed — confirmed in source, not an error in this page. It matters if you key any logic off `GetModuleName()`.

### `DesignationCallback(oSelf)`
Runs on satellite-designation complete. Flies the delivery jet in with [`Airstrike.Flyby`](../namespaces/airstrike) (using `oSelf.uDeliveryVehicle`, callback `DropBomb`, jet stored in `oSelf.uJet`), then plays a random Misha freeplay-support line via [`MrxSupport.PlayAirstrikeVO`](mrxsupport).

### `DropBomb(oSelf)`
Reads the target, computes a normalized heading, and drops one bomb with [`Airstrike.SpawnOrdnance`](../namespaces/airstrike) using `oSelf.uBomb` at velocity scale `110`, `"impact"` detonation, callback `BombExplodes` with index `1`. Stored in `oSelf.tBombs[1]`. (Note `oSelf.uTarget = uGuid` reads a `uGuid` that is never assigned in this function, so it's set to `nil` — a decompile artifact.)

### `BombExplodes(oSelf, nIndex)`
Impact callback. Reads the bomb's position and, if valid, spawns `"Explosion (Grenade)"` there via [`Pg.Spawn`](../namespaces/pg).

### `FinalExplosion(oSelf)`
Would spawn `"Explosion (C4)"` at `oSelf.uSpawnedBomb`. **Dead code in this module** — nothing here sets `oSelf.uSpawnedBomb` (it uses `tBombs[]` instead) and nothing calls `FinalExplosion`. Present but unreachable as written.

## Events
No event subscriptions. `DesignationCallback` is the satellite designator's completion callback (via [`MrxSupport:Commence`](mrxsupport)); `DropBomb`/`BombExplodes` are flyby-arrival and ordnance-impact callbacks. No `Event.Create`/`TimerRelative`.

## Module constants & tunables
- `sBomb = "Smart Bomb Projectile"` — module-level global (settable per-instance since it's not `local`).
- Satellite cost: `0` (free), set via `SetCost(0)` in `Create`.
- Mini-game sectors: `{{45,90},{152,203},{270,315}}` — three wide success bands.
- Recruit: `"Pilot"`.
- Bomb velocity scale: `110`; explosion effect: `"Explosion (Grenade)"`.

## Notes for modders
- This is the free/easy sibling of [`MrxSatelliteGuidedBomb`](mrxsatelliteguidedbomb); the code is nearly identical apart from `SetCost(0)`, the wider sectors, the `"Pilot"` recruit, and the added `"Explosion (Grenade)"` in `BombExplodes`.
- Because `sBomb` is a non-`local` global, you can reassign `oInstance.sBomb` to change the payload before firing — see [Airstrike](../namespaces/airstrike#notes-for-modders).
- The mismatched module name (`"MrxSatelliteGuidedBomb"`) is worth remembering before you build any per-module routing.