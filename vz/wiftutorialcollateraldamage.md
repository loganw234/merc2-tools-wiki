---
title: WifTutorialCollateralDamage
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 8
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialCollateralDamage

## Overview
Shown when the player deals collateral damage to a civilian or neutral. The message auto-hides after
10 seconds; both activation and completion are guarded so a re-trigger while already active can't stack
a second completion timer.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: none

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. Per-instance state: `self._CompleteEvent`,
the guard/handle used by both overrides below.

## Functions
### GetMessage()
Returns the fixed message key `"[Tutorial.Collateral]"`.

### ActivateTutorial(self, bDontNetSync)
Overridden: only calls `MrxTutorial.ActivateTutorial(self, bDontNetSync)` if `self._CompleteEvent` isn't
already set — guards against a re-trigger while the tutorial is already active from re-arming the
completion timer.

### SetupCompletionCriteria(self)
Same guard: only creates the 10-second `Event.TimerRelative` (→ `self.EndTutorial(self, true)`) if
`self._CompleteEvent` isn't already set, storing the handle in that field.

## Events
- `Event.TimerRelative` — 10-second completion delay, guarded to fire only once per activation via
  `self._CompleteEvent`.

## Notes for modders
- Trigger key: `"CollateralDamage"`. **No `SetupActivationCriteria` override in this file** — confirmed
  sole call site: [`MrxFactionManager`](../resident/mrxfactionmanager) calls
  `MrxTutorialManager.StartTutorial("CollateralDamage", true)` as part of its civilian-casualty penalty
  handling, alongside a cash penalty and faction-relation cues.
- The `self._CompleteEvent` guard on both `ActivateTutorial` and `SetupCompletionCriteria` means calling
  `ActivateTutorial` again while already active is a safe no-op — the same guarded pattern used by
  [`WifTutorialTrespass`](wiftutorialtrespass).
