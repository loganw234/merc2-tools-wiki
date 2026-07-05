---
title: MrxGuiCinematicLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, cinematic]
verified: true
verified_note: confirmed no Event.* calls (widget EventHandlers keys only), only one top-level function (ReInit), no inherit; minor Events-section wording fix
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
Reinitializes the cinematic GUI by removing any previously added widgets and loading new ones from the predefined `LocalWidgetList`. This function ensures that the cinematic interface is correctly set up for each sequence. This is the only top-level function defined in this file.

## Events
No `Event.Create`/`Event.*` engine-event references appear in this file. The `LocalWidgetList` table wires two widgets' `EventHandlers.GuiInitialization` key directly to functions from the imported `MrxGuiCinematic` module (`MrxGuiCinematic._HandleInitializationEvent` on the root widget, `MrxGuiCinematic._InitializeSubtitleBuffer` on the "Movie subtitle" child) — these are Scaleform/widget-level event handler names (dispatched by the GUI system when a widget initializes), not `Event.*` engine constants, and the handler functions themselves live in `mrxguicinematic.lua`, not this file.

## Notes for modders
- Ensure that `ReInit()` is called appropriately to manage the lifecycle of cinematic GUI elements.
- Customize widget properties by modifying the fields in `LocalWidgetList`.
- Be aware that changes to widget configurations may affect the visual presentation and functionality of cinematics.