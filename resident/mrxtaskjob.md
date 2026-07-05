---
title: MrxTaskJob
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskMission
tags: [mission, task]
verified: true
verified_note: 'deeper pass: re-confirmed all functions; documented _TargetComplete''s reward mechanics
  (grants <MissionId>_PerTarget key + tMilestones key matching, checkpoints/autosaves via
  WifMissionFlow/MrxPlayState), the weighted-random VO hat in _PlayRandomVoSequenceFromTable
  (knPriorityBounties), and the mpPlayerJoin secondary-nearby event; flagged the _GetTargetList operator-
  precedence quirk; cross-linked MrxLayerManager/MrxVoSequence/MrxRewardData/WifMissionFlow.'
---

# MrxTaskJob

*Module: mrxtaskjob.lua*

## Overview
The `MrxTaskJob` module is a base class for multi-target mission tasks, built on
[`MrxTaskMission`](mrxtaskmission) (itself built on [`MrxTask`](mrxtask)). It extends the functionality of `MrxTaskMission` to handle multiple targets, manage their completion states, and award rewards accordingly. This module also supports nearby-VO (voice-over) selection based on proximity. [`MrxTaskJobCollectType`](mrxtaskjobcollecttype)/[`MrxTaskJobDestroySet`](mrxtaskjobdestroyset)/[`MrxTaskJobDestroyType`](mrxtaskjobdestroytype)/[`MrxTaskJobVerifySet`](mrxtaskjobverifyset) all build directly on this.

## Inheritance
- Inherits from: [`MrxTaskMission`](mrxtaskmission)
- Imports: `MrxLayerManager`, `MrxPlayState`, `MrxRewardData`, `MrxVoSequence`, `WifMissionFlow`, `MrxFactionManager`

## Instance pattern
Class-style object, not per-`uGuid` — inherited from [`MrxTask`](mrxtask)'s factory pattern (identity by
name/lineage, not world-object GUID; see that page for the general mechanism). Key fields:
- `_tTargets`: A table of target data, including completion status and associated layers.
- `_nTargetsComplete`: The number of completed targets.
- `_bTrackOnActivate`: Whether to track targets on activation.
- `_bSkipInitialNotifications`: Whether to skip initial notifications for targets.
- `_tTargetGuidsToNames`: A mapping from GUIDs to target names.
- `_bNearVoInProgress`: Indicates whether a nearby VO is currently playing.
- `_tTargetCompleteVo`: Table of VO sequences for completed targets.
- `_tTargetNearbyVo`: Table of VO sequences for nearby targets.
- `_sDspShortDesc`: Short description of the mission.

## Functions
### `LoadAssets(self, tSaveData)`
Loads assets for the task based on saved data. If save data is provided, it restores the number of completed targets and their completion states. It also loads per-target layers if they are not already loaded.

### `Activated(self)`
Called when the task is activated. Initializes tracking settings and maps target names to GUIDs. Also sets up nearby VO events for player proximity.

### `_AddTarget(self, sTarget, sTargetLayer)`
Adds a new target with its associated layer to the task. If the target already exists, it logs a warning and overwrites it.

### `_SetTargetMilestoneKey(self, sTarget, sMilestoneKey)`
Sets the milestone key for a specific target.

### `_GetTargetData(self, vTarget)`
Retrieves data for a given target, which can be specified by name or GUID.

### `_GetTargetList(self)`
Returns a list of incomplete target names. (Source quirk: the filter is written
`if not tTargetData.bComplete == true` — which Lua parses as `(not tTargetData.bComplete) == true`, i.e.
"include when `bComplete` is falsy." Behaves correctly, just reads oddly; a decompiler-preserved precedence
artifact.)

### `_GetPartsCompletedList(self)`
Returns a list of completed targets.

### `_TargetComplete(self, uGuid)`
The shared per-target completion path all job subclasses funnel their `fOnPartComplete` into. Increments
`_nTargetsComplete`, then:
- Grants the reward key `<MissionId>_PerTarget` via [`MrxRewardData.GrantRewardKey`](mrxrewarddata) (a
  per-kill/collect reward hook keyed off the mission ID).
- Marks the target's data `bComplete`, removes its `sTargetLayer` ([`MrxLayerManager`](mrxlayermanager)), and
  if it has an `sMilestoneKey`, awards it via [`WifMissionFlow.AwardKey`](mrxmissionflow).
- Matches `tConfig.tMilestones` by count: any milestone whose `nMilestone == _nTargetsComplete` awards its
  `sKey`.
