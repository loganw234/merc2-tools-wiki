---
title: WifTutorialTrespass
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 20
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialTrespass

## Overview
Shown when the player trespasses into hostile/restricted territory. The message auto-hides after 10
seconds; both activation and completion are guarded so a re-trigger while already active can't stack a
second completion timer.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: none

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. Per-instance state: `self._CompleteEvent`,
the guard/handle used by both overrides below — identical shape to
[`WifTutorialCollateralDamage`](wiftutorialcollateraldamage).

## Functions
### GetMessage()
Returns the fixed message key `"[Tutorial.Trespassing]"`.

### ActivateTutorial(self, bDontNetSync)
Overridden: only calls `MrxTutorial.ActivateTutorial(self, bDontNetSync)` if `self._CompleteEvent` isn't
already set.

### SetupCompletionCriteria(self)
Same guard: only creates the 10-second `Event.TimerRelative` (→ `self.EndTutorial(self, true)`) if
`self._CompleteEvent` isn't already set, storing the handle in that field.

## Events
- `Event.TimerRelative` — 10-second completion delay, guarded to fire only once per activation via
  `self._CompleteEvent`.

## Notes for modders
- Trigger key: `"Trespass"`. **No `SetupActivationCriteria` override** — confirmed sole call site:
  [`MrxGuiHudRadar`](../resident/mrxguihudradar) calls
  `MrxTutorialManager.StartTutorial("Trespass", true)` when it sets a radar widget's
  `CustomData.bTrespass` flag to `true`.
- Same `self._CompleteEvent` double-activation guard as
  [`WifTutorialCollateralDamage`](wiftutorialcollateraldamage).
