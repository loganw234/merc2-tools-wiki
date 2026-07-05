---
title: MrxGuiSniperscope
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, sniper]
verified: true
verified_note: 'deeper pass: cross-linked MrxGuiBinoculars/MrxGuiManager/MrxSound/MrxGui; documented the "Guns"/"Health Counter" HUD wakeups, the Player.GetTargetUnderReticle+Object.GetHealth health source, and the 180-deg scroll-texture math; re-confirmed the single Event.Post("InFocus", bSniper=true) and the missing layout file'
---

# MrxGuiSniperscope

*Module: mrxguisniperscope.lua*

## Overview
The `MrxGuiSniperscope` module is responsible for managing the sniper scope GUI elements in the game. It handles events related to entering and exiting the sniper scope, updating health information, zoom level, camera heading, focus updates, faction texture, and horizontal/vertical scroll updates. The module ensures that the GUI elements are correctly displayed and updated based on player actions and game state.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: [MrxGuiManager](mrxguimanager) (`ToggleHud`/`GetHudState`), [MrxGui](mrxgui) (`PushWidgetToFront/Back`, `GetWidgetByNameAndOwner`, `GetObjectiveDescription`), [MrxSound](mrxsound) (`EnterScopeView`/`ExitScopeView`)

This is the sniper counterpart of [MrxGuiBinoculars](mrxguibinoculars) — same enter/exit/zoom structure and shared `_nIntroZoomScale`/`_nIntroZoomTime` constants, but keyed on `tEvent.bSniper == true` (binoculars handles the `not bSniper` case) and with an added health bar for the target under the reticle.

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
Caches the health bar (`oWidget:GetChildren()[1]` → `CustomData.oBar`) and records its left edge (`nX`) and full width (`nLength`) so updates can scale it by health fraction.

### `HandleSniperHealthUpdate(oWidget, nTargetRelation, nScreenX, nScreenY, nSpreadX, nSpreadY, nHealth, nMaxHealth)`
Shrinks the bar to `nLength * (nHealth / nMaxHealth)` and shows it; hides the widget if either value is negative. In `_FinishEnter`, the scope reads the current target itself via `Player.GetTargetUnderReticle(owner)` and, if there's a target, calls this with `Object.GetHealth(uTarget)` / `Object.GetMaxHealth(uTarget)` (defaulting to `-1` when unavailable → bar hidden).

### `HandleZoomUpdate(oWidget, tEvent)`
Updates the zoom level display in the sniper scope GUI element.

### `HandleHeadingUpdate(oWidget, tEvent)`
Updates the camera heading display in the sniper scope GUI element.

### `HandleFocusUpdate(oWidget, tEvent)`
Updates the focus name and description in the sniper scope GUI element.

### `HandleFactionUpdate(oWidget, tEvent)`
Updates the faction texture in the sniper scope GUI element based on the faction type.

### `HandleHorizScrollUpdate(oWidget, tEvent)`
Scrolls the U texture coordinate to reflect camera heading: wraps `nCameraHeading` into a 180° range, normalizes to 0-0.5, and sets `SetTextureCoordinates(u, nil, u+0.5, nil)` — a sliding half-texture window used for the compass strip.

### `HandleVertScrollUpdate(oWidget, tEvent)`
Same idea on the V axis for pitch: wraps into 180°, normalizes, `SetTextureCoordinates(nil, v, nil, v+0.5)`.

### `_RecursiveWakeup(oWidget, bAwaken)`
Recursively toggles `SetSleeping(not bAwaken)` on a widget and all descendants. Used to wake/sleep the `"Guns"` and `"Health Counter"` HUD widgets (looked up by name) alongside the scope, so ammo/health stay live while scoped even though the rest of the HUD is toggled off.

## Events
Only one real `Event.*` call exists in this file: `Event.Post("InFocus", {uTarget=tEvent.uFocusGuid, uViewer=oWidget:GetOwner(), bSniper=true})`, fired from `HandleFocusUpdate` whenever a new focus target is set (this *posts* an event; it doesn't listen for one).

Every function named `Handle*` in this file (`HandleSniperScopeEnter`, `HandleSniperScopeExit`, `HandleInitialization`, `HandleSniperHealthInit`, `HandleSniperHealthUpdate`, `HandleZoomUpdate`, `HandleHeadingUpdate`, `HandleFocusUpdate`, `HandleFactionUpdate`, `HandleHorizScrollUpdate`, `HandleVertScrollUpdate`) is shaped like a GUI-widget event handler (`(oWidget, tEvent)` signature, matches the `EventHandlers = {EventName = Module.HandlerFn}` wiring pattern seen in this wiki's layout-file pages, e.g. `mrxguishelllayout.md`). **However, no layout file for this module (something like `mrxguisniperscopelayout.lua`) exists anywhere in the decompiled `resident/` corpus**, so the actual event names wired to each handler can't be confirmed from static reading of this repo. The previous version of this page listed specific guessed names (`SniperScopeEnter`, `Initialization`, `SniperHealthInit`, etc.) that matched no grep hits anywhere in the source — those have been removed. A sibling module, `mrxguibinoculars.lua`, defines its own separate copies of several same-named handlers (`HandleInitialization`, `HandleHeadingUpdate`, `HandleZoomUpdate`, `HandleFactionUpdate`, `HandleFocusUpdate`, `HandleVertScrollUpdate`) for the binoculars widget — worth checking if you need to cross-reference likely event-name conventions, but it's a different file's wiring, not this one's.

## Notes for modders
- **Tune the zoom feel** with the module constants `_nIntroZoomScale = 3` and `_nIntroZoomTime = 0.25` (shared naming with [MrxGuiBinoculars](mrxguibinoculars)). The zoom-in path only runs when `bUsingZoom` is set, which itself requires the engine API `_GuiInternal.SetWidgetUseNewRescale` to exist — otherwise enter/exit go straight to `_FinishEnter`/`_FinishExit` with no animation.
- **`HandleInitialization`'s fixed child indices are load-bearing**: `tChildren[3]`=focus text, `[4]`=faction texture, `[5]`=description, `[6]`=health. Reordering the (undocumented, not-in-corpus) layout's children silently rebinds the wrong widgets. Note these indices differ from the binoculars layout's (`[7]`=faction, `[8]`=description there).
- **The scope keeps ammo/health live** by waking the HUD widgets literally named `"Guns"` and `"Health Counter"` (via `_RecursiveWakeup`) when it toggles the rest of the HUD off with `MrxGuiManager.ToggleHud(..., false, "scope")`. Rename those HUD widgets and the lookups fail.
- **`HandleFocusUpdate` posts `Event.Post("InFocus", {uTarget, uViewer, bSniper=true})`** when a target is focused — the same signal binoculars post with `bSniper=false`. Hook that event to react to what the player is looking at through a scope.