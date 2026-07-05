---
title: MrxGuiAttractMode
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, attract]
verified: true
verified_note: clarified Events section — GuiGameStateChange/ControllerInput are widget SetEventHandler bindings made in this file's own HandleInit, not Event.* engine constants; rest of page confirmed accurate against source
---

# MrxGuiAttractMode

*Module: mrxguiattractmode.lua*

## Overview
The `MrxGuiAttractMode` module is responsible for managing the attract mode screen in the game. It handles the initialization, opening, and closing of the attract mode GUI, including playing movies and handling input to transition to the shell menu.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGui`, `MrxGuiBase`, `MrxSound`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages global attract mode behavior through custom data fields in the widget.

## Functions
### `Init()`
Initializes the list of movies to play in attract mode, setting `_tMovies` to `{"attract"}`.

### `HandleInit(oWidget)`
Handles the initialization of the attract mode GUI widget. It sets up event handlers for game state changes and controller input, configures the movie widget, and prepares the widget for opening.

### `HandleGameStateChangeEvent(oWidget, sStateName, sStateAction)`
Responds to changes in the game state. If entering or exiting the "Attract" state, it calls `_Open` or `_Close`, respectively.

### `HandleInput(oWidget, tEvent)`
Handles controller input events. When an input is detected and the widget is not closing, it requests a transition to the shell menu and sets a flag to prevent further transitions.

### `_Open(oWidget)`
Opens the attract mode GUI. It checks if the widget is already active, sets it visible, plays the next movie in the list, and starts the fade-in effect. It also handles sound and control focus changes.

### `_Close(oWidget)`
Closes the attract mode GUI. It stops the current movie, hides the widget, removes child widgets, releases control focus, and handles sound state changes.

## Events
This file has no `Event.*` references (no `Event.Create`, no engine event constants). Both bindings
below are widget-level `SetEventHandler` calls made directly in this file's own `HandleInit`, not the
engine `Event.*` system:
- `oWidget:SetEventHandler("GuiGameStateChange", HandleGameStateChangeEvent)` — opens/closes attract
  mode when the game state enters/exits `"Attract"`.
- `oWidget:SetEventHandler("ControllerInput", HandleInput)` — on any controller input while not already
  closing, requests a transition to the `"Shell"` game state.

## Notes for modders
- Ensure that `Init`, `HandleInit`, `_Open`, and `_Close` are called appropriately to manage the lifecycle of the attract mode GUI.
- Customize the list of movies in `_tMovies` to change the content played during attract mode.
- Be aware of the transition logic between attract mode and other game states, especially when handling controller input.