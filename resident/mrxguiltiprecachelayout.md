---
title: MrxGuiLtiPrecacheLayout
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui]
verified: true
verified_note: fixed malformed title casing; corrected LocalWidgetList structure/field description; source has zero functions, only a static table
---

# MrxGuiLtiPrecacheLayout

*Module: mrxguiltiprecachelayout.lua*

## Overview
The `mrxguiltiprecachelayout.lua` file defines a static `LocalWidgetList` table describing a single full-screen (0,0)-(640,480) GUI widget named `LTI_precache`, centered both horizontally and vertically, with no children. It is a layout-data file, not a behavior module — it contains no functions of its own. It imports `MrxGuiLTIPrecache` and wires that module's functions in as the widget's event handlers.

## Inheritance
- Inherits from: `none — base/utility module` (no `inherit(...)` call in the file)
- Imports: `MrxGuiLTIPrecache`

## Instance pattern
Not applicable. This file has no `Create`/`OnActivate`/`Awake`/`tInstance` — it's a single static table (`LocalWidgetList[1]`) built once at load time and never instantiated per-object.

## Functions
There are no functions defined in this file (top-level `function` or `Name = function`). The two handlers referenced in `LocalWidgetList[1].EventHandlers` — `MrxGuiLTIPrecache.HandleStateChangeEvent` and `MrxGuiLTIPrecache._Initialize` — are looked up from the imported `MrxGuiLTIPrecache` module and are not defined here. (Note: if `import` fails/is unavailable, the file falls back to `MrxGuiLTIPrecache = {}`, an empty table — in that fallback case both `EventHandlers` entries would be `nil`.)

## Events
No `Event.*` calls appear in this file. The table's `EventHandlers` field maps two GUI-system event names (used by the wider GUI framework that consumes `LocalWidgetList`, not by this file directly) to `MrxGuiLTIPrecache` functions:
- `GuiGameStateChange` → `MrxGuiLTIPrecache.HandleStateChangeEvent`
- `GuiInitialization` → `MrxGuiLTIPrecache._Initialize`

## Notes for modders
- This is pure layout data (position, anchor, color/translucency levels, event-handler wiring) for one widget — there's no logic to modify here beyond the table fields themselves.
- Actual behavior lives in `MrxGuiLTIPrecache`, not in this file. To understand what `HandleStateChangeEvent` and `_Initialize` actually do, read `mrxguiltiprecache.lua` (not covered by this page).
- Widget geometry (`x1,y1,x2,y2` = 0,0,640,480, anchored center/center) suggests this is a full-screen invisible-ish precache widget rather than a rendered HUD element.