---
title: WifTutorialC4
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 6
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialC4

## Overview
Teaches basic C4 usage. Activates when the player equips a C4 charge that actually has reserve ammo,
cancels if they stow it again, and — unlike most tutorials in this category — has a real gameplay
completion condition (pulling the detonator trigger) layered on top of the inherited timeout fallback.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: none (uses the engine's `Human.Inventory`, `Weapon`, and `Object` namespaces directly)

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. No module-level or per-instance state
beyond what the base class itself tracks (`_tEvents`).

## Functions
### GetMessage()
Returns the fixed message key `"[Tutorial.C4]"`.

### SetupActivationCriteria(self)
Registers an `Event.WeaponEvent` listener for the player equipping `"c4"` that calls
`self.ActivateTutorial2(self)`.

### ActivateTutorial2(self)
Re-checks the equip: iterates `Human.Inventory.GetAllWeapons(uPlayer)`, and if any weapon both
`Object.HasLabel(weapon, "c4")` and has `Weapon.GetReserveAmmo(weapon) > 0`, activates the tutorial.
Otherwise (no C4 with reserve ammo found), re-arms by calling `self:SetupActivationCriteria()` again to
wait for the next equip.

### SetupCancellationCriteria(self)
Registers an `Event.WeaponEvent` listener for the player stowing `"weapon.c4"` that calls
`self.EndTutorial(self, false)`.

### SetupCompletionCriteria(self)
Registers an `Event.HumanStateTransition` listener (any state → `"Upright.TriggerDetonator"`) that calls
`self.EndTutorial(self, true)` — a real gameplay completion signal. It then also explicitly calls
`MrxTutorial.SetupCompletionCriteria(self)`, the base class's own 20-second fallback timer, as an
explicit "super" call — so both completion paths are armed simultaneously.

## Events
- `Event.WeaponEvent` (x2) — equipping `"c4"` triggers the reserve-ammo re-check; stowing
  `"weapon.c4"` cancels.
- `Event.HumanStateTransition` — transitioning into `"Upright.TriggerDetonator"` completes the tutorial.
- `Event.TimerRelative` — the inherited 20-second fallback from the explicit `MrxTutorial.
  SetupCompletionCriteria(self)` super-call.

## Notes for modders
- Trigger key: `"C4"`. Self-arms via `SetupActivationCriteria`.
- Completion here is layered, unlike most of this category: it ends on **whichever comes first** —
  the player actually triggering the detonator, or the inherited 20-second timeout.
- Equipping C4 alone isn't sufficient to activate — `ActivateTutorial2` double-checks reserve ammo via
  `Weapon.GetReserveAmmo`, so equipping an empty charge re-arms instead of activating.
