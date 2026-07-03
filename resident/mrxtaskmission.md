---
title: MrxTaskMission
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTask
tags: [mission, task]
verified: true
verified_note: read directly from source -- corrects Instance pattern (class-factory via MrxTask, not per-uGuid), removes a fabricated bNetSync reference, and clarifies IsContract/IsJob as override points confirmed used by MrxTaskContract/MrxTaskJob
---

# MrxTaskMission

*Module: mrxtaskmission.lua*

## Overview
`MrxTaskMission` extends [`MrxTask`](mrxtask) with mission-specific behavior: voice-over cue tracking,
PDA objective-display refreshing, and mission identity (which mission this is, its faction, its start
locations). [`MrxTaskContract`](mrxtaskcontract) and [`MrxTaskJob`](mrxtaskjob) both build directly on
this.

**Not the `Inheritable`/per-`uGuid` pattern** — inherits [`MrxTask`](mrxtask)'s class-factory/lineage-based
identity, not a world-object GUID.

## Inheritance
- Inherits from: [`MrxTask`](mrxtask)
- Imports: `MrxSubtitle`, `MrxVoSequence`, `WifMissionData`, `WifMissionFlow`, `MrxTaskObjective`, `MrxFactionManager`, `MrxRewardData`

## Instance pattern
Class-style object (inherited from [`MrxTask`](mrxtask)), not per-`uGuid`. Per-instance field: `_tVo` — a
list of `{vSpeaker, sCueHandle}` pairs for every voice-over cue played via `_PlayVo`, cancelled on cleanup.

`_knContract = 0` / `_knJob = 1` are **module-level constants**, not per-instance fields — they don't
appear to be referenced anywhere else in this file's visible logic; likely used by other mission-flow code
to classify a mission by type rather than something a mod would set directly.

## Functions

### `Activated(self)`
Calls `MrxTask.Activated(self)`, then `Graphics.InitTinyGeometry()` and initializes `self._tVo = {}`.

### `Cleanup(self)`
Removes this mission from its starter (`tConfig.oStarter:RemoveMission(self)`, if set), cancels every
pending voice-over cue in `_tVo` (`VO.Cancel`), clears pending subtitles
(`MrxSubtitle.ClearPending()`), then defers to `MrxTask.Cleanup(self)` for the rest (event/timer/child
cleanup).

### `_PlayVo(self, vSpeaker, sCueHandle, fCallback, tCallbackArgs)`
Plays a voice-over cue (`VO.Cue`) and tracks it in `_tVo` so `Cleanup` can cancel it if the mission ends
before the cue finishes.

### `RefreshPdaDisplay(self)`
Walks the entire task subtree looking for children that look like objectives (have
`GetDisplayDescription`/`GetDescription`/`RefreshPdaDisplay` and aren't completed/cancelled), collects
their description + inline icon, and pushes the list to `WifMissionFlow.AddPdaMissionDetails`. Recurses
into every descendant, not just direct children.

### `IsContract()` / `IsJob()`
**Override points, not fixed answers.** This base implementation returns `false` for both (mission types
are neither by default) — [`MrxTaskContract`](mrxtaskcontract) overrides `IsContract()` and
[`MrxTaskJob`](mrxtaskjob) overrides `IsJob()`, confirmed directly in both files. **Neither function
declares a `self` parameter here**, so calling them as `self:IsContract()` silently discards the passed
`self` (Lua doesn't error on unused extra arguments) — harmless in this base implementation since it
ignores its arguments anyway and just returns a constant, but worth knowing if you're tracing why `self`
never appears used in these two specific functions while it's used everywhere else in this file.

### `GetNumCompletions(self)`
`WifMissionFlow.GetKeyValue(self:GetMissionId()) or 0` — how many times this mission has been completed.

### `GetMissionId(self)`
Returns `self:GetParent():GetName()` — a mission's own ID is its parent task's name, not something stored
on the mission itself.

### `GetFactionId(self)` / `GetStartLocations(self)`
Read `sFactionId` from config, and delegate to `WifMissionFlow.GetMissionStartLocations` respectively.

## Events
No direct engine event subscriptions in this file — lifecycle is driven through the inherited
`MrxTask.Activate`/`Complete`/`Cancel` calls and config-driven callbacks (see [`MrxTask`](mrxtask)).

## Notes for modders
- **`IsContract`/`IsJob` are meant to be overridden**, not read as fixed facts about "mission-ness" — see
  above. If you're checking a task's type, prefer calling these methods (which correctly resolve to the
  actual subclass's override) over assuming every `MrxTaskMission` behaves like this base implementation.
- **`_PlayVo` self-tracks for cleanup** — prefer it over calling `VO.Cue` directly if you want the voice
  line properly cancelled should the mission end mid-cue.
- `RefreshPdaDisplay` recurses the *entire* subtree, not just immediate children — a deeply nested
  objective structure is all still reflected on the PDA in one call.
