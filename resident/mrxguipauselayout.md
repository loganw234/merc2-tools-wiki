---
title: MrxGuiPauseLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, pause]
---

# MrxGuiPauseLayout

*Module: mrxguipauselayout.lua*

## Overview
The `MrxGuiPauseLayout` module is responsible for managing the layout and behavior of the pause screen in the game. It defines a widget list that includes properties such as position, color, visibility, and event handlers. The module also provides functionality to reinitialize the pause screen by removing existing widgets and adding new ones based on the defined layout.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGuiPauseScreen`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages global widget configurations and interactions.

## Functions
### `ReInit()`
Reinitializes the pause screen by removing existing widgets and adding new ones based on the defined layout in `LocalWidgetList`. This function ensures that the pause screen is correctly set up with all necessary widgets and event handlers.

## Events
- Listens for custom events to handle state changes, initialization, toggle events, and imposter shell events through the imported `MrxGuiPauseScreen` module.

## Notes for modders
- Ensure that `ReInit()` is called appropriately to refresh the pause screen layout.
- Customize widget properties by modifying the `LocalWidgetList` configuration.
- Be aware of event handlers defined in `MrxGuiPauseScreen` and ensure they are correctly implemented for custom behavior.