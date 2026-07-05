---
title: MrxTankBuster
parent: Support & Airstrikes
grand_parent: Resident Modules
nav_order: 1
inherits: MrxSupport
tags: [support, airstrike]
verified: true
verified_note: "deeper pass: documented FastCollectTanks/non-PMC targeting (200 units), red smoke + basic AA designator, Airstrike AT Missile with Object.Kill callback, inherited BlipAircraft; corrected Events; cross-linked Airstrike/smoke designator"
---

# MrxTankBuster

*Module: mrxtankbuster.lua*

## Overview
`MrxTankBuster` is a smoke-designated anti-armor strike: the player pops red smoke, a jet flies in and fires a guided AT missile at every non-PMC tank within range. It inherits from [`MrxSupport`](mrxsupport) and designates with [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke).

## Inheritance
- Inherits from: [`MrxSupport`](mrxsupport)
- Imports: [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke)

## Instance pattern
**Same class-factory pattern as `MrxSupport`, not per-`uGuid`** — `Create(self, uPlayerGuid)` builds a new
table via `setmetatable`/`__index`, exactly like its parent. No `OnActivate`/`Awake`, no `tInstance`
registry. It tracks the following key fields:
- `uOwner`: The GUID of the player who owns this support.
- `uJet`: The GUID of the aircraft performing the airstrike.
- `uDeliveryVehicle`: The vehicle used to deliver the ordnance.
- `oDesignator`: The designator object for guiding the strike.

## Functions
### `Create(self, uPlayerGuid)`
Builds the instance. Creates a [`MrxSupportDesignatorSmoke`](mrxsupportdesignatorsmoke), sets smoke color `"red"`, AA test level `"basic"`, and clears its validation function (`SetValidationFunction(nil)` — no drop-zone check). Recruit `"Pilot"`, module name `"MrxTankBuster"`.

### `DesignationCallback(self)`
Runs on smoke-designation complete. Flies the delivery jet in with [`Airstrike.Flyby`](../namespaces/airstrike) (spawn/target points from the camera, speed 120, callback `Strike`, jet in `self.uJet`), then schedules a Misha freeplay-support VO 3 seconds later via [`Event.TimerRelative`](../namespaces/event) → [`MrxSupport.PlayAirstrikeVO`](mrxsupport).

### `Strike(self)`
Runs when the jet arrives. `Pg.FastCollectTanks` within **200 units** of the player, then for each tank that either has **no driver** or whose driver is **not labeled "PMC"**, schedules `LaunchMissile` with [`Event.TimerRelative`](../namespaces/event) staggered `0.2 * nCount` seconds apart.

### `LaunchMissile(self, uTarget)`
Launches one homing `"Airstrike AT Missile"` from the jet at `uTarget` via [`Airstrike.SpawnTargettedOrdnance`](../namespaces/airstrike) (speed scale 30, `"impact"`, callback `Object.Kill` on the target). Then blips the missile red on the radar via `BlipAircraft` (inherited from [`MrxSupport`](mrxsupport)).

### `_ValidateDropZone(fCallback, nX, nY, nZ, oSupport)`
Drop-zone validator wrapping `Ai.TestDropZone`. Note: this one is **defined but not wired up** — `Create` explicitly passes `SetValidationFunction(nil)`, so the smoke designator never calls it. Present as a spare/override hook.

## Events
No event subscriptions. `DesignationCallback` is the smoke designator's completion callback (via [`MrxSupport:Commence`](mrxsupport)), `Strike` is the flyby-arrival callback, and `LaunchMissile` / the VO are fired by [`Event.TimerRelative`](../namespaces/event) timers — none are `Event.Create` subscriptions.

## Module constants & tunables
All inline (no module-level `local`s):
- Payload: `"Airstrike AT Missile"` (homing), `nSpeedScale = 30`, callback `Object.Kill` (guaranteed one-shot kill on hit).
- Target search: `Pg.FastCollectTanks`, radius **200** units, non-PMC only, `0.2s` between launches.
- Designator: red smoke, AA level `"basic"`, no validation.
- Jet flyby speed: 120; recruit `"Pilot"`.

## Notes for modders
- The kill is deterministic: the missile's impact callback is `Object.Kill(uTarget)`, so any tank hit dies regardless of missile damage. Change that callback in `LaunchMissile` (a plain global) if you want normal damage instead.
- Targeting is tank-only and non-PMC-only. Swap `Pg.FastCollectTanks` or drop the PMC-label check in `Strike` to broaden it.
- `_ValidateDropZone` exists but is disabled by `SetValidationFunction(nil)`; pass it (or your own) to `SetValidationFunction` if you want the smoke to require a clear drop zone.