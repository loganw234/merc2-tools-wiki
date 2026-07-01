---
title: MrxTaskObjectiveDestroy
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, objective, destroy]
---

# MrxTaskObjectiveDestroy

*Module: mrxtaskobjectivedestroy.lua*

## Overview
The `MrxTaskObjectiveDestroy` module is a specific type of task objective that requires the player to destroy certain game objects. It inherits from `MrxTaskObjective` and adds functionality to handle object destruction events, manage target lists, and provide appropriate icons for different UI elements.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tEvents`: A table to store event handles.
- `_uTgtObjFilter`: A filter for target objects.

## Functions
### `Activated(self)`
Called when the task objective is activated. It sets up persistent events to listen for object deaths and client kills, and registers them in the `_tEvents` table. It also asserts that the death event handle is valid.

### `_TargetDestroyed(self, uGuid, uCause, uKiller)`
A private function called when a target object dies. It checks if the objective requires hero-only destruction and processes the destruction accordingly by removing the target and completing the part of the task.

### `_GetShortDescription()`
Returns a short description string for the task objective.

### `GetInlineIcon(self)`
Returns an inline icon based on whether the objective is optional or not.

### `_GetTargetRadarIcon()`
Returns the radar icon for the target object.

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA (Personal Digital Assistant) icon for the target object, depending on whether it's optional or not.

### `_GetTargetGameSpaceIcon()`
Returns the game space icon for the target object.

### `_IsValidTarget(uGuid)`
A private function that checks if a given GUID is a valid target. It verifies if the GUID corresponds to any player character or an alive object.

## Events
- Listens for `Event.ObjectDeath` to call `_TargetDestroyed` when a target object dies.
- Listens for `Event.ScriptEvent` with the event name "ClientKill" to handle client kills and remove targets accordingly.

## Notes for modders
- Ensure that `Activated` is called appropriately to set up event listeners.
- Customize the behavior by modifying the `_uTgtObjFilter` to target specific objects.
- Use `_GetShortDescription`, `GetInlineIcon`, `_GetTargetRadarIcon`, `_GetTargetPdaIcon`, and `_GetTargetGameSpaceIcon` to provide appropriate UI feedback for the task objective.
- Be aware of the hero-only destruction requirement, which may affect how the task is completed.