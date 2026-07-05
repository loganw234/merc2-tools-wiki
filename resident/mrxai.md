---
title: MrxAi
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, command]
verified: true
verified_note: flagged a real Deploy() field mismatch (guards on tParameters.Vehicle, waits on tParameters.AIGuid) — rest of file matches source
---

# MrxAi

*Module: mrxai.lua*

## Overview
The `MrxAi` module provides a thin, awake-gated shim over the engine `Ai.*` API. It ensures that AI commands are only issued once the associated AIGuid object is fully awake and ready to receive instructions.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It does not track any specific state fields.

## Functions
### `Goal(tParameters)`
Issues an AI goal to the specified AIGuid. The goal is a one-shot task with a fulfillment callback and a priority ("hiPri"/"loPri"). Waits for the object to leave hibernation before forwarding the parameters to the engine `Ai.Goal`.

### `DefaultGoal(tParameters)`
Sets the default goal for the specified AIGuid. This fallback behavior ensures that the AI has a persistent task if its current goals are removed or completed. Waits for the object to leave hibernation before forwarding the parameters to the engine `Ai.DefaultGoal`.

### `RemoveGoal(tParameters)`
Removes an AI goal from the specified AIGuid. This is used to clear out any existing tasks that are no longer relevant. Waits for the object to leave hibernation before forwarding the parameters to the engine `Ai.RemoveGoal`.

### `Deploy(tParameters)`
Deploys an AI to a vehicle. This function ensures that the AI is properly assigned to the specified vehicle once it is awake and ready. Waits for the object to leave hibernation before forwarding the parameters to the engine `Ai.Deploy`.

**Confirmed in source, likely a bug:** unlike `Goal`/`DefaultGoal`/`RemoveGoal`/`Role` (which all guard
*and* wait on `tParameters.AIGuid`), `Deploy` guards on `tParameters.Vehicle` (`if tParameters.Vehicle
then`) but then registers the `Event.ObjectHibernation` wait on `tParameters.AIGuid`. If a caller passes
`Vehicle` without also setting `AIGuid` on the same table, the guard passes but `Event.Create` is handed
a `nil` guid for the hibernation-wait target — the callback would either never fire or behave
unpredictably depending on how the engine's `Event.Create` treats a `nil` first list element. No call
sites for any `MrxAi.*` function (`Goal`, `DefaultGoal`, `RemoveGoal`, `Deploy`, or `Role`) were found
anywhere in the decompiled corpus, so it's unclear whether real callers always set both `Vehicle` and
`AIGuid` on the same table (sidestepping the bug) or whether this path is simply never exercised.

### `Role(tParameters)`
Sets the role of the specified AIGuid. The role defines the persistent stance of the AI, such as "Follow" or "Idle". Waits for the object to leave hibernation before forwarding the parameters to the engine `Ai.Role`.

## Events
- Listens for `Event.ObjectHibernation` to ensure that all AI commands are only issued once the AIGuid object is fully awake.

## Notes for modders
- Ensure that the AIGuid object is properly activated and hibernated before issuing any AI commands through this module.
- Use `Goal`, `DefaultGoal`, `RemoveGoal`, `Deploy`, and `Role` to manage the behavior of AI entities in the game world.
- Be aware that the priority of goals ("hiPri"/"loPri") can affect the order in which tasks are executed by the AI.
- The module ensures that all commands are only sent once the object is fully awake, preventing any potential issues with uninitialized AI states.