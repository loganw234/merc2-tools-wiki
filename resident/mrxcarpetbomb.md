---
title: MrxCarpetBomb
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: 'deeper pass: documented the line-walk mechanism via Airstrike.SpawnCarpetBombLine (7 lines @ 0.35s), the B2 delivery vehicle literal and 5/15 spread args, flagged explode() as a dev helper and a stop-scheduling quirk in NextExplosionCallback; cross-linked Airstrike/MrxSupport'
---

# MrxCarpetBomb

*Module: mrxcarpetbomb.lua*

## Overview
`MrxCarpetBomb` is the satellite-designated carpet-bomb support: a B2 flies over the marked point and lays
down a **walking string of explosions**, advancing a "line" of blasts along the jet's heading every
0.35 s. Unlike the other bombs here it never calls `Airstrike.SpawnOrdnance` — each line is produced by
[`Airstrike.SpawnCarpetBombLine`](../namespaces/airstrike), which returns the next position to continue
from. Extends [`MrxSupport`](mrxsupport) and targets with [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSatellite`](mrxsupportdesignatorsatellite)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uOwnerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `nTotalLines`: Total number of bomb lines to deploy.
- `nRemainingLines`: Number of remaining bomb lines to deploy.
- `nTimeInterval`: Time interval between each explosion.
- `uJet`: GUID of the jet performing the airstrike.
- `nHeading`: Heading direction for bomb deployment.
- `uOwner`: GUID of the player or entity owning the support.

## Module constants & tunables
Set on the instance in `Create` (per-instance fields, freely reassignable):
- `nTotalLines = 7` — how many blast lines the run lays down.
- `nTimeInterval = 0.35` — seconds between successive lines.

The B2 delivery vehicle is a **hardcoded literal** in `DesignationCallback`
(`Airstrike.Flyby("Support Vehicle (B2)", …)`), not an instance field — to change it you must override the
function. Recruit is `"Fiona"`.

## Functions
### `Create(self, uOwnerGuid)`
Class-factory constructor. Seeds `nTotalLines = 7`, `nRemainingLines = nTotalLines`, `nTimeInterval = 0.35`,
builds a satellite designator, and sets recruit `"Fiona"` / owner / module name `"MrxCarpetBomb"`.

### `DesignationCallback(self)`
Reads the satellite target, records `self.nHeading = Camera.GetYaw(...)` (the direction the lines will walk),
computes a spawn point 300 units back and clamps its altitude to at least 100 above the target, then flies
the B2 with `Airstrike.Flyby("Support Vehicle (B2)", …, 100, DropBomb, {self})`. Plays an (empty) VO via
[`MrxSupport.PlayAirstrikeVO`](mrxsupport).

### `DropBomb(oAirstrike)`
The over-target callback. Lays the **first** line with
`Airstrike.SpawnCarpetBombLine(nSpawnX, nSpawnY, nSpawnZ, oAirstrike.nHeading, owner, nil, 5, 15)` — the
trailing `5, 15` are the line's spread parameters — stores the returned next-position (nudged up by a random
`math.randi(10, 30)` in Y), and schedules `NextExplosionCallback` after `nTimeInterval`.

### `NextExplosionCallback(oAirstrike)`
Lays the next line from the stored position (same `5, 15` spread), decrements `nRemainingLines`, and
reschedules itself until the counter hits 0.

{: .note }
> **Quirk:** when `nRemainingLines <= 0` the code resets it back to `nTotalLines` but does **not** schedule
> another callback, so the run simply stops after 7 lines. The reset means a *reused* instance would start
> the next run with a full count — but it also means the counter is never left at 0.

### `explode()`
Standalone helper: spawns `"carpetbomb_explosion"` at the local player's own position. Takes no target and
isn't part of the run flow — effectively a **dev/test** trigger (spawns the effect on yourself), not called
by the module's normal path.

## Events
- **No `Event.Create` subscriptions.** The only `Event.*` use is `Event.TimerRelative`, chaining
  `NextExplosionCallback` at `nTimeInterval` spacing. `DesignationCallback`/`DropBomb` are wired by the
  parent designation flow and `Airstrike.Flyby`.

## Notes for modders
- **`nTotalLines` and `nTimeInterval` are the main "make the carpet longer / faster" knobs** — and because
  they're per-instance fields (not `local`s), you can reassign them on the instance before firing.
- The `5, 15` spread arguments to `Airstrike.SpawnCarpetBombLine` control the line's shape — override
  `DropBomb`/`NextExplosionCallback` (plain globals) to change them, or to swap the `"Support Vehicle (B2)"`
  delivery jet.
- `explode()` is safe to call from a dev/`OnKey` script to preview the `"carpetbomb_explosion"` effect on
  yourself; it is not part of the live weapon.