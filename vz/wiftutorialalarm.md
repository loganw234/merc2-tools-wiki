---
title: WifTutorialAlarm
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 2
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialAlarm

## Overview
Shown when the player sets off a physical alarm object in the world. This is one of the minimal
tutorial files in the category: it defines only the message and a fixed completion timer, with no
self-registered activation trigger at all.

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
Returns the fixed message key `"[Tutorial.Alarms]"`.

### SetupCompletionCriteria(self)
Standard pattern: a 10-second `Event.TimerRelative` that calls `self.EndTutorial(self, true)`.

## Events
- `Event.TimerRelative` — 10-second completion delay in `SetupCompletionCriteria`.

## Notes for modders
- Trigger key: `"Alarm"`. **No `SetupActivationCriteria` override exists in this file at all** — it
  inherits the base class's empty no-op, so it can never self-arm from any event. Confirmed sole
  activation path: [`Alarm`](../resident/alarm) (`resident/alarm.lua`) calls
  `MrxTutorialManager.StartTutorial("Alarm")` directly, right after arming an alarm object's
  deactivation events and starting its own 60-second mute timer — i.e. this fires whenever the player
  sets off a resident alarm object, bypassing `SetupActivationCriteria` entirely.
- No `SetupCancellationCriteria` override either — inherits the base no-op.
