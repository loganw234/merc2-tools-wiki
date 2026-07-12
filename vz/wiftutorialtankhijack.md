---
title: WifTutorialTankHijack
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 19
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialTankHijack

## Overview
Shown near an enemy tank crewed by two or more gunners, teaching the tank-hijack mechanic. Notably, this
tutorial can never permanently complete: its `EndTutorial` override forces every completion attempt back
into a re-arm instead, so it just keeps reappearing for the rest of the playthrough.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: `MrxFactionManager` (used — `GetFactionStringAbbrev`, `GetAttitudeLabel`).

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. No module-level or per-instance state
beyond what the base class itself tracks (`_tEvents`).

## Functions
### GetMessage()
Returns the fixed message key `"[Tutorial.TankHijack]"`.

### SetupActivationCriteria(self)
Registers an `Event.ObjectProximity` listener for any object labeled `"tank"` within 20 units of the
player, calling `self.ActivateTutorial2(self, tGuids)` with the (possibly multi-element) table of
matched tank objects.

### ActivateTutorial2(self, tGuids)
For each matched tank: gets its gunner riders (`Vehicle.GetRiders(uVehicleObject, "g")`); computes the
tank's faction attitude toward the player via `MrxFactionManager.GetFactionStringAbbrev`/
`GetAttitudeLabel` and logs it via `Debug.Printf` (the `if sFactionAttitude == "Hostile" then end` check
has an **empty body** — the attitude is computed and logged but never used to gate anything); counts
gunners via `table.getn`. If this tank does **not** have more than 1 gunner, returns immediately without
activating — a single non-multi-gunner tank in the matched set blocks activation for that whole check,
even if a different matched tank might otherwise qualify. If every matched tank passes, calls
`self:ActivateTutorial()` — note, unlike most tutorials in this category, **no `bDontNetSync` argument is
passed**, so it defaults to falsy (net-synced).

### EndTutorial(self, bComplete)
Overridden: if `bComplete == true`, forcibly rewrites it to `false` before calling
`MrxTutorial.EndTutorial(self, bComplete)`.

## Events
- `Event.ObjectProximity` — any `"tank"`-labeled object within 20 units of the player.
- `Event.TimerRelative` — the inherited 20-second completion timer still fires (no
  `SetupCompletionCriteria` override in this file), but see the note below on what actually happens when
  it does.

## Notes for modders
- Trigger key: `"TankHijack"`. Self-arms via `SetupActivationCriteria`.
- **This tutorial never permanently completes.** `EndTutorial`'s override rewrites any
  `bComplete == true` call to `false` before forwarding to the base class, so even the inherited
  20-second completion timer ends up re-arming the tutorial (via `SetupActivationCriteria`) rather than
  marking it done in save data — it will keep reappearing every time the proximity/gunner-count
  conditions are met again.
- The `if sFactionAttitude == "Hostile" then end` branch is empty — the attitude is computed and logged
  but never actually used to gate anything. This is a genuine empty branch in the decompiled source
  (not a decompiler artifact), likely leftover/debug code.
- Requires 2+ gunners on **every** proximity-matched tank to activate at all — a single 0-or-1-gunner
  tank in range short-circuits the whole check via an early `return`.
