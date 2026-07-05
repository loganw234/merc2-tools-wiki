---
title: LevelBootstrap
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [level, loading]
verified: true
verified_note: spot-checked against source (single-function 18-line file), no changes needed — content and events section were already accurate.
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
Loads the specified level and master script. If `LevelName` is `nil`, defaults to `Sys.GetLevelName()`; if
`MasterScript` is `nil`, defaults to `Sys.GetMasterScriptName()`. Calls `Sys.SetLevelName(LevelName)` and
`Sys.SetMasterScriptName(MasterScript)`, logs a debug message (`"Loading " .. LevelName .. " level with "
.. MasterScript .. " masterscript"`), defaults `Reload` to `false` if not provided (the parameter itself
is otherwise unused in this function body), requests `LevelName .. "_base"` as a `"layer"` asset at
priority `-2` and `MasterScript` as a `"script"` asset at priority `-3` (both via `Sys.RequiredAsset`,
non-blocking per the trailing `false` argument), and finally calls `Sys.RequestGameState("Loading")`.

## Events
- Listens for none (this module does not subscribe to any engine events).

## Notes for modders
- Ensure that `LevelName` and `MasterScript` are correctly set or omitted to use defaults.
- Be aware of the asset loading order and ensure that required assets are available.
- This function is typically called during level transitions or when starting a new game.