- Runs a local `_Presentation()` that checkpoints (`MrxPlayState.GetCurrentMission():_Checkpoint`) and either
  refreshes the flow (if keys were awarded but the objective quota isn't yet met) or autosaves — gated by
  `_GetAutosaveMode()` and whether keys were awarded. If a `_tTargetCompleteVo` is set, the presentation runs
  *after* the completion VO finishes; otherwise immediately.

### `_ExcludeCompletedTargets(self)`
Excludes completed targets from further processing (currently a no-op).

### `_SetTargetCompleteVo(self, tVo)`
Sets the VO sequence for target completion.

### `_SetTargetNearbyVo(self, tVo)`
Sets the VO sequence for when a target is nearby.

### `_SetShortDescription(self, sDspShortDesc)`
Sets the short description of the mission.

### `EnableTracking(self, bEnable)`
Enables or disables tracking for the task's objective.

### `_AddToPda(self)`
Adds the task to the player's PDA (currently a no-op).

### `CreateChild(self, tConfig)`
Creates a child task with optional configuration settings.

### `_GetMissionType()`
Returns the mission type identifier for jobs.

### `IsJob()`
Indicates whether the task is a job.

### `_GetPerTargetLayerKeys()`
Returns the keys for per-target layers.

### `_GetNearRadius()`
Returns the near radius for proximity checks (default 30).

### `_GetFarRadius()`
Returns the far radius for proximity checks (default 60).

### `_GetAutosaveMode()`
Indicates whether autosave is enabled after every target completion (default true).

### `_GetNearbyVoPlaybackMode()`
Indicates whether nearby VO playback mode is enabled (default false).

### `SaveInstance(self)`
Saves the current state of the task, including completed targets and their states.

### `_RemoveSecondaryNearbyEvent(self)`
Removes the secondary nearby event if it exists.

### `_CreateSecondaryNearbyEvent(self)`
Creates a secondary nearby event for the player's secondary character.

### `_PlayerJoin(self)`
Handles player join events to manage nearby events accordingly.

### `_CreateNearbyEvent(self)`
Sets up nearby and faraway events for target proximity checks.

### `_NearbyRadiusEntry(self, tGuids)`
Handles entries for objects within the near radius, playing nearby VO sequences if applicable.

### `_TargetNearby(self, uGuid)`
Plays a nearby VO sequence for a given object if conditions are met.

### `_CreateFarawayEvent(self, uGuid)`
Creates an event for objects that move beyond the far radius.

### `_NearbyRadiusExit(self, tGuids)`
Handles exits from the near radius, updating proximity filters and playing faraway VO sequences if applicable.

### `_TargetFaraway(self, uGuid)`
Handles objects moving beyond the far radius (currently a no-op).

### `_PlayRandomVoSequenceFromTable(tVo, nRangeFilter, fCallback, tCallbackArgs)`
Weighted-random "hat" VO picker. Each `tVo` entry may carry a `tRange` (an interval spec — supports 1, 2, or
4-element forms with `"["`/`"]"` inclusivity markers) filtered against `nRangeFilter` (e.g. the current
completed-target count), and an `nWeight` (default 1) controlling how many times it's entered into the draw.
A winner is chosen via [`MrxUtil.GetRandomTableElement`](mrxutil); if `fCallback` is given it's appended to
the sequence, and the whole thing is played via [`MrxVoSequence.Start`](mrxvosequence) at
`MrxVoSequence.knPriorityBounties`. This is a **module-level function** (no `self`), called bare.

### `_NearVoComplete(self)`
Marks the end of a nearby VO sequence.

## Events
- Listens for `Event.ObjectProximity` to handle nearby and faraway events.
- Listens for `Event.ScriptEvent` with `mpPlayerJoin` to manage secondary nearby events when players join or leave.

## Notes for modders
- Ensure that targets are correctly added using `_AddTarget` and milestone keys are set using `_SetTargetMilestoneKey`.
- Customize VO sequences by setting `_tTargetCompleteVo` and `_tTargetNearbyVo`.
- **`_GetNearRadius`/`_GetFarRadius`/`_GetAutosaveMode`/`_GetNearbyVoPlaybackMode` are override points, not
  setters** — each takes no arguments and just returns a fixed value (`30`/`60`/`true`/`false`
  respectively in this base class). A subclass changes proximity/autosave/VO behavior by redefining the
  function to return something else, not by calling it with a new value.
- `_GetMissionType()`/`IsJob()` are the same override-point pattern documented on
  [`MrxTaskMission`](mrxtaskmission) for `IsContract`/`IsJob` — this file's `IsJob()` is the confirmed
  override that flips it to `true` for every job-type mission.