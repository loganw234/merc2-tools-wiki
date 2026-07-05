---
title: Fountain
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: 'deeper pass: re-confirmed all four functions; reframed them as the engine query→action-name→action-function dispatch pattern (QueryActiveUse returns "SuperUse", QueryRepair always ""), cross-linked Bench which shares the pattern, and clarified they are engine callbacks not Event.* subscriptions'
---

# Fountain

*Module: fountain.lua*

## Overview
The `Fountain` module is a thin action-dispatch script for a fountain prop — the same shape as
[Bench](bench). The `Query*` functions are called by the engine to ask "what named action does this input
map to?" and return an action-name string; the action functions (`Use`, `SuperUse`) are the hooks the engine
then calls, and both are empty here, so the fountain has no scripted behaviour out of the box.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state.

## Functions
### `QueryActiveUse(intVal)`
Engine dispatcher: returns the name of the "active use" action. Returns `"SuperUse"` when `intVal == 1`,
otherwise `""`. The returned string is the function name the engine then calls.

### `Use(floatval, aiguid)`
Engine-invoked "use" hook. Empty body — both arguments are declared but unused.

### `SuperUse(floatval, aiguid)`
Engine-invoked "super use" hook (the action `QueryActiveUse` maps `intVal == 1` to). Empty body, same as
`Use`.

### `QueryRepair(intVal)`
Engine dispatcher for the repair action. Ignores `intVal` entirely and always returns `""` — so this fountain
exposes no repair action (contrast [Bench](bench), whose `QueryRepair` returns `"MakeUpright"`).

## Events
This module does not listen for or fire any engine events. The `Query*`/`Use`/`SuperUse` functions are
engine callbacks, not `Event.Create` subscriptions.

## Notes for modders
- Same query→action-name→action-function indirection as [Bench](bench): change what `QueryActiveUse` returns
  (or the `intVal` it gates on) to remap which action fires, and fill in the matching `SuperUse`/`Use` body
  to give it behaviour. The returned name must match an action function the engine can call.
- Both action functions are empty, so there is no existing behaviour to preserve if you override them.