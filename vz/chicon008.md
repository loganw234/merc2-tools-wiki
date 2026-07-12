---
title: ChiCon008
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 4
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# ChiCon008

## Overview
A China minor/side contract: spawn a locked "ZTZ98" tank and race it through roughly 20 checkpoints,
optionally destroying 19 roadside barrels along the way for bonus time. Shows a one-shot tutorial message
on start. Like [AllCon008](allcon008)'s helicopter race, replaying it tightens the time limit and shrinks
the per-barrel time bonus (`self:GetNumCompletions()`); the tank dying cancels the contract.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxTaskObjectiveDeliver`, `MrxLayerManager`, `MrxTimer`, `MrxSubtitle`, `MrxAchievements`,
  `MrxTutorialManager`, `MrxFactionManager`, `MrxMusic`

`MrxTaskObjectiveDeliver`, `MrxTimer`, and `MrxFactionManager` have no visible call site in this file —
this contract only creates `MrxTaskObjectiveDestroy`/`MrxTaskRace` children and never touches a delivery
objective, a `MrxTimer` countdown, or faction relations directly.

## Instance pattern
A native `MrxTaskContract` subclass. Module-level globals: `chineseRaceTank` (the spawned tank),
`nTimeLimit`/`nTimeToAdd` (difficulty scaling), and `self.oTankRaceObjective` (the race child task).

## Functions
### `Activated(self)`
Calls the base `MrxTaskContract.Activated`, removes the pre-mission layer, spawns the locked tank, arms
special-mission-music on driver entry, resolves the time limit/bonus from prior completions, starts
`StartRace`, arms a tank-death cancel trigger, and shows the race tutorial.

### `RaceTutorial(self)`
Shows the `[ChiCon008.Terms.Tutorial]` tutorial message via `MrxTutorialManager`.

### `StartRace(self, tVehicle, nTime, nAddTime)`
Plays the opening VO, creates the optional `MrxTaskObjectiveDestroy` child for the 19 barrels (wiring
`ObjectDestroyed` per barrel), and creates the `MrxTaskObjectiveRace` (`MrxTaskRace`) child over the ~20
named checkpoints; on race completion, grants "Highway to Hell" achievement progress and completes the
contract.

### `ObjectDestroyed(self)`
Hides the tutorial message, flashes a green "+time" message in HUD slot 2, and adds the bonus time to the
race timer.

### `FionaVoChiCon008(self)`
Plays the opening VO and arms two proximity-triggered VO lines at specific checkpoints.

### `VehicleUnentered(self)`
Sets a cancel message and cancels the contract.

### `RaceFailed(self)`
Sets a different cancel message and cancels the contract.

### `Cleanup(self)`
Clears the HUD objective-tray slots, removes the spawned tank, stops the special music, restores the
pre-mission layer, and calls the base `MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectInSeat` — the player entering/exiting the tank's driver seat starts special mission music.
- `Event.ObjectDeath` — the tank dying cancels the contract.
- `Event.ObjectProximity` — two checkpoint-proximity triggers play VO lines partway through the race.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- Time-limit/bonus tunables scale down with `self:GetNumCompletions()`: 60s/15s bonus on first play,
  50s/10s on the second, 40s/10s from the third onward.
- The barrel-destroy bonus completion VO reuses the key `Fiona-In-Mission-Contract-Pmc01-10` — the same
  generic "you won the race" line also used in [ChiCon009](chicon009)'s ambulance-delivery completion,
  suggesting it's a shared cue reused across race/delivery-style missions regardless of faction rather
  than a copy-paste mistake.
- Several imports (`MrxTaskObjectiveDeliver`, `MrxTimer`, `MrxFactionManager`) are unused in this
  particular file.
