---
title: GurCon005
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 4
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# GurCon005

## Overview
A short Guerilla minor contract: assassinate four named Universal Petroleum targets scattered around a
single location. No travel, escort, or defense phase — just one `MrxTaskObjectiveDestroy` with milestone VO
barks as targets fall. The simplest full story contract in this batch.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxLayerManager`, `MrxUtil`, `MrxSupportData`, `MrxFactionManager`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` pattern.
The only module-level state is `TargetsKilled`, a counter reset in `Activated` and incremented in
`TargetKilledVO`. Unlike most other contracts in this batch, this file defines no `Cleanup` override at
all — whatever `MrxTaskContract.Cleanup` does by default is all that runs.

## Functions
### `LoadAssets(self, tSaveData)`
Adds four state layers (`VZ_state_gurcon005*`) via `MrxLayerManager.Add`.

### `Activated(self)`
Calls `MrxTaskContract.Activated(self)`, resets `TargetsKilled`, and creates the single
`MrxTaskObjectiveDestroy` covering all four `GurCon005_Target0N` objects, with per-part completion routed
to `TargetKilledVO`, full completion to `self.Complete`, and cancel to `self.Cancel`.

### `TargetKilledVO(self)`
Plays one of four milestone VO lines keyed by how many targets have died so far (0–3), then increments
`TargetsKilled`.

### `Reported(self)`
Sets a bare global `bNoReport = false`. Nothing else in this file reads `bNoReport`, so its effect (if any)
is consumed elsewhere — possibly by the native `MrxTaskContract` base itself as a "player called this
target in" hook. Not enough visible in this file alone to say more.

## Events
None registered directly by name in this file beyond the objective's own built-in completion callbacks
(`tOnPartComplete`/`tOnComplete`/`tOnCancel`), which are `MrxTaskObjectiveDestroy` fields, not raw
`Event.Create` calls.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- Good minimal-example file if you want to see the smallest possible "real" (non-outpost, non-job) contract
  shape: `LoadAssets` + `Activated` + one objective + one VO callback.
