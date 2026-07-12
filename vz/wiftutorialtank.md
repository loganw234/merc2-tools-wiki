---
title: WifTutorialTank
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 18
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialTank

## Overview
Shown the first time the player mounts the driver seat of a tank (specifically excluding APCs). Cancels
if the player exits before the tutorial finishes on its own.

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
Returns the fixed message key `"[Tutorial.Tank]"`.

### SetupActivationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player entering the driver seat of an object matching
the label expression `"Tank && !APC"` (`"D"`, `"E"`) that calls `self.ActivateTutorial(self, true)`.

### SetupCancellationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player exiting the driver seat of an object labeled
`"Tank"` (`"D"`, `"X"`) that calls `self.EndTutorial(self, false)`.

## Events
- `Event.ObjectInSeat` (x2) — entering a Tank-but-not-APC driver seat activates; exiting a Tank-labeled
  driver seat cancels.

## Notes for modders
- Trigger key: `"Tanks"` (plural), per [`MrxTutorialManager`](../resident/mrxtutorialmanager)'s catalog.
  Self-arms via `SetupActivationCriteria`.
- The label filter supports boolean expressions — `"Tank && !APC"` excludes APCs from counting as tanks
  for **activation** — but the cancellation listener just uses plain `"Tank"` with no `&& !APC`
  exclusion. Minor asymmetry between the two filters, worth knowing if debugging edge cases involving
  APC-labeled objects.
- No `SetupCompletionCriteria` override — completes via the inherited **20-second** timer, not the
  10-second pattern common elsewhere in this category.
