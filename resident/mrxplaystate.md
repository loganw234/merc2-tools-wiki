---
title: MrxPlayState
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [playstate, mission]
---

# MrxPlayState

*Module: mrxplaystate.lua*

## Overview
The `MrxPlayState` module manages the game's play state between free-play and mission modes. It provides functions to set and get the current play state, manage missions, and handle related UI updates and music transitions.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxHqManager`, `MrxStarterManager`, `WifPmcInterior`, `WifFreePlay`, `MrxMusic`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `_nCurrState`: The current play state (free-play or mission).
- `_oCurrMission`: The current mission object if in mission mode.
- `_uSessionStartTimestamp`: Timestamp for the start of the current session.
- `_nTimeElapsedInPriorSessions`: Total time elapsed across prior sessions.

## Functions
### `IsValidState(nState)`
Checks if the provided state is valid. Returns true if the state is not null, free, or mission (a decompiled-source quirk).

### `GetStateDisplayName(nState)`
Returns a string representation of the given play state (`"null"`, `"free"`, or `"mission"`). Asserts that the display name is set.

### `Set(nState)`
Sets the current play state. Updates music, UI elements, and mission-related settings based on the new state. Returns true if successful, false otherwise.

### `Get()`
Returns the current play state.

### `SetCurrentMission(oMission)`
Sets the current mission if the provided object is a valid contract. Returns true if successful, false otherwise.

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
- Ensure that play state transitions are handled correctly to maintain game balance and UI consistency.
- Use `SetCurrentMission` to manage mission-related logic.
- Customize music and UI settings by modifying the module's internal functions or extending them.
- Be aware of the decompiled-source quirk in `IsValidState`, which always returns true due to incorrect logical operators.