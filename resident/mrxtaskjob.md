---
title: MrxTaskJob
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskMission
tags: [mission, task]
verified: true
verified_note: read directly from source -- corrects Instance pattern (class-factory via MrxTask/MrxTaskMission, not per-uGuid); rest of this page was already largely accurate
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
Returns a list of incomplete targets.

### `_GetPartsCompletedList(self)`
Returns a list of completed targets.

### `_TargetComplete(self, uGuid)`
Handles the completion of a target. It increments the count of completed targets, awards relevant milestone keys, and triggers autosave if configured. It also plays nearby VO sequences if applicable.

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
Plays a random VO sequence from a table based on range filters and weights. It also handles callbacks after playback.

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