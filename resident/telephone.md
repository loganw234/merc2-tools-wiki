---
title: Telephone
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [utility]
verified: true
verified_note: 'deeper pass: re-confirmed the whole file (2-line stub, one empty Use function, no imports/inherit/events); made the modder note actionable (Use is an overridable interact hook, same shape as outhouse.lua).'
---

# Telephone

*Module: telephone.lua*

## Overview
The `Telephone` module is a stub: it defines a single empty `Use` function and nothing else. As
shipped the telephone is pure set dressing — the `Use` hook exists but does nothing. (Identical shape
to [`outhouse`](outhouse).)

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless utility module with no per-instance tables or fields.

## Functions
### `Use(aiguid, floatval)`
Empty function — no body. `aiguid` is the telephone object handle; `floatval` is unused. By naming
convention this is the "use/interact" hook the engine calls when the player activates the phone, but
it is a no-op as shipped.

## Events
- none — no `Event.*` calls of any kind.

## Notes for modders
- `Use` is a plain global; override it to give the telephone behavior on interaction (play a line,
  trigger a call, etc.). See [Function override](../deep-dives/function-override).
- No inherit, imports, state, or events — nothing to clean up or sequence.