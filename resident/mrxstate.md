---
title: MrxState
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [state management, global lifecycle]
verified: true
verified_note: confirms Enter/Exit's unconditional Debug.Printf(Debug.GetCallstack()) calls directly from
  source, found while debugging a real briefing-flow crash — see the
  [Custom Contract deep dive](../deep-dives/custom-contract).
---

# MrxState

*Module: mrxstate.lua*

## Overview
The `MrxState` module manages the global state transitions and lifecycle events in the game. It handles fading effects, player input suppression, and coordination of various states such as cinematic sequences, streaming, tethering, and game readiness. This module is crucial for ensuring smooth transitions between different gameplay phases.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxUtil`, `MrxGui`, `MrxSoundCategories`, `MrxVoSequence`, `MrxMunitionsPickup`, `MrxGuiInterface`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance data but manages global state transitions and events.

## Functions
### `_GlobalEnter(fComplete, tData)`
Handles the global enter transition by fading out, ducking audio, suppressing player input, and setting characters invincible. Logs `###! GlobalEnter - Begin` and `###! GlobalEnter - Complete`.

### `_GlobalExit()`
Handles the global exit transition by fading in, restoring player input, and running global-exit callbacks. Logs `###! GlobalExit - Begin` and `###! GlobalExit - Complete`.

### `Reset()`
Resets various internal flags and callback tables to their initial states.

### `_StateComplete(nState)`
Completes a state transition by calling the state's exit function and attempting a global exit if all states are exited. Logs detailed debug information about the state completion process.

### `Enter(nState, fEnterCompleteCallback, tEnterCompleteCallbackData, fReadyToExitCallback, tReadyToExitCallbackData)`
Enters a specified state, increments its reference count, and sets up callbacks for when the state is complete or ready to exit. Handles global locking and fading if necessary.

- **Confirmed: calls `Debug.Printf(Debug.GetCallstack())` unconditionally on every single invocation** (line
  224 of `mrxstate.lua`), in addition to a state-name/refcount log line just before it. Worth knowing before
  wrapping this function heavily or calling it in a tight loop — it's a real, if minor, per-call cost, and
  it's the highest-frequency function in this file to log through if you're also bracketing it with your
  own diagnostic wrapper for an unrelated investigation (stacking enough hooks near `Enter`/`Exit` was one
  contributing factor in a real crash encountered while debugging a separate briefing-flow issue — see the
  [Custom Contract deep dive](../deep-dives/custom-contract)).

### `_CompleteEnter(tStateData)`
Completes the enter transition by calling the state's enter function and processing any queued enter callbacks. Logs `###! GlobalEnter - Complete`.

### `Exit(nState, fCallback, tCallbackData)`
Exits a specified state by decrementing its reference count and calling the exit callback if the reference count reaches zero. Attempts a global exit if all states are exited.

- **Confirmed: also calls `Debug.Printf(Debug.GetCallstack())` unconditionally on every call**, both the
  normal case and the "unpaired exit" warning case — same caution as `Enter` above.

### `_AttemptGlobalExit()`
Attempts to perform a global exit if no states are active and the game is not globally locked. Logs detailed debug information about the attempt.

### `_GetTotalRefCount()`
Returns the total reference count across all states.

### `IsLocked()`
Checks if the game is globally locked.

### `SetQuickFade(bEnable)`
Enables or disables quick fading effects.

### `EnableFade(bEnable)`
Enables or disables global fade effects.

### `PrintStatus()`
Logs the current status of all states, indicating which are active.

### `GetStateName(nState)`
Returns the name of a specified state.

### `SafeEnterCallback(nState)`
Handles safe entry callbacks by managing enter and exit counts.

### `SafeEnter(nState)`
Safely enters a state by setting up a callback to handle potential exits.

### `SafeExit(nState)`
Safely exits a state by decrementing the safe enter count or incrementing the force exit count.

### `AddGlobalExitCallback(fCallback, tCallbackArgs)`
Adds a global exit callback that will be executed when all states are exited.

## Events
- Listens for `Event.GameStateChange` to handle state transitions.
- Triggers `Event.TimerRelative` for fade-in and fade-out timing.

## Notes for modders
- Ensure proper handling of state transitions using `Enter` and `Exit` functions.
- Use `SetQuickFade` and `EnableFade` to control fading effects during global transitions.
- Be aware of the reference count mechanism to avoid unpaired exits.
- Utilize `SafeEnter` and `SafeExit` for safer state management in complex scenarios.