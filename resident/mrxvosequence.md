---
title: MrxVoSequence
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, vo]
---

# MrxVoSequence

*Module: mrxvosequence.lua*

## Overview
The `MrxVoSequence` module is responsible for playing voice-over (VO) sequences in the game. It handles the normalization of VO sequences, arbitration by priority, and execution of each stage in the sequence, including delays and callbacks.

## Inheritance
- Inherits from: `none`
- Imports: `MrxUtil`, `MrxSoundCategories`

## Instance pattern
This is a stateless manager/utility module (no per-instance table). It tracks the following key fields:
- `_tSequence`: The current VO sequence being played.
- `_nBaseDelay`: Base delay between stages in the sequence.
- `_bStoppingSequence`: Flag indicating if the sequence is currently stopping.
- `_uTimeoutEvent`: Event handle for timeouts during cue playback.
- `_knTimeout`: Timeout duration for each cue.

## Functions
### `Start(vSequence, bCinematic, nPriority, bSendNetEvent)`
Normalizes a VO sequence (cue/speaker, delay, callback stages), arbitrates by priority (higher pre-empts; equal/lower is rejected), fades the sequence, registers speakers, and runs stage 1. Returns a boolean indicating success or failure.

### `_ExecuteStage(nStage)`
Executes a specific stage in the VO sequence. Plays the cue via `VO.Cue`, logs to PDA dialog, sets a timeout, and schedules the next stage via `Event.TimerRelative`.

### `Stop(bFadeSound, bIssueDanglingCallbacks, nPriorityFilter)`
Cancels all cues in the current sequence, optionally fires dangling callbacks, and cleans up associated events.

### `Cleanup(bFadeSound)`
Fades out the VO sequence sound category and removes sequences from registered speakers.

### `Reset()`
Resets the module's internal state by fading out the VO sequence sound category and clearing all tracked fields.

### `_CallSequenceCallbacks(tFormattedSequence)`
Fires uncalled, non-`bIgnoreOnSkip` callbacks on skip for each stage in the sequence.

### `IsSequenceInProgress()`
Returns a boolean indicating whether a VO sequence is currently in progress.

## Events
- Listens for custom event triggers within its own functions to manage sequence execution and cleanup.

## Notes for modders
- Ensure that `Start`, `Stop`, and `Reset` are called appropriately to manage the lifecycle of VO sequences.
- Customize VO sequence properties by setting fields like `_nBaseDelay` and `_knTimeout`.
- Be aware that network synchronization (`bSendNetEvent`) may affect multiplayer behavior.
- The module uses internal state tracking, so ensure proper cleanup when stopping sequences.