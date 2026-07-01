---
title: MrxTaskObjectiveRelease
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjectiveAction
tags: [task, objective, release]
---

# MrxTaskObjectiveRelease

*Module: mrxtaskobjectiverelease.lua*

## Overview
The `MrxTaskObjectiveRelease` module is a specific type of task objective that deals with the release of prisoners or controlled entities. It inherits from `MrxTaskObjectiveAction` and provides functionality to manage nearby targets, set their states, and adjust AI relations based on configuration settings.

## Inheritance
- Inherits from: `MrxTaskObjectiveAction`
- Imports: `MrxUtil`, `MrxFactionManager`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_uFarTgtFilter`: A filter for nearby targets.
- `_knTgtNearbyRadius`: The radius within which targets are considered "nearby".

## Functions
### `Activated(self)`
Called when the objective is activated. It calls the base class's `Activated` method and sets up a nearby event to monitor targets.

### `_PrepTargets(self)`
A placeholder function that currently does nothing.

### `_TargetActioned(self, uActionerGuid, uActioneeGuid)`
Handles the action taken on a target. It calls the base class's `_TargetActioned` method, sets the target's state to "Upright", and adjusts AI relations based on configuration settings.

### `_GetShortDescription()`
Returns a short description of the objective, which is "[Generic.ObjectiveRelease]".

### `_CreateNearbyEvent(self)`
Creates an event that listens for nearby targets within a specified radius. It sets up a filter to exclude the player character and creates a persistent event to monitor proximity.

### `_TargetNearby(self, tGuids)`
Handles the detection of nearby targets. It adjusts AI relations, sets the target's state to "Subdued", adds a context action for releasing the prisoner, and removes the target from the nearby filter while setting up a faraway event.

### `_CreateFarawayEvent(self, uGuid)`
Creates an event that listens for targets moving beyond the specified radius. It adds the target back to the nearby filter when they move away.

### `_TargetFaraway(self, uGuid)`
Handles the detection of targets moving beyond the specified radius by adding them back to the nearby filter.

## Events
- Listens for `Event.ObjectProximity` to call `_TargetNearby` and `_TargetFaraway` based on target proximity.
- Listens for custom events related to target actions and proximity.

## Notes for modders
- Ensure that `Activated` is called appropriately to set up nearby event monitoring.
- Customize AI relations and target states by adjusting configuration settings.
- Be aware of the radius (`_knTgtNearbyRadius`) used for detecting nearby targets.
- Use `_TargetActioned` to handle specific actions taken on targets, such as releasing prisoners.