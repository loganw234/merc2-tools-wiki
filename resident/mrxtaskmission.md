---
title: MrxTaskMission
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTask
tags: [mission, task]
---

# MrxTaskMission

*Module: mrxtaskmission.lua*

## Overview
The `MrxTaskMission` module is a base class for mission tasks in the game. It extends the functionality of `MrxTask` by adding specific methods and properties related to missions, such as handling voice-over cues, refreshing PDA displays, and managing mission objectives.

## Inheritance
- Inherits from: `MrxTask`
- Imports: `MrxSubtitle`, `MrxVoSequence`, `WifMissionData`, `WifMissionFlow`, `MrxTaskObjective`, `MrxFactionManager`, `MrxRewardData`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tVo`: A table to store voice-over cues.
- `_knContract` and `_knJob`: Constants for mission types.

## Functions
### `Activated(self)`
Called when the object instance is activated. It calls the base class's `Activated` method, initializes tiny geometry, and sets up a table for voice-over cues.

### `Cleanup(self)`
Cleans up resources associated with the mission task. It removes the mission from the starter if present, cancels any pending voice-over cues, clears pending subtitles, and calls the base class's `Cleanup`.

### `_PlayVo(self, vSpeaker, sCueHandle, fCallback, tCallbackArgs)`
Plays a voice-over cue for the mission. It inserts the cue into the `_tVo` table and returns whether the cue was successfully played.

### `RefreshPdaDisplay(self)`
Refreshes the PDA display with the current mission details. It collects objective descriptions and icons from child objects and adds them to the PDA using `WifMissionFlow.AddPdaMissionDetails`.

### `IsContract()`
Returns false, indicating that this is not a contract type of mission.

### `IsJob()`
Returns false, indicating that this is not a job type of mission.

### `GetNumCompletions(self)`
Retrieves the number of completions for the mission using `WifMissionFlow.GetKeyValue`.

### `GetMissionId(self)`
Returns the mission ID by getting the name of the parent object.

### `GetFactionId(self)`
Returns the faction ID from the mission configuration.

### `GetStartLocations(self)`
Retrieves the start locations for the mission using `WifMissionFlow.GetMissionStartLocations`.

## Events
- Listens for custom events to handle voice-over cues and PDA display refreshes.

## Notes for modders
- Ensure that `Activated` and `Cleanup` are called appropriately to manage mission lifecycle.
- Use `_PlayVo` to play voice-over cues for the mission.
- Customize mission properties by setting fields like `_knContract` and `_knJob`.
- Be aware of network synchronization (`bNetSync`) may affect multiplayer behavior.