---
title: MrxGuiAttractLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, layout]
verified: true
verified_note: 'deeper pass: re-confirmed the GuiInitialization→MrxGuiAttractMode.HandleInit wiring and ReInit against source; added the widget geometry (640x480 container "Attract" + black "attract bg" child) constants'
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

## Widget geometry
- **`"Attract"` root:** full-screen `640×480` `container` widget, white (`255,255,255,255`), center-anchored. Its
  one handler is `GuiInitialization` → [`MrxGuiAttractMode.HandleInit`](mrxguiattractmode), which builds the actual
  letterboxed `MovieWidget` at runtime.
- **`"attract bg"` child:** full-screen `640×480` **black** (`0,0,0,255`) image, full UV, no handlers — the
  backdrop the attract movie plays over.

## Notes for modders
- This file is pure layout data. All attract behavior (movie playback, input-to-shell transition) lives in
  [`MrxGuiAttractMode`](mrxguiattractmode); the movie playlist is its `_tMovies` table, not anything here.
- `ReInit()` is a full teardown/rebuild of the widget tree (same `AddedWidgetList`-must-pre-exist caveat as the
  other layout files).