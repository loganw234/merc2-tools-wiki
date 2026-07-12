---
title: WifTutorialVehicleDisguise
parent: VZ Tutorials
grand_parent: VZ Modules
nav_order: 21
inherits: MrxTutorial
tags: [tutorial]
verified: false
---

# WifTutorialVehicleDisguise

## Overview
The other heavily stateful tutorial in this category, alongside
[`WifTutorialCollectibles`](wiftutorialcollectibles). Walks the player through the vehicle-disguise
mechanic via the engine's own `Player.VehicleDisguise` callback system rather than `Event.Create`,
alternating between two hint messages as disguise is toggled on and off, and only fully completing after
the player has toggled disguise off three times having seen both messages.

## Inheritance
- Inherits from: [`MrxTutorial`](../resident/mrxtutorial) (`src/resident/mrxtutorial.lua`) — a real corpus
  module, already documented under Resident Modules, not an opaque native-only engine class despite this
  file living in `src/vz/`.
- Imports: `MrxTutorialManager` (used — `UpdateCurrentTutorial`, `HideMessage`), `MrxFactionManager`
  (used — `GetInlineIcon`, `GetFactionStringAbbrev`).

## Instance pattern
A subclass of the corpus's `MrxTutorial` task-framework base class — `self`-based lifecycle overrides,
not the `Inheritable`/`uGuid` object pattern used in `resident/`. Nearly all state is module-level
(singleton-style, not per-`uGuid`):
- `msg`: current message key — `GetMessage()` returns this instead of a fixed string.
- `nLastDisguiseState`: tracks the last-seen disguise boolean (`-2` initial, `1`/`0` while active, `-1`
  after ending).
- `nCount`: counts "un-disguise" transitions since first activation; completion requires `nCount >= 3`.
- `oSelf`: a module-level stash of the active instance — needed because `DisguiseChangedCallback` is a
  bare function callback with no `self` parameter of its own.
- `bDisguised2Not`, `bNot2Disgusied` (typo in the name, as in-source): declared at module scope but
  **never referenced again anywhere else in the file** — dead fields.
- `bDisplayedMsgOne`, `bDisplayedMsgTwo`: assigned as bare globals with **no upfront `local`
  declaration**, unlike their sibling flags above. They still land as fields on this module's own
  environment table (each module file gets its own environment per this corpus's module system), not a
  true cross-module leak — just an inconsistent style choice.
- `_tEvents`: a module-level table declared separately from (and shadowing the name of) the base class's
  own per-instance `self._tEvents` — never populated or read again after its declaration; effectively
  dead.

## Functions
### GetMessage()
Returns the module-level `msg` variable.

### SetupActivationCriteria(self)
Registers a callback directly with the engine's `Player.VehicleDisguise` API (`{Player = uRider, Callback
= DisguiseChangedCallback}`) — the **only** tutorial in this batch that arms itself this way instead of
via `Event.Create`/`_CreateEvent`. Stashes `self` into the module-level `oSelf` and resets
`oSelf._bDoOnce`.

### DisguiseChangedCallback(playerGuid, nDisguiseState, uFaction)
The actual driver of this tutorial. Bails if `Player.GetVehicleDisguise()` is falsy or the rider has no
vehicle. Builds a faction icon string via `MrxFactionManager`. Reads the current disguise state (via the
same `tostring(bDisguiseState) == "true"/"false"` idiom seen in
[`WifTutorialGateHonk`](wiftutorialgatehonk)) to pick between two message keys —
`"[Tutorial.VehicleDisguise.Key1:<icon>]"` or `"...Key2:<icon>]"`. On the first successful read,
activates the tutorial; on later reads, refreshes the displayed message via
`MrxTutorialManager.UpdateCurrentTutorial` and, on "un-disguise" events, increments `nCount`. Once both
messages have been shown at least once and `nCount >= 3`, schedules a bare (untracked)
`Event.Create(Event.TimerRelative, {6}, EndTutorial, {oSelf, true})`; otherwise (re)schedules a bare
10-second timer to `HideDisguiseMessage`, canceling any prior pending one via `_oHideMessageEvent`.

### HideDisguiseMessage()
Calls `MrxTutorialManager.HideMessage(false, "VehicleDisguise")`.

### SetupCancellationCriteria(self)
Registers an `Event.ObjectInSeat` listener (via `self:_CreateEvent`, properly tracked in
`self._oCancelEvent`) on the rider's vehicle-at-setup-time for exiting (`"A"`, `"X"`) that calls
`self.EndTutorial(self, false)`.

### EndTutorial(self, bComplete)
Overridden: resets `nLastDisguiseState = -1`; if completing, calls `Player.VehicleDisguise({Player =
uRider, Remove = true})` to actually strip the disguise state; then calls
`MrxTutorial.EndTutorial(self, bComplete)`.

### SetupCompletionCriteria(self)
Empty — no timer-based completion at all. Completion is entirely driven by the counter logic inside
`DisguiseChangedCallback`.

## Events
- `Event.ObjectInSeat` — cancellation listener, properly tracked via `self:_CreateEvent`.
- Two **untracked** `Event.Create(Event.TimerRelative, ...)` calls inside `DisguiseChangedCallback` — the
  6-second pre-completion delay and the 10-second message-hide delay (`_oHideMessageEvent`). Their
  handles live in module-level globals rather than `self._tEvents`, so they bypass the base class's
  `DestroyEvents` cleanup.
- `Player.VehicleDisguise`'s own callback registration is the real activation "event," despite not going
  through the `Event` system at all.

## Notes for modders
- Trigger key: `"VehicleDisguise"`. Arms via `Player.VehicleDisguise`'s own callback mechanism, not
  `Event.Create`/`Event.ObjectProximity` like most of this category — if tracing how disguise-state
  changes reach this tutorial, start at `Player.VehicleDisguise`, not `Event`.
- `bDisguised2Not`/`bNot2Disgusied` are dead fields, safe to ignore.
- The two `Event.TimerRelative` handles inside `DisguiseChangedCallback` are **not** cleaned up by the
  base class's `DestroyEvents`/`EndTutorial` bookkeeping the way every other event in this file is —
  worth knowing if you see this tutorial's timers seemingly outlive a reset.
- Fully completes only after the player has toggled disguise off 3 times (`nCount >= 3`) having seen both
  hint messages at least once — a much longer, more stateful arc than the "single trigger + fixed timer"
  shape most other tutorials in this category use.
