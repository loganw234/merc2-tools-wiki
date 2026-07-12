---
title: WifTutorialAlliesHonk
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 3
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialAlliesHonk

## Overview
Teaches the player to honk their vehicle horn to attract allied NPCs. It fires when the player, while
riding in any vehicle, comes within 500 units of one of five hardcoded per-faction world positions
while that faction currently has a friendly (positive) relation with the player's PMC.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: `MrxTutorialManager`, `MrxFactionManager` — **both declared, neither referenced anywhere in
  this file's body.** Only `Ai`, `Pg`, and `Debug` are actually called. Likely vestigial imports.

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. Module-level state, shared across all
instances (not per-`uGuid`):
- `tFactions`: fixed array of 5 faction name strings (`"OC"`, `"Pirate"`, `"Guerilla"`, `"Allied"`,
  `"China"`).
- `tPositions`: fixed array of 5 `{x, y, z}` world coordinates, index-aligned with `tFactions` —
  presumably each faction's home base/hub, though that's not stated in-file.

## Functions
### GetMessage()
Returns the fixed message key `"[Tutorial.VehicleHorn.Attract]"`.

### SetupActivationCriteria(self)
Calls `self:OnExitSeat()` to arm the initial state — treats the player as "not currently in a seat" and
sets up the enter-seat listener.

### OnEnterSeat(self)
Registers an `Event.ObjectInSeat` listener (seat `0`, filter `"a"`/`"x"`) that calls `OnExitSeat` when
the player leaves their seat. Then, for every faction in `tFactions`, calls `self:CreateEvent(uFaction)`
— arming all 5 per-faction proximity watchers at once.

### OnExitSeat(self)
Tears down all currently-registered events (`self:DestroyEvents()`), then registers an
`Event.ObjectInSeat` listener (seat `0`, filter `"d"`/`"e"`) that calls `OnEnterSeat` when the player
enters a seat.

### CreateEvent(self, uFaction)
Registers an `Event.ObjectProximity` watching whether the player is within 500 units of
`tPositions[uFaction]`. On trigger, calls `WithinRegion(self, uFaction)`.

### WithinRegion(self, uFaction)
Looks up `Ai.GetRelation(Pg.GetGuidByName(tFactions[uFaction]), Pg.GetGuidByName("PMC"))`. If the
relation is positive (`0 < fRelation`), activates the tutorial and logs the result via `Debug.Printf`.

## Events
- `Event.ObjectInSeat` (x2) — ping-pongs between `OnEnterSeat`/`OnExitSeat`. The enter-listener uses
  filter codes `"d"`/`"e"` and the exit-listener uses `"a"`/`"x"`; the exact meaning of these single-letter
  codes isn't confirmable from source alone, but the enter/exit ping-pong behavior itself is clear.
- `Event.ObjectProximity` (x5) — one per faction hub position, each independently able to fire
  `WithinRegion`.

## Notes for modders
- Trigger key: `"AlliesHonk"`. Self-arms via `SetupActivationCriteria`; no direct `StartTutorial` call
  site was found elsewhere in the corpus, nor is one needed.
- **No `SetupCompletionCriteria`/`SetupCancellationCriteria` override** — both fall back to the base
  class defaults, so once activated this auto-completes after the inherited **20-second** timer, not the
  10-second pattern most other tutorials in this category use.
- The 500-unit radius and the `0 < fRelation` friendliness threshold are the two tunables if you want to
  adjust range or require a stronger/weaker relationship before this fires.
