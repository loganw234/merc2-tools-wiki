---
title: WifTutorialCoopTether
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 11
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialCoopTether

## Overview
Presumably shown around the co-op "tether" mechanic that keeps two players from straying too far apart,
per its message key and the manager catalog entry — per static source reading, this file only defines
the message and a fixed completion timer; the actual trigger isn't in this file.

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
Returns the fixed message key `"[Tutorial.Tether]"`.

### SetupCompletionCriteria(self)
Standard pattern: a 10-second `Event.TimerRelative` that calls `self.EndTutorial(self, true)`.

## Events
- `Event.TimerRelative` — 10-second completion delay.

## Notes for modders
- Trigger key: `"CoopTether"`. **No `SetupActivationCriteria` override** (inherits the base no-op), and
  same as [`WifTutorialCoopRevive`](wiftutorialcooprevive), **no call site for
  `StartTutorial("CoopTether")` or `BeginCustomTutorial("CoopTether")` was found anywhere in this
  corpus** — can't confirm the actual trigger from static reading alone. Likely native/engine-side co-op
  tether logic not expressed in Lua.
