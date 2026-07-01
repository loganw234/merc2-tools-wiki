---
title: MrxGuiLoadLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, load screen]
---

# MrxGuiLoadLayout

*Module: mrxguiloadlayout.lua*

## Overview
The `MrxGuiLoadLayout` module is responsible for defining and managing the layout of the loading screen GUI. It sets up a container widget that includes a background image and a text widget displaying "Loading". The module also handles reinitialization of these widgets.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiLoadScreen`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state but manages the loading screen GUI layout and reinitialization.

## Functions
### `ReInit()`
Reinitializes the loading screen GUI by removing any previously added widgets and then adding new ones based on the predefined `LocalWidgetList`. This function is likely called when the game needs to refresh or reset the loading screen.

## Events
- Listens for custom events (not explicitly defined in this module) that trigger reinitialization of the loading screen.

## Notes for modders
- Ensure that `ReInit` is called appropriately to manage the loading screen layout.
- Customize the loading screen by modifying the fields in `LocalWidgetList`, such as widget positions, colors, and text content.
- Be aware that changes to the loading screen may affect user experience during game load times.