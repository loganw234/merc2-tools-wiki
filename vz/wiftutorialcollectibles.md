---
title: WifTutorialCollectibles
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 9
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialCollectibles

## Overview
The most stateful tutorial in this category. Walks the player through picking up `"SpareParts"`-labeled
collectibles with two successive hint messages, ten seconds apart, triggered by proximity to any such
object, and only fully completes once both messages have been shown.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: `MrxTutorialManager` (used — `UpdateCurrentTutorial`, `HideMessage`), `MrxFactionManager`
  (declared, **never referenced** anywhere in this file's body).

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. Unusually, nearly all of its state is
module-level (shared across instances, singleton-style) rather than per-`self`:
- `msg`: the current message key — `GetMessage()` returns this instead of a fixed string, unlike most
  other tutorials in this category.
- `nCount`: index into `msgtable` (starts at 1, advances to 2, then beyond triggers completion).
- `bActivated` / `bMessageShowing`: activation/display-state flags.
- `msgtable`: the fixed 2-entry array of message keys (`"[Tutorial.Collectibles]"`,
  `"[Tutorial.Collectibles2]"`).
- `eventHandle`: the pending hide/end timer handle.
- `uFilter` / `uEvent`: the `ObjectFilter` and its proximity-event handle — reassigned (not
  re-declared `local`) each time `SetupActivationCriteria` runs, to support tearing down and
  re-registering.

## Functions
### GetMessage()
Returns the module-level `msg` variable (mutable), not a fixed string.

### SetupActivationCriteria(self)
Tears down any previous `uEvent`; creates an `ObjectFilter` matching label `"SpareParts"`; registers an
`Event.ObjectProximity` (filtered objects within 5 units of the player) that calls `ShowMessage`.

### ShowMessage(self)
On the first proximity hit, activates the tutorial (`bActivated = true`). If activated and no message
is currently showing, sets `msg = msgtable[nCount]`, pushes it via
`MrxTutorialManager.UpdateCurrentTutorial(self, true)`, and arms a 10-second timer to `HideMessage`.

### HideMessage(self)
Calls `MrxTutorialManager.HideMessage(false, "Collectibles")`, then advances `nCount`. Once `nCount`
exceeds 2 (both messages have been shown), arms a final 10-second timer to the file's own `EndTutorial`
(`bComplete = true`). Otherwise, calls `SetupActivationCriteria(self)` again to wait for the next
proximity hit and show the second message.

### SetupCompletionCriteria(self)
Empty — no timer-based completion. Completion is entirely driven by the `HideMessage`/`nCount` chain
above.

### EndTutorial(self, bComplete)
Overridden: clears `eventHandle` and resets `bMessageShowing`, then calls
`MrxTutorial.EndTutorial(self, bComplete)`.

## Events
- `Event.ObjectProximity` — any `"SpareParts"`-labeled object within 5 units of the player.
- `Event.TimerRelative` — reused for both the 10-second per-message hide delay and the final
  pre-completion delay.

## Notes for modders
- Trigger key: `"Collectibles"`. Self-arms via proximity.
- The two hint messages are shown 10 seconds apart on the first two proximity triggers; the tutorial
  only completes for good after both have displayed at least once.
- `msg`, `nCount`, `bActivated`, `bMessageShowing`, and `eventHandle` are module-level, not per-`uGuid` —
  consistent with this being a singleton tutorial rather than a per-object one.
- `MrxFactionManager` is imported but never used anywhere in this file — likely vestigial.
- Minor inconsistency spotted: `ShowMessage` assigns to a bare `bResult` (no `local`) in one branch, then
  declares a *separate*, properly-scoped `local bResult` later in the same function. Harmless (the first
  value is never read again) but worth knowing if tracing this function's state.
