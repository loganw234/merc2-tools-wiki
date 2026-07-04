---
title: MrxTaskJobDestroyType
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskJob
tags: [task, destroy]
verified: true
verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTaskJob](mrxtaskjob) for the general mechanism.
---

# MrxTaskJobDestroyType

*Module: mrxtaskjobdestroytype.lua*

## Overview
The `MrxTaskJobDestroyType` module is a subclass of `MrxTaskJob` designed to handle tasks where the player must destroy objects filtered by a specific label. It manages the destruction quota, message display settings, and other related task properties.

## Inheritance
- Inherits from: `MrxTaskJob`
- Imports: `none`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskJob`](mrxtaskjob)'s class-factory pattern** (itself inherited from
[`MrxTaskMission`](mrxtaskmission)/[`MrxTask`](mrxtask); see that page for the general mechanism),
identified by name/lineage rather than a world-object GUID. Key fields:
- `_sLabelFilter`: The label filter for the objects to be destroyed.
- `_nQuota`: The quota of objects that need to be destroyed.
- `_bDspMsg`: A boolean indicating whether messages should be displayed.
- `_bHeroOnly`: A boolean indicating if the task is only available to heroes.
- `_bSkipInitialNotifications`: A boolean indicating whether initial notifications should be skipped.
- `_oObjective`: The objective module instance for this task.

## Functions
### `_SetLabelFilter(self, sLabelFilter)`
Sets the label filter for the objects to be destroyed. This function is used to specify which objects should be targeted by the task.

### `_SetQuota(self, nQuota)`
Sets the quota of objects that need to be destroyed. This function determines how many objects must be destroyed to complete the task.

### `_SetMessageDisplay(self, bDspMsg)`
Sets whether messages should be displayed for this task. This function controls the visibility of in-game messages related to the task.

### `_Go(self, fCallback, tCallbackArgs)`
Starts the task by excluding completed targets, adding it to the PDA, and creating a child objective module (`MrxTaskObjectiveDestroy`). It sets up various properties and callbacks for the objective, including activation, part completion, completion, and cancellation events.

### `_SetHeroOnly(self, bHeroOnly)`
Sets whether the task is only available to heroes. This function restricts the availability of the task based on player character type.

### `_GetAutosaveMode()`
Returns `false`, indicating that this task does not support autosaving. This means the task state will not be automatically saved and loaded during gameplay.

## Events
- Listens for custom events through callbacks within the `_Go` function to handle activation, part completion, completion, and cancellation of the objective.

## Notes for modders
- Ensure that `_SetLabelFilter`, `_SetQuota`, and `_SetMessageDisplay` are called appropriately to configure the task properties.
- Use `_SetHeroOnly` to restrict the task availability based on player character type.
- Be aware that this task does not support autosaving, so ensure proper handling of task state persistence if needed.