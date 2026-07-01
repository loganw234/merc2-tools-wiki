---
title: MrxTaskJobDestroySet
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskJob
tags: [mission, task]
---

# MrxTaskJobDestroySet

*Module: mrxtaskjobdestroyset.lua*

## Overview
The `MrxTaskJobDestroySet` module is a subclass of `MrxTaskJob` designed to handle mission tasks where the player must destroy a set of named targets. Each target can have different layers (pristine, staging, defense) that are managed during the task. The module also handles tracking the completion of these targets and updating the player's progress.

## Inheritance
- Inherits from: `MrxTaskJob`
- Imports: `MrxUtil`, `MrxStatsManager`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_oObjective`: The objective instance created for this task.
- `_bTrackOnActivate`: Whether to track targets on activation.
- `_bSkipInitialNotifications`: Whether to skip initial notifications.

## Functions
### `_AddTarget(self, ...)`
Adds a target to the task. If the first argument is a table, it configures the target with additional layers (staging, defense, pristine). Otherwise, it calls the base class's `_AddTarget` method.

### `_Go(self, fCallback, tCallbackArgs)`
Starts the task by excluding completed targets, adding the task to the PDA, and creating an objective instance (`MrxTaskObjectiveDestroy`). This objective manages the destruction of targets, updates layers as targets are destroyed, and tracks progress. It also handles callbacks for activation, part completion, completion, and cancellation.

### `_GetPerTargetLayerKeys(self)`
Returns a list of keys used to store per-target layer information (target, pristine, staging, defense).

### `_GetNearRadius(self)`
Returns the radius within which targets are considered "near" (150 units).

### `_GetFarRadius(self)`
Returns the radius beyond which targets are considered "far" (200 units).

### `_TargetNearby(self, uGuid)`
Handles nearby target logic. If the target is alive and has a near-VO sequence, it starts that sequence. Otherwise, it calls the base class's `_TargetNearby` method.

## Events
- Listens for custom events related to target completion and destruction within the objective instance.
- Responds to target activation by creating nearby events and starting VO sequences if applicable.

## Notes for modders
- Ensure that targets are correctly configured with their respective layers (staging, defense, pristine) when adding them to the task.
- Use `_Go` to start the task and provide any necessary callbacks for task completion or cancellation.
- Customize target behavior by modifying the objective instance's properties and methods.
- Be aware of the radius thresholds (`_GetNearRadius`, `_GetFarRadius`) that affect how targets are handled.