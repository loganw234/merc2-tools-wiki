---
title: Oilrig
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [oilrig, destruction]
verified: true
verified_note: 'deeper pass: rewrote the Events section (previous ObjectHibernation/HideMarker claims are fabricated — the only real subscription is Event.TimerRelative; it also Event.Posts oilrigDestroyed); documented the two trigger state hashes, the tTGLayers layer map, the sound cues, camera-shake presets and the explosion-fx hashes; re-confirmed all functions + the bare _tOilrigEvents bookkeeping pattern.'
---

# Oilrig

*Module: oilrig.lua*

## Overview
The `Oilrig` module manages the destruction sequence of oil rig objects in the game. It handles state changes that trigger various destruction events, including sound cues, camera shakes, and timed emitter sequences. The module also ensures proper cleanup when the oil rig is deactivated.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxLayerManager`](mrxlayermanager)

## Instance pattern
**Not the `Inheritable`/rich-instance pattern, and not a class-factory either** — confirmed from source: a
plain module-level table, `_tOilrigEvents[uGuid]`, populated once via a module-level `Init()`/`Deinit()`
pair, with no `Create`/`setmetatable`/rich-instance factory anywhere. Each activated oil rig gets a
sub-table entry, not a full instance object with inherited methods. It tracks the following key fields:
- `_tOilrigEvents`: A table to store event handles for each oil rig instance.
- `tTGLayers`: A mapping of GUIDs to layer names used for managing game layers.

## Functions
### `Init()`
Initializes the module by setting up global tables `_tOilrigEvents` and `tTGLayers` if they haven't been initialized yet.

### `Deinit()`
Cleans up all event handles for each oil rig instance and resets the global tables `_tOilrigEvents` and `tTGLayers`.

### `OnDeactivate(uGuid, args)`
Called when the oil rig instance is deactivated. It cleans up any ongoing destruction events and removes associated layers if the object is no longer alive.

### `OnStateChange(uiGuid, uiNodeHashName, uiStateHashName)`
Engine lifecycle callback (not an event subscription). Converts `uiStateHashName` to a string via
[`Sys.GuidToString`](../namespaces/sys) and branches:
- `"0x28825D4C"` (full destruction) — removes the `_tg` variant of the rig's authored layer, plays the
  `"seq_oilrig_destruction"` sound cue, starts a strong constant camera shake, then schedules
  `_DestroyOilrigSequence` 2.5s later via `Event.TimerRelative` and records the handle in
  `_tOilrigEvents[uiGuid]`.
- `"0x694683EB"` (a lighter/ambient stage) — plays the `"sfx_amb_oilrig_destruction"` cue and a
  gentler camera shake. Does **not** start the timed sequence.

### `_CleanupOilrigEvents(uiGuid)`
Cleans up all event handles associated with a specific oil rig instance by deleting each event and removing the entry from `_tOilrigEvents`.

### `_FinishDestruction(uiGuid)`
Stops any ongoing camera shake effects and cleans up destruction events for the specified oil rig instance. It then posts an `oilrigDestroyed` event.

### `_DestroyBuildingA(uOilrig)`
Destroys specific parts of building A linked to the oil rig by calling `_DestroyLinkedGuid` with appropriate arguments and scheduling subsequent steps using `_ProcessNextEvent`.

### `_DestroyBuildingB(uOilrig)`
Destroys specific parts of building B linked to the oil rig in a similar manner as `_DestroyBuildingA`.

### `_DestroyBuildingC(uOilrig)`
Destroys specific parts of building C linked to the oil rig.

### `_DestroyBuildingD(uOilrig)`
Destroys specific parts of building D linked to the oil rig.

### `_DestroyOilrigSequence(uOilrig, uNodeHashName)`
Manages the main destruction sequence for the oil rig by starting various emitters, destroying linked objects, setting states, and scheduling subsequent steps using `_ProcessNextEvent`.

### `_ProcessNextEvent(uiGuid, tEventTable, iIndex)`
The scheduler that drives the whole cinematic. Each step is a `{fn, args, minTime, maxTime}` record.
It calls `data.fn(unpack(data.args))` immediately, then: if the step has no `minTime`, recurses to the
next step synchronously; otherwise schedules the next step after `minTime` (or a random time between
`minTime`/`maxTime` via `Math.randf`) using `Event.TimerRelative`, appending the handle to
`_tOilrigEvents[uiGuid]` so it can be cancelled.

### `_DestroyLinkedGuid(uParent, sLinkName)`
Destroys a linked object by getting its GUID and calling `Object.Kill` on it. If the linked object does not exist, it logs an error message.

## Events
The **only** real subscription in this file is [`Event.TimerRelative`](../namespaces/event), used to
schedule the destruction steps (`OnStateChange` → 2.5s → `_DestroyOilrigSequence`, and every delayed
step inside `_ProcessNextEvent`). There is no `Event.ObjectHibernation`/`Awake` wiring and no
`HideMarker` listener — those were fabricated on the previous draft.

The module also **emits** one event: `Event.Post("oilrigDestroyed", {uiGuid})` (in `_FinishDestruction`),
which other scripts can subscribe to as the "rig is done collapsing" signal. `OnStateChange`,
`OnDeactivate`, `Init`, `Deinit` are engine/manager lifecycle callbacks, not subscriptions.

## Module constants & tunables
- **Trigger state hashes**: `"0x28825D4C"` (full destruction sequence) and `"0x694683EB"`
  (ambient/secondary stage).
- **`tTGLayers`** — maps the rig object's GUID string to its "pristine" layer name, used to swap out
  the intact geometry when it blows:
  - `"0x000B637B"` → `"vz_state_mer_oilrig_pristine"`
  - `"0x0009878A"` → `"vz_state_chijob009_a_pristine"`
  - `"0x00098789"` → `"vz_state_chijob009_b_pristine"`

  On destruction it removes the `<layer>.."_tg"` variant; on `OnDeactivate` of a dead rig it removes
  the base layer via [`MrxLayerManager`](mrxlayermanager).
- **Sound cues**: `"seq_oilrig_destruction"` (main), `"sfx_amb_oilrig_destruction"` (ambient stage).
- **Camera shake presets** ([`Camera.Shake`](../namespaces/camera)):
  `"ShakeCameraConstantlyRandom"` (0.5 then 1.2 intensity), `"StopShakeCameraConstantly"` (in
  `_FinishDestruction`), `"ShakeCameraMedium"` (per-piece punches at 0.3/0.8).
- **Explosion FX hashes**: `"fx_Explosion_HugeOil_RigOnly"` (large) and
  `"fx_Explosion_HugeOilTower_RigOnly"` (huge), fired at emitter nodes `hp_fx_explosionA..N` via
  `ObjectState.StartEmitter`.
- **Sequence length**: the full collapse takes well over a dozen seconds — note the deliberate
  `minTime=12, maxTime=13` gap before `_DestroyBuildingC` near the end.

## Notes for modders
- To **retime or restage** the collapse, edit the `{fn, args, minTime, maxTime}` records inside
  `_DestroyOilrigSequence` (and the per-building tables). `minTime`/`maxTime` are seconds; omit both to
  fire the next step instantly.
- The destruction is driven entirely by **named link nodes** (`hp_snap_oilrig_*`) resolved with
  `ObjectState.GetLinkGuid`. If you re-author the rig model, these link names must match or
  `_DestroyLinkedGuid` logs `********** ERROR` and skips that piece.
- Subscribe to the posted `"oilrigDestroyed"` event rather than guessing when the sequence ends.
- `Init()` must run before any rig activates (it lazy-builds `_tOilrigEvents`/`tTGLayers`); `Deinit()`
  cancels all in-flight timers and clears the maps. `tTGLayers` is a **module global**, not a local.