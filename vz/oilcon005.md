---
title: OilCon005
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 4
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# OilCon005

## Overview
A straightforward Oil Company minor contract: a sports-car race. One or two "Veyron" cars (solo vs. coop)
run a roughly 40-checkpoint `MrxTaskRace` course, with a solo-win achievement and a separate two-player-win
achievement.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxTaskRace`, `MrxTaskObjectiveDeliver`, `MrxLayerManager`, `MrxAchievements`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` pattern.
Module-level `nComp` (completion count, clamped to a max of 2 for difficulty purposes), `tCars`/`oCar01`/
`oCar02` (spawned vehicle guids), and `self.oRaceObjective` (the one field stored on `self` rather than as
a bare global in this file).

## Functions
### `LoadAssets(self)` / `GetSportsCars(self)`
`LoadAssets` loads the main + staging layers, then calls `GetSportsCars` once loaded. `GetSportsCars`
spawns one Veyron per player (two if `Player.GetCurrentPlayers() == 2`) at two fixed spawn markers, and
waits for the first car to wake before calling `AssetsLoaded`.

### `Activated(self)` / `CarRace(self, tVeh)`
`Activated` calls the base `Activated` then `self:CarRace(tCars)`. `CarRace` builds the race objective
itself — course length and start-time bonus both scale down with `nComp` (harder each replay) — with
`fOnComplete` marking the staging layer for removal, granting the solo achievement
(`ACHIEVEMENT_HIGHWAY_TO_HELL`) to whichever car's driver actually won, and additionally granting a
two-player achievement (`ACHIEVEMENT_WHEELS_OF_STEEL`, via `NetGrantAchievement`) if both players raced.
`fVehiclesDestroyedCallback` sets a different cancel message depending on whether one or both cars were
destroyed. A boarding event separately cues special mission music once a player gets into `oCar01`.

### `Cleanup(self)`
Stops special music, marks the staging and bonus layers for removal, and arms a per-car
"remove once hibernated" event for every spawned Veyron, then calls `MrxTaskContract.Cleanup(self)`.

## Events
`Event.ObjectHibernation` (car-ready gate, per-car cleanup-on-hibernate), `Event.ObjectInSeat` (music cue
on boarding `oCar01`).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- One of the few files in this batch that calls `MrxAchievements` directly — a useful reference if you want
  a mod contract to grant a real Xbox/Steam-style achievement rather than just an in-fiction reward.
- `fVehiclesDestroyedCallback` on the race objective is a hook worth knowing about generally: it fires
  independent of win/lose, purely to adjust messaging when the race's own vehicles get destroyed mid-run.
