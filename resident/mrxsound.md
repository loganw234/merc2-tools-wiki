---
title: MrxSound
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, sound]
verified: true
verified_note: "deeper pass: re-confirmed all 30 functions + the single Event.GameStateChange subscription against source; pruned vacuous 'call things appropriately' notes; documented the survival-mode sound cue (sfx_survival_lp) and the shell/ui bank set loaded by EnterShellState; cross-linked MrxMusic/MrxSoundCategories/MrxSoundBanks and the Sound namespace"
---

# MrxSound

*Module: mrxsound.lua*

## Overview
The `MrxSound` module is responsible for managing audio-related functionalities in the game. It handles transitions between different music states, manages sound banks and wave banks, and controls various one-shot sound effects. This module ensures that the audio system is properly initialized and synchronized with the game's state changes.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: [`MrxMusic`](mrxmusic), [`MrxSoundCategories`](mrxsoundcategories), [`MrxSoundBanks`](mrxsoundbanks)

This module is the high-level **state façade** over the audio system: game states (shell, pause,
cinematic, PDA, attract, interior, transit, satellite/scope view, action-hijack, survival) each get an
`Enter…`/`Exit…` pair that orchestrates the three imported modules plus the engine's own
[`Sound`](../namespaces/sound) namespace. It holds almost no data of its own — it delegates.

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages global audio
settings and transitions. A few module-level flags gate behavior: `_bExitingGame`, `_bSurvivalModeStarted`,
`_bSoundSystemReady`, `_bWaitForSoundAssets`, and the one-shot callback `_funcSoundReadyCallback`.

## Functions
### `EnterShellState()`
Sets master volume to full, transitions music to `"silence"`, calls `MrxSoundBanks._LoadRequiredAssetsCommon()`,
then loads six banks — the `"ui_shell"`, `"ui_hud"`, and `"music"` sound- **and** wave-banks — each with
`_StartShellMusic` as the batch-complete callback (so shell music starts only once every bank finishes loading).

### `ExitShellState()`
Exits the shell state by unloading sound banks, resetting the master volume, and transitioning to silence.

### `_StartShellMusic()`
A helper function that starts the shell music after all sound banks are loaded.

### `_SetupGameExit()`
Sets up an event listener for game state changes to handle the exit process.

### `ExitGame()`
Handles the game exit by reducing the master volume and setting a flag indicating the game is exiting.

### `ExitingGame()`
Returns whether the game is currently in the process of exiting.

### `EnterPauseState()`
Enters the pause state by transitioning to the "pause" music state and disabling dynamic music.

### `ExitPauseState()`
Exits the pause state by restoring dynamic music and transitioning to silence.

### `EnterCinematicState()`
Enters the cinematic state by disabling dynamic music.

### `ExitCinematicState()`
Exits the cinematic state by restoring dynamic music.

### `EnterPDAState()`
Enters the PDA (Personal Data Assistant) state by disabling dynamic music and stopping timer updates for music.

### `ExitPDAState()`
Exits the PDA state by restoring dynamic music and enabling timer updates for music.

### `EnterAttractState()`
Enters the attract state by disabling dynamic music.

### `ExitAttractState()`
Exits the attract state by enabling dynamic music.

### `BeginActionHijack(bUseHijackMusic)`
Begins an action hijack by fading in the "actionhijack" category and transitioning to the "hijack" music state if specified.

### `EndActionHijack(bUseHijackMusic, bSuccess)`
Ends an action hijack by transitioning to either "hijack_success" or "action" music states based on success status and fading out the "actionhijack" category.

### `BeginSurvivalMode()`
Calls `Sound.SetSurvivalMode(true)`, fades in the `"survivalmode"` category, plays the looped cue
`Sound.CueSound(0, "sfx_survival_lp")`, applies the survival-mode pitch bend, and sets `_bSurvivalModeStarted`.

### `EndSurvivalMode()`
Guarded on `_bSurvivalModeStarted` (no-op if survival mode was never started). Clears survival mode, fades
the `"survivalmode"` category back out, stops the looped `"sfx_survival_lp"` cue via `Sound.StopSound(0, …)`,
and restores pitch. The `0` first arg to `CueSound`/`StopSound` is the sound-slot handle both calls share.

### `EnterInterior()`
Enters an interior by resetting music, locking action level music, and transitioning to silence.

### `ExitInterior()`
Exits an interior by unlocking action level music and transitioning back to the "explore" music state.

### `BeginTransit()`
Begins transit by transitioning to silence.

### `EndTransit()`
Ends transit by resuming special music if playing, otherwise transitioning back to the "explore" music state.

### `EnterSatelliteView()`
Enters satellite view by fading in the "satelliteview" category and locking the listener position.

### `ExitSatelliteView()`
Exits satellite view by unlocking the listener position and fading out the "satelliteview" category.

### `EnterScopeView()`
Enters scope view by locking the listener position.

### `ExitScopeView()`
Exits scope view by unlocking the listener position.

### `_FlagSystemReady()`
Flags the sound system as ready and checks if it is fully initialized.

### `SetSoundReadyFunc(funcSoundReady, bWaitForSoundAssets)`
Sets a callback function to be called when the sound system is ready. Optionally waits for all sound assets to load before calling the callback.

### `_CheckSoundReady()`
Checks if the sound system is ready and calls the registered callback if conditions are met.

### `Initialize()`
The bring-up entry point: calls `MrxMusic._InitializeMusic()` (registers every music state/cue with the
engine — see [MrxMusic](mrxmusic)), `MrxSoundCategories._AdditionalFadeSetup()` (registers the credits
sfx/vo fades), and `_SetupGameExit()` (wires the game-exit volume fade). Must run before the state
`Enter…`/`Exit…` functions are meaningful.

## Events
Only one real `Event.*` reference exists in this file:
- `_SetupGameExit()` calls `Event.Create(Event.GameStateChange, {"unloading", "enter"}, ExitGame)` —
  subscribes `ExitGame` (defined in this file) to fire when the game state transitions to `"unloading"`
  `"enter"`.

Sound-asset/system-readiness notification is **not** event-based — it's a plain callback registered via
`Sound.RegisterReadyCallback(_FlagSystemReady)` in `SetSoundReadyFunc`. `_FlagSystemReady` is defined in
this file, so there's no undefined-callback issue.

## Notes for modders
- `Initialize()` is the required bring-up call; the `Enter…`/`Exit…` state functions are the actual
  levers — pair them (every `Enter` has a matching `Exit`). Leaving a state un-exited leaves dynamic
  music disabled or the listener position locked.
- Swap the survival-mode loop by changing the cue string `"sfx_survival_lp"` in `BeginSurvivalMode`/
  `EndSurvivalMode` (both must match — one cues, one stops the same slot `0`).
- The shell bank set is hardcoded in `EnterShellState`/`ExitShellState`: `"ui_shell"`, `"ui_hud"`,
  `"music"` (each loaded as both a sound- and wave-bank). Add a bank here if a shell mod needs extra audio.
- `_bExitingGame` is **not** unused — `ExitingGame()` exposes it as a getter, and it gates logic in
  `mrxplayer.lua` (two call sites check `not MrxSound.ExitingGame()` before running hero-death/local-player
  checks), so it's a real cross-module flag, not decompiler dead weight.
- `MrxSound.lua` and `MrxSoundBootstrap.lua` both define a top-level `ExitGame()` function. Since each
  `.lua` file is its own module/environment (no shared global namespace — see the
  [index page](index#how-these-modules-actually-work)), these are two distinct functions
  (`MrxSound.ExitGame` vs `MrxSoundBootstrap.ExitGame`), not a naming collision.