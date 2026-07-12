---
title: GurJob020
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 11
inherits: MrxTaskJobDestroySet
tags: [job]
verified: false
---

# GurJob020

## Overview
The largest Guerilla side job in this batch: a destroy-set covering 13 buildings across two location
series (`GurJob007_Target01`–`03` and `GurJob011a`–`j`_Target), with `DangerousBuilding`-tuned AI spawners
armed on each one and a VO table that scales its line selection by how many targets remain, not just a flat
weight.

## Inheritance
- Inherits from: [`MrxTaskJobDestroySet`](../resident/mrxtaskjobdestroyset) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `DangerousBuilding`

## Instance pattern
A native task-framework subclass. Module-level tables: `_tTargetNearbyVo` (5 lines), `_tTargetCompleteVo`
(8 entries, several using `tRange` — e.g. `{"[", 1, 11, "]"}` or a bare `{13}` — to gate which line plays
by remaining-target count rather than a flat weight), and `_tBuildings` (the 10 `GurJob011x_Target` names).

## Functions
### `LoadAssets(self, tSaveData)`
Registers all 13 targets via `self:_AddTarget{...}` — the three `GurJob007_TargetNN` buildings first
(each with pristine/defense/destroyed layers), then the ten `_tBuildings` entries — then calls
`MrxTaskJobDestroySet.LoadAssets(self, tSaveData)`.

### `Activated(self)` / `ActivateBuilding(self, sBuildingName)`
`Activated` calls the base `Activated`, sets both VO tables, then arms spawners on all 13 targets: the
first three via plain `ActivateBuilding(self, "...")` calls and the remaining ten via a
`for ... do self:ActivateBuilding(sTargetName) end` loop — cosmetically inconsistent call syntax
(`self` passed explicitly vs. via `:`), but functionally identical since `ActivateBuilding`'s first
parameter is `self` either way. Finishes with `_Go()`. `ActivateBuilding` itself turns on
`DangerousBuilding` for the given target and tunes its `"Ground"`-group spawner to the VZ ground spawn
list.

## Events
None registered directly in this file — target discovery/completion events live in the native
`MrxTaskJobDestroySet` base; only the `DangerousBuilding`/`Ai.TweakAttachedSpawners` calls in
`ActivateBuilding` are this file's own doing.

## Notes for modders
This is the native `MrxTaskJobDestroySet`/`WifMissionData` job system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- The `tRange`-gated VO table (`_tTargetCompleteVo`) is a richer pattern than the flat-weighted tables seen
  elsewhere (e.g. [GurJob001](gurjob001)) — worth copying if you want completion barks that change as a
  destroy-set job nears its end rather than staying uniformly random throughout.
