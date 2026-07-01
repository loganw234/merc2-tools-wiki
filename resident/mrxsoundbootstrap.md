---
title: MrxSoundBootstrap
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [sound, initialization]
---

# MrxSoundBootstrap

*Module: mrxsoundbootstrap.lua*

## Overview
The `MrxSoundBootstrap` module is responsible for initializing and managing the sound system in the game. It handles tasks such as setting up reverb presets, configuring pitch and fade categories, binding music cues for different factions and scenarios, loading necessary sound banks, registering music playlists, and ensuring proper initialization of the sound engine. Additionally, it manages unloading sound resources when the game exits.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxSound`, `MrxMusic`, `MrxSoundBanks`

## Instance pattern
This is a stateless utility module (no per-instance tables). It does not track any specific state but manages global sound system settings and resources.

## Functions

### Init()
- **Description**: Initializes the sound system by defining reverb presets, setting pitch and fade categories, binding music cues for various factions and freeplay scenarios, enabling duck-on-global-table-load, loading required sound banks, registering music playlists, and initializing the sound engine.
- **Steps**:
  - Defines a reverb preset `CITY_KG_LIGHT_REFLECTIONS` with specific parameters.
  - Sets the reverb preset based on the library version.
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
This function sets up a music playlist for the PMC radio. It clears any existing playlist named "mu_src_radio" using `MrxMusic.ClearMusicPlaylist`. Then, it binds several predefined music cues to this playlist using `MrxMusic.BindPlaylistCue`. If an additional cue (`sInsertedCue`) is provided as an argument, it also binds this cue to the playlist. This function is used to manage the radio's music selection and ensure that the correct tracks are played.

## Events

- **Event.GameExit**: Listens for the game exit event and calls `ExitGame()` to unload all sound banks.

## Notes for modders

- **Call-order requirements**: Ensure that `Init()` is called before any other functions in this module to properly initialize the sound system. Conversely, `UnloadBanks()` should be called when unloading resources to avoid memory leaks.
  
- **Pitfalls**: Be cautious with modifying reverb presets or music playlists directly, as these changes can affect the overall audio experience for players.

- **Tunables**: The pitch and fade categories can be adjusted in the `Init()` function to fine-tune the sound system according to different game modes or player preferences.

- **Decompiler artifacts**: There may be unused local variables or redundant operator groupings due to decompiler quirks. These should not affect the functionality of the module.