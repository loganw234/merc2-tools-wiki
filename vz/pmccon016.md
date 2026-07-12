---
title: PmcCon016
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 7
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon016

## Overview
PmcCon016 is a race contract (a Panhard in solo, a Buggy in co-op) around a longer course of roughly 27 checkpoints, with a secondary parallel objective to shoot down 6 destructible pylons along the way for bonus time. The time limit and bonus-per-pylon both shrink with each replay.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxTaskRace`, `MrxTaskObjectiveDeliver`, `MrxSubtitle`, `MrxLayerManager`, `MrxMusic`, `MrxAchievements`, `MrxTutorialManager`

## Instance pattern
A native `MrxTaskContract` subclass with bare-global state (`tVehicle`, `nTimeLimit`, `nTimeToAdd`).

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)` / `GetVehicles(self)`
`LoadAssets` adds the mission layer. `Activated` spawns the race vehicle via `GetVehicles` (Panhard solo / Buggy co-op), plays intro VO, scales the time limit/bonus by replay count, disables the vehicle until the race starts, calls `StartRace`, watches the vehicle for death, arms a proximity VO trigger, and shows a race tutorial message.

### `StartRace(self, tVehicle, nTimeLimit, nTimeToAdd)`
Creates the `MrxTaskRace` child (21 checkpoints; achievements + VO + complete on finish, `CourseUnfinished` on time-out) alongside a parallel `MrxTaskObjectiveDestroy` child targeting 6 named pylons, where each destroyed pylon calls `ObjectDestroyed`.

### `ObjectDestroyed(self)`
Adds `nTimeToAdd` bonus seconds to the race's internal timer and briefly flashes a "bonus time" HUD message.

### `FionaProximityVO(self)` / `VehicleDeath(self)` / `VehicleUnentered(self)` / `CourseUnfinished(self)`
Flavor VO and fail paths. `VehicleUnentered` has no visible caller in this file — possibly invoked by `MrxTaskRace` via a naming convention this corpus doesn't show.

### `Cleanup(self)`
Stops music, removes the mission layer, calls base `MrxTaskContract.Cleanup`, removes the spawned vehicle, and clears two HUD slots.

## Events
- `Event.ObjectHibernation` — the vehicle stays unusable until the race's disable-lock is lifted.
- `Event.ObjectDeath` — watches the race vehicle for destruction.
- `Event.ObjectProximity` — triggers `FionaProximityVO` near a specific course location.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- The parallel race + destroy-for-bonus-time pattern (`StartRace` spawning both an `MrxTaskRace` and an `MrxTaskObjectiveDestroy` child side by side) is a reusable template if you want to add a secondary scoring mechanic to a race contract.
- The `sModuleName = "MrxTaskObjectiveDestroy"` child is created purely by string name via `CreateChild` — it doesn't require (and this file doesn't have) an explicit `import("MrxTaskObjectiveDestroy")` to work, unlike calling a namespace's functions directly.
