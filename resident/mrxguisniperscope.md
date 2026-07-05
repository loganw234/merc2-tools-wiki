---
title: MrxGuiSniperscope
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, sniper]
verified: true
verified_note: function coverage was accurate; corrected Events section — the specific event names listed (SniperScopeEnter, Initialization, etc.) were guessed from function names and not confirmed anywhere in this corpus (no layout file for this module exists in src/resident/, unlike its sibling mrxguibinoculars.lua); only one real Event.* call exists (Event.Post("InFocus", ...))
---

# MrxGuiSniperscope

*Module: mrxguisniperscope.lua*

## Overview
The `MrxGuiSniperscope` module is responsible for managing the sniper scope GUI elements in the game. It handles events related to entering and exiting the sniper scope, updating health information, zoom level, camera heading, focus updates, faction texture, and horizontal/vertical scroll updates. The module ensures that the GUI elements are correctly displayed and updated based on player actions and game state.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGuiManager`, `MrxGui`, `MrxSound`

## Instance pattern
Stateless singleton/utility module — plain module-level globals (`_nIntroZoomScale = 3`, `_nIntroZoomTime = 0.25`), no `Create`/`OnActivate`/`Awake`/`tInstance`. Per-widget state lives on each widget's own `CustomData` table (`bOn`, `bUsingZoom`, `bHaveHudState`, `bHudState`, `oFocusText`, `oFaction`, `oDescription`, `oHealth`, `nBigPoint`, `nEndPoint`, animation coordinates, etc.), set up once in `HandleInitialization` and read/written by every other handler — the widget instance itself is the "instance," not anything this module tracks centrally.

## Functions
### `HandleSniperScopeEnter(oWidget, tEvent)`
Called when the player enters the sniper scope. It sets up the GUI elements and plays the enter scope sound.

### `HandleSniperScopeExit(oWidget, tEvent)`
Called when the player exits the sniper scope. It cleans up the GUI elements and plays the exit scope sound.

### `_FinishEnter(oWidget)`
Finishes the process of entering the sniper scope by enabling all child widgets and setting their locations and visibilities.

### `_FinishExit(oWidget)`
Finishes the process of exiting the sniper scope by hiding all child widgets and restoring the HUD state if necessary.

### `HandleInitialization(oWidget, tEvent)`
Initializes the sniper scope GUI elements. Hides the widget, marks `CustomData.bNeedsPush = true`, disables all children, and caches specific children by fixed index into `CustomData` (`tChildren[3]` → `oFocusText`, `tChildren[4]` → `oFaction`, `tChildren[5]` → `oDescription`, `tChildren[6]` → `oHealth` — these indices assume a specific child ordering from the (undocumented, not present in this corpus) layout file). Calls `oDescription:Wrap()`. If `_GuiInternal.SetWidgetUseNewRescale` exists (a rescale API only present in some engine versions), sets up the zoom-in animation: captures original text/description locations, computes an enlarged "big point" animation target scaled by `_nIntroZoomScale` centered at (320, 240), registers both the big point and the original-size "end point" via `oWidget:AddAnimationPoint`, sets `CustomData.bUsingZoom = true`, calls `_GuiInternal.SetWidgetUseNewRescale(oWidget.BasicData.uId, true)`, and immediately snaps the widget to the big point (0-duration animate). If that API isn't present, `bUsingZoom` is never set (stays `nil`/falsy), so `HandleSniperScopeEnter`/`HandleSniperScopeExit` skip the zoom-animation branch entirely and go straight to `_FinishEnter`/`_FinishExit`.

### `HandleSniperHealthInit(oWidget, tEvent)`
Initializes the health bar for the sniper scope GUI element.

### `HandleSniperHealthUpdate(oWidget, nTargetRelation, nScreenX, nScreenY, nSpreadX, nSpreadY, nHealth, nMaxHealth)`
Updates the health bar based on the current health and maximum health of the target.

### `HandleZoomUpdate(oWidget, tEvent)`
Updates the zoom level display in the sniper scope GUI element.

### `HandleHeadingUpdate(oWidget, tEvent)`
Updates the camera heading display in the sniper scope GUI element.

### `HandleFocusUpdate(oWidget, tEvent)`
Updates the focus name and description in the sniper scope GUI element.

### `HandleFactionUpdate(oWidget, tEvent)`
Updates the faction texture in the sniper scope GUI element based on the faction type.

### `HandleHorizScrollUpdate(oWidget, tEvent)`
Updates the horizontal scroll texture coordinates based on the camera heading.

### `HandleVertScrollUpdate(oWidget, tEvent)`
Updates the vertical scroll texture coordinates based on the pitch.

### `_RecursiveWakeup(oWidget, bAwaken)`
Recursively sets the sleeping state of a widget and its children to either awake or asleep.

## Events
Only one real `Event.*` call exists in this file: `Event.Post("InFocus", {uTarget=tEvent.uFocusGuid, uViewer=oWidget:GetOwner(), bSniper=true})`, fired from `HandleFocusUpdate` whenever a new focus target is set (this *posts* an event; it doesn't listen for one).

Every function named `Handle*` in this file (`HandleSniperScopeEnter`, `HandleSniperScopeExit`, `HandleInitialization`, `HandleSniperHealthInit`, `HandleSniperHealthUpdate`, `HandleZoomUpdate`, `HandleHeadingUpdate`, `HandleFocusUpdate`, `HandleFactionUpdate`, `HandleHorizScrollUpdate`, `HandleVertScrollUpdate`) is shaped like a GUI-widget event handler (`(oWidget, tEvent)` signature, matches the `EventHandlers = {EventName = Module.HandlerFn}` wiring pattern seen in this wiki's layout-file pages, e.g. `mrxguishelllayout.md`). **However, no layout file for this module (something like `mrxguisniperscopelayout.lua`) exists anywhere in the decompiled `resident/` corpus**, so the actual event names wired to each handler can't be confirmed from static reading of this repo. The previous version of this page listed specific guessed names (`SniperScopeEnter`, `Initialization`, `SniperHealthInit`, etc.) that matched no grep hits anywhere in the source — those have been removed. A sibling module, `mrxguibinoculars.lua`, defines its own separate copies of several same-named handlers (`HandleInitialization`, `HandleHeadingUpdate`, `HandleZoomUpdate`, `HandleFactionUpdate`, `HandleFocusUpdate`, `HandleVertScrollUpdate`) for the binoculars widget — worth checking if you need to cross-reference likely event-name conventions, but it's a different file's wiring, not this one's.

## Notes for modders
- Ensure that the sniper scope GUI elements are correctly initialized and updated by handling the appropriate events.
- Customize the behavior of the sniper scope GUI elements by modifying the functions in this module.
- Be aware of the dependencies on `MrxGuiManager`, `MrxGui`, and `MrxSound` for managing GUI elements, sound playback, and other functionalities.
- `HandleInitialization`'s fixed child-index lookups (`tChildren[3]` through `tChildren[6]`) are fragile — if you're modifying the layout that spawns this widget's children, preserve child ordering or these caches will point at the wrong widgets.
- The zoom-in animation path (`bUsingZoom`) is conditional on an engine API (`_GuiInternal.SetWidgetUseNewRescale`) that may not exist on all engine builds — don't assume the zoom animation always runs.