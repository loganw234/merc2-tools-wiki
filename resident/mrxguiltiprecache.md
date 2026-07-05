---
title: MrxGuiLTIPrecache
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, loading screen]
verified: true
verified_note: 'deeper pass: re-verified all 3 bugs against source (ClosePauseScreen unimported; oPrecacheScreen.Open = OpenPrecacheScreen undefined name; _HandleCloseEvent/_LTIUpdateTo reference undeclared global oPrecacheScreen). Confirmed the GuiInitialization→_Initialize / GuiGameStateChange→HandleStateChangeEvent wiring is supplied by mrxguiltiprecachelayout; surfaced the SWF name "LTI_precache" and cross-linked the layout page. Imports/instance-pattern still correct'
---

# MrxGuiLTIPrecache

*Module: mrxguiltiprecache.lua*

## Overview
The `MrxGuiLTIPrecache` module is responsible for managing the pre-cache loading screen in the game. It handles the initialization, display, and interaction with the pre-cache flash animation, ensuring that the loading process is visually engaging and user-friendly.

## Inheritance
- Inherits from: none — base/utility module (no `inherit(...)` call in this file)
- Imports: `MrxGuiBase`, `MrxGuiManager`, `MrxGuiDialogBox` (source lines 1-3; the previous version of this page omitted `MrxGuiBase`)

## Instance pattern
This module does not follow the per-instance object pattern (no `OnActivate`/`Awake`/`tInstance`). It manages the pre-cache screen as a stateless utility module, storing state on the widget's own `CustomData` table rather than a module-level registry:
- `CustomData.bActive`: Indicates whether the pre-cache screen is currently active.
- `CustomData.oFlash`: The flash widget used for displaying the pre-cache animation.
- `CustomData.bHaveFlash`: A boolean indicating if the flash widget has been successfully loaded.
- `CustomData.tHudStates`: A table to store HUD states (initialized empty in `HandleInitializationEvent`; not otherwise populated in this file).
- `tArgument = nil`: a module-level global declared at the top of the file (line 4). No other read or write of `tArgument` exists anywhere in this file — appears unused/dead.

## Functions
### `OpenPrecache(oPrecacheScreen)`
Called when the pre-cache screen should be opened. It checks if the flash widget is available, resets it, and starts playing the animation. Sets the screen as active and visible.

### `ClosePrecacheScreen(oPrecacheScreen)`
Called when the pre-cache screen should be closed. It stops the flash animation, releases control focus, hides the screen, and removes any child widgets.

### `HandleStateChangeEvent(oWidget, sStateName, sStateAction)`
Handles state change events for the pre-cache screen. If the state name is "Precache" and the action is "Exit", it closes the pre-cache screen.

### `HandleInitializationEvent(oWidget, tUnused)`
Handles initialization events for the pre-cache screen. It sets the screen to fullscreen mode, closes any pause screens, and initializes custom data fields.

**Confirmed bug**: calls `ClosePauseScreen(oWidget)` (line 51) as a bare global. `ClosePauseScreen` is a real function — but it's defined in [`mrxguipausescreen.lua`](mrxguipausescreen) (`function ClosePauseScreen(oPauseMenu)`), and this file does **not** `import("MrxGuiPauseScreen")` (its only imports are `MrxGuiBase`, `MrxGuiManager`, `MrxGuiDialogBox` — see Inheritance). Per this wiki's documented `import()` semantics, a module only gets a global name from another module if it explicitly imports that module. Calling `HandleInitializationEvent` as written would fail with `attempt to call global 'ClosePauseScreen' (a nil value)`, unless something else in the runtime environment happens to expose that name first. This is a strong candidate for a genuine, previously-unconfirmed source bug — same class as the `mrxapcdrop`/`moonpatrol` undefined-callback bugs documented elsewhere on this wiki.

### `_Initialize(oPrecacheScreen)`
The main initialization function for the pre-cache screen. It creates a flash widget, sets its properties, adds it as a child of the pre-cache screen, and registers various event handlers. It also opens the pre-cache screen.

**Confirmed bug**: line 69, `oPrecacheScreen.Open = OpenPrecacheScreen`, assigns a function value from the global name `OpenPrecacheScreen`. No function named `OpenPrecacheScreen` is defined anywhere in this file, and a corpus-wide search of `src/resident/` for `function OpenPrecacheScreen` finds zero matches — the name does not exist anywhere in the decompiled tree. The function that actually does the "open" work in this file is named `OpenPrecache` (one word shorter, no `Screen`). As written, `oPrecacheScreen.Open` is assigned `nil`, so any later call to `oPrecacheScreen:Open()` (see `_HandleToggleEvent`) fails with `attempt to call method 'Open' (a nil value)`. This looks like a typo/rename bug: `OpenPrecacheScreen` almost certainly should have been `OpenPrecache`.

### `_FinishLoad(oPrecacheScreen)`
Called when the flash file has finished loading. It marks the flash widget as available and calls another function to handle the completion of the pre-cache process.

### `_HandleToggleEvent(oPrecacheScreen, tUnused)`
Handles toggle events for the pre-cache screen. If the screen is active, it closes it; otherwise, it opens it.

### `_HandleCloseEvent(oFlash)`
Called when the flash widget should be closed.

