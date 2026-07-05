---
title: MrxGuiShellLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, layout]
verified: true
verified_note: enumerated the full real EventHandlers set for both the root and "Shell Background" child widget; corrected Instance pattern field descriptions; flagged AddedWidgetList initialization ambiguity (same as mrxguipauselayout.lua)
---

# MrxGuiShellLayout

*Module: mrxguishelllayout.lua*

## Overview
The `mrxguishelllayout.lua` file is a layout-data file (same shape as `mrxguipauselayout.lua`) defining a three-level widget tree in `LocalWidgetList[1]`: a full-screen `"Shell"` root widget, containing a `"Shell Background"` image child, which in turn contains a `"New Text"` text child. It also defines one function, `ReInit()`, identical in body to the one in `mrxguipauselayout.lua`, that tears down and reloads the widget set. Imports `mrxguishell` (event handlers) and `MrxGuiBase` (widget add/remove API).

## Inheritance
- Inherits from: `none — base/utility module` (no `inherit(...)` call)
- Imports: `mrxguishell`, `MrxGuiBase`

## Instance pattern
Not applicable. No `Create`/`OnActivate`/`Awake`/`tInstance` — a static nested layout table plus one free function operating on module-level globals:
- `LocalWidgetList`: the static widget-tree definition (root + 2 nested children), built once at load time.
- `AddedWidgetList`: populated at runtime by `ReInit()`/`MrxGuiBase.LoadAndAddWidgetFromLayoutFileData` — not initialized anywhere in this file itself (see `ReInit` note below).

## Functions
### `ReInit()`
Rebuilds the shell's active widget set: for every entry in `AddedWidgetList`, calls `MrxGuiBase.RemoveWidget(...)`, resets `AddedWidgetList` to `{}`, then for every entry in `LocalWidgetList` calls `MrxGuiBase.LoadAndAddWidgetFromLayoutFileData(LocalWidgetList[i], AddedWidgetList)`.

Note: as in `mrxguipauselayout.lua`, `AddedWidgetList` is never declared in this file before `ReInit`'s first `pairs(AddedWidgetList)` call, which would error on a `nil` table. Whatever external caller invokes `ReInit` (likely `MrxGuiBase`'s widget-management code, which is seen elsewhere setting `ModuleName.AddedWidgetList = {}` on the modules it manages) must guarantee the table already exists. Not confirmable from this file alone.

## Events
No `Event.*` calls appear in this file. `EventHandlers` tables wire GUI-system event names to `mrxguishell` functions at two widget levels:

Root `"Shell"` widget:
- `LobbyServerUpdated` → `mrxguishell.HandleServerUpdate`
- `LobbyServerAdded` → `mrxguishell.HandleServerAdd`
- `ControllerInput` → `mrxguishell.HandleInput`
- `LobbyServerRemoved` → `mrxguishell.HandleServerRemove`
- `GuiInitialization` → `mrxguishell.HandleInitializationEvent`
- `GuiGameStateChange` → `mrxguishell.HandleGameStateChangeEvent`

`"Shell Background"` child widget:
- `GuiInitialization` → `mrxguishell.MakeFullscreen`

The `"New Text"` grandchild widget has empty `EventHandlerFile`/`EventHandlers`/`EventHandlerNames` — no handlers.

## Notes for modders
- Actual shell behavior (server list updates, controller input, fullscreen sizing) lives in `mrxguishell`, not here — this file only supplies the widget tree and handler-name wiring.
- `ReInit()` is a full teardown/rebuild of the widget tree, same caveat as `mrxguipauselayout.lua`'s `ReInit`.
- The `"New Text"` widget starts with `text = ""` — it's presumably populated at runtime by `mrxguishell` handler code, not visible in this layout file.
- The module uses the `MrxGuiBase` library to manage widgets, so any modifications should stay compatible with its API.