---
title: WifTutorialWheeledVehicleBasic
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 22
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialWheeledVehicleBasic

## Overview
Shown the first time the player mounts the driver seat of a car. Cancels if the player exits before the
tutorial finishes on its own. The message text is device-aware, like
[`WifTutorialBoat`](wiftutorialboat).

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: none

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. Per-instance state: `self._oActivate1`
(see the bug noted below — `self._oActivate2` is referenced but never actually set).

## Functions
### GetMessage()
Returns `"[Tutorial.WheeledVehicleBasic]"` if `Gui.ControllerInUse` exists and reports a controller in
use, otherwise the PC-specific `"[SHELL.PCShell.Tutorial_WheeledVehicleBasic_PC]"` — identical pattern to
[`WifTutorialBoat`](wiftutorialboat).

### SetupActivationCriteria(self)
Registers **two** `Event.ObjectInSeat` listeners for entering the driver seat of a `"Car"`-labeled
object: one with action `"E"` and one with action `"I"` (a code not seen elsewhere in this batch —
possibly catching "already seated at setup time" versus a fresh enter, but not confirmable from source
alone). Both call `self.ActivateTutorial2(self)`. **Both handles are assigned to the same field,
`self._oActivate1`** — the second assignment silently overwrites the first.

### ActivateTutorial2(self)
Deletes `self._oActivate1` if set, then checks `if self._oActivate2 then Event.Delete(self._oActivate1)
end` — see the bug noted below. Calls `self:ActivateTutorial(true)`.

### SetupCancellationCriteria(self)
Registers an `Event.ObjectInSeat` listener for the player exiting the driver seat (`"Car"`, `"D"`,
`"X"`) that calls `self.EndTutorial(self, false)`.

## Events
- `Event.ObjectInSeat` (x3) — two activation variants (`"E"` and `"I"`) and one cancellation (`"X"`).

## Notes for modders
- Trigger key: `"WheeledVehicleBasic"`. Self-arms via `SetupActivationCriteria`.
- **Confirmed copy/paste bug**: `SetupActivationCriteria` assigns both event handles to
  `self._oActivate1` (clobbering the first), and `ActivateTutorial2`'s second cleanup check tests
  `self._oActivate2` — which is **never set anywhere in this file** and is therefore always `nil`, making
  that whole branch dead code. Even if it weren't dead, the branch deletes `self._oActivate1` again
  rather than a distinct second handle. This very likely should have been `self._oActivate2 =
  self:_CreateEvent(...)` in the second registration. Functionally close to harmless — the base class's
  own `_tEvents` bulk-delete still tears down both registered events on deactivation — but if you're
  extending this file expecting `_oActivate1`/`_oActivate2` to independently track the `"E"` and `"I"`
  listeners, they don't. A good candidate file to actually fix if you're patching tutorials.
- Same device-aware `GetMessage()`/`Gui.ControllerInUse()` pattern as
  [`WifTutorialBoat`](wiftutorialboat) — the only two tutorials in this category with separate
  PC-specific shell text.
- No `SetupCompletionCriteria` override — completes via the inherited **20-second** timer, not the
  10-second pattern common elsewhere in this category.
