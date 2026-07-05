---
title: MrxGui
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: 'deeper pass: documented the full Init() aliasing table (MrxGui is a facade that copies MrxGuiBase widget classes + add/remove/getbyname functions, plus MrxGuiDialogBox/MrxGuiNumericBox entry points, into this namespace — this is why every HUD module calls MrxGui.GetWidgetByNameAndOwner / MrxGui.ImageWidget:new); surfaced the loadingscreen_standalone fade SWF, fade widget name, reticle default 48, E3HudMode SendEvent dispatch, AddMessage defaults; re-confirmed the single Event.Delete + dead _oTimerEvent guard'
---

# MrxGui

*Module: mrxgui.lua*

## Overview
`MrxGui` is the **top-level GUI facade** for Mercenaries 2. Most of its surface is not defined here — `Init()` copies the widget classes and widget-management functions from [MrxGuiBase](mrxguibase) (plus the dialog/numeric-box entry points) into the `MrxGui` namespace. That is why virtually every HUD module in this category calls `MrxGui.GetWidgetByNameAndOwner(...)`, `MrxGui.ImageWidget:new()`, `MrxGui.AddWidget(...)`, `MrxGui.FlashWidget:new()`, etc. — those are aliases established here. On top of that aliasing, this file *originally* implements a handful of things: the objective-description callback, global screen fades (both a Scaleform wipe and a flat color fade), HUD messages, the E3 demo-mode toggle, and a couple of shell/reticle lookups.

