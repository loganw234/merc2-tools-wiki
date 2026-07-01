---
title: MrxGuiCinematicLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, cinematic]
---

# MrxGuiCinematicLayout

*Module: mrxguicinematiclayout.lua*

## Overview
The `MrxGuiCinematicLayout` module is responsible for managing the layout and initialization of widgets used in cinematic sequences within the game. It defines a set of local widget configurations and provides functions to reinitialize these widgets, ensuring they are correctly loaded and displayed during cinematic events.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGuiCinematic`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages the layout of widgets used in cinematics.

## Functions
### `ReInit()`
Reinitializes the cinematic GUI by removing any previously added widgets and loading new ones from the predefined `LocalWidgetList`. This function ensures that the cinematic interface is correctly set up for each sequence.

## Events
- Listens for custom event `GuiInitialization` to handle initialization of specific widgets, such as setting up subtitle buffers.

## Notes for modders
- Ensure that `ReInit()` is called appropriately to manage the lifecycle of cinematic GUI elements.
- Customize widget properties by modifying the fields in `LocalWidgetList`.
- Be aware that changes to widget configurations may affect the visual presentation and functionality of cinematics.