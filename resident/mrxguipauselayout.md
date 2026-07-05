---
title: MrxGuiPauseLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, pause]
verified: true
verified_note: named the four real EventHandlers entries (Events section was vague); flagged AddedWidgetList as never initialized in this file (relies on external MrxGuiBase-style setup)
---

# MrxGuiPauseLayout

*Module: mrxguipauselayout.lua*

## Overview
The `mrxguipauselayout.lua` file is a layout-data file (like `mrxguiltiprecachelayout.lua`) defining a single full-screen `"Pause Layout"` widget in `LocalWidgetList[1]`, plus one function, `ReInit()`, that swaps the currently-added widgets for the ones described by that layout. It imports `MrxGuiPauseScreen` (for the widget's event handlers) and `MrxGuiBase` (for the widget add/remove API used by `ReInit`).

## Inheritance
- Inherits from: `none` (base/utility module; no `inherit(...)` call)
- Imports: `MrxGuiPauseScreen`, `MrxGuiBase`

## Instance pattern
Not applicable. No `Create`/`OnActivate`/`Awake`/`tInstance` — a static layout table plus one free function operating on module-level globals (`LocalWidgetList`, `AddedWidgetList`).

## Functions
### `ReInit()`
Rebuilds the pause screen's active widget set from `LocalWidgetList`. For every entry currently in `AddedWidgetList`, calls `MrxGuiBase.RemoveWidget(...)` on it, resets `AddedWidgetList` to `{}`, then for every entry in `LocalWidgetList` calls `MrxGuiBase.LoadAndAddWidgetFromLayoutFileData(LocalWidgetList[i], AddedWidgetList)` to (re)add it.

Note: `AddedWidgetList` is never declared/initialized anywhere in this file before `ReInit`'s first `pairs(AddedWidgetList)` call — `pairs(nil)` would raise a Lua error. No call sites for `ReInit` were found in this file itself, so whatever caller (likely `MrxGuiBase`'s widget-loading machinery, which sets `ModuleName.AddedWidgetList = {}` on modules it manages) must guarantee `AddedWidgetList` already exists as a table by the time `ReInit` runs. Not confirmable from this file alone.

## Events
No `Event.*` calls appear in this file. `LocalWidgetList[1].EventHandlers` wires four GUI-system event names to `MrxGuiPauseScreen` functions:
- `GuiGameStateChange` → `MrxGuiPauseScreen.HandleStateChangeEvent`
- `GuiInitialization` → `MrxGuiPauseScreen._Initialize`
- `TogglePAUSE` → `MrxGuiPauseScreen._HandleToggleEvent`
- `ImposterShellEvent` → `MrxGuiPauseScreen.HandleImposterEvent`

## Notes for modders
- Actual pause-screen behavior lives in `MrxGuiPauseScreen`, not here — this file only supplies layout/position data and the handler-name wiring.
- `ReInit()` is a full widget teardown/rebuild — calling it discards whatever's currently in `AddedWidgetList` and reloads fresh from `LocalWidgetList`, so any per-widget runtime state set outside this layout is lost.
- Widget geometry (0,0)-(640,480), anchored center/center, mirrors the pattern used by `mrxguiltiprecachelayout.lua` for a full-screen widget.