---
title: WifTutorialHeliRepairPad
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 14
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialHeliRepairPad

## Overview
Presumably shown around landing on/using a helicopter repair pad, per its message key
(`"[Tutorial.LandingZoneHealth]"`). Unlike the vehicle-seat tutorials, this file overrides
`ActivateTutorial` itself with a helicopter-only guard rather than relying on the activation-criteria
event filter to restrict when it can fire.

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
Returns the fixed message key `"[Tutorial.LandingZoneHealth]"`.

### ActivateTutorial(self)
Overridden with a single-parameter signature — note this **drops the base class's `bDontNetSync`
parameter entirely** and always net-syncs `true` internally. Bails out (returns without activating)
unless the player's current ridden vehicle both exists (`Vehicle.GetFromRider`) and
`Object.HasLabel(uVehicle, "Helicopter")`; otherwise calls `MrxTutorial.ActivateTutorial(self, true)`.

### SetupCompletionCriteria(self)
Standard pattern: a 10-second `Event.TimerRelative` that calls the bare global `EndTutorial(self, true)`
(resolves through inheritance to `MrxTutorial.EndTutorial`).

## Events
- `Event.TimerRelative` — 10-second completion delay.

## Notes for modders
- Trigger key: `"HeliRepairPad"`. **No `SetupActivationCriteria` override exists in this file**, and no
  call site for its `ActivateTutorial` or a `StartTutorial("HeliRepairPad")`/
  `BeginCustomTutorial("HeliRepairPad")` call was found anywhere in this corpus —
  [`Repairpad`](../resident/repairpad) (`resident/repairpad.lua`) imports `MrxTutorialManager` but
  contains no further reference to it in its own (very short) body. The actual trigger — presumably tied
  to landing-pad repair logic — isn't confirmable from static reading alone.
- The `ActivateTutorial(self)` override silently ignores any `bDontNetSync` argument a caller might pass
  — it always net-syncs `true` regardless of what's asked for.
