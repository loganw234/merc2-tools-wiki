---
title: WifTutorialSwimming
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 17
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialSwimming

## Overview
Shown when the player's character enters a swimming state. Cancels if they climb back onto dry ground
or into a vehicle rather than completing naturally.

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
Returns the fixed message key `"[Tutorial.Swimming]"`.

### SetupActivationCriteria(self)
Registers an `Event.HumanStateTransition` listener on the local player (any state `"*"` →
`"Swim.*"`) that calls `self.ActivateTutorial(self, true)`.

### SetupCancellationCriteria(self)
Registers two `Event.HumanStateTransition` listeners on the local player, both calling
`self.EndTutorial(self, false)`: `"Swim.*"` → `"Upright.*"` (climbing out) and `"Swim.*"` →
`"InVehicle.*"` (boarding a vehicle while swimming).

## Events
- `Event.HumanStateTransition` (x3) — one wildcard-to-`Swim` transition activates; `Swim`-to-`Upright`
  and `Swim`-to-`InVehicle` both cancel.

## Notes for modders
- Trigger key: `"Swimming"`. Self-arms via `SetupActivationCriteria`.
- The wildcard state filters (`"*"`, `"Swim.*"`, `"Upright.*"`, `"InVehicle.*"`) suggest a dotted,
  hierarchical state-machine naming convention for player movement states; only entering/leaving the
  `"Swim.*"` subtree matters here.
- No `SetupCompletionCriteria` override — completes via the inherited **20-second** timer, so a player
  who just keeps swimming without surfacing or boarding a vehicle still has the message auto-clear after
  20 seconds.
