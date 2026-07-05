---
title: MrxGuiAttractLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, layout]
verified: true
verified_note: clarified Events section — GuiInitialization is a widget EventHandlers table key (visible in this file's own LocalWidgetList literal), not an Event.* engine constant; rest of page confirmed accurate
---

# MrxGuiAttractLayout

*Module: mrxguiattractlayout.lua*

## Overview
The `MrxGuiAttractLayout` module defines the layout and initialization of a GUI attract mode screen. It sets up a widget list containing a main container with an image background, and provides functionality to reinitialize the GUI by removing and reloading widgets.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiAttractMode`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages global GUI widget lists.

## Functions
### `ReInit()`
Reinitializes the GUI by removing all added widgets and reloading them from the local widget list. This function is used to refresh or reset the attract mode screen.

## Events
This file has no `Event.*` references (no `Event.Create`, no engine event constants). The one
"listener" here is a widget-layout `EventHandlers` table entry, visible directly in this file's own
`LocalWidgetList[1]` literal: `EventHandlers = {GuiInitialization = MrxGuiAttractMode.HandleInit}`
(mirrored in `EventHandlerNames = {GuiInitialization = "HandleInit"}`). This is the GUI layout system's
own widget-event dispatch (triggered when the widget is loaded/added), not the engine `Event.*` system
used elsewhere in `resident/`.

## Notes for modders
- Ensure that `ReInit` is called appropriately to manage the lifecycle of the GUI widgets.
- Customize the widget properties by modifying the `LocalWidgetList` table before calling `ReInit`.
- Be aware that the module imports `MrxGuiAttractMode` and `MrxGuiBase`, so any modifications to these modules may affect this layout.