---
title: MrxGuiLTIPrecache
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: MrxGuiBase
tags: [gui, loading screen]
---

# MrxGuiLTIPrecache

*Module: mrxguiltiprecache.lua*

## Overview
The `MrxGuiLTIPrecache` module is responsible for managing the pre-cache loading screen in the game. It handles the initialization, display, and interaction with the pre-cache flash animation, ensuring that the loading process is visually engaging and user-friendly.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiManager`, `MrxGuiDialogBox`

## Instance pattern
This module does not follow the per-instance object pattern. It manages the pre-cache screen as a stateless utility module, tracking the following key fields:
- `bActive`: Indicates whether the pre-cache screen is currently active.
- `oFlash`: The flash widget used for displaying the pre-cache animation.
- `bHaveFlash`: A boolean indicating if the flash widget has been successfully loaded.
- `tHudStates`: A table to store HUD states.

## Functions
### `OpenPrecache(oPrecacheScreen)`
Called when the pre-cache screen should be opened. It checks if the flash widget is available, resets it, and starts playing the animation. Sets the screen as active and visible.

### `ClosePrecacheScreen(oPrecacheScreen)`
Called when the pre-cache screen should be closed. It stops the flash animation, releases control focus, hides the screen, and removes any child widgets.

### `HandleStateChangeEvent(oWidget, sStateName, sStateAction)`
Handles state change events for the pre-cache screen. If the state name is "Precache" and the action is "Exit", it closes the pre-cache screen.

### `HandleInitializationEvent(oWidget, tUnused)`
Handles initialization events for the pre-cache screen. It sets the screen to fullscreen mode, closes any pause screens, and initializes custom data fields.

### `_Initialize(oPrecacheScreen)`
The main initialization function for the pre-cache screen. It creates a flash widget, sets its properties, adds it as a child of the pre-cache screen, and registers various event handlers. It also opens the pre-cache screen.

### `_FinishLoad(oPrecacheScreen)`
Called when the flash file has finished loading. It marks the flash widget as available and calls another function to handle the completion of the pre-cache process.

### `_HandleToggleEvent(oPrecacheScreen, tUnused)`
Handles toggle events for the pre-cache screen. If the screen is active, it closes it; otherwise, it opens it.

### `_HandleCloseEvent(oFlash)`
Called when the flash widget should be closed. It checks if the pre-cache screen is active and closes it if necessary.

### `_HandleInput(oPrecacheMenu, tInput)`
Handles input events for the pre-cache menu. It passes the input to the flash widget's event handlers.

### `IsAnalog(nValue)`
Checks if a given value corresponds to an analog input (e.g., joystick buttons).

### `_LTIPrecacheDone(oFlash, iNumber)`
Called when the pre-cache process is done. It triggers a function in the `LTILibName` module to handle the completion of the pre-cache.

### `_LTIPrecacheDone2()`
A secondary function called after `_LTIPrecacheDone`. It also triggers a function in the `LTILibName` module.

### `_LTIPrecacheSmokeDone(oFlash, iNumber)`
Called when the smoke effect during pre-cache is done. It triggers a function in the `LTILibName` module to handle the completion of the smoke effect.

### `_LTIPrecacheSmokeDone2()`
A secondary function called after `_LTIPrecacheSmokeDone`. It also triggers a function in the `LTILibName` module.

### `_LTIUpdateTo(oFlash, iNumber)`
Updates the pre-cache screen to a specific state by calling an action script callback on the flash widget.

## Events
- Listens for custom events related to the pre-cache process and handles them accordingly.
- Triggers functions in the `LTILibName` module when specific stages of the pre-cache are completed.

## Notes for modders
- Ensure that the pre-cache screen is properly initialized and closed to avoid resource leaks or display issues.
- Customize the pre-cache animation by modifying the flash widget's properties or replacing the SWF file.
- Be aware of the dependencies on `MrxGuiBase`, `MrxGuiManager`, and `MrxGuiDialogBox` when extending or modifying this module.
- The decompiler artifacts include unused local variables and redundant operator groupings, which should be ignored.