---
title: MrxAi
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, command]
verified: true
verified_note: "deeper pass: re-confirmed all 5 functions and the Event.ObjectHibernation awake-wait pattern against source; the Deploy Vehicle/AIGuid guard mismatch still stands; cross-linked the Ai namespace, pruned vacuous notes"
---

# MrxAi

*Module: mrxai.lua*

## Overview
The `MrxAi` module provides a thin, awake-gated shim over the engine [`Ai.*`](../namespaces/ai) API. Each
function guards on a parameter, registers an `Event.ObjectHibernation` "awake" wait for the target, and only
forwards the `tParameters` table to the matching `Ai.*` call once the object has left hibernation — so AI
commands aren't dropped by being issued against a still-sleeping object.

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
- **Use these instead of raw `Ai.*` when the target might not be awake yet** — that's the whole point.
  The `tParameters` table you pass is forwarded verbatim to the corresponding [`Ai.*`](../namespaces/ai)
  call, so consult that namespace page for the actual field set each command expects (e.g. `AIGuid`,
  `Role`, `Target`, `Priority`, `Callback`).
- **`AIGuid` must be set on `tParameters`** for `Goal`/`DefaultGoal`/`RemoveGoal`/`Role` — it's both the
  guard and the hibernation-wait target. `Deploy` is the odd one out (guards on `Vehicle`, waits on
  `AIGuid`) — see the bug callout above; set both to be safe.
- Goal priority (`"hiPri"`/`"loPri"`) affects execution order; that behavior lives in the engine `Ai`
  layer, not here.