---
title: Gurpodium
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, speech]
verified: true
verified_note: "deeper pass: re-confirmed all 10 functions, the 3 Event.Create types (ObjectDeath/ObjectInSeat/TimerRelative) and the VO.CueWithoutSubtitles/VO.Cancel calls against source; surfaced the 5 hardcoded cue strings and 1.5s timer as tunables; replaced lifecycle boilerplate in Notes with actionable levers"
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
Starts the next speech cue for the vehicle. If a speaker exists, it plays `tSpeech[tSpeechIndex[uGuid]]` via
`VO.CueWithoutSubtitles(uSpeaker, cue, CueFinished, {uGuid}, false, false)` — passing `CueFinished` as the
completion callback. If there is no speaker it logs `"Starting cue on non-existent speaker"` via
`Debug.Printf`. It then clears `myEvents.eStartNext` (the timer that fired it). Note: it does **not** create
the finish timer — that is done in `CueFinished`.

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

## Module constants & tunables
- **Speech cues** (`tSpeech`, defined in `Init`): a fixed array of 5 strings,
  `"GuerillaSoldier_Rebecca01_Guerilla Soldier_Prop1"` through `Prop5`. Shared across all vehicles.
- **Cue delay:** `1.5` seconds — the `Event.TimerRelative, {1.5, true}` gap between one cue finishing and
  the next starting (in `CueFinished`).
- **Wrap point:** index wraps from 6 back to 1 (`if tSpeechIndex[uGuid] > 5 then ... = 1`), i.e. the 5 cues
  loop indefinitely while a rider is aboard.

## Notes for modders
- **Change what's said:** edit the 5 `tSpeech` strings in `Init` — they are voice-over cue names, spoken by
  the rider character (`tSpeakers[uGuid]`) via `VO.CueWithoutSubtitles`.
- **Change the pacing:** the `1.5` in `CueFinished` is the inter-cue delay; the `true` makes the
  `Event.TimerRelative` looping/persistent.
- **Speaker binding:** the current speaker is `tSpeakers[uGuid]`, set to the first rider found in
  `OnActivate` (via `Vehicle.GetRiders`) or the entering rider in `OnEnter`. `OnExit`/`OnDeath` cancel the
  in-flight cue via `VO.Cancel`.