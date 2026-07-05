---
title: Pmcgate
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [pmc, gate]
verified: true
verified_note: 'deeper pass: re-confirmed the whole file (2 functions, ObjectHibernation→OpenGate→TimerRelative(2s)→Object.OpenGate); noted the args param is unused and the 2s open delay is the only tunable; cross-linked Event/Object namespaces; pruned the vacuous OnActivate modder bullet.'
---

# Pmcgate

*Module: pmcgate.lua*

## Overview
`Pmcgate` is a minimal "auto-open" script for a PMC gate object: once the gate wakes, it opens itself
2 seconds later. That's the entire module. (Contrast [`FriendlyGate`](friendlygate) for a
richer/faction-aware gate.)

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
Stateless — no per-instance table, no stored event handles. It just chains two engine events and
never keeps a reference to them.

## Functions
### `OnActivate(uGateGuid, args)`
Engine lifecycle callback. Wires an `Event.ObjectHibernation` `"awake"` event that runs `OpenGate`
once the gate leaves hibernation. `args` is received but not used.

### `OpenGate(uGateGuid)`
Schedules `Object.OpenGate(uGateGuid)` via [`Event.TimerRelative`](../namespaces/event) after `2`
seconds. Note it passes [`Object.OpenGate`](../namespaces/object) directly as the timer callback rather
than a wrapper.

## Events
- **`Event.ObjectHibernation`** (`"awake"`, in `OnActivate`) → `OpenGate`.
- **`Event.TimerRelative`** (`2`s, in `OpenGate`) → `Object.OpenGate`.

Neither handle is stored, so there is no cancellation path — the gate will open 2s after waking
regardless of anything else.

## Notes for modders
- The **only tunable** is the `2` (seconds) in `OpenGate`'s `Event.TimerRelative` — change it to open
  the gate sooner or later after it wakes.
- Because the timer handle isn't kept, you can't cancel the open. If you need a gate that can stay
  closed conditionally, this module won't do it — override `OpenGate` or use a different gate script.