The global fade-to-black uses a Scaleform `FlashWidget` (the `loadingscreen_standalone` movie with the spinning skull + loading hints); the simpler `FadeToColor`/`FadeFromColor` uses a plain full-screen `ImageWidget`.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports (via [`import()`](../glossary#importname)): `MrxGuiBase`, `MrxGuiDialogBox`, `MrxGuiNumericBox`, `MrxUtil_Shell` — see [MrxGuiBase](mrxguibase), [MrxGuiDialogBox](mrxguidialogbox), [MrxGuiNumericBox](mrxguinumericbox), [MrxUtil_Shell](mrxutil_shell). Also calls the [Gui](../namespaces/gui) and [Sys](../namespaces/sys) namespaces and the `MessageBox`/`Pda`-style singletons.

## Instance pattern
**Stateless facade + module-level globals.** No `tInstance`/metatable. State is a few module globals: the fade-flash singleton `_oFadeFlash`, the color-fade widget `_oGlobalScreenFadeWidget`, the fade counters `_nGlobalFadeCountNew`/`_nGlobalFadeCount`, the objective callback `_fObjectiveInformationCallback`/`_tObjectiveInformationCallbackData`, and the E3 flag `_bE3HudModeOn`. The many top-level `X = 0` declarations (`AddWidget = 0`, `ImageWidget = 0`, …) are placeholders that `Init()` overwrites with the real `MrxGuiBase.*` references.

### The facade / aliasing table (set by `Init()`) — HIGH modder value
`Init()` binds these `MrxGui.*` names to their real implementations:
- **Widget classes** (call `:new()` on these): `Widget`, `ImageWidget`, `TextWidget`, `FlashWidget`, `SpriteWidget`, `MovieWidget`, `MinimapWidget` ← `MrxGuiBase.*`.
- **Widget management**: `AddWidget`, `AddWidgetWithChildren`, `RemoveWidget`, `RemoveWidgetWithChildren`, `RemoveEverySingleWidget` (← `MrxGuiBase.WidgetManager.RemoveAll`), `PushWidgetToFront`/`PushWidgetToBack`, `PushAllTextToFront`.
- **Lookup**: `GetWidgetByName`, `GetAllWidgetsByName`, `GetWidgetByNameAndOwner` ← `MrxGuiBase.*`.
- **Layout**: `LoadGuiFile`/`LoadGUIFile` (← `MrxGuiBase.LoadGUIFile`), `UnloadGuiFile`, `RemoveAllWidgets`/`RemoveAllWidgetsInLayout`, `DeleteTransientWidgets`, `ReAddAllWidgets`, `HideAllWidgets`, `ShowAllWidgets`, `SetAllWidgetsSleep`, `AssignLayoutToPlayer`, `DuplicateLayout`.
- **Dialog/numeric**: `DisplayDialogBox` ← `MrxGuiDialogBox.DisplayDialogBox`, `CloseDialogBox` ← `MrxGuiDialogBox.Close`, `DisplayNumericBox` ← `MrxGuiNumericBox.DisplayNumericBox`.
- **Input constants**: `Joystick` ← `MrxGuiBase.Joystick` (the button-id table other modules read).
- **Event dispatch**: `SendEvent` ← `MrxGuiBase.SentEvent` (note the source's `SentEvent` spelling).

## Functions
### `GetObjectiveDescription(uGuid)`
Retrieves the description of an objective using a callback function if available. Returns `nil` if no callback is set or if the input is invalid.

### `SetObjectiveInformationCallback(fCallback, tCallbackData)`
Sets a callback function to provide objective information. The callback data can be a table that will be stored and passed back when the callback is invoked.

### `RemoveObjectiveInformation(oObjective)`
Removes an objective from the list of tracked objectives in the callback data.

### `GlobalFadeToBlack(fCallback, tData)`
Initiates a global fade to black effect. If multiple fades are requested simultaneously, they are queued and executed sequentially. The function also handles loading the necessary SWF file for the fade effect.

### `GlobalFadeFromBlack()`
Completes the global fade from black effect by cleaning up resources and resetting internal state.

**Confirmed in source:** this function guards `if _oTimerEvent then Event.Delete(_oTimerEvent) ... end`,
but `_oTimerEvent` is declared `nil` at module scope (line 84 of source) and is never assigned anywhere
else in the file — no `Event.Create` call in this module ever sets it. The guard can therefore never be
true; this looks like dead defensive code, possibly a leftover from a removed timer-based fade path.

### `HandleLoadingHint(oFlash, tData)`
Handles the display of loading hints during the fade effect by updating the text in the flash widget.

### `_FinishFadeToBlack(_oFadeFlash)`
Finishes the fade to black process by setting up event handlers and preparing for the next phase of the fade effect.

### `_FinishFadeFromBlack(_oFadeFlash)`
Finishes the fade from black process by pausing the animation, hiding the widget, and cleaning up resources.

### `_InitFadeFlash()`
Initializes the flash widget used for global fades. Sets up event handlers and adds the widget to the GUI system.

### `CleanupFadeFlash()`
Cleans up the fade flash widget by deleting it and resetting related state.

### `_CompleteFadeFlashLoad()`
Completes the loading of the fade flash SWF file, sets up necessary event handlers, and starts the fade effect if queued.

### `_FadeUpdate(oWidget)`
Processes any queued callbacks after a fade update event.

### `SetGlobalFadeVisible(bVisible)`
Sets the visibility of the global fade widget.

### `FadeToColor(nTime, uPlayerGuid, nRed, nGreen, nBlue, nAlpha)`
Initiates a color-based fade effect for either the global screen or a specific player's screen. The function handles setting up the animation points and starting the fade process.

### `FadeFromColor(nTime, uPlayerGuid)`
Completes a color-based fade effect by animating the widget back to full transparency and hiding it when done.

### `SetFadeEnabled(bEnable)`
Enables or disables the global screen fade widget based on the provided boolean flag.

### `_HideWhenDone(oWidget)`
Hides the widget after an animation completes.

### `AddMessage(tArgs)`
Adds a message to the HUD. The function accepts various parameters such as text, priority, duration, and type of message.

### `ClearMessages()`
Clears all messages from the HUD.

### `SetE3HudMode(bOn)`
Toggles the E3/HUD mode on or off. This mode is used for demonstration purposes and can affect how certain UI elements are displayed.

### `IsE3HudModeActive()`
Returns a boolean indicating whether the E3/HUD mode is currently active.

### `FindShellWidget()`
Finds and returns the ID of the shell widget, which is often used as a base for other GUI elements.

### `GetReticleSize(uPlayer)`
Retrieves the size of the reticle image for a given player. If the reticle widget is not found, it defaults to a size of 48.

### `Init()`
Initializes the `MrxGui` module by copying functions and constants from imported modules into its own namespace. This setup allows for easier access to GUI-related functionality throughout the game.

## Events
This file has exactly **one** real `Event.*` call — `Event.Delete(_oTimerEvent)` inside
`GlobalFadeFromBlack` (see the note on that function above; the guard around it can never be true since
`_oTimerEvent` is never set). Everything else described as an "event" here is the Scaleform widget
event-handler mechanism, not the engine `Event.*` system:
- `_InitFadeFlash` calls `_oFadeFlash:SetEventHandler("UpdateLoadingHint", HandleLoadingHint)` — a
  widget-level binding for loading-hint text updates.
- `_CompleteFadeFlashLoad` calls `_oFadeFlash:SetFlashEventHandler("wipeComplete", _FinishFadeToBlack)`
  and `_oFadeFlash:SetFlashEventHandler("close", _FinishFadeFromBlack)` — ActionScript-side flash
  callbacks fired by the SWF itself.
- `_FinishFadeToBlack` calls `_oFadeFlash:SetEventHandler("GuiUpdate", _FadeUpdate)` — a per-frame GUI
  update binding, cleared again inside `_FadeUpdate` itself.

## Notes for modders
- **`MrxGui.*` widget calls resolve here**: if you see `MrxGui.ImageWidget:new()` or `MrxGui.GetWidgetByNameAndOwner(...)` in another HUD module, the real function lives in [MrxGuiBase](mrxguibase) — this facade just re-exports it. Before `Init()` runs those names are literally `0`, so nothing in this namespace works until the GUI bootstrap has called `Init()`.
- **Global fade-to-black**: `GlobalFadeToBlack(fCallback, tData)` / `GlobalFadeFromBlack()` drive the Scaleform `loadingscreen_standalone` movie (skull spin + loading hints via `HandleLoadingHint` → `textDisplay`). They're **reference-counted** (`_nGlobalFadeCountNew`) so nested fades stack — every `GlobalFadeToBlack` must be paired with a `GlobalFadeFromBlack` or the screen stays black. Loading hints are toggled through `Gui.ShowLoadingHints`.
- **Flat color fade**: `FadeToColor(nTime, uPlayerGuid, nR, nG, nB, nAlpha)` / `FadeFromColor(nTime, uPlayerGuid)` fade a full-screen `ImageWidget` (defaults: color black `0,0,0`, alpha `255`, time `1`s). Pass a `uPlayerGuid` for a split-screen per-player fade, or `nil` for the shared global one (`_oGlobalScreenFadeWidget`, also ref-counted via `_nGlobalFadeCount`). The fade widget is named `"Fullscreen Fade Effect Widget"`.
- **`AddMessage(tArgs)`**: forwards to `MessageBox:AddMessage`. Recognized keys: `sText`, `iPriority` (default 5), `nDuration` (default 2s), `nFadeTime` (default 0.5s), `bClear`, `bExclusive`. `ClearMessages()` clears them.
- **E3/demo mode**: `SetE3HudMode(bOn)` fires a GUI event `{EventType = "E3HudMode", bOn = ...}` via `SendEvent` — this is what the `HandleE3HudModeEvent` handlers across the HUD widgets (ammo, health, damage-indicator, etc.) respond to. `IsE3HudModeActive()` reads the flag. `Init()` auto-enables it when `Sys.IsDemoMode()` is true.
- **`GetReticleSize(uPlayer)`** returns the width of the `"reticle image"` widget, defaulting to `48` if absent. `FindShellWidget()` returns the flash id of the `"Shell"` widget or `nil`.
- **Objective descriptions**: `SetObjectiveInformationCallback(fCallback, tData)` registers a provider that `GetObjectiveDescription(uGuid)` calls; `RemoveObjectiveInformation(oObjective)` unregisters one entry.

{: .note }
> **Confirmed dead code** in `GlobalFadeFromBlack`: it guards `if _oTimerEvent then Event.Delete(_oTimerEvent) ... end`, but `_oTimerEvent` is initialized to `nil` and never assigned anywhere in this file (no `Event.Create` sets it), so the guard is always false. This is the module's only `Event.*` call and it never runs — leftover from a removed timer-based fade path.

- **Debug noise**: the fade functions `Debug.Printf` several `~~~~~~ GlobalFadeToBlack, count = N` lines — engine log spam, ignore when watching logs.