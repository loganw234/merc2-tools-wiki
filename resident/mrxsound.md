---
title: MrxSound
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, sound]
---

# MrxSound

*Module: mrxsound.lua*

## Overview
The `MrxSound` module is responsible for managing audio-related functionalities in the game. It handles transitions between different music states, manages sound banks and wave banks, and controls various one-shot sound effects. This module ensures that the audio system is properly initialized and synchronized with the game's state changes.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxMusic`, `MrxSoundCategories`, `MrxSoundBanks`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages global audio settings and transitions.

## Functions
### `EnterShellState()`
Enters the shell state by loading required sound banks, setting the master volume, and transitioning to the "shell" music state.

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
Begins survival mode by setting the survival mode flag, fading in the "survivalmode" category, playing a looped sound effect, and adjusting pitch settings.

### `EndSurvivalMode()`
Ends survival mode by resetting the survival mode flag, fading out the "survivalmode" category, stopping the looped sound effect, and restoring pitch settings.

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
Initializes the music system, sets up additional fade settings, and prepares for game exit.

## Events
- Listens for `Event.GameStateChange` to handle game state changes during exit.
- Listens for internal events related to sound asset loading and system readiness.

## Notes for modders
- Ensure that audio-related functions are called appropriately to manage transitions between different states (e.g., pause, cinematic, PDA).
- Use the provided functions to control music states and sound effects effectively.
- Be aware of the dependencies on other modules like `MrxMusic` and `MrxSoundCategories`.
- The decompiler artifact noted is `_bExitingGame`, which appears unused but is part of the internal state management.