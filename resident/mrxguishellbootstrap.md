---
title: MrxGuiShellBootstrap
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, shell]
verified: true
verified_note: 'deeper pass: re-confirmed the Events section (zero Event.* — pure GUI-load-callback wiring), the module-level fields, and the unused SetExitSingleplayerCallback; added the concrete front-end layout asset names (MrxGuiLoadLayout/MrxGuiAttractLayout/MrxGuiCinematicLayout/MrxGuiLTIPrecacheLayout/MrxGuiShellLayout) and the two Sys.RequestGameState strings ("LTI_precache"/"Shell")'
---

# MrxGuiShellBootstrap

*Module: mrxguishellbootstrap.lua*

## Overview
The `MrxGuiShellBootstrap` module is responsible for managing the loading and display of various GUI layouts in the game's front-end, including the main shell interface, precache screen, and attract/cinematic screens. It handles the initialization of GUI files, manages widget visibility, and provides functions to enter and exit different game states.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGui`, `MrxGuiBase`

## Instance pattern
Stateless singleton/utility module — plain module-level globals, no `Create`/`OnActivate`/`Awake`/`tInstance`. Key fields:
- `oPrecacheModule` / `oShellModule`: the currently-loaded precache-screen / shell-screen module handles, set by the various `*Loaded` callbacks, cleared by `Reset()`/`ExitShell()`.
- `nPlayersSelected`: initialized to `1`. Not read or written anywhere in this file — read externally via `MrxGuiShellBootstrap.nPlayersSelected` by `mrxguibootstrap.lua`, and reset to `1` externally by `mrxguishell.lua`.
- `bNeedsReloading`: initialized to `false`. Not read anywhere in this file — set to `true` externally by `mrxguishell.lua`.
- `_sSelectedCharacter`: initialized to `false`, set/read via `SetSelectedCharacter`/`GetSelectedCharacter` (the latter returns `nil` instead of `false` when unset).
- Four callback-slot pairs (`f*CallbackFunction` + `t*CallbackArguments`) for entering/exiting singleplayer/multiplayer, set via the four `Set*Callback` functions. Three of the four have a matching "run it" function (`SetUpSingleplayer`/`SetUpMultiplayer`/`ExitMultiplayer`); see the `SetExitSingleplayerCallback` function entry below for the one that doesn't.

## Functions
### `Init()`
Called during the initialization of the module. Loads the initial GUI layouts for attract and cinematic screens.

### `LoadMovieLayouts()`
Loads additional GUI files for attract and cinematic layouts after initializing fade flash effects.

### `Reset()`
Resets the shell module by removing all widgets in the current layout and cleaning up fade flash effects.

### `EnterPrecache()`
Enters the precache screen by loading its GUI layout. Logs a debug message when called.

### `PrecacheScreenLoaded(PrecacheScreenModule)`
Handles the completion of loading the precache screen. Sets the visibility of the precache widget, restarts and plays its flash animation, and requests the game state to "LTI_precache".

### `LoadPrecache()`
Loads the precache screen layout again.

### `ClosePrecacheOnLoad(PrecacheScreenModule)`
Closes the precache screen by setting its visibility to false and calling `EnterShell` to load the main shell interface. Logs debug messages at various stages.

### `EnterShell()`
Enters the main shell interface by loading its GUI layout.

### `ExitShell()`
Exits the shell interface by closing it, cleaning up fade flash effects, and setting related variables to nil.

### `ShellScreenLoaded(ShellScreenModule)`
Handles the completion of loading the shell screen. Requests the game state to "Shell" and sets the shell module variable.

### `LoadShell()`
Loads the main shell interface layout again.

### `CloseShellOnLoad(ShellScreenModule)`
Closes the shell screen by setting its visibility to false, disabling all child widgets, and cleaning up related variables.

### `SetUpSingleplayer()`
Sets up the single-player game state by calling a callback function with provided arguments if it is defined.

### `SetUpMultiplayer()`
Sets up the multiplayer game state by calling a callback function with provided arguments if it is defined.

### `ExitMultiplayer()`
Exits the multiplayer game state by calling a callback function with provided arguments if it is defined.

### `SetSelectedCharacter(sCharacter)`
Sets the selected character to the specified string.

### `GetSelectedCharacter()`
Returns the currently selected character or nil if none is set.

### `SetEnterSingleplayerCallback(fFunction, tArguments)`
Sets the callback function and its arguments for entering the single-player game state.

### `SetExitSingleplayerCallback(fFunction, tArguments)`
Sets `fExitSingleplayerCallbackFunction`/`tExitSingleplayerCallbackArguments`. **Note:** unlike its three siblings (`SetEnterSingleplayerCallback` → `SetUpSingleplayer`, `SetEnterMultiplayerCallback` → `SetUpMultiplayer`, `SetExitMultiplayerCallback` → `ExitMultiplayer`), there is no corresponding "run this callback" function anywhere in this file, and no other file in the decompiled `resident/` corpus reads `fExitSingleplayerCallbackFunction`/`tExitSingleplayerCallbackArguments` either. Whatever this was meant to drive appears unused/vestigial, at least within this corpus.

### `SetEnterMultiplayerCallback(fFunction, tArguments)`
Sets the callback function and its arguments for entering the multiplayer game state.

### `SetExitMultiplayerCallback(fFunction, tArguments)`
Sets the callback function and its arguments for exiting the multiplayer game state.

## Events
No `Event.*` calls appear anywhere in this file. GUI-load completion is handled by plain callback functions passed as arguments to `MrxGuiBase.LoadGUIFile(sLayoutName, fCallback, ...)` — e.g. `EnterPrecache` passes `PrecacheScreenLoaded`, `EnterShell` passes `ShellScreenLoaded`, `LoadPrecache` passes `ClosePrecacheOnLoad`, `LoadShell` passes `CloseShellOnLoad`, `Init` passes `LoadMovieLayouts`. This is a direct function-reference callback, not the engine `Event` system or `MrxGui.SendEvent`'s `EventType`-table pattern seen in other GUI modules (e.g. `mrxguimanager.lua`).

## Module constants & tunables
- **Front-end layout asset names** loaded here (all via `MrxGuiBase.LoadGUIFile`):
  `"MrxGuiLoadLayout"` (loaded first, in `Init`), `"MrxGuiAttractLayout"` + `"MrxGuiCinematicLayout"` (loaded by
  `LoadMovieLayouts`), `"MrxGuiLTIPrecacheLayout"` (precache), and `"MrxGuiShellLayout"` (main shell). These are
  the raw layout definitions behind the [attract](mrxguiattractlayout)/[precache](mrxguiltiprecachelayout)/
  [shell](mrxguishelllayout) screens.
- **Game-state strings** passed to `Sys.RequestGameState`: `"LTI_precache"` (from `PrecacheScreenLoaded`) and
  `"Shell"` (from `ShellScreenLoaded`). These are the engine state names the front-end transitions request.
- **Named widgets driven here:** `"LTI_precache"` (precache flash; its `CustomData.oFlash` is
  `Restart()`/`Play()`ed on show) and `"Shell"` (the shell root, hidden + children disabled by `CloseShellOnLoad`).

## Notes for modders
- Use `EnterPrecache`, `EnterShell`, and related functions to manage transitions between different game states.
- `EnterPrecache`/`EnterShell` vs `LoadPrecache`/`LoadShell` are two different entry points into the same layouts: the `Enter*` pair makes the screen visible and requests the corresponding game state; the `Load*` pair (`LoadPrecache`/`LoadShell`) loads the layout but immediately hides it and disables its children (`ClosePrecacheOnLoad`/`CloseShellOnLoad`) — apparently a pre-warm/pre-load path distinct from actually entering that screen.
- Customize callback functions for entering and exiting single-player or multiplayer modes by setting appropriate functions and arguments using the provided setter functions — but note `SetExitSingleplayerCallback`'s stored callback has no known consumer (see its Functions entry above).
- Be aware of widget visibility and state management when extending or modifying GUI interactions.