**Confirmed bug**: the function's only parameter is `oFlash`, but its body (lines 99-101) reads and calls methods on `oPrecacheScreen` — a name that is never assigned anywhere in this file (checked: no `oPrecacheScreen =` assignment at module scope, and it isn't a parameter here). It is not the same thing as the `oPrecacheScreen` parameter names used in `OpenPrecache`, `ClosePrecacheScreen`, and `_Initialize` — those are local to their own function bodies and out of scope here. As written, `oPrecacheScreen` inside `_HandleCloseEvent` is an undeclared global and evaluates to `nil` at runtime (unless some unrelated code elsewhere happens to have set a global of that exact name, which nothing in this file does), so `oPrecacheScreen.CustomData.bActive` would error with `attempt to index a nil value (global 'oPrecacheScreen')`. This looks like it should reference `oFlash.CustomData.oParent` (set in `_Initialize`, line 66) instead.

### `_HandleInput(oPrecacheMenu, tInput)`
Handles input events for the pre-cache menu. It passes the input to the flash widget's event handlers.

### `IsAnalog(nValue)`
Checks if a given value corresponds to an analog input (e.g., joystick buttons).

### `_LTIPrecacheDone(oFlash, iNumber)`
Called when the pre-cache process is done. It triggers a function in the `LTILibName` module to handle the completion of the pre-cache.

### `_LTIPrecacheDone2()`
A secondary function called after `_LTIPrecacheDone`. It also triggers a function in the `LTILibName` module.

### `_LTIPrecacheSmokeDone(oFlash, iNumber)`
Called when the smoke effect during pre-cache is done. It triggers a function in the `LTILibName` module to handle the completion of the smoke effect.

### `_LTIPrecacheSmokeDone2()`
A secondary function called after `_LTIPrecacheSmokeDone`. It also triggers a function in the `LTILibName` module.

### `_LTIUpdateTo(oFlash, iNumber)`
Updates the pre-cache screen to a specific state by calling an action script callback on the flash widget.

**Confirmed bug**: same pattern as `_HandleCloseEvent`. The function's parameters are `oFlash, iNumber`, but line 141 calls `oPrecacheScreen.CustomData.oFlash:CallActionScriptCallback("updateTo", {iNumber})` — referencing the same undeclared-global `oPrecacheScreen`, never assigned anywhere in this file, instead of the `oFlash` parameter it actually received. This would error with `attempt to index a nil value (global 'oPrecacheScreen')` if called as written.

## Events
No `Event.*`/`Event.Create(...)` engine-event references appear in this file — confirmed by grep. Wiring is a mix of widget-level Flash callbacks and direct calls:
- `oFlash:SetFlashEventHandler("precacheDone", _LTIPrecacheDone, {})` (in `_Initialize`) — fired by the Scaleform/Flash side when precaching completes; calls `LTILibName.LTIPrecacheDone()` (an external module not covered by this page).
- `oPrecacheScreen:SetEventHandler("ControllerInput", _HandleInput)` (in `_Initialize`) — passes controller input through to the Flash widget's own `ControllerInput` handler.
- `HandleStateChangeEvent` and `_Initialize` are wired **externally** by
  [`mrxguiltiprecachelayout.lua`](mrxguiltiprecachelayout)'s `LocalWidgetList`, which sets the `"LTI_precache"`
  widget's `EventHandlers.GuiGameStateChange = MrxGuiLTIPrecache.HandleStateChangeEvent` and
  `EventHandlers.GuiInitialization = MrxGuiLTIPrecache._Initialize`. (So `_Initialize`, not
  `HandleInitializationEvent`, is the real init entry point here — `HandleInitializationEvent` has no wiring found
  in the corpus and is the function carrying the `ClosePauseScreen` bug.)
- `_LTIPrecacheDone`, `_LTIPrecacheDone2`, `_LTIPrecacheSmokeDone`, `_LTIPrecacheSmokeDone2` all call into an external `LTILibName` module (not imported in this file, and not one of the modules covered by this wiki page set) — its own function definitions were not verified as part of this pass.

## Notes for modders
- **Three confirmed bugs in this file** (see Functions above for detail): `HandleInitializationEvent` calls `ClosePauseScreen` without this file importing `MrxGuiPauseScreen` (the only module that defines it); `_Initialize` assigns `oPrecacheScreen.Open` from `OpenPrecacheScreen`, a name that doesn't exist anywhere in the decompiled `resident/` tree (probably meant `OpenPrecache`); and both `_HandleCloseEvent` and `_LTIUpdateTo` reference an undeclared global `oPrecacheScreen` instead of their actual `oFlash` parameter. Any of these code paths would throw a runtime error if exercised as written — worth confirming with live testing if pursuing this as a fix target.
- **Precache Scaleform file: `"LTI_precache"`** — the SWF/`.gfx` name loaded by `_Initialize` (via
  `oFlash:SetSwfFile("LTI_precache", _FinishLoad, {oFlash})`). This is also the name of the widget the flash lives
  on. Replace it to swap the precache animation.
- **Analog detection range** (`IsAnalog`): joystick indices `BUTTON_L_STICK_L`..`BUTTON_R_STICK_D` (9–16), same as
  [`mrxguiloadscreen`](mrxguiloadscreen).
- Given the three bugs above, treat this module as **known-broken as decompiled** — the precache screen in the
  shipped game may rely on native code paths that don't hit the buggy Lua branches, but any mod re-driving these
  functions directly should fix the `OpenPrecache`/`oPrecacheScreen`/`ClosePauseScreen` references first.
- The layout that drives this module is [`mrxguiltiprecachelayout`](mrxguiltiprecachelayout).