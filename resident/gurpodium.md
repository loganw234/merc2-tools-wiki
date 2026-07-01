---
title: Gurpodium
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [vehicle, speech]
---

# Gurpodium

*Module: gurpodium.lua*

## Overview
The `Gurpodium` module manages the in-vehicle speech cues for a specific type of vehicle. It handles events related to the vehicle's activation, deactivation, rider entry/exit, and death, triggering speech cues accordingly.

## Inheritance
- Inherits from: `none`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `tEvents`: A table to store event handles for each vehicle instance.
- `tSpeakers`: A table to track which player character is speaking for each vehicle instance.
- `tSpeechIndex`: A table to keep track of the current speech index for each vehicle instance.
- `tSpeech`: An array containing the list of speech cues.

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
Called when a speech cue finishes playing. It increments the speech index, wraps it around if necessary, and schedules the next speech cue to start after a delay.

### `StartNextCue(uGuid)`
Starts the next speech cue for the specified vehicle instance. If there is no speaker or the speech index is out of range, it logs an error message. It also sets up a timer event to handle the cue finishing.

### `CancelCue(uGuid)`
Cancels any ongoing speech cue for the specified vehicle instance and deletes the associated timer event.

## Events
- Listens for `Event.ObjectDeath` to call `OnDeath` when the vehicle dies.
- Listens for `Event.ObjectInSeat` to handle rider entry/exit by calling `OnEnter` or `OnExit`.
- Listens for custom event `CueFinished` to manage speech cue transitions.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of speech cues.
- Customize the list of speech cues by modifying the `tSpeech` array.
- Be aware that speech cues are tied to specific rider characters, so ensure that the correct player is speaking at any given time.
- The module uses a timer event to schedule the next speech cue after a delay; adjust the delay as needed for different pacing.