---
title: LevelBootstrap
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [level, loading]
---

# LevelBootstrap

*Module: levelbootstrap.lua*

## Overview
The `LevelBootstrap` module is responsible for loading a game level and its associated master script. It sets the current level name and master script, requests the necessary assets, and transitions the game state to "Loading".

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `none`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state.

## Functions
### `LoadLevel(LevelName, MasterScript, Reload)`
Loads the specified level and master script. If `LevelName` or `MasterScript` are not provided, it defaults to using the current level name and master script from the system. It sets these values in the system, logs a debug message, requests the necessary assets (`<level>_base` layer and master script), and transitions the game state to "Loading".

## Events
- Listens for none (this module does not subscribe to any engine events).

## Notes for modders
- Ensure that `LevelName` and `MasterScript` are correctly set or omitted to use defaults.
- Be aware of the asset loading order and ensure that required assets are available.
- This function is typically called during level transitions or when starting a new game.