---
title: MrxSoundBanks
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, sound]
---

# MrxSoundBanks

*Module: mrxsoundbanks.lua*

## Overview
The `MrxSoundBanks` module is responsible for managing the loading and unloading of sound banks and wave banks in the game. It provides functions to asynchronously load and unload these assets, ensuring that the audio system remains responsive by throttling the number of concurrent requests.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxSound`, `MrxSoundCategories`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `_nOutstandingAssets`: The number of assets currently being processed.
- `_nSubmittedRequests`: The number of asset requests that have been submitted but not yet completed.
- `MAX_SUBMITTED`: The maximum number of concurrent asset requests allowed (64).
- `_tPendingRequests`: A table storing pending asset requests.
- `_nLastAddedIndex`: The index of the last added request in `_tPendingRequests`.
- `_funcBatchComplete`: A callback function to be called when all outstanding assets have been processed.

## Functions
### `LoadSoundBank(sBank, funcBatchComplete)`
Enqueues a request to load a sound bank. If a batch complete callback is provided, it sets `_funcBatchComplete` to this function.

### `UnloadSoundBank(sBank, funcBatchComplete)`
Enqueues a request to unload a sound bank. If a batch complete callback is provided, it sets `_funcBatchComplete` to this function.

### `LoadWaveBank(sBank, funcBatchComplete)`
Enqueues a request to load a wave bank. If a batch complete callback is provided, it sets `_funcBatchComplete` to this function.

### `UnloadWaveBank(sBank, funcBatchComplete)`
Enqueues a request to unload a wave bank. If a batch complete callback is provided, it sets `_funcBatchComplete` to this function.

### `LoadTempBank(sBank, sType, funcCallback, tCallbackData)`
Loads a temporary sound bank or wave bank with a specified type and callback. It localizes the asset name before loading.

### `UnloadTempBank(sBank, sType, funcCallback, tCallbackData)`
Unloads a temporary sound bank or wave bank with a specified type and callback. It localizes the asset name before unloading.

### `RequestAmbienceBank(sBank)`
Requests an ambience bank if the audio library version is 12 or higher. It localizes the asset name before requesting.

### `_SubmitAssetRequest()`
Submits pending asset requests to the sound system, ensuring that no more than `MAX_SUBMITTED` requests are in flight at any time. It calls `Sound.LoadBankWithCallback` or `UnloadBankWithCallback` based on the request type and decrements counters accordingly.

### `_AddAssetRequest(sBank, sType, bLoad)`
Adds an asset request to the pending queue. It increments the outstanding assets counter and submits the request if possible.

### `_GetLocalizedName(sAssetName)`
Appends the current language to `vo_`-prefixed asset names to ensure localization.

### `_OpenStreamFiles()`
Opens stream files for voice, music, and ambience by localizing their names and opening them with aliases.

### `_LoadRequiredAssetsCommon()`
Loads common assets required for sound processing, including opening stream files and loading global sound data.

### `_UnloadRequiredAssetsCommon()`
Unloads common assets loaded by `_LoadRequiredAssetsCommon`.

### `_LoadRequiredAssets()`
Loads additional assets required for sound processing, including vehicle engines, sounds, and sound keys.

### `_UnloadRequiredAssets()`
Unloads additional assets loaded by `_LoadRequiredAssets`.

### `_FlagAssetOpComplete()`
Flags an asset operation as complete. It decrements the submitted requests and outstanding assets counters, resubmits pending requests if necessary, and calls the batch complete callback when all assets are processed.

## Events
- None

## Notes for modders
- Ensure that sound banks and wave banks are loaded and unloaded appropriately to manage memory usage.
- Use `LoadTempBank` and `UnloadTempBank` for temporary sound assets that need to be loaded and unloaded dynamically.
- Be aware of the maximum number of concurrent asset requests (`MAX_SUBMITTED`) to avoid overwhelming the audio system.
- Localize asset names using `_GetLocalizedName` if they are prefixed with `vo_`.
- Use `_LoadRequiredAssetsCommon` and `_UnloadRequiredAssetsCommon` for common sound assets, and `_LoadRequiredAssets` and `_UnloadRequiredAssets` for additional sound assets.