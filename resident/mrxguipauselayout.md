---
title: MrxGuiPauseLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, pause]
verified: true
verified_note: 'deeper pass: cross-linked MrxGuiPauseScreen/MrxGuiBase and mapped each EventHandlers key to its target function; re-confirmed the single "Pause Layout" widget, ReInit, and the uninitialized-AddedWidgetList caveat; no source contradictions found'
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
No `Event.*` calls appear in this file. `LocalWidgetList[1].EventHandlers` wires four GUI-system event names to [MrxGuiPauseScreen](mrxguipausescreen) functions (the parallel `EventHandlerNames` table holds the same bindings as strings, which is how the loader re-resolves them):
- `GuiGameStateChange` → `MrxGuiPauseScreen.HandleStateChangeEvent` (opens/closes on entering/exiting the "Pause" game state)
- `GuiInitialization` → `MrxGuiPauseScreen._Initialize` (builds the backdrop + `pause_menu` flash on first load)
- `TogglePAUSE` → `MrxGuiPauseScreen._HandleToggleEvent`
- `ImposterShellEvent` → `MrxGuiPauseScreen.HandleImposterEvent`

Note the guarded `if import then ... else MrxGuiPauseScreen = {} end` at the top: when loaded outside the engine (no `import`), `MrxGuiPauseScreen` is stubbed so the `EventHandlers` values resolve to `nil` rather than erroring — the layout table can still be inspected offline.

## Notes for modders
- Actual pause-screen behavior lives in [MrxGuiPauseScreen](mrxguipausescreen), not here — this file only supplies layout/position data and the handler-name wiring. The widget is named `"Pause Layout"`; other modules look it up by that exact name (e.g. `MrxGuiDialogBox.OpenSystemDialogBox` closes `"Pause Layout"`).
- `ReInit()` is a full widget teardown/rebuild — calling it discards whatever's currently in `AddedWidgetList` and reloads fresh from `LocalWidgetList`, so any per-widget runtime state set outside this layout is lost.
- Widget geometry (0,0)-(640,480), anchored center/center, mirrors the pattern used by `mrxguiltiprecachelayout.lua` for a full-screen widget.