---
title: WifTutorialCoopRevive
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 10
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialCoopRevive

## Overview
Presumably shown around reviving a downed co-op partner, per its message key and the manager catalog
entry — per static source reading, this file only defines the message and a fixed completion timer; the
actual trigger isn't in this file.

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
Returns the fixed message key `"[Fiona.Misc.Revive01]"` — note this uses the `"[Fiona.Misc...]"`
localization namespace rather than the `"[Tutorial...]"` namespace every other file in this batch uses;
a naming outlier, though functionally identical.

### SetupCompletionCriteria(self)
Standard pattern: a 10-second `Event.TimerRelative` that calls `self.EndTutorial(self, true)`.

## Events
- `Event.TimerRelative` — 10-second completion delay.

## Notes for modders
- Trigger key: `"CoopRevive"`. **No `SetupActivationCriteria` override** (inherits the base no-op), and
  unlike [`WifTutorialAlarm`](wiftutorialalarm)/[`WifTutorialLowFuel`](wiftutoriallowfuel)/
  [`WifTutorialNoFuel`](wiftutorialnofuel)/[`WifTutorialTrespass`](wiftutorialtrespass)/
  [`WifTutorialCollateralDamage`](wiftutorialcollateraldamage), **no call site for
  `StartTutorial("CoopRevive")` or `BeginCustomTutorial("CoopRevive")` was found anywhere in this
  corpus** — can't confirm the actual trigger from static reading alone. Likely native/engine-side
  co-op revive logic not expressed in Lua.
- The `"[Fiona.Misc.Revive01]"` message key stands out from the rest of the category's `"[Tutorial.*]"`
  convention — worth double-checking in-game/localization data if retexting this.
