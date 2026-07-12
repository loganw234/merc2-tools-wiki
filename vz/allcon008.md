---
title: AllCon008
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 4
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# AllCon008

## Overview
An Allied Nation minor/side contract: a "Coanda Transport" helicopter race through roughly 35 checkpoints.
Solo players race alone; a second copter is spawned automatically if two players are present. Replaying
the contract makes it harder — `self:GetNumCompletions()` shortens the starting time and the per-checkpoint
time bonus. Winning grants "Highway to Hell" achievement progress, and — in two-player co-op specifically —
the "Wheels of Steel" achievement.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxTaskRace`, `MrxTaskObjectiveDeliver`, `MrxLayerManager`, `MrxAchievements` (imported twice
  in a row — a harmless duplicate `import()` call)

`MrxTaskObjectiveDeliver` has no visible use in this file (no child is created with that
`sModuleName`) — likely an unused leftover import.

## Instance pattern
A native `MrxTaskContract` subclass. Module-level globals track race state: `uPlayer`/`tPlayers`/
`nPlayers`, `nComp` (difficulty scaling from completion count), `tCopters`/`oCopter01`/`oCopter02`/
`nCopters`, and `self.oRaceObjective` (the race child task).

## Functions
### `Activated(self)`
Calls the base `MrxTaskContract.Activated`, resolves the player count and prior-completion count (capped
at 2 for scaling purposes), adds the staging layer, and starts `ChopperRace`.

### `ChopperRace(self)`
Creates the `MrxTaskRace` child over the ~35 named checkpoints, scaling the start time and per-checkpoint
bonus down as `nComp` increases; on completion grants achievement progress and removes the staging layer;
also arms a seat-enter event that starts special mission music.

### `VehicleCheck(self)`
Decrements `nCopters` and cancels the contract if fewer copters remain than there are players. **No call
site found anywhere in this file** — presumably meant to run off a copter-destroyed event that isn't
wired up here.

### `LoadAssets(self)`
Adds the main/staging layers, then calls `GetCopters` once loaded.

### `GetCopters(self)`
Spawns one "Coanda Transport" per player (one or two) at the two named spawn points and signals
`AssetsLoaded` once the first copter wakes.

### `Cleanup(self)`
Stops the special music, marks the staging layer for removal, arms a hibernation-triggered removal for
each spawned copter, and calls the base `MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectInSeat` — the player entering/exiting `oCopter01`'s driver seat starts the special race
  music.
- `Event.ObjectHibernation` — `oCopter01` waking signals `AssetsLoaded`; each copter hibernating in
  `Cleanup` triggers its removal.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **Likely typo/bug**: `GetCopters` computes `local nYaw21 = Object.GetYaw(uSpawn02)` (note the `21`) but
  then spawns the second copter with `nYaw2` — a different, never-declared name — so `oCopter02` in the
  two-player case would spawn with a `nil` yaw argument instead of the intended second spawn point's yaw.
- Race difficulty tunables live in `ChopperRace`: `nStartTime = 20 - nComp * 4`, `nAddTime = 9 - nComp`.
- `VehicleCheck` is dead code as shipped in this file — a copter being destroyed mid-race does not appear
  to cancel the contract via this path.
