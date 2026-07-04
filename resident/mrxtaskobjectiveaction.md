---
title: MrxTaskObjectiveAction
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, objective]
verified: true
verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTaskObjective](mrxtaskobjective) for the general mechanism.
---

# MrxTaskObjectiveAction

*Module: mrxtaskobjectiveaction.lua*

## Overview
The `MrxTaskObjectiveAction` module is a specialized task objective that involves player interaction with specific game objects. It sets up context actions for these targets and tracks their destruction or successful interaction to mark the task as complete or canceled.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `MrxUtil`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTaskObjective`](mrxtaskobjective)'s class-factory pattern** (itself
inherited from [`MrxTask`](mrxtask); see that page for the general mechanism), identified by name/lineage
rather than a world-object GUID. Key fields:
- `_tEvents`: Stores event handles for action and death events.
- `_uTgtObjFilter`: Filter used to identify target objects.

## Functions
### `Activated(self)`
Called when the task objective is activated. It initializes the base class, prepares target objects by setting context actions, and sets up persistent events to handle target interactions (`_TargetActioned`) and destruction (`_TargetDestroyed`).

### `_PrepTargets(self)`
Prepares the target objects for interaction by adding context actions to them using `Pg.AddContextAction`. It retrieves the configuration for the action label and applies it to each target.

### `_TargetActioned(self, uActionerGuid, uActioneeGuid)`
Handles the event when a target object is interacted with. It removes the context action from the target, updates the task state by removing the target if necessary, and marks the part of the task as complete for both the actor and the target.

### `_TargetDestroyed(self, uGuid)`
Handles the event when a target object is destroyed. It removes the context action from the target, updates the task state by removing the target if necessary, and cancels the part of the task.

### `Cleanup(self)`
Cleans up any remaining context actions on the target objects and calls the base class's cleanup method to ensure proper resource management.

### `_GetShortDescription()`
Returns a short description for the task objective action, which is used in UI displays.

### `_GetTargetRadarIcon()`
Returns the radar icon associated with the target object, used for visual representation on the radar.

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA (Personal Digital Assistant) icon associated with the target object. The icon changes based on whether the target is optional or mandatory.

### `_GetTargetGameSpaceIcon()`
Returns the game space icon associated with the target object, used for visual representation in the game world.

### `_IsValidTarget(uGuid)`
Checks if a given GUID represents a valid target object. It considers any player character and alive objects as valid targets.

## Events
- Listens for `Event.ContextAction` to call `_TargetActioned` when a target is interacted with.
- Listens for `Event.ObjectDeath` to call `_TargetDestroyed` when a target is destroyed.

## Notes for modders
- Ensure that the task objective is properly activated and cleaned up to manage context actions and event subscriptions.
- Customize the action label and icons by modifying the configuration fields in the task setup.
- Be aware of the validity checks for targets to ensure proper task progression.