---
title: MrxGuiLoadScreen
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, loading screen]
---

# MrxGuiLoadScreen

*Module: mrxguiloadscreen.lua*

## Overview
The `MrxGuiLoadScreen` module is responsible for managing the loading screen GUI in the game. It handles the initialization, activation, and deactivation of the loading screen, as well as managing input events and animations related to saving icons.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages the loading screen GUI globally.

## Functions
### `HandleInit(oLoadScreen)`
Initializes the loading screen by setting up its properties, adding a Flash widget for rendering, and initializing save icon elements. This function sets the loading screen to use immortal events, fullscreen mode, and adds event handlers for input and state changes.

### `HandleStateChangeEvent(oLoadScreen, tData)`
Handles state change events by activating or deactivating the loading screen based on the `bLoading` flag in the event data.

### `_SetActive(oLoadScreen, bActive)`
Sets the active state of the loading screen. If the screen is being deactivated, it calls a Flash action script callback to close the loading screen and resets various flags. If the screen is being activated, it loads the Flash file if not already loaded and sets up the necessary properties.

### `_CompleteFlashLoad(oLoadScreen)`
Completes the loading of the Flash file by setting the `bFlashLoaded` flag and obtaining control focus for the loading screen.

### `HandleInput(oLoadScreen, tInput)`
Handles input events by updating the analog input state and calling appropriate Flash action script callbacks to handle left analog stick movement.

### `IsAnalog(nValue)`
Checks if a given value corresponds to an analog controller input.

### `_SaveIconAnimationComplete(oIcon)`
Handles the completion of the save icon animation by reversing the texture coordinates and restarting the animation.

### `HandleSaveIconShow(oContainer, tEvent)`
Shows the save icon by setting its visibility and starting the animation sequence.

### `HandleSaveIconHide(oContainer, tEvent)`
Hides the save icon by resetting its animation state and hiding it from view.

## Events
- Listens for custom event `ShowSaveIcon` to show the save icon.
- Listens for custom event `HideSaveIcon` to hide the save icon.
- Listens for `ControllerInput` events to handle player input during the loading screen.

## Notes for modders
- Ensure that the loading screen is properly initialized and activated when needed.
- Customize the Flash file used by setting `_gLoadFlashFile` to a different `.gfx` or `.swf` file.
- Be aware of the save icon animation behavior and adjust parameters like `_knSaveIconSize` and `_knSaveIconTime` as needed.
- The module uses `MrxGui` and `MrxGuiBase` for GUI operations, so ensure these modules are available and properly configured.