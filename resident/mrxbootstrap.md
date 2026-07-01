---
title: MrxBootstrap
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [bootstrap, initialization]
---

# MrxBootstrap

*Module: mrxbootstrap.lua*

## Overview
The `MrxBootstrap` module is responsible for initializing the game world by handling GUI loading and local player joining events. It sets up the initial atmosphere settings, manages faction setup, and optionally grants starting resources to the player if a cheat is enabled.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxSoundBootstrap`, `MrxFactionManager`, `MrxGuiBootstrap`, `MrxLayerManager`, `MrxSupportData`, `MrxPlayer`, `MrxPmc`, `MrxState`, `MrxUtil`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages global initialization tasks.

## Functions
### `Start(fCallback, tArgs)`
Wires GUI-loaded and local-player-joined callbacks, calls `MrxPlayer.Start()`. Sets up the initial state for bootstrapping the game world.

### `IsGuiLoaded()`
Returns whether the GUI has been loaded.

### `_GuiLoaded()`
Called when the first GUI load event is received. Logs a debug message and sets `_bGuiLoaded` to true. If `_bHandleStateTransitions` is enabled, it enters the `STATE_WAITFORGAME` state and calls `_End`.

### `_LocalPlayerJoined()`
Called when the local player joins the game session. Logs a debug message and sets `_bLocalPlayerJoined` to true. Calls `_End` to complete initialization.

### `_End()`
Completes the bootstrapping process by exiting the `STATE_WAITFORGAME` state, setting up factions, and applying default atmosphere settings for non-VZ levels. If the `StartWithResources` cheat is enabled, it grants 10 million cash and 9999 fuel to the player.

### `SetDefaultAtmosphere()`
Sets the default atmosphere/bloom/monochrome/contrast settings for non-VZ levels. This function configures various graphics parameters to create a consistent visual environment.

### `SetHeroSpawnLocation(sHeroSpawnLocation)`
Sets the hero spawn location, which is not used in this module but can be referenced elsewhere.

### `SetHandleStateTransitions(bEnable)`
Enables or disables state transition handling during bootstrapping. This allows for more control over the initialization process.

## Events
- Listens for GUI-loaded event to call `_GuiLoaded`.
- Listens for local player joined event to call `_LocalPlayerJoined`.

## Notes for modders
- Ensure that `Start` is called at the beginning of the game to properly initialize the world.
- Use `SetHeroSpawnLocation` if you need to set a specific spawn point for the hero.
- Customize atmosphere settings by modifying the parameters in `SetDefaultAtmosphere`.
- Be aware that enabling `StartWithResources` will grant starting resources to the player, which may not be desirable in all scenarios.