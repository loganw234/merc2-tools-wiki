---
title: MrxSoundBanks
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, sound]
verified: true
verified_note: "deeper pass: re-confirmed all 16 functions + LIFO-stack finding + the nested _OpenFile/_StripPWSExtension globals; noted MAX_SUBMITTED is a file-local (64, not externally settable), RequestAmbienceBank gates on Sound._GetLibVersion() >= 12, and the exact Pg.LoadAsset asset set _LoadRequiredAssets pulls in; cross-linked MrxSound/MrxSoundCategories and the Sound/Pg namespaces; pruned vacuous notes"
---

# MrxSoundBanks

*Module: mrxsoundbanks.lua*

## Overview
The `MrxSoundBanks` module is responsible for managing the loading and unloading of sound banks and wave banks in the game. It provides functions to asynchronously load and unload these assets, ensuring that the audio system remains responsive by throttling the number of concurrent requests.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: [`MrxSound`](mrxsound), [`MrxSoundCategories`](mrxsoundcategories)

Actual bank/wave loading goes through the engine [`Sound`](../namespaces/sound) namespace
(`Sound.LoadBankWithCallback`, `Sound.OpenStreamFile`, `Sound.GetAudioDir`, …); the data-table assets go
through [`Pg`](../namespaces/pg) (`Pg.LoadAsset`/`Pg.UnloadAsset`). This module is the throttling/queueing
layer on top of those.

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `_nOutstandingAssets`: The number of assets currently being processed. Read cross-module by
  [`MrxSound._CheckSoundReady`](mrxsound) to gate the "sound ready" callback.
- `_nSubmittedRequests`: The number of asset requests that have been submitted but not yet completed.
- `MAX_SUBMITTED`: The maximum number of in-flight asset requests (64). **Declared `local`** — it is not a
  module field you can read or change from another script; to raise the cap you'd edit this literal in source.
- `_tPendingRequests`: A table storing pending asset requests (used as a LIFO stack — see below).
- `_nLastAddedIndex`: The top-of-stack index in `_tPendingRequests`; doubles as the count of pending requests.
- `_funcBatchComplete`: A callback function called once, when `_nOutstandingAssets` returns to 0.

## Functions
### `LoadSoundBank(sBank, funcBatchComplete)`
Pushes a request to load a sound bank onto the pending-request stack via `_AddAssetRequest`. If a batch complete callback is provided, it sets `_funcBatchComplete` to this function.

### `UnloadSoundBank(sBank, funcBatchComplete)`
Pushes a request to unload a sound bank onto the pending-request stack via `_AddAssetRequest`. If a batch complete callback is provided, it sets `_funcBatchComplete` to this function.

### `LoadWaveBank(sBank, funcBatchComplete)`
Pushes a request to load a wave bank onto the pending-request stack via `_AddAssetRequest`. If a batch complete callback is provided, it sets `_funcBatchComplete` to this function.

### `UnloadWaveBank(sBank, funcBatchComplete)`
Pushes a request to unload a wave bank onto the pending-request stack via `_AddAssetRequest`. If a batch complete callback is provided, it sets `_funcBatchComplete` to this function.

### `LoadTempBank(sBank, sType, funcCallback, tCallbackData)`
Loads a temporary sound bank or wave bank with a specified type and callback. It localizes the asset name before loading.

### `UnloadTempBank(sBank, sType, funcCallback, tCallbackData)`
Unloads a temporary sound bank or wave bank with a specified type and callback. It localizes the asset name before unloading.

### `RequestAmbienceBank(sBank)`
Localizes the name and calls `Sound.RequestAmbienceBank(...)` — but **only if `Sound._GetLibVersion() >= 12`**.
On an older audio-lib build this function is a silent no-op (no error, nothing loaded), so a mod relying on
ambience banks may quietly do nothing on the wrong runtime.

