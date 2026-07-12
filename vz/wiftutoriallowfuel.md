---
title: WifTutorialLowFuel
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 15
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialLowFuel

## Overview
Shown when the player's fuel drops to 10% of capacity or below. Defines only the message and a fixed
completion timer; activation is entirely external.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: none

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. No module-level or per-instance state
beyond what the base class itself tracks (`_tEvents`).

## Functions
### GetMessage()
Returns the fixed message key `"[Tutorial.LowFuel]"`.

### SetupCompletionCriteria(self)
Standard pattern: a 10-second `Event.TimerRelative` that calls `self.EndTutorial(self, true)`.

## Events
- `Event.TimerRelative` — 10-second completion delay.

## Notes for modders
- Trigger key: `"LowFuel"`. **No `SetupActivationCriteria` override** — confirmed sole call site:
  [`MrxPmc`](../resident/mrxpmc) fires `MrxTutorialManager.StartTutorial("LowFuel")` when a negative
  fuel-amount change brings the new total to 10% or less of `_nFuelCapacity` (checked only when the
  0-fuel `"NoFuel"` case, see [`WifTutorialNoFuel`](wiftutorialnofuel), doesn't already apply).
