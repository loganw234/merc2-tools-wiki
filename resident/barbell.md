---
title: Barbell
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: 'deeper pass: confirmed the whole 3-line source; clarified UnUse is an engine-invoked un-use callback (not an Event.* subscription), cross-linked the Object namespace, and pruned vacuous Notes boilerplate'
---

# Barbell

*Module: barbell.lua*

## Overview
The entire `barbell.lua` is a single function: when the player stops "using" the barbell prop, detach it
from whoever was holding it. This is a minimal world-prop script — the barbell is a hold-and-carry object,
and this is the one bit of scripted behaviour it needs.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
Stateless. No module-level tables, no per-`uGuid` bookkeeping, no `setmetatable`/`tInstance` factory — just
one global function the engine calls.

## Functions
### `UnUse(objectGuid, holdersGuid)`
Calls `Object.Detach(holdersGuid, objectGuid)` to release the barbell (`objectGuid`) from its holder
(`holdersGuid`). `UnUse` is an engine-invoked lifecycle callback fired when the "use" interaction ends — it
is **not** an `Event.*` subscription and is never called from within this file.

## Events
- Subscribes to: none. `UnUse` is an engine callback, not an `Event.Create` listener.

## Notes for modders
- The whole prop reduces to one `Object.Detach` call — see the [Object namespace](../namespaces/object) for
  the attach/detach primitives (`Object.Attach`/`Object.Detach`) if you want to build a similar
  pick-up/put-down prop.
- Note the argument order: `Object.Detach(holdersGuid, objectGuid)` takes the **holder first**, then the
  attached object — the reverse of the `UnUse(objectGuid, holdersGuid)` parameter order.