### `_SubmitAssetRequest()`
Submits the most-recently-added pending asset request to the sound system, ensuring that no more than `MAX_SUBMITTED` requests are in flight at any time. It calls `Sound.LoadBankWithCallback` or `UnloadBankWithCallback` based on the request type and decrements counters accordingly.
**Confirmed in source:** `_tPendingRequests` is a **LIFO stack**, not a FIFO queue — both
`_AddAssetRequest` (push) and `_SubmitAssetRequest` (pop) operate on `_tPendingRequests[_nLastAddedIndex]`,
the same top-of-stack slot, so the *last* bank request added is the *first* one submitted. A modder queuing
several bank loads back-to-back should expect them to fire in reverse order, not the order they were
requested.

### `_AddAssetRequest(sBank, sType, bLoad)`
Pushes an asset request onto the pending stack (`_tPendingRequests[_nLastAddedIndex]`, incrementing
`_nLastAddedIndex`). It increments the outstanding assets counter and calls `_SubmitAssetRequest` to submit
immediately if the in-flight limit allows.

### `_GetLocalizedName(sAssetName)`
Appends the current language to `vo_`-prefixed asset names to ensure localization.

### `_OpenStreamFiles()`
Opens stream files for voice, music, and ambience by localizing their names and opening them with aliases.
**Confirmed in source:** it does this via two nested helper functions defined *inside its own body* without
`local` — `_StripPWSExtension(sFileName)` (strips the trailing `.pws`) and `_OpenFile(sFileName)` (re-adds
the extension after localizing the stripped name, then calls `Sound.OpenStreamFile`). Because neither uses
`local`, both are actually (re-)defined as ordinary globals every time `_OpenStreamFiles` runs — harmless
here since they're only ever called from directly below their own definition, for the three hardcoded
filenames `"vo_stream.pws"`, `"music.pws"`, `"ambience.pws"`, but worth knowing if you go looking for where
`_OpenFile`/`_StripPWSExtension` are defined.

### `_LoadRequiredAssetsCommon()`
Opens the three stream files (via `_OpenStreamFiles`), then `Pg.LoadAsset`s the three always-needed data
tables: `"Mercs2Globals"` (`"sounddb"`, with `MrxSoundCategories._DuckGlobalTable` as its load callback),
`"MusicMarkers"` (`"musicmarkers"`), and `"MusicTransitions"` (`"musictransitions"`).

### `_UnloadRequiredAssetsCommon()`
Unloads the three assets loaded by `_LoadRequiredAssetsCommon` (`Mercs2Globals`, `MusicMarkers`, `MusicTransitions`).

### `_LoadRequiredAssets()`
Calls `_LoadRequiredAssetsCommon()` then loads five more animation/material tables via `Pg.LoadAsset`:
`"VehicleEngines"`, `"Sounds"`, `"SoundsAppendix"`, `"SoundMatch"` (all type `"animationtable"`) and
`"SoundKey"` (type `"materialkeytable"`).

### `_UnloadRequiredAssets()`
Unloads everything `_LoadRequiredAssets` loaded (the common three plus the five gameplay tables).

### `_FlagAssetOpComplete()`
Flags an asset operation as complete. It decrements the submitted requests and outstanding assets counters, resubmits pending requests if necessary, and calls the batch complete callback when all assets are processed.

## Events
- None

## Notes for modders
- The pending-request buffer is LIFO, not FIFO — if you queue several `LoadSoundBank`/`LoadWaveBank` calls
  in a row expecting first-requested-first-loaded order, the last one you called actually submits first.
- Load/unload every bank in matched pairs. The three stream files (`vo_stream.pws`, `music.pws`,
  `ambience.pws`) are opened wholesale by `_LoadRequiredAssetsCommon`; individual banks come and go via
  the `Load*`/`Unload*` functions.
- Names prefixed `vo_` are auto-localized (current language appended) by `_GetLocalizedName` before
  loading. A non-`vo_` name is loaded verbatim — don't add the language suffix yourself.
- `MAX_SUBMITTED` (64) is a `local`, so the throttle can't be widened from a mod without editing this file.
- `RequestAmbienceBank` silently no-ops on audio-lib versions below 12 (see its entry) — don't assume it ran.