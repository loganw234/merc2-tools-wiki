---
title: MrxTaskJobVerifySet
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskJob
tags: [mission, task]
---

# MrxTaskJobVerifySet

*Module: mrxtaskjobverifyset.lua*

## Overview
The `MrxTaskJobVerifySet` module is a subclass of `MrxTaskJob` designed to handle mission tasks where players need to verify or capture specific high-value targets (HVTs). It manages the lifecycle of these verification tasks, including adding targets, handling events, and updating player notifications.

## Inheritance
- Inherits from: `MrxTaskJob`
- Imports: `MrxFactionManager`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_oObjective`: The objective associated with the verification task.
- `_sFactionId`: The faction ID for the task.
- `_bPlayedVerificationVO`: A flag indicating whether the verification voice-over has been played.

## Functions
### `_AddTarget(self, ...)`
Adds a target to the verification set. If the first argument is a table, it configures the target with various layers and properties. Otherwise, it calls the base class's `_AddTarget` method.

### `_Go(self, fCallback, tCallbackArgs)`
Starts the verification task by excluding completed targets, adding them to the PDA, and creating an objective module (`MrxTaskObjectiveVerify`). It sets up callbacks for activation, part completion, completion, and cancellation of the objective. It also handles fanfare events and updates cash rewards based on whether targets are killed.

### `_SetFactionId(self, sFactionId)`
Sets the faction ID for the task.

### `_GetPerTargetLayerKeys()`
Returns a list of layer keys associated with each target.

### `_GetNearRadius()`
Returns the radius within which nearby events are triggered (150 units).

### `_GetFarRadius()`
Returns the radius beyond which far events are triggered (200 units).

### `_GetNearbyVoPlaybackMode()`
Returns a boolean indicating whether nearby voice-over playback is enabled.

### `_PlayVerificationVO(self)`
Plays the verification voice-over if it hasn't been played yet.

### `_NearVoComplete(self)`
Handles the completion of the nearby voice-over by scheduling the verification voice-over to play after a delay.

### `_TargetNearby(self, uGuid)`
Handles events for targets that are nearby. If the target has a near VO sequence, it plays it; otherwise, it calls the base class's method.

### `LoadAssets(self, tSaveData)`
Loads saved data, including whether the verification voice-over has been played.

### `SaveInstance(self)`
Saves the current state of the instance, including whether the verification voice-over has been played.

## Events
- Listens for custom events to manage target nearby and completion.
- Triggers fanfare events when targets are captured or killed.

## Notes for modders
- Ensure that `_AddTarget` is called with appropriate arguments to configure targets correctly.
- Use `_SetFactionId` to set the faction ID for the task.
- Customize voice-over sequences by modifying `vNearVoSequence` in target configurations.
- Be aware of network synchronization and ensure that events are handled appropriately on both client and server sides.