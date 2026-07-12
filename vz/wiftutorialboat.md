---
title: WifTutorialBoat
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 5
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialBoat

## Overview
Shown the first time the player mounts the driver seat of a boat. Cancels if the player exits before
the tutorial finishes on its own. The message text is device-aware — it differs between controller and
mouse/keyboard play.

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
Returns `"[Tutorial.Boat]"` if `Gui.ControllerInUse` exists and reports a controller in use, otherwise
returns the PC-specific `"[SHELL.PCShell.Tutorial_Boat_PC]"`. The `Gui.ControllerInUse and
Gui.ControllerInUse()` guard checks the function exists before calling it.

### SetupActivationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player entering the driver seat (`"Boat"`, `"D"`,
`"E"`) that calls `self.ActivateTutorial(self, true)`.

### SetupCancellationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player exiting the driver seat (`"Boat"`, `"D"`,
`"X"`) that calls `self.EndTutorial(self, false)`.

## Events
- `Event.ObjectInSeat` (x2) — entering the boat driver seat activates; exiting it cancels.

## Notes for modders
- Trigger key: `"Boats"` (plural — not `"Boat"`), per
  [`MrxTutorialManager`](../resident/mrxtutorialmanager)'s catalog. Self-arms via
  `SetupActivationCriteria`.
- No `SetupCompletionCriteria` override — completes via the inherited **20-second** timer, not the
  10-second pattern common elsewhere in this category.
- The device-aware `GetMessage()`/`Gui.ControllerInUse()` pattern is reused verbatim in
  [`WifTutorialWheeledVehicleBasic`](wiftutorialwheeledvehiclebasic) — the only two tutorials in this
  category with separate PC-specific message text.
