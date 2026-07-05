---
title: MrxVoSequence
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, vo]
verified: true
verified_note: "deeper pass: documented the four stage shapes Start accepts (cue / callback / delay / J-M-C identity table), the priority pre-emption rule, _nBaseDelay 0.25 default and dead _knTimeout branch; cross-linked imports; Events (TimerRelative only) re-confirmed"
---

# MrxVoSequence

*Module: mrxvosequence.lua*

## Overview
The `MrxVoSequence` module is responsible for playing voice-over (VO) sequences in the game. It handles the normalization of VO sequences, arbitration by priority, and execution of each stage in the sequence, including delays and callbacks.

## Inheritance
- Inherits from: `none`
- Imports: [`MrxUtil`](mrxutil), [`MrxSoundCategories`](mrxsoundcategories)

## Instance pattern
This is a stateless manager/utility module (module-level globals, no `Create`/`uGuid`/`tInstance` pattern) — there is only ever one VO sequence in flight at a time, module-wide. It tracks the following key fields:
- `_tSequence`: The current, normalized VO sequence being played (nil when idle). Also carries `.nPriority`, `.bSendNetEvent`, and `.tSpeakers` as extra keys on the same table.
- `_nBaseDelay`: Base delay (seconds) between stages that don't specify their own delay; defaults to `0.25`, overridable via `vSequence.nBaseDelay`.
- `_bStoppingSequence`: Flag indicating if the sequence is currently stopping (guards against reentrant `_NextStage` calls during `Stop`).
- `_uDelayTimer`: Event handle for the inter-stage delay timer (`Event.TimerRelative`), cleared in `Stop`.
- `_uTimeoutEvent`: Event handle for the per-cue timeout timer, cleared when the cue finishes or the sequence stops.
- `_knTimeout`: Timeout duration for each cue. Never assigned anywhere in this file — no call site sets it, so `_ExecuteStage`'s timeout branch (`if _knTimeout then ...`) is dead in practice unless another module/native code sets it.
- `knPriorityCinematic`, `knPriorityBriefing`, `knPriorityContract`, `knPriorityBounties`, `knPriorityFreeplay`: Priority constants, aliased from `VO.PRIORITY_*` at load time.

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
- `Event.TimerRelative`: Used twice — to delay execution of the next stage (`_ExecuteStage`, via `_uDelayTimer`) and to enforce a per-cue timeout that calls `VO.Cancel` (via `_uTimeoutEvent`, only created when `_knTimeout` is set — see Instance pattern above).
- `Event.Delete`: Called to cancel pending `_uDelayTimer`/`_uTimeoutEvent` timers during `Stop` and `_NextStage`.
- No other `Event.*` constants appear in this file; sequence advancement between non-delayed stages happens via direct recursive calls to `_ExecuteStage`, not events.

## Notes for modders
- **A stage in `vSequence` can be one of four shapes**, auto-detected by `Start`: `{sCue, vSpeaker}` (a
  spoken cue — speaker may be a name string, a GUID, or `nil`=`0`), `{fFn, tArgs, bIgnoreOnSkip}` (a
  callback stage, runs instantly), `{nDelay}` (a pause; negatives clamp to `0`), or a bare
  `{J=cue, M=cue, C=cue}` table keyed by the primary character's identity (Jennifer/Mattias/Chris) — the
  matching cue is picked automatically. This is the actual authoring surface.
- **Priority decides who wins**: pass one of the `knPriority*` constants (they alias `VO.PRIORITY_*`).
  A higher-priority `Start` pre-empts the current sequence; equal-or-lower is rejected and its callbacks are
  fired as "skipped". `bCinematic = true` forces `knPriorityCinematic`.
- **`_nBaseDelay` defaults to `0.25s`** between stages that don't specify their own delay; override
  per-call by putting `nBaseDelay` on the sequence table itself.
- **`_knTimeout` is dead in this file** — nothing sets it, so the per-cue timeout branch in `_ExecuteStage`
  never runs unless native/other code assigns it. Don't rely on it as a safety net.
- Only one sequence runs at a time module-wide; call `Stop`/`Reset` if you need to force-clear before
  starting another at equal-or-lower priority.