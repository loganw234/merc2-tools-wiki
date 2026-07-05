---
title: MrxState
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [state management, global lifecycle]
verified: true
verified_note: 'deeper pass: added the STATE_* enum (values 0-4), the exact log-marker strings (###!
  GlobalEnter/GlobalExit + @@@@@@@@@@ MrxState.Enter/Exit/StateComplete/AttemptGlobalExit), the fade-time
  constants, and precise refcount/global-lock semantics; re-confirmed Enter/Exit''s unconditional
  Debug.Printf(Debug.GetCallstack()) and corrected the Events section (GameStateChange is created only inside
  two states'' Enter closures, not a module-level subscription).'
---

# MrxState

*Module: mrxstate.lua*

## Overview
The `MrxState` module manages the global state transitions and lifecycle events in the game. It handles fading effects, player input suppression, and coordination of various states such as cinematic sequences, streaming, tethering, and game readiness. This module is crucial for ensuring smooth transitions between different gameplay phases.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxUtil`, `MrxGui`, `MrxSoundCategories`, `MrxVoSequence`, `MrxMunitionsPickup`, `MrxGuiInterface`

## Instance pattern
This is a stateless singleton module — no `Create`/`setmetatable`/`tInstance`/`uGuid`. All state lives in
module-level globals: the `_States` table (one entry per state, each holding its own `nRefCount`, `bLocked`,
`Enter`/`Exit` closures, and callback queues), plus the global-lock/fade flags (`_bGloballyLocked`,
`_bGloballyFading`, `_bStateComplete`) and the two global callback queues (`_tGlobalEnterCallbacks`,
`_tGlobalExitCallbacks`).

## Module constants
Confirmed at the top of the source:

**State enum** (the `nState` argument every `Enter`/`Exit`/`SafeEnter`/etc. takes):

| Constant | Value | `sName` in `_States` | Enter behavior |
| --- | --- | --- | --- |
| `STATE_NONE` | `0` | — (no `_States` entry) | not a real state; sentinel only |
| `STATE_CINEMATIC` | `1` | `"STATE_CINEMATIC"` | completes immediately (`_StateComplete`) |
| `STATE_WAITFORSTREAMING` | `2` | `"STATE_WAITFORSTREAMING"` | `Sys.RequestGameState("WaitForStreaming")`, then waits for the `"WaitForStreaming"` `"exit"` `Event.GameStateChange` |
| `STATE_WAITFORTETHER` | `3` | `"STATE_WAITFORTETHER"` | `Sys.RequestGameState("WaitForTether")`, waits for the `"WaitForTether"` `"exit"` game-state change |
| `STATE_WAITFORGAME` | `4` | `"STATE_WAITFORGAME"` | completes immediately (`_StateComplete`) |

{: .note }
> `STATE_NONE = 0` has no entry in `_States`, so `Enter(STATE_NONE, ...)` / `GetStateName(STATE_NONE)` return
> `false`/`nil` — it's a sentinel, not a usable state. The four usable states are `1`–`4`.
> `STATE_WAITFORSTREAMING` (2) is the one the mission-load path enters/exits: [`WifMissionFlow.UnlockMission`](mrxmissionflow)
> calls `MrxState.Enter(MrxState.STATE_WAITFORSTREAMING, oMission.Activate, ...)` and the mission's
> `fOnAssetsLoaded` calls `MrxState.Exit(STATE_WAITFORSTREAMING)` + `Exit(STATE_WAITFORGAME)`.

**Fade timing constants** (seconds; used by `_GlobalEnter`/`_GlobalExit`):
`_nQuickFadeOutTime = 0.1`, `_nQuickFadeInTime = 0.5`, `_nLongFadeOutTime = 1.1`, `_nLongFadeInTime = 1.1`.
`_bEnableFade` (default `true`) and `_bUseQuickFade` (default `false`) gate whether a fade happens and which
timing pair is used.

## Log markers (load-probe / diagnostics)
This module emits the world-load / state-transition markers that log-analysis tooling keys on. Exact strings,
confirmed from source:

- **Global transition** (prefix `###!`): `"###! GlobalEnter - Begin"` (start of `_GlobalEnter`),
  `"###! GlobalEnter - Complete"` (end of `_CompleteEnter` **and** end of `_GlobalExit`'s fade-in timer —
  note this string is printed in two places), `"###! GlobalExit - Begin"` (start of `_GlobalExit`),
  `"###! GlobalExit - Complete"` (end of `_GlobalExit`'s fade-in timer).
- **State/refcount** (prefix `@@@@@@@@@@ MrxState.`): each line embeds `GetStateName(nState)` and the current
  `nRefCount`:
  - `Enter`: `"@@@@@@@@@@ MrxState.Enter: state <NAME> (refcount=<n>)"` — printed **after** the increment.
  - `Exit`: `"@@@@@@@@@@ MrxState.Exit: state <NAME> (refcount=<n>)"` — printed **after** the decrement; the
    unpaired case instead prints `"@@@@@@@@@@ MrxState.Exit: UNPAIRED EXIT to state <NAME>"`.
  - `_StateComplete`: `"@@@@@@@@@@ MrxState._StateComplete:  state <NAME>, about to _AttemptGlobalExit"`.
  - `_AttemptGlobalExit`: `"@@@@@@@@@@ MrxState._AttemptGlobalExit"`, then one of
    `"... not globally locked, bailing out"`, `"...  state <NAME> still active .. (refcount=<n>,bLocked=<b>)"`,
    or `"... all states exited; success"`.
- Both `Enter` and `Exit` also call `Debug.Printf(Debug.GetCallstack())` on the line immediately after their
  refcount line — see the per-function notes below.

{: .warning }
> Other tooling (the `loadprobe` log analyzer) matches these exact strings to decide how far the world-load
> got. Do not change the marker text if you hook or wrap `Enter`/`Exit`/`_GlobalEnter`/`_GlobalExit`, and
> avoid suppressing them — downstream analysis depends on them appearing verbatim.

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
Increments `_States[nState].nRefCount` and enters/re-enters the state. Returns `false` for an unknown
`nState`. The four callback args each accept the literal string `"nil"` as a stand-in for `nil` (so they can
survive being requeued through `_tGlobalEnterCallbacks` while a fade is in progress — if `_bGloballyFading`
is set, the whole call is deferred into that queue and returns `false`). On the **first** state entered
(when neither `_bGloballyLocked` nor `_bGloballyFading` is set) it takes the global lock, sets the fading
flag, and kicks off `_GlobalEnter(_CompleteEnter, ...)` (the fade-out). Subsequent `Enter` calls while
already locked just queue their callbacks and bump the refcount.

- **Confirmed: calls `Debug.Printf(Debug.GetCallstack())` unconditionally on every non-deferred invocation**
  (the line right after the refcount log), in addition to the state-name/refcount marker line. Worth knowing
  before wrapping this function heavily or calling it in a tight loop — it's a real, if minor, per-call cost,
  and it's the highest-frequency function in this file to log through if you're also bracketing it with your
  own diagnostic wrapper for an unrelated investigation (stacking enough hooks near `Enter`/`Exit` was one
  contributing factor in a real crash encountered while debugging a separate briefing-flow issue — see the
  [Custom Contract deep dive](../deep-dives/custom-contract)).

### `_CompleteEnter(tStateData)`
Completes the enter transition by calling the state's enter function and processing any queued enter callbacks. Logs `###! GlobalEnter - Complete`.

### `Exit(nState, fCallback, tCallbackData)`
Decrements `_States[nState].nRefCount`. **Unpaired-exit guard:** if the refcount is already `<= 0`, it logs
`"UNPAIRED EXIT to state <NAME>"`, calls `fCallback` immediately, and returns `false` without decrementing —
so an over-Exit is a no-op with a warning, not an underflow. Queues `fCallback` into `_tGlobalExitCallbacks`
(to run after the eventual `_GlobalExit` fade-in), and only when the refcount hits **exactly 0** does it call
that state's `Exit()` closure, then `_AttemptGlobalExit()`. Like `Enter`, if `_bGloballyFading` is set the
call is deferred into `_tGlobalEnterCallbacks` instead. `_AttemptGlobalExit` runs the real global exit
(fade-in + `_tGlobalExitCallbacks`) only once **every** state's `nRefCount` is 0 and no state is `bLocked`.

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

### `_StateComplete(nState)`
The "ready to exit" trigger for a state — runs its `tReadyToExitCallbacks` and then `_AttemptGlobalExit()`.
Clears the state's `bLocked` flag. **`STATE_WAITFORTETHER` is special-cased**: its refcount is forced to `0`
here (it can be entered multiple times but a single tether resolution clears them all at once).

### `SafeEnter(nState)` / `SafeEnterCallback(nState)` / `SafeExit(nState)`
A deferred-exit wrapper for the case where an `Exit` might arrive *before* its matching `Enter` has finished.
`SafeEnter` calls `Enter(nState, SafeEnterCallback, {nState})` and increments the state's `safeEnterCount`
when the enter completes. `SafeExit` either consumes one pending safe-enter (decrement `safeEnterCount` +
real `Exit`) or, if none is pending yet, increments `forceExitCount` — a "you owe me an exit" tally that
`SafeEnterCallback` pays down as safe-enters complete. Use this pair instead of raw `Enter`/`Exit` when the
enter/exit ordering isn't guaranteed.

### `AddGlobalExitCallback(fCallback, tCallbackArgs)`
Registers a callback to fire on the next global exit. **If the game is not currently `_bGloballyLocked`, it
runs the callback immediately instead of queuing it** — confirmed used by
[`MrxTaskContract.AssetsLoaded`](mrxtaskcontract) to run a contract's `Activated` right after its assets
finish loading, whether or not a load transition is in flight.

## Events
- **No module-level `Event.*` subscription.** The only `Event.Create(Event.GameStateChange, ...)` calls live
  inside the `Enter` closures for `STATE_WAITFORSTREAMING` and `STATE_WAITFORTETHER`, each wired to
  `_StateComplete` for that state — they exist only while those states are active, not as a persistent
  listener. (The previous version of this page implied a standing `GameStateChange` subscription; corrected.)
- `Event.TimerRelative` is used by `_GlobalEnter`/`_GlobalExit` to time the fades (using the fade-timing
  constants above) — these are one-shot scheduled timers, not subscriptions.

## Notes for modders
- **Do not alter or suppress the log markers** listed above — the `loadprobe` tool matches them verbatim to
  classify how far a world-load got. This is the single most important thing to preserve in this file.
- The refcount is per-state and additive: N `Enter`s on the same state need N `Exit`s before that state
  clears. A global exit (fade back in) only happens once **all four** states are at refcount 0 — a single
  stuck `Enter` anywhere holds the whole game in the faded/locked state. If a load appears to hang faded-out,
  a state left at refcount > 0 is the first thing to check (`PrintStatus()` dumps every active state).
- `SetQuickFade(true)` before an `Enter` swaps the 1.1s long fade for the 0.1s/0.5s quick fade for that
  transition; `EnableFade(false)` skips the visual fade entirely (still honors the timing for sequencing).
- Prefer `SafeEnter`/`SafeExit` over raw `Enter`/`Exit` when an exit can race ahead of its enter.