---
title: MrxGuiLoadLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, load screen]
verified: true
verified_note: confirmed zero Event.* calls (LoadStateChange/GuiInitialization are widget EventHandlers keys pointing into MrxGuiLoadScreen), only one top-level function (ReInit), no inherit; tightened Events section
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
Reinitializes the loading screen GUI by removing any previously added widgets and then adding new ones based on the predefined `LocalWidgetList`. This function is likely called when the game needs to refresh or reset the loading screen. This is the only top-level function defined in this file.

## Events
No `Event.Create`/`Event.*` engine-event references appear in this file — confirmed by grep. The root "Loading Screen" widget in `LocalWidgetList` wires its `EventHandlers.LoadStateChange` key to `MrxGuiLoadScreen.HandleStateChangeEvent` and its `EventHandlers.GuiInitialization` key to `MrxGuiLoadScreen.HandleInit` — both are widget-level event handler names, not `Event.*` constants, and both handler functions live in `mrxguiloadscreen.lua`, not this file. `ReInit()` itself is not wired to anything here; it's a plain callable function invoked directly by other code.

## Notes for modders
- Ensure that `ReInit` is called appropriately to manage the loading screen layout.
- Customize the loading screen by modifying the fields in `LocalWidgetList`, such as widget positions, colors, and text content.
- Be aware that changes to the loading screen may affect user experience during game load times.