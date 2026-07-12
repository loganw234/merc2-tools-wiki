---
title: WifTutorialHelicopter
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 13
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialHelicopter

## Overview
Shown the first time the player mounts the driver seat of a helicopter. Cancels if the player exits
before the tutorial finishes on its own.

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
Returns the fixed message key `"[Tutorial.Helicopter]"`.

### SetupActivationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player entering the driver seat (`"helicopter"`,
`"D"`, `"E"`) that calls `self.ActivateTutorial(self, true)`.

### SetupCancellationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player exiting the driver seat (`"helicopter"`,
`"D"`, `"X"`) that calls `self.EndTutorial(self, false)`.

## Events
- `Event.ObjectInSeat` (x2) — entering the helicopter driver seat activates; exiting it cancels.

## Notes for modders
- Trigger key: `"Helicopters"` (plural), per
  [`MrxTutorialManager`](../resident/mrxtutorialmanager)'s catalog. Self-arms via
  `SetupActivationCriteria`.
- No `SetupCompletionCriteria` override — completes via the inherited **20-second** timer, not the
  10-second pattern common elsewhere in this category.
- Note the lowercase `"helicopter"` label, versus the PascalCase `"Boat"`/`"APC"`/`"Tank"`/`"Car"` labels
  used by the other seat-based tutorials in this category — label matching is presumably case-sensitive,
  so use this exact casing if extending.
