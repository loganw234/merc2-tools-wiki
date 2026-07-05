---
title: LevelBootstrap
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [level, loading]
verified: true
verified_note: "deeper pass: re-confirmed the single LoadLevel function against source; replaced vacuous notes with the concrete asset-request shape (<Level>_base layer @-2, master script @-3, non-blocking), flagged the dead Reload param, cross-linked GameBootstrap"
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
- **This is the one-call level loader**: `LevelBootstrap.LoadLevel(sLevel, sScript)` sets the level/master
  script names, requests the assets, and flips the game state to `"Loading"`. [`GameBootstrap.Start`](gamebootstrap)
  calls it directly on the `Sys.AutoLoad()` (non-server) path.
- **The asset request shape is fixed**: it requests `<LevelName>_base` as a `"layer"` at priority `-2` and
  `<MasterScript>` as a `"script"` at priority `-3`, both non-blocking (trailing `false`). If you're adding
  a new level, those two names (`_base` layer + master script) are what the engine will go looking for.
- **`Reload` is dead** — the third parameter is defaulted to `false` and then never read again in the
  function body. Passing it has no effect.
- Pass `nil` for `LevelName`/`MasterScript` to fall back to `Sys.GetLevelName()`/`Sys.GetMasterScriptName()`.