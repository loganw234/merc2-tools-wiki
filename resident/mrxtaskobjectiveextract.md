---
title: MrxTaskObjectiveExtract
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTaskObjective
tags: [task, extraction]
---

# MrxTaskObjectiveExtract

*Module: mrxtaskobjectiveextract.lua*

## Overview
The `MrxTaskObjectiveExtract` module is responsible for handling the extraction task objective in the game. It manages the extraction process, including setting up followers, checking for allied helicopters, and handling various events related to the target's proximity and health.

## Inheritance
- Inherits from: `MrxTaskObjective`
- Imports: `MrxSupportData`, `MrxFollow`, `MrxUtil`, `MrxGui`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_uTgtObjFilter`: Filter for the target object.
- `oFollower`: Follower object managing the extraction process.
- `eHeliClose`, `eHeliFar`, `eHeliHurt`, `eHeliFailsafe`, `eAIenter1`, `eAIenter2`: Event handles for various events related to the extraction process.

## Functions
### `Activated(self)`
Called when the task objective is activated. It sets default configuration values, retrieves target objects, and initializes a follower if necessary. It also creates events for object death and player join.

### `SendPlayerJoinEvents()`
Sends player join events to the server. This function ensures that the extraction process is properly synchronized with new players joining the game.

### `CheckForHeli(self, uGuid)`
Checks for allied helicopters in proximity to the target. If an allied helicopter is found, it sets up events for handling the extraction process.

### `TargetDestroyed(self, uGuid)`
Cancels the part of the task related to the destroyed target.

### `TargetStopsForHeli(self, uGuid, tHeliExt)`
Handles the scenario where the target stops for an allied helicopter. It activates the follower, sets up AI goals for entering the helicopter, and creates events for handling various extraction-related scenarios.

### `TargetRunsForHeli(self, uGuid, tHeliExt)`
Sets up AI goals for the target to run towards the helicopter.

### `CheckEnter(self, tHeliExt, uGuid, nState)`
Checks if the target has successfully entered the helicopter. If not, it retries entering after a short delay.

### `AbortExtract(self, uGuid)`
Aborts the extraction process due to various failure conditions, such as the destruction of the extraction heli or the target moving too far away. It resets the prisoner's AI goals and activates the follower again.

### `ResetPrisoner(self, uGuid)`
Resets the prisoner's AI goals and reactivates the follower. It also checks for allied helicopters again.

### `TargetIn(self, uGuid, tHeliExt, Guid, State)`
Handles the scenario where the target is inside the helicopter. It completes the part of the task related to the extraction process after a short delay.

### `Cleanup(self)`
Cleans up the module by removing the freebie associated with the extraction task and calling the base class's cleanup function.

## Events
- Listens for `Event.ObjectDeath` to call `TargetDestroyed` when the target object dies.
- Listens for custom event `mpPlayerJoin` to send player join events.
- Listens for `Event.ObjectProximity` to handle scenarios where the target is close or far from an allied helicopter.
- Listens for `Event.ObjectHealth` to handle scenarios where the extraction heli's health drops below a certain threshold.
- Listens for `Event.ObjectInSeat` to handle scenarios where the target enters the helicopter.

## Notes for modders
- Ensure that `Activated` and `Cleanup` are called appropriately to manage the lifecycle of the extraction task objective.
- Customize the behavior of the extraction process by modifying the configuration values in `tConfig`.
- Be aware that network synchronization (`Net.IsServer`) may affect multiplayer behavior.
- The module relies on various engine events and functions, such as `Ai.Goal` and `Event.CreatePersistent`, to manage the extraction process.