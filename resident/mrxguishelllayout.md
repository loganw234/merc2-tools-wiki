---
title: MrxGuiShellLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, layout]
---

# MrxGuiShellLayout

*Module: mrxguishelllayout.lua*

## Overview
The `MrxGuiShellLayout` module defines the layout and event handling for a GUI shell in the game. It sets up a main widget with child widgets, each configured with properties like position, color, visibility, and event handlers. The module also provides functionality to reinitialize the GUI layout.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `mrxguishell`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module (no per-instance tables). It tracks the following key fields:
- `LocalWidgetList`: A table containing the layout data for the GUI shell and its child widgets.
- `AddedWidgetList`: A table to keep track of added widgets during initialization.

## Functions
### `ReInit()`
Reinitializes the GUI layout by removing any previously added widgets and then loading and adding new widgets from the `LocalWidgetList`. This function is used to refresh or reset the GUI when needed.

## Events
- Listens for custom event `GuiInitialization` to call `MakeFullscreen` on the background widget.
- Listens for various other events like `LobbyServerUpdated`, `LobbyServerAdded`, `ControllerInput`, `LobbyServerRemoved`, and `GuiGameStateChange` through the imported `mrxguishell` module.

## Notes for modders
- Ensure that the `ReInit` function is called appropriately to refresh the GUI layout.
- Customize widget properties by modifying the `LocalWidgetList` table before calling `ReInit`.
- Be aware of event handlers and ensure they are correctly set up in the `EventHandlers` table for each widget.
- The module uses the `MrxGuiBase` library to manage widgets, so any modifications should be compatible with its API.