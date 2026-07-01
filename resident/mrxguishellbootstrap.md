---
title: MrxGuiShellBootstrap
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, shell]
---

# MrxGuiShellBootstrap

*Module: mrxguishellbootstrap.lua*

## Overview
The `MrxGuiShellBootstrap` module is responsible for managing the loading and display of various GUI layouts in the game's front-end, including the main shell interface, precache screen, and attract/cinematic screens. It handles the initialization of GUI files, manages widget visibility, and provides functions to enter and exit different game states.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGui`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages global GUI layout loading and widget interactions.

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
Sets the callback function and its arguments for exiting the single-player game state.

### `SetEnterMultiplayerCallback(fFunction, tArguments)`
Sets the callback function and its arguments for entering the multiplayer game state.

### `SetExitMultiplayerCallback(fFunction, tArguments)`
Sets the callback function and its arguments for exiting the multiplayer game state.

## Events
- Listens for custom events to manage GUI layout loading and widget interactions (e.g., precache screen loaded, shell screen loaded).

## Notes for modders
- Ensure that `Init` is called during module initialization to load initial GUI layouts.
- Use `EnterPrecache`, `EnterShell`, and related functions to manage transitions between different game states.
- Customize callback functions for entering and exiting single-player or multiplayer modes by setting appropriate functions and arguments using the provided setter functions.
- Be aware of widget visibility and state management when extending or modifying GUI interactions.