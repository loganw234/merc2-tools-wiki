---
title: PmcCon015
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 6
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon015

## Overview
PmcCon015 is a short "Phoenix" street-race contract: spawn a race car (or two, one per player, in co-op) and run a course of roughly 17 checkpoints against a shrinking timer that tightens with each replay (45s down to 25s). Finishing grants racing achievements; running out of time or destroying the race car both fail the contract.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxTaskRace`, `MrxTaskObjectiveDeliver`, `MrxTaskObjectiveDestroy`, `MrxLayerManager`, `MrxSubtitle`, `MrxMusic`, `MrxFactionManager`, `MrxAchievements`

## Instance pattern
A native `MrxTaskContract` subclass with bare-global state (`spVehicle`/`mpVehicle`, `tVehicle`).

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)`
`LoadAssets` adds the mission layer. `Activated` spawns one `"Phoenix (racing)"` car in solo, or two (one per named spawn point) in co-op, scales the time limit and bonus-time-per-checkpoint down with each replay, starts the race via `StartRace`, plays special music once a player boards, and watches the race car for death (`VehicleDeath`).

### `StartRace(self, tVeh, nTimeLimit, nTimeToAdd)`
Creates the `MrxTaskRace` child with 17 checkpoints. On completion, grants `ACHIEVEMENT_HIGHWAY_TO_HELL` (and `ACHIEVEMENT_WHEELS_OF_STEEL` in co-op if there's a winner) before completing via VO. On cancellation (time expired), calls `CourseUnfinished`.

### `VehicleDeath(self)` / `CourseUnfinished(self)`
Cancel paths with an appropriate VO line and cancel message.

### `Cleanup(self)`
Stops music, removes the mission layer, calls base `MrxTaskContract.Cleanup`, then removes the spawned vehicle(s).

## Events
- `Event.ObjectInSeat` — boarding the race car triggers special music.
- `Event.ObjectDeath` — watches the race car for destruction.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- **Cleanup bug worth knowing about if you're studying this file:** `Cleanup` checks `if isMultiplayer == 2` to decide whether to remove both `mpVehicle` and `spVehicle`, but `isMultiplayer` was only ever declared as a `local` inside `Activated` — the bare (global) `isMultiplayer` that `Cleanup` reads is a different, always-`nil` variable. In practice this means the co-op branch of the vehicle cleanup never actually runs; only `spVehicle` gets removed regardless of player count. Not something to copy if you're writing similar cleanup logic.
- `MrxTaskObjectiveDestroy` and `MrxFactionManager` are both imported but never referenced anywhere in this file's body — likely leftover imports from an earlier version of the contract.
