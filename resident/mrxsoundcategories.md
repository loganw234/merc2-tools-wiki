---
title: MrxSoundCategories
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [audio, sound]
verified: true
verified_note: corrected Events section — no Event.* calls exist anywhere in source; the two entries were invented (this module is called directly by other scripts, not event-driven)
---

# MrxSoundCategories

*Module: mrxsoundcategories.lua*

## Overview
The `MrxSoundCategories` module manages audio ducking, fading, and pitch adjustments for different sound categories in the game. It provides functions to set fade levels, apply fades, manage pitch settings, and handle master volume ducks.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager utility module (no per-instance tables). It tracks the following key fields:
- `_tFadeSettings`: A table to store fade settings for different modes and categories.
- `_tPitchSettings`: A table to store pitch settings for different modes and categories.
- `_bDuckOnGlobalTableLoad`: A boolean flag indicating whether to duck the master volume when the sound database loads.
- `_nMasterVolumeRefCount`: A reference count for managing master volume ducks.

## Functions
### `SetFadeCategory(sMode, sCategory, fLevel, fEnterLength, fExitLength)`
Sets the fade settings for a specific category in a given mode. The settings include the fade level and enter/exit lengths.

### `Fade(sMode, bDown)`
Applies fades to all categories in the specified mode. If `bDown` is true, it applies a fade down; otherwise, it applies a fade up.

### `_AdditionalFadeSetup()`
Adds additional fade settings for the "credits" mode, specifically for "sfx" and "vo" categories.

### `SetPitchCategory(sMode, sCategory, fLevel, fEnterLength, fExitLength)`
Sets the pitch settings for a specific category in a given mode. The settings include the pitch level and enter/exit lengths.

### `Pitch(sMode, bDown)`
Applies pitch adjustments to all categories in the specified mode. If `bDown` is true, it activates the pitch adjustment; otherwise, it deactivates it.

### `SetDuckOnGlobalTableLoad(bDuck)`
Sets a flag indicating whether to duck the master volume when the sound database loads.

### `_DuckGlobalTable()`
Ducks the master volume to 0 over 0.3 seconds if the global table load ducking is enabled.

### `DuckMasterVolume(fLength)`
Ref-counted function to duck the master volume over a specified length of time.

### `UnduckMasterVolume(fLength)`
Ref-counted function to unduck the master volume over a specified length of time.

## Events
No `Event.*` references anywhere in this file — this module is **not** event-driven. `_AdditionalFadeSetup`
and `_DuckGlobalTable` are plain functions (note the leading underscore, this codebase's usual
"internal/private" convention), called directly by whatever other script wants this behavior — there are
no call sites for either inside this file itself, so triggering is entirely external (no call sites found
in the decompiled corpus for either from this side).

## Notes for modders
- Use `SetFadeCategory` and `Fade` to manage audio fades for different categories and modes.
- Customize pitch adjustments using `SetPitchCategory` and `Pitch`.
- Control master volume ducks with `SetDuckOnGlobalTableLoad`, `DuckMasterVolume`, and `UnduckMasterVolume`.
- Be aware that the master volume ducking is ref-counted to ensure proper state management — call
  `DuckMasterVolume`/`UnduckMasterVolume` in matched pairs, or the ref count drifts and the volume never
  restores.
- `Fade`/`Pitch` iterate `_tFadeSettings[sMode]`/`_tPitchSettings[sMode]` with `pairs()` — if `sMode` was
  never registered via `SetFadeCategory`/`SetPitchCategory` (or via the module's own `_tFadeSettings`/
  `_tPitchSettings` table literals, which only pre-declare `vosequence`, `credits`, `actionhijack`,
  `survivalmode`, `fanfare`, `satelliteview` for fade and `survivalmode` for pitch), indexing
  `_tFadeSettings[sMode]` with an unknown mode returns `nil` and the `pairs(nil)` call errors.