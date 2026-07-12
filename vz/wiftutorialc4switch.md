---
title: WifTutorialC4Switch
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 7
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialC4Switch

## Overview
A narrower, separate C4 tutorial about the detonator switch itself. Activates as soon as the player
picks up a C4 charge and completes as soon as they equip C4 — there is no timer involved in either
direction.

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
Returns the fixed message key `"[Tutorial.C4Switch]"`.

### SetupActivationCriteria(self)
Registers a **persistent** `Event.WeaponEvent` listener (`_CreatePersistentEvent`, not the plain
`_CreateEvent` most other tutorials use for activation) for the player picking up `"C4 Pickup"`, calling
the bare global `ActivateTutorial` — which resolves through inheritance to `MrxTutorial.ActivateTutorial`
since this file doesn't define its own; equivalent in effect to `self:ActivateTutorial(true)` since
`self` is passed explicitly in the callback args.

### SetupCompletionCriteria(self)
Registers an `Event.WeaponEvent` listener for the player equipping `"c4"` that calls
`self.EndTutorial(self, true)`. No timer of any kind is involved — completion is purely event-driven.

## Events
- `Event.WeaponEvent` (x2) — a persistent listener for picking up `"C4 Pickup"` arms the tutorial; a
  plain listener for equipping `"c4"` completes it.

## Notes for modders
- Trigger key: `"C4Switch"`. Self-arms via `SetupActivationCriteria`, using a *persistent* event for
  activation — see [`MrxTutorial`](../resident/mrxtutorial) for what `_CreatePersistentEvent` guarantees
  versus the plain `_CreateEvent` most other tutorials in this category use.
- No `SetupCancellationCriteria` override (inherited no-op), and no timer-based completion at all — this
  tutorial only ever ends by the player equipping C4 (or via an external manager call).
- Distinct from, and presumably shown around the same time as, [`WifTutorialC4`](wiftutorialc4) — that
  one is keyed on reserve ammo and detonator use, this one on the pickup-then-equip sequence.
