---
title: MrxSoundBootstrap
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [sound, initialization]
verified: true
verified_note: "deeper pass: corrected imports (added missing MrxSoundCategories), surfaced reverb preset 1/CITY_KG_LIGHT_REFLECTIONS and the seven default mu_src_radio cues; all 5 functions and the no-Event.* finding re-confirmed"
---

# MrxSoundBootstrap

*Module: mrxsoundbootstrap.lua*

## Overview
The `MrxSoundBootstrap` module is responsible for initializing and managing the sound system in the game. It handles tasks such as setting up reverb presets, configuring pitch and fade categories, binding music cues for different factions and scenarios, loading necessary sound banks, registering music playlists, and ensuring proper initialization of the sound engine. Additionally, it manages unloading sound resources when the game exits.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxSound`](mrxsound), [`MrxMusic`](mrxmusic), [`MrxSoundCategories`](mrxsoundcategories),
  [`MrxSoundBanks`](mrxsoundbanks) (the previous version omitted `MrxSoundCategories`, which `Init` uses
  heavily for its pitch/fade category setup)

## Instance pattern
This is a stateless utility module (no per-instance tables). It does not track any specific state but manages global sound system settings and resources.

## Functions

### Init()
- **Description**: Initializes the sound system by defining reverb presets, setting pitch and fade categories, binding music cues for various factions and freeplay scenarios, enabling duck-on-global-table-load, loading required sound banks, registering music playlists, and initializing the sound engine.
- **Steps**:
  - Defines reverb preset `1` / `"CITY_KG_LIGHT_REFLECTIONS"` (`Sound.DefineReverbPreset`) with fixed
    parameters.
  - Selects it by name if `Sound._GetLibVersion() >= 10`, otherwise by numeric id `1`, then `Sound.SetReverb(1)`.
  - Configures pitch categories for different modes (e.g., survival mode).
  - Sets fade categories for various sound sequences and actions.
  - Binds music cues for multiple factions (`an`, `oc`, `gr`, `ch`, `pmc`) and freeplay scenarios (`freeplay_city`, `freeplay_jungle`, `freeplay_water`).
  - Enables duck-on-global-table-load to adjust volume when global tables are loaded.
  - Loads required sound banks using the `LoadBanks()` function.
  - Registers music playlists for various sources (e.g., PMC radio, civilian, GR HQ).
  - Initializes the sound engine with `MrxSound.Initialize()`.

### ExitGame()
- **Description**: Unloads all sound banks when the game exits.
- **Steps**:
  - Calls `UnloadBanks()` to unload all previously loaded sound banks.

### LoadBanks()
This function is responsible for loading various sound banks and wave banks related to the game's ambient sounds, collisions, destructions, foliage, vehicles, weapons, music, UI/HUD, and voice-over cues. It calls `MrxSoundBanks.LoadWaveBank` and `MrxSoundBanks.LoadSoundBank` with different bank names to ensure all necessary sound assets are loaded.

### UnloadBanks()
This function unloads the same set of sound banks and wave banks that were loaded by `LoadBanks()`. It calls `MrxSoundBanks.UnloadWaveBank` and `MrxSoundBanks.UnloadSoundBank` with the corresponding bank names to free up resources when they are no longer needed.

### SetPmcRadio(sInsertedCue)
Rebuilds the `"mu_src_radio"` playlist. Clears it (`MrxMusic.ClearMusicPlaylist`), then re-binds the seven
default PMC-HQ cues (`MU_SRC_PMC_HQ_01` through `_05`, plus `MU_SRC_UP_OP_04_for_HQ` and
`MU_SRC_UP_OP_03_for_HQ`). If `sInsertedCue` is provided, it's bound last — so the extra cue is added on top
of the standard rotation, not a replacement. Called once with no argument during `Init`, and repeatedly
with a mission VO cue from the mission flow (see below).

## Events

No `Event.*` references appear anywhere in this file — there is no `Event.Create`/`Event.CreatePersistent`
call, so `ExitGame()` is **not** wired to an engine event of any kind. Grepping the decompiled corpus shows
`MrxSoundBootstrap.ExitGame()` is invoked as a plain direct function call from `src/vz/xQ!L.lua:612` (a
mission-flow script), not through an event subscription. The previous "Event.GameExit" entry on this page
did not correspond to anything in source and has been removed.

`Init()` itself has no call sites found anywhere in the decompiled corpus — consistent with it being invoked
by native/engine bootstrap code rather than from other Lua modules; this can't be confirmed from static
reading alone.

## Notes for modders

- **Call-order requirements**: Ensure that `Init()` is called before any other functions in this module to properly initialize the sound system. Conversely, `UnloadBanks()` should be called when unloading resources to avoid memory leaks.
  
- **Pitfalls**: Be cautious with modifying reverb presets or music playlists directly, as these changes can affect the overall audio experience for players.

- **Tunables**: The pitch and fade categories can be adjusted in the `Init()` function to fine-tune the sound system according to different game modes or player preferences.

- **Decompiler artifacts**: There may be unused local variables or redundant operator groupings due to decompiler quirks. These should not affect the functionality of the module.

- **Confirmed real usage**: `MrxSoundBootstrap.SetPmcRadio(sInsertedCue)` is called from `src/vz/wifmissionflow.lua`
  at over a dozen points across the mission flow, each time swapping in a mission-specific VO cue (e.g.
  `"ReporterNeutral.MissionVO.Gur01"`) onto the `mu_src_radio` playlist. That's the intended mod surface if
  you want a mission to override the PMC radio chatter — call `SetPmcRadio` with your own cue string rather
  than touching `mu_src_radio` directly.