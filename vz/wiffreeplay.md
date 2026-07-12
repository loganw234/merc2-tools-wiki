---
title: WifFreePlay
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 8
inherits: none
tags: [world-flow]
verified: false
---

# WifFreePlay

## Overview
`WifFreePlay` is Fiona's freeplay "idle nag" system — a repeating, self-rescheduling timer that, once
armed, periodically checks whether the player is idling in freeplay with an available hint queued up,
and if so, plays a short VO line prompting them to go check it out. It's a small, self-contained example
of the timer-driven "ambient VO" pattern used throughout the campaign.

## Inheritance
- Inherits from: none — singleton utility module.
- Imports: `MrxActionHijack`, `MrxHqManager`, `MrxPlayState`, `MrxUtil`, `MrxVoSequence`,
  [`WifHints`](wifhints), [`WifPmcInterior`](wifpmcinterior).

## Instance pattern
Singleton-state manager. Module-level fields: `_bNagEnabled` (is the system armed at all),
`_bNagInProgress` (a VO line is actively playing right now), `_uNagTimer` (the current pending
`Event.TimerRelative` handle).

## Functions
### `StartNag()`
No-ops if already enabled; otherwise sets `_bNagEnabled = true` and arms the first timer at
`_knInitialDelay` (60s).

### `StopNag()`
No-ops if not enabled; otherwise stops any in-progress VO
(`MrxVoSequence.Stop(nil, nil, MrxVoSequence.knPriorityFreeplay)`), deletes the pending timer, and clears
`_bNagEnabled`.

### `IsNagEnabled()`
Plain `_bNagEnabled == true`.

### `_CreateNagTimer(nTime)`
Deletes any existing timer, then either arms a new `Event.TimerRelative` for `_Nag` in `nTime` seconds (if
`_TestNagConditions()` currently passes) or calls `StopNag()` outright if conditions no longer hold.

### `_DeleteNagTimer()`
Deletes `_uNagTimer` if set.

### `_Nag()`
The timer callback. If a VO sequence of any kind is already playing
(`MrxVoSequence.IsSequenceInProgress()`), reschedules itself after `_knRetryDelay` (30s) instead of
stepping on it. Otherwise re-checks `_TestNagConditions()`, bails via `StopNag()` if they've stopped
holding, and otherwise picks a random line from `{"Fiona.Misc.NoState01", "Fiona.Misc.NoState02"}` and
starts it through `MrxVoSequence.Start(..., MrxVoSequence.knPriorityFreeplay)`. If the VO system rejects
the start (e.g. pre-empted by something higher priority), retries after `_knRetryDelay` instead of waiting
the full cycle.

### `_NagComplete()`
The VO-finished callback; clears `_bNagInProgress` and reschedules the next nag after
`_knSubsequentDelay` (600s / 10 minutes).

### `_TestNagConditions()`
The actual gate: not already mid-VO, `MrxPlayState.IsFree()` (not in a mission/cutscene), not
`MrxActionHijack.IsInHijack()`, not `MrxHqManager.IsInside()`, not `WifPmcInterior.IsInside()`, and
`WifHints.HasHint("Fiona")` (there's actually a hint queued up worth nagging about).

## Events
`Event.TimerRelative` only, via `_CreateNagTimer`/`_Nag` — the entire timer chain is self-rescheduling
rather than a single repeating interval.

## Notes for modders
- **Tunables:** `_knInitialDelay = 60` (first nag after `StartNag()`), `_knSubsequentDelay = 600` (gap
  between successful nags), `_knRetryDelay = 30` (retry gap when blocked by another VO sequence or
  conditions not yet met) — all local to this file, so changing them means editing this module directly
  rather than overriding from outside.
- Externally controlled by `resident/mrxactionhijack.lua`, `resident/mrxhq.lua`,
  `resident/mrxplaystate.lua`, [`WifHints`](wifhints), and [`WifPmcInterior`](wifpmcinterior), all of
  which `import("WifFreePlay")` — [`WifHints`](wifhints)' `AddActiveHint` specifically calls
  `WifFreePlay.StartNag()` every time a new hint becomes active, so the nag system is normally kept alive
  automatically as hint content accumulates rather than needing a manual `StartNag()` call from mission
  code.
- The nag only ever plays if `WifHints.HasHint("Fiona")` is true — this file only knows about Fiona's
  hint pool specifically, not any other speaker's.
