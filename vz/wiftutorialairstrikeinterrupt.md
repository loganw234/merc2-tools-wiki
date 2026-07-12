---
title: WifTutorialAirstrikeInterrupt
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 1
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialAirstrikeInterrupt

## Overview
Teaches the player that taking damage while calling in a satellite/airstrike targeting sequence
interrupts it. The tutorial arms itself when a targeting sequence starts, snapshots the player's
health, and only actually activates if that health drops before the sequence ends without success —
i.e. it fires specifically on "you got hit mid-targeting," not on every cancelled targeting attempt.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: none

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. Per-instance state is a single field,
`self._nPlayerHealth`, the health snapshot taken when targeting starts. No module-level globals.

## Functions
### GetMessage()
Returns the fixed message key `"[Tutorial.SatelliteInterrupted]"`.

### SetupActivationCriteria(self)
Listens for `Event.ScriptEvent` named `"Satellite Targetting Start"` (filter function always returns
`true`, i.e. matches any occurrence). On fire, calls `SetupNextActivationCriteria`.

### SetupNextActivationCriteria(self)
Snapshots `self._nPlayerHealth = Object.GetHealth(Player.GetLocalCharacter())`, then listens for
`Event.ScriptEvent` named `"Satellite Targetting Cancelled"`. On fire, calls `ActivateTutorial2`.

### ActivateTutorial2(self)
Compares the snapshot to current health. If `self._nPlayerHealth > Object.GetHealth(...)` (health
dropped since targeting started), activates the tutorial (`bDontNetSync = true`). Otherwise re-arms by
calling `self:SetupActivationCriteria()` again, waiting for the next targeting attempt.

### SetupCompletionCriteria(self)
Standard pattern: a 10-second `Event.TimerRelative` that calls `self.EndTutorial(self, true)`.

## Events
- `Event.ScriptEvent` (x2) — `"Satellite Targetting Start"` and `"Satellite Targetting Cancelled"`.
  Confirmed by direct grep: both are posted by
  [`MrxGuiSatellite`](../resident/mrxguisatellite)'s satellite-targeting overlay — `Event.Post("Satellite
  Targetting Start", {uPlayer = ...})` when the overlay opens, and `Event.Post("Satellite Targetting
  Cancelled", {uPlayer = ...})` when it closes without a successful lock. (`MrxGuiSatellite` also posts a
  third event, `"Satellite Targetting Success"`, which this tutorial does not listen for.)
- `Event.TimerRelative` — 10-second completion delay in `SetupCompletionCriteria`.

## Notes for modders
- Trigger key: `"AirstrikeInterrupt"` (`MrxTutorialManager.StartTutorial("AirstrikeInterrupt")`), per
  [`MrxTutorialManager`](../resident/mrxtutorialmanager)'s tutorial catalog. This file self-arms via
  `SetupActivationCriteria`, so no external `StartTutorial` call is needed for normal activation.
- The event name is spelled `"Targetting"` (double T) in both this file and `MrxGuiSatellite` — that
  matches the shipped game's own string, not a decompiler artifact, so match it exactly if hooking into
  either event.
- No `SetupCancellationCriteria` override — inherits the base no-op, so once the "start" listener fires
  there's no explicit cancel path other than the completion timer / the health-check re-arm logic above.
