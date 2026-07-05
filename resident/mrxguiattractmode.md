---
title: MrxGuiAttractMode
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, attract]
verified: true
verified_note: 'deeper pass: re-confirmed the GuiGameStateChange/ControllerInput SetEventHandler bindings and all six functions against source; added the _tMovies={"attract"} movie name, the Letterbox movie fullscreen mode, and the game-state strings — flagged the "shell" (lowercase, SetEndCallback) vs "Shell" (HandleInput) case mismatch'
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

## Module constants & tunables
- **`_tMovies = {"attract"}`** (set in `Init`) — the attract-mode playlist. `_Open` plays entries in order,
  advancing `nMovieNum` and wrapping back to `1` at the end, so adding entries here (`{"attract", "attract2", …}`)
  makes attract mode cycle through multiple movies. This is the main mod lever on this page.
- **Movie widget mode: `"Letterbox"`** (`HandleInit`) — the attract movie is presented letterboxed, unlike the
  shell's `"pan and scan"` intro.
- **Game-state strings:** enters/exits on `"Attract"` (`HandleGameStateChangeEvent`); requests `"Shell"` on
  controller input (`HandleInput`) and `"shell"` when a movie ends (`_Open`'s `SetEndCallback`).

{: .note }
> The movie-end callback requests state `"shell"` (lowercase) while the input handler requests `"Shell"`
> (capitalized). If `Sys.RequestGameState` is case-sensitive these hit different code paths — worth knowing if you
> repurpose attract mode and one exit route behaves differently from the other. (Case sensitivity not verified.)

## Notes for modders
- `_Open` early-returns when `CustomData.bActive` is already true. `HandleInit` sets `bActive = true` *before*
  calling `Close()`, so the first real open happens through the `"Attract"` game-state enter path, not directly.
- Any controller input during attract mode requests the `"Shell"` state and latches `bClosing` so a second input
  can't double-fire the transition.