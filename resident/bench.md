---
title: Bench
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: 'deeper pass: re-confirmed all five functions; clarified that Query* are engine "what action string?" dispatchers returning "MakeUpright"/"SuperUse", while SuperUse/Use/MakeUpright are empty engine-called hook stubs; fixed misleading Notes'
---

# Bench

*Module: bench.lua*

## Overview
The `Bench` module is a thin action-dispatch script for a bench prop. The two `Query*` functions are called
by the engine to ask "what named action should this input map to?" and return an action-name string; the
three action functions (`SuperUse`, `Use`, `MakeUpright`) are the hooks the engine then calls — all three are
empty stubs here, so the actual behaviour is engine-side (or intentionally a no-op).

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module with no per-instance tables or fields.

## Functions
### `QueryRepair(intVal)`
Engine dispatcher: returns the name of the repair action to run. Returns the string `"MakeUpright"` when
`intVal == 1`, otherwise `""` (no action). The returned name is the function the engine will call.

### `QueryActiveUse(intVal)`
Engine dispatcher: returns the name of the "active use" action. Returns `"SuperUse"` when `intVal == 1`,
otherwise `""`. Again the return value is a function name, not the behaviour itself.

### `SuperUse(floatval, aiguid)`
Placeholder function for handling the "SuperUse" action. Currently does nothing.

### `Use(aiguid, floatval)`
Placeholder function for handling general use actions. Currently does nothing.

### `MakeUpright(objectguid, aiguid)`
Placeholder function for making an object upright. Currently does nothing.

## Events
This module does not listen to or fire any engine events.

## Notes for modders
- The `Query*` → action-name → action-function indirection is the reusable lever here: change what
  `QueryRepair`/`QueryActiveUse` return (or the `intVal` they gate on) to remap which action fires, and fill
  in the matching `SuperUse`/`Use`/`MakeUpright` body to give it behaviour. The names returned by the
  `Query*` functions must match the action functions the engine then calls.
- All three action functions are currently empty — this bench prop does nothing scripted out of the box, so
  there is no existing behaviour to preserve if you override them.