---
title: GameBootstrap
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [init, intro]
---

# GameBootstrap

*Module: gamebootstrap.lua*

## Overview
The `GameBootstrap` module is responsible for initializing the game environment and playing introductory movies. It sets up the necessary components such as sound and GUI systems, then routes to the appropriate shell, lobby, or autoload level based on configuration settings.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `LevelBootstrap`, `MrxSoundBootstrap`, `MrxGuiShellBootstrap`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state; instead, it manages global game initialization and movie playback.

## Functions
### `_PlayMovie()`
A helper function that plays the next movie in the sequence defined by `tMovies`. It handles looping movies and transitioning to the main game logic once all movies are complete.

### `Init()`
The primary initialization function called by the engine. It sets the Lua save version, adjusts the gamma settings, and checks if the shell is already finished. If not, it proceeds to play intro movies or directly starts the game based on configuration.

### `Start()`
Determines the next step in the game startup process based on network and auto-load settings. It loads the appropriate shell, connects to a server, enters a lobby, or autoloads a level as needed.

### `GetSaveDataVersion()`
Returns the save data version number, which is set to 3.

## Events
- Listens for internal events related to movie playback and game initialization through callbacks within `_PlayMovie` and `Init`.

## Notes for modders
- Ensure that `Init` and `Start` are called appropriately during game startup.
- Customize the list of intro movies in `tMovies` if you want to change or add new introductory content.
- Be aware that modifying save data version may affect compatibility with existing saves.