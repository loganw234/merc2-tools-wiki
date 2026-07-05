---
title: MrxTaskState
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [task, enum]
verified: true
verified_note: deeper pass — re-confirmed all 4 constants (0/1/2/3) and both functions against source; cross-linked the consuming base class MrxTask; no inaccuracies found
---

# MrxTaskState

*Module: mrxtaskstate.lua*

## Overview
The `MrxTaskState` module defines the enumeration for task states used by the whole mission/task
framework. It provides functions to validate a state and to turn one into a human-readable name. Every
task's current state (stored as `_nState` on the task) is one of these four values — see
[`MrxTask`](mrxtask), which reads/writes them via `_GetState`/`_SetState` and defaults an unset state to
`_knLatent`.

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
- Reference the states as `MrxTaskState._knLatent` / `._knActive` / `._knCompleted` / `._knCancelled`
  rather than hard-coding `0`/`1`/`2`/`3` — the numeric values are an implementation detail.
- `GetStateDisplayName` returns the lowercase strings `"latent"`, `"active"`, `"completed"`,
  `"cancelled"`; these are what show up in [`MrxTask`](mrxtask)'s `Debug.Printf` state-change logs.
- `GetStateDisplayName` **asserts** on any value not in the enum, so only pass it a validated state.