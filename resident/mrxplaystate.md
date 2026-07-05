---
title: MrxPlayState
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [playstate, mission]
verified: true
verified_note: 'deeper pass: added the _kn* state-constant values (-1/0/1) + cross-links; re-confirmed the
  IsValidState always-true bug and SetCurrentMission''s IsContract() gate against source; Events/Instance-
  pattern/function-list all still accurate.'
---

# MrxPlayState

*Module: mrxplaystate.lua*

## Overview
The `MrxPlayState` module manages the game's play state between free-play and mission modes. It provides functions to set and get the current play state, manage missions, and handle related UI updates and music transitions.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxHqManager`, `MrxStarterManager`, `WifPmcInterior`, `WifFreePlay`, `MrxMusic`

## Instance pattern
This is a stateless singleton module (module-level globals, no `Create`/`uGuid`). It tracks:
- `_nCurrState`: The current play state — one of the state constants below.
- `_oCurrMission`: The current mission object if in mission mode.
- `_uSessionStartTimestamp`: Timestamp for the start of the current session.
- `_nTimeElapsedInPriorSessions`: Total time elapsed across prior sessions.

## Module constants
The three play-state values (the `nState` passed to `Set`/compared by `Get`/`IsFree`):

| Constant | Value | `GetStateDisplayName` |
| --- | --- | --- |
| `_knNull` | `-1` | `"null"` |
| `_knFree` | `0` | `"free"` |
| `_knMission` | `1` | `"mission"` |

Entering `_knMission` is done via `Set(MrxPlayState._knMission)` — confirmed called by
[`MrxTaskContract.Activated`](mrxtaskcontract) when a contract starts (which also calls `SetCurrentMission`
with itself). Returning to `_knFree` is what [`WifMissionFlow`](mrxmissionflow)'s container
complete/cancel handlers do at the end of a contract.

## Functions
### `IsValidState(nState)`
Intends to check if `nState` is one of the three known states. Implemented as `nState ~= _knNull or nState ~= _knFree or nState ~= _knMission`. **Confirmed bug:** for any single value of `nState`, it can match at most one of the three constants, so at least two of the three `~=` comparisons are always true — the `or` chain evaluates to `true` unconditionally, for every input including garbage values. This looks like an `and`/`or` mix-up (De Morgan's law error): the intended check was almost certainly `nState == _knNull or nState == _knFree or nState == _knMission`.

### `GetStateDisplayName(nState)`
Returns a string representation of the given play state (`"null"`, `"free"`, or `"mission"`). Asserts that the display name is set.

### `Set(nState)`
Sets the current play state. Updates music, UI elements, and mission-related settings based on the new state. Returns true if successful, false otherwise.

### `Get()`
Returns the current play state.

### `SetCurrentMission(oMission)`
Sets `_oCurrMission` only if `oMission.IsContract` exists **and** `oMission:IsContract()` returns true —
so jobs (which return `false` from `IsContract`) are rejected here; the "current mission" tracked by this
module is specifically the active contract. Returns true on success, false (with a debug log) otherwise.

### `GetCurrentMission()`
Returns the current mission object.

### `IsFree()`
Checks if the current play state is free-play.

### `Reset()`
Resets the play state to null and clears the current mission. Reverts music settings and destroys all starters.

### `_UpdateHqObjectiveMarkers()`
Updates UI display for HQ objectives based on current starters and PMCs.

### `GetTotalTimeElapsed()`
Calculates the total time elapsed across prior sessions and the current session.

### `StartSessionTimer()`
Starts a new session timer by setting the start timestamp.

### `GetSessionTimer()`
Returns the session start timestamp.

### `SetTimeElapsedInPriorSessions(n)`
Sets the total time elapsed in prior sessions.

### `GetTimeElapsedInPriorSessions()`
Returns the total time elapsed in prior sessions.

## Events
- None

## Notes for modders
- **`Set` has real side effects beyond storing the value:** switching to `_knFree` clears `_oCurrMission`,
  starts freeplay music ([`MrxMusic.EnterFreeplayMusic`](mrxmusic)) and the freeplay nag; switching to any
  other state stops the nag. It also toggles whether the PDA map allows changing the tracked mission
  (`Pda.Map:SetMissionChangeAllowed` — only allowed in free-play) and refreshes HQ objective markers. `Set`
  no-ops (returns false) if the requested state equals the current one.
- **`IsValidState` always returns `true`** (see its entry) — because of this, `Set` never rejects an `nState`
  as invalid; the only reason `Set` returns false is the "already in this state" check.
- **`GetTotalTimeElapsed`** falls back to `Sys.MainTime()` if the prior/this-session numbers aren't both
  numbers — safe to call before `StartSessionTimer` has run.
- **`Reset`** does more than clear state: it re-enters freeplay music and calls
  [`MrxStarterManager.DestroyAllStarters`](mrxstartermanager). Call it on teardown, not mid-mission.