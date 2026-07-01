---
title: MrxTaskObjectiveCaptureOutpost
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, outpost]
---

# MrxTaskObjectiveCaptureOutpost

*Module: mrxtaskobjectivecaptureoutpost.lua*

## Overview
The `MrxTaskObjectiveCaptureOutpost` module is a specific type of task objective that focuses on capturing or destroying outposts. It inherits from the `MrxTaskObjective` module and integrates with the `MrxOutpostManager` to handle outpost status changes.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `MrxOutpostManager`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tConfig`: Configuration settings for the task objective.
- `_HandleOutpostStatusChange`: Internal function to handle changes in outpost status.

## Functions
### `Activated(self)`
Called when the task objective instance is activated. It logs a debug message and sets up an event to call `Awake` once the object leaves hibernation.

### `Cleanup(self)`
Cleans up any resources associated with the task objective, such as unregistering outpost events and calling the base class's `Cleanup`.

### `_HandleOutpostStatusChange(self, uOutpost, nStatus)`
Handles changes in outpost status. If the outpost is captured (`knStatusCaptured`), it removes the target and completes the part of the task. If the outpost is destroyed (`knStatusDestroyed`), it removes the target and cancels the part of the task.

### `_GetShortDescription()`
Returns a short description for the task objective, which is "[Generic.ObjectiveOutpost]".

### `GetInlineIcon(self)`
Returns an inline icon based on whether the outpost capture is optional. If optional, returns `[objoutpost2]`; otherwise, returns `[objoutpost]`.

### `_GetTargetRadarIcon()`
Returns the radar icon for the task objective target, which is `"objective_outpost"`.

### `_GetTargetPdaIcon(bOptional)`
Returns the PDA (Personal Digital Assistant) icon for the task objective target based on whether it's optional. If optional, returns `"icon_outpost_2_mc"`; otherwise, returns `"icon_outpost_1_mc"`.

### `_GetTargetGameSpaceIcon()`
Returns the game space icon for the task objective target, which is `"HUD_objective_outpost"`.

## Events
- Listens for outpost status changes to handle capturing or destroying outposts.

## Notes for modders
- Ensure that `Activated` and `Cleanup` are called appropriately to manage the lifecycle of the task objective.
- Customize outpost capture behavior by modifying the `_HandleOutpostStatusChange` function.
- Use `GetInlineIcon`, `_GetTargetRadarIcon`, `_GetTargetPdaIcon`, and `_GetTargetGameSpaceIcon` to customize the visual representation of the task objective in different contexts.