---
title: MrxTaskState
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [task, enum]
---

# MrxTaskState

*Module: mrxtaskstate.lua*

## Overview
The `MrxTaskState` module defines the enumeration for task states in the game. It provides functions to validate task states and retrieve their display names.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless utility module (no per-instance tables). It does not track any state; it only defines constants and helper functions.

## Functions
### `_knLatent` (constant)
Represents the latent task state. Value: `0`.

### `_knActive` (constant)
Represents the active task state. Value: `1`.

### `_knCompleted` (constant)
Represents the completed task state. Value: `2`.

### `_knCancelled` (constant)
Represents the cancelled task state. Value: `3`.

### `IsValidState(nState)`
Checks if a given task state is valid.
- **Parameters**: `nState` (number) — The task state to validate.
- **Returns**: `boolean` — True if the state is valid, false otherwise.

### `GetStateDisplayName(nState)`
Retrieves the display name for a given task state.
- **Parameters**: `nState` (number) — The task state to get the display name for.
- **Returns**: `string` — The display name of the task state.
- **Side Effects**: Asserts if the state is unknown.

## Events
This module does not listen for or fire any engine events.

## Notes for modders
- Use `IsValidState` to check if a task state is valid before processing it.
- Use `GetStateDisplayName` to retrieve the display name of a task state for UI or logging purposes.
- Be aware that the constants `_knLatent`, `_knActive`, `_knCompleted`, and `_knCancelled` are used throughout the mission task framework, so ensure they are consistent when extending or modifying task-related logic.