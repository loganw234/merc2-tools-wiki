---
title: WifTutorialAPC
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 4
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialAPC

## Overview
Shown the first time the player mounts the driver seat of an APC. Cancels if the player exits the
driver seat before the tutorial finishes on its own.

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
Returns the fixed message key `"[Tutorial.APC]"`.

### SetupActivationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player entering the driver seat (`"APC"`, `"D"`,
`"E"`) that calls `self.ActivateTutorial(self, true)`.

### SetupCancellationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player exiting the driver seat (`"APC"`, `"D"`,
`"X"`) that calls `self.EndTutorial(self, false)`.

## Events
- `Event.ObjectInSeat` (x2) — entering the APC driver seat activates; exiting it cancels.

## Notes for modders
- Trigger key: `"APC"`. Self-arms via `SetupActivationCriteria`; no external `StartTutorial` call needed.
- No `SetupCompletionCriteria` override — completes via the inherited **20-second** timer, not the
  10-second pattern common elsewhere in this category.
- `"D"`/`"E"`/`"X"` read as seat = Driver, action = Enter/eXit, by comparison with the identically-shaped
  [`WifTutorialBoat`](wiftutorialboat), [`WifTutorialHelicopter`](wiftutorialhelicopter),
  [`WifTutorialTank`](wiftutorialtank), and [`WifTutorialWheeledVehicleBasic`](wiftutorialwheeledvehiclebasic)
  files — exact code semantics aren't spelled out anywhere in source.
