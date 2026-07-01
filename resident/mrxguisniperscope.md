---
title: MrxGuiSniperscope
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, sniper]
---

# MrxGuiSniperscope

*Module: mrxguisniperscope.lua*

## Overview
The `MrxGuiSniperscope` module is responsible for managing the sniper scope GUI elements in the game. It handles events related to entering and exiting the sniper scope, updating health information, zoom level, camera heading, focus updates, faction texture, and horizontal/vertical scroll updates. The module ensures that the GUI elements are correctly displayed and updated based on player actions and game state.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGuiManager`, `MrxGui`, `MrxSound`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but rather manages global GUI elements related to the sniper scope.

## Functions
### `HandleSniperScopeEnter(oWidget, tEvent)`
Called when the player enters the sniper scope. It sets up the GUI elements and plays the enter scope sound.

### `HandleSniperScopeExit(oWidget, tEvent)`
Called when the player exits the sniper scope. It cleans up the GUI elements and plays the exit scope sound.

### `_FinishEnter(oWidget)`
Finishes the process of entering the sniper scope by enabling all child widgets and setting their locations and visibilities.

### `_FinishExit(oWidget)`
Finishes the process of exiting the sniper scope by hiding all child widgets and restoring the HUD state if necessary.

### `HandleInitialization(oWidget, tEvent)`
Initializes the sniper scope GUI elements. It sets up the widget visibility, enables/disables child widgets, and initializes custom data for the widget.

### `HandleSniperHealthInit(oWidget, tEvent)`
Initializes the health bar for the sniper scope GUI element.

### `HandleSniperHealthUpdate(oWidget, nTargetRelation, nScreenX, nScreenY, nSpreadX, nSpreadY, nHealth, nMaxHealth)`
Updates the health bar based on the current health and maximum health of the target.

### `HandleZoomUpdate(oWidget, tEvent)`
Updates the zoom level display in the sniper scope GUI element.

### `HandleHeadingUpdate(oWidget, tEvent)`
Updates the camera heading display in the sniper scope GUI element.

### `HandleFocusUpdate(oWidget, tEvent)`
Updates the focus name and description in the sniper scope GUI element.

### `HandleFactionUpdate(oWidget, tEvent)`
Updates the faction texture in the sniper scope GUI element based on the faction type.

### `HandleHorizScrollUpdate(oWidget, tEvent)`
Updates the horizontal scroll texture coordinates based on the camera heading.

### `HandleVertScrollUpdate(oWidget, tEvent)`
Updates the vertical scroll texture coordinates based on the pitch.

### `_RecursiveWakeup(oWidget, bAwaken)`
Recursively sets the sleeping state of a widget and its children to either awake or asleep.

## Events
- Listens for custom event `SniperScopeEnter` to handle entering the sniper scope.
- Listens for custom event `SniperScopeExit` to handle exiting the sniper scope.
- Listens for custom event `Initialization` to initialize the sniper scope GUI elements.
- Listens for custom event `SniperHealthInit` to initialize the health bar.
- Listens for custom event `SniperHealthUpdate` to update the health bar.
- Listens for custom event `ZoomUpdate` to update the zoom level display.
- Listens for custom event `HeadingUpdate` to update the camera heading display.
- Listens for custom event `FocusUpdate` to update the focus name and description.
- Listens for custom event `FactionUpdate` to update the faction texture.
- Listens for custom event `HorizScrollUpdate` to update the horizontal scroll texture coordinates.
- Listens for custom event `VertScrollUpdate` to update the vertical scroll texture coordinates.

## Notes for modders
- Ensure that the sniper scope GUI elements are correctly initialized and updated by handling the appropriate events.
- Customize the behavior of the sniper scope GUI elements by modifying the functions in this module.
- Be aware of the dependencies on `MrxGuiManager`, `MrxGui`, and `MrxSound` for managing GUI elements, sound playback, and other functionalities.