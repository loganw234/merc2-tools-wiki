---
title: MrxTaskObjectiveProtect
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, objective]
---

# MrxTaskObjectiveProtect

*Module: mrxtaskobjectiveprotect.lua*

## Overview
The `MrxTaskObjectiveProtect` module is a specific type of task objective that focuses on protecting targets. It inherits from the `MrxTaskObjective` class and adds functionality to handle target deaths, check if targets are valid, and provide various icons for different interfaces (radar, PDA, game space).

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tEvents.uDeathEvent`: Event handle for target death events.
- `_uTgtObjFilter`: Filter for target objects.

## Functions
### `Activated(self)`
Called when the task objective is activated. It sets up a persistent event listener for object deaths (`Event.ObjectDeath`) and registers it to call `_TargetDestroyed` when triggered.

### `_TargetDestroyed(self, uGuid, uCause, uKiller)`
Handles the event when a target object dies. Checks if the target should be removed based on configuration settings (e.g., `bHeroOnly`). If the target is valid, it removes the target and cancels any associated parts of the task.

### `_GetShortDescription()`
Returns a short description string for the objective, which is "[Generic.ObjectiveProtect]".

### `_IsValidTarget(uGuid)`
Checks if a given object GUID is a valid target. Returns true if the object is alive or matches any player character.

### `_GetTargetRadarIcon()`
Returns the radar icon for the target, which is "objective_defend".

### `GetInlineIcon(self)`
Returns an inline icon string based on the configuration of the objective. If the objective is optional, it returns "[objdefend2]"; otherwise, it returns "[objdefend]".

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA icon for the target based on whether the objective is optional. Returns "icon_defend_2_mc" if optional; otherwise, returns "icon_defend_1_mc".

### `_GetTargetGameSpaceIcon()`
Returns the game space icon for the target, which is "HUD_objective_defend".

## Events
- Listens for `Event.ObjectDeath` to call `_TargetDestroyed` when a target object dies.

## Notes for modders
- Ensure that `Activated` and other lifecycle functions are called appropriately to manage task objective behavior.
- Customize target validation by modifying the `_IsValidTarget` function.
- Adjust icons by changing the return values of `_GetTargetRadarIcon`, `GetInlineIcon`, `_GetTargetPdaIcon`, and `_GetTargetGameSpaceIcon`.
- Be aware that network synchronization may affect multiplayer behavior, especially if targets are player-controlled.