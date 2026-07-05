---
title: Gurpodium
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, speech]
verified: true
verified_note: corrected Events section — CueFinished is a plain VO.CueWithoutSubtitles callback, not an Event.Create listener; confirmed no Create/setmetatable anywhere (genuinely stateless, uGuid-keyed plain tables only); all 9 functions and event constants verified against source
---

# Gurpodium

*Module: gurpodium.lua*

## Overview
The `Gurpodium` module manages the in-vehicle speech cues for a specific type of vehicle. It handles events related to the vehicle's activation, deactivation, rider entry/exit, and death, triggering speech cues accordingly.

## Inheritance
- Inherits from: `none`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module — no `Create`/`setmetatable`/`tInstance` registry anywhere in
the file. Per-vehicle state is tracked with plain `uGuid`-keyed globals instead of real instance tables:
- `tEvents`: `uGuid -> {eDeath, eEntryExit, eStartNext}` table of event handles for each vehicle.
- `tSpeakers`: `uGuid -> uRider` — which rider character is currently the speaker for that vehicle.
- `tSpeechIndex`: `uGuid -> current index into tSpeech` (1–5, wraps via `CueFinished`).
- `tSpeech`: a fixed array of 5 hardcoded VO cue names (`"GuerillaSoldier_Rebecca01_Guerilla Soldier_Prop1"`
  through `Prop5`), shared across all vehicle instances — not per-`uGuid`.

All four tables are initialized in `Init()` and torn down (set to `nil`) in `Deinit()`.

## Functions
### `Init()`
Initializes the module by setting up tables to store event handles, speakers, and speech indices. It also defines an array of speech cues.

### `Deinit()`
Cleans up the module by setting all tracked tables to `nil`.

### `OnActivate(uGuid, args)`
Called when a vehicle instance is activated. It sets up an event for the vehicle's death and checks if there are any riders in the vehicle. If there are, it calls `OnEnter` for the first rider.

### `OnDeactivate(uGuid, args)`
Called when a vehicle instance is deactivated. It deletes all associated events, clears the speakers table, and resets the speech index for that vehicle instance.

### `OnExit(uRider, uGuid)`
Called when a player exits the vehicle. It sets up an event to handle re-entry and cancels any ongoing speech cue.

### `OnEnter(uRider, uGuid)`
Called when a player enters the vehicle. It sets up an event to handle exit, updates the speaker table, initializes the speech index, and starts the next speech cue.

### `OnDeath(uGuid)`
Called when the vehicle dies. It cancels any ongoing speech cue and deactivates the vehicle instance.

### `CueFinished(uGuid)`
Callback passed to `VO.CueWithoutSubtitles` (not an `Event.Create` listener — see Events below). Called when a speech cue finishes playing. Only runs its body if `tSpeechIndex[uGuid]` is still set (guards against a cue finishing after `OnDeactivate`/`OnExit` already cleared state). Increments the speech index, wraps from 6 back to 1, and schedules `StartNextCue` after a fixed 1.5s persistent-looping timer (`Event.TimerRelative, {1.5, true}`).

### `StartNextCue(uGuid)`
Starts the next speech cue for the specified vehicle instance. If there is no speaker or the speech index is out of range, it logs an error message. It also sets up a timer event to handle the cue finishing.

### `CancelCue(uGuid)`
Cancels any ongoing speech cue for the specified vehicle instance and deletes the associated timer event.

## Events
- `Event.ObjectDeath` — registered in `OnActivate` (`{uGuid}`) to call `OnDeath`.
- `Event.ObjectInSeat` — registered in `OnEnter`/`OnExit`, alternating between `"a","e"` (enter) and
  `"a","x"` (exit) filters, to detect the next rider transition and flip between `OnEnter`/`OnExit`.
- `Event.TimerRelative` — used in `CueFinished` (`{1.5, true}`, persistent/looping) to delay
  `StartNextCue`.
- `CueFinished` itself is **not** an engine event — it's passed as a plain function-pointer callback to
  `VO.CueWithoutSubtitles`, a voice-over system API, not `Event.Create`.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of speech cues.
- Customize the list of speech cues by modifying the `tSpeech` array.
- Be aware that speech cues are tied to specific rider characters, so ensure that the correct player is speaking at any given time.
- The module uses a timer event to schedule the next speech cue after a delay; adjust the delay as needed for different pacing.