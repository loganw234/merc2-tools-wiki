---
title: GameBootstrap
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [init, intro]
verified: true
verified_note: corrected Events section (no Event.* calls in this file at all — movie sequencing uses MovieWidget:SetEndCallback, not the Event system); added tMovies/_oIntroMovieWidget to Instance pattern; all 4 functions confirmed
---

# GameBootstrap

*Module: gamebootstrap.lua*

## Overview
The `GameBootstrap` module is responsible for initializing the game environment and playing introductory movies. It sets up the necessary components such as sound and GUI systems, then routes to the appropriate shell, lobby, or autoload level based on configuration settings.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `LevelBootstrap`, `MrxSoundBootstrap`, `MrxGuiShellBootstrap`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module — no `uGuid`, no `OnActivate`/`Awake`/`Create`, no `tInstance` registry. It runs once at process/game startup and tracks module-level globals instead:
- `tMovies`: hardcoded list of `{sMovieName, nLoopTime}` pairs — `{"Pandemic", -1}` and `{"EA", -1}` (a `nTime` of `-1` means non-looping, per `bLoop = -1 < nTime` in `_PlayMovie`).
- `_oIntroMovieWidget`: the active `MrxGuiBase.MovieWidget` instance, or `nil` when no movie is playing.
- `_nMovie` (declared without `local` inside `_PlayMovie`, so it's a global): the index of the current movie in `tMovies`.

## Functions
### `_PlayMovie()`
Advances `_nMovie` and plays the next entry in `tMovies`. If the next slot is empty (no more movies) or `_oIntroMovieWidget` is `nil`, it logs "All movies complete", removes/deletes the movie widget via `MrxGuiBase.RemoveWidget` + `:delete()`, clears `_oIntroMovieWidget`, and calls `Start()`. Otherwise it sets the widget's movie, registers a local `_EndMovie` closure as the end callback (via `:SetEndCallback`), and calls `:Play()`. `_EndMovie` stops the widget and recurses into `_PlayMovie()` to advance to the next one.

### `Init()`
The primary initialization function called by the engine. Calls `Sys.SetLuaSaveVersion(GetSaveDataVersion())`, sets gamma via `Graphics.SetGamma(0, 0.8, 1)`, and bails early (returns) if `Sys.FinishedShell()` is true. If `Sys.PlayIntroMovies()` returns false, it calls `Start()` directly and returns. Otherwise it creates `_oIntroMovieWidget` as a new `MrxGuiBase.MovieWidget`, sets it fullscreen-letterboxed and pause-ignoring, adds it via `MrxGuiBase.AddWidget`, and kicks off `_PlayMovie()`.

### `Start()`
Determines the next step in the game startup process based on network and auto-load settings, in this priority order: `Net.AutoClient()` (load shell, `Net.ConnectToServer()`), `Net.AutoLobby()` (load shell, `Net.EnterLobby()`), `Sys.AutoLoad()` with `Net.AutoServer()` (load shell, `Net.StartServer(...)`), `Sys.AutoLoad()` alone (`LevelBootstrap.LoadLevel(...)` directly, no shell), else falls through to `MrxGuiShellBootstrap.EnterShell()`.

### `GetSaveDataVersion()`
Returns the save data version number, hardcoded to `3`.

## Events
This file contains no `Event.*` calls at all — no `Event.Create`, no engine event constants. Movie sequencing is driven entirely by `MovieWidget:SetEndCallback(_EndMovie, {sMovie})`, a widget-level callback, not the engine Event system used elsewhere in this codebase.

## Notes for modders
- Ensure that `Init` and `Start` are called appropriately during game startup.
- Customize the list of intro movies in `tMovies` if you want to change or add new introductory content.
- Be aware that modifying save data version may affect compatibility with existing saves.