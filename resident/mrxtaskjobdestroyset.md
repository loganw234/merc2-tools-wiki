---
title: MrxTaskJobDestroySet
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskJob
tags: [mission, task]
verified: true
verified_note: 'deeper pass: confirmed all functions; documented the per-target 4-layer swap on kill
  (pristine/staging/defense removed, destroyed added), the MrxTaskObjectiveDestroy child config
  (icon_destroy_3_mc PDA icon, quota = target count), the 150/200 near/far radii, and MrxStatsManager.JobDestroyPart;
  cross-linked MrxTaskObjectiveDestroy/MrxLayerManager/MrxVoSequence; corrected Events section.'
---

# MrxTaskJobDestroySet

*Module: mrxtaskjobdestroyset.lua*

## Overview
The `MrxTaskJobDestroySet` module is a subclass of `MrxTaskJob` designed to handle mission tasks where the player must destroy a set of named targets. Each target can have different layers (pristine, staging, defense) that are managed during the task. The module also handles tracking the completion of these targets and updating the player's progress.

## Inheritance
- Inherits from: `MrxTaskJob`
- Imports: `MrxUtil`, `MrxStatsManager`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskJob`](mrxtaskjob)'s class-factory pattern** (itself inherited from
[`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask); see that page for the general mechanism),
identified by name/lineage rather than a world-object GUID. Key fields:
- `_oObjective`: The objective instance created for this task.
- `_bTrackOnActivate`: Whether to track targets on activation.
- `_bSkipInitialNotifications`: Whether to skip initial notifications.

## Functions
### `_AddTarget(self, ...)`
Adds a target to the task. If the first argument is a table, it configures the target with additional layers (staging, defense, pristine). Otherwise, it calls the base class's `_AddTarget` method.

### `_Go(self, fCallback, tCallbackArgs)`
Creates the child [`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy) (named `"DestroySet"`) covering the
named target list: `vTgtInclude = self:_GetTargetList()`, `vTgtExclude` = already-completed parts,
`nQuota` = remaining targets + completed count, `bDspBounty = true`, PDA icon `"icon_destroy_3_mc"`. On
`fOnActivate` it arms proximity/VO tracking via the inherited `_CreateNearbyEvent` then runs `fCallback`. Its
`fOnPartComplete(uGuid)` does the **per-target layer swap** through [`MrxLayerManager`](mrxlayermanager):
removes that target's `sPristineLayer`/`sStagingLayer`/`sDefenseLayer` and adds its `sDestroyedLayer` (each
guarded), calls the inherited `_TargetComplete`, then
[`MrxStatsManager.JobDestroyPart`](mrxstatsmanager)`(self:GetFactionId())`. `fOnComplete`/`fOnCancel` route to
`self:Complete()`/`self:Cancel()`.

### `_GetPerTargetLayerKeys(self)`
Returns a list of keys used to store per-target layer information (target, pristine, staging, defense).

### `_GetNearRadius(self)`
Returns the radius within which targets are considered "near" (150 units).

### `_GetFarRadius(self)`
Returns the radius beyond which targets are considered "far" (200 units).

### `_TargetNearby(self, uGuid)`
Overrides the base: if the target is alive **and** has a per-target `vNearVoSequence`, plays it directly via
[`MrxVoSequence.Start`](mrxvosequence) at `knPriorityBounties`. Otherwise falls back to
`MrxTaskJob._TargetNearby` (the shared nearby-VO-hat behavior). Note it only acts on a live target — a
destroyed target near the player produces no VO.

## Events
No `Event.*` calls of its own. The proximity events are created by the inherited
[`MrxTaskJob._CreateNearbyEvent`](mrxtaskjob) (fired from this subclass's `fOnActivate`) using this class's
`150`/`200` near/far radii. `fOnActivate`/`fOnPartComplete`/`fOnComplete`/`fOnCancel` are config callbacks on
the child [`MrxTaskObjectiveDestroy`](mrxtaskobjectivedestroy), invoked directly — not subscriptions.

## Notes for modders
- **Per-target config via the table form of `_AddTarget`:** pass `{sTarget=, sPristineLayer=, sStagingLayer=,
  sDefenseLayer=, sDestroyedLayer=, sMilestoneKey=}`. The first three layers are removed and `sDestroyedLayer`
  is added when that target dies — the standard "building intact → rubble" swap. `sMilestoneKey` awards a
  mission-flow key on that specific kill.
- **Proximity radii are `150`/`200`** (near/far) here, vs. the `30`/`60` base — destroy targets are large
  (buildings/vehicles), so the "you're near an objective" trigger fires from much further out. Override
  `_GetNearRadius`/`_GetFarRadius` to change them (they're no-arg return-a-constant override points).
- `nQuota` is derived automatically (`#targets + completed`); you set the target set, not the count.