---
title: MrxGuiBinoculars
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, binoculars]
---

# MrxGuiBinoculars

*Module: mrxguibinoculars.lua*

## Overview
The `MrxGuiBinoculars` module manages the behavior of the binoculars GUI in the game. It handles events related to entering and exiting the binoculars scope, updates various UI elements such as focus text, faction texture, and zoom level, and ensures proper HUD state management during these interactions.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGuiManager`, `MrxGui`, `MrxSound`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages the binoculars GUI based on events and player interactions.

## Functions
### `HandleBinocularsEnter(oWidget, tEvent)`
Called when a player enters the binoculars scope. It checks if the event's player GUID matches the widget's owner, plays the enter scope sound, sets the widget visible, toggles the HUD state if necessary, and animates the UI elements to their respective positions.

### `HandleBinocularsExit(oWidget, tEvent)`
Called when a player exits the binoculars scope. It disables all child widgets, animates the UI elements back to their original positions, restores the HUD state if toggled earlier, and plays the exit scope sound.

### `_FinishEnter(oWidget)`
A helper function that enables all child widgets, sets their locations, and makes them visible after the initial animation completes when entering the binoculars scope.

### `_FinishExit(oWidget)`
A helper function that hides the widget, restores the HUD state if toggled earlier, and resets various custom data fields after the exit animation completes.

### `HandleInitialization(oWidget)`
Initializes the binoculars GUI by setting it invisible, disabling all child widgets, storing references to key UI elements, and configuring animation points for zooming effects.

### `HandleHeadingUpdate(oWidget, tEvent)`
Updates the position of a pointer on the binoculars GUI based on the player's camera heading. It ensures the pointer stays within the bounds of the widget.

### `HandleZoomUpdate(oWidget, tEvent)`
Updates the position of a pointer on the binoculars GUI based on the zoom level. It ensures the pointer stays within the bounds of the widget.

### `HandleFactionUpdate(oWidget, tEvent)`
Updates the faction texture and translucency of the binoculars GUI based on the event's faction texture information.

### `HandleFocusUpdate(oWidget, tEvent)`
Updates the focus text and description in the binoculars GUI based on the event's focus name and GUID. It also posts an "InFocus" event to notify other systems about the current focus target.

### `HandleVertScrollUpdate(oWidget, tEvent)`
Updates the vertical scroll position of a pointer on the binoculars GUI based on the player's pitch angle. It ensures the pointer stays within the bounds of the widget.

## Events
- Listens for custom event `BinocularsEnter` to call `HandleBinocularsEnter`.
- Listens for custom event `BinocularsExit` to call `HandleBinocularsExit`.
- Listens for custom event `Initialization` to call `HandleInitialization`.
- Listens for custom event `HeadingUpdate` to call `HandleHeadingUpdate`.
- Listens for custom event `ZoomUpdate` to call `HandleZoomUpdate`.
- Listens for custom event `FactionUpdate` to call `HandleFactionUpdate`.
- Listens for custom event `FocusUpdate` to call `HandleFocusUpdate`.
- Listens for custom event `VertScrollUpdate` to call `HandleVertScrollUpdate`.

## Notes for modders
- Ensure that the binoculars GUI events (`BinocularsEnter`, `BinocularsExit`, etc.) are properly triggered in your mod to manage the UI behavior.
- Customize the appearance and behavior of the binoculars GUI by modifying the animation points, pointer positions, and other custom data fields as needed.
- Be aware that toggling the HUD state during binoculars use may affect the player's experience, so test thoroughly in multiplayer scenarios.