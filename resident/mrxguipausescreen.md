---

title: MrxGuiPauseScreen

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, pause]

verified: true
verified_note: 'deeper pass: fixed Imports (10 real imports, not "none"); rewrote the fabricated Events section (no Event.* calls exist — these are Scaleform flash-event + widget-event handlers); added the pause_menu movie + pause_graphic asset, the full tControlMap (8 vehicle types), the ActionScript callbacks pushed on open, and the LTILibName settings bridge'

---



# MrxGuiPauseScreen



*Module: mrxguipausescreen.lua*



## Overview

`MrxGuiPauseScreen` drives the in-game **pause menu**. Almost all of the visible menu (video/input/audio options, the resume/quit buttons, the control display) is a **Scaleform movie named `"pause_menu"`**; this Lua module builds the widget, loads that movie, pushes the current settings/state into it via ActionScript callbacks, and receives the movie's button/setting events back — forwarding most of them to the engine's `LTILibName` options library. It also implements the "imposter" pause path (a lightweight placeholder pause used in shell/loading contexts) and the med-evac confirmation flow. Widget layout and event wiring come from [MrxGuiPauseLayout](mrxguipauselayout).

## Inheritance

- Inherits from: none — base/utility module
- Imports (10, all real `import(...)` lines): [MrxGuiBase](mrxguibase), [MrxGuiManager](mrxguimanager), [MrxGuiDialogBox](mrxguidialogbox), [MrxSound](mrxsound), [MrxPlayState](mrxplaystate), `WifMissionFlow`, [MrxPlayer](mrxplayer), [MrxTutorialManager](mrxtutorialmanager), [MrxStatsManager](mrxstatsmanager), [MrxUtil](mrxutil). (The previous draft's "Imports: none" was wrong.) It also calls the engine namespaces `Sys.*`, `Net.*`, `Player.*`, `Pg.*`, `_GuiInternal.*`, and the `LTILibName.*` options bridge directly.

## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: only a one-time `Init()` setup function, no
`OnActivate`/`Create`/`tInstance` registry anywhere in source. This is the one shared pause screen, not
something spawned per world object. Per-menu state lives on the pause widget's `CustomData`
(`bActive`, `bHaveFlash`, `bLoading`, `oMapFlash`, `tHudStates`, `bSaveDisabled`, `bImposterEnabled`).
Module-level state/constants:

- **`Joystick`**: the button-id constant table (`BUTTON_PAD1_U=1` … `BUTTON_SYS2=24`) used as keys into `tControlMap`. This is the module's own copy of the same constants [MrxGuiBase](mrxguibase) exposes.
- **`tControlMap`**: starts as `false`; `Init()` fills it with per-context control-label maps (see below).
- **`_bMedEvac`** / **`bTutorials`**: module globals — a latch for the med-evac confirm dialog, and a cached "were tutorials on when we opened" flag used on close.

## Module constants & assets (the retheme knobs)

- Scaleform movie: `oMapFlash.CustomData.sFile = "pause_menu"` — the whole options UI.
- Texture asset preloaded on init: `Pg.LoadAsset("pause_graphic", "texture")`.
- Backdrop: full-screen black `ImageWidget` at alpha `192` behind the movie.
- On close, an ammo/health counter re-show is fired for `nTime = 3` seconds (`GuiShowAmmoCounter` / `ShowAllCounters` events via `MrxGuiBase.SentEvent`).

## The control map (`tControlMap`)

`Init()` builds `tControlMap[sContext] = { [Joystick.BUTTON_*] = "[SHELL.Controls.*]" , ... }` for eight contexts: `human`, `car`, `tank`, `helicopter`, `jet`, `boat`, `ladder`, `seat`. On open, `OpenPauseScreen`/`_FinishPauseOpen` looks up the player's current context via `Player.GetControlBindingType(uPlayerGuid)` and calls the movie's `controllerDisplay(nButtonId, sLabel)` ActionScript callback for each mapped button — this is what fills the on-screen "controls" legend. Values are localization tokens except the `jet` map, whose labels are plain English strings (`"Seat Menu"`, `"Toggle VTOL"`, etc.) — an unlocalized outlier worth knowing if you localize.



## Functions



### Init()

Initializes the control map with different configurations for various vehicle types and human controls. Each entry in the table maps a joystick button constant to a string representing the corresponding action or menu item.



### OpenPauseScreen(oPauseMenu)

Opens the pause screen. Bails early if a system dialog box is up (`MrxGuiDialogBox.oSystemDialogBoxFlash`) or the menu is already `bActive`. Otherwise adds the flash widget and loads the `"pause_menu"` SWF, with `_FinishPauseOpen` as the load callback. Assigned to the widget as `oPauseMenu.Open` by `_Initialize`.

### _FinishPauseOpen(oPauseMenu)

The load callback that actually populates the menu. Enters pause sound state, restarts/plays the movie, takes control focus (pauses), and: registers the movie's setting/event handlers via `oFlash:SetFlashEventHandler(...)`; calls `_GuiInternal.SetFlashPauseMenu(...)` with mission/stats context; toggles the HUD off (remembering prior state in `CustomData.tHudStates`); and pushes the current options into the movie via ActionScript callbacks — `controllerDisplay` (per control-map entry), `videoSubtitles`, `gameRumble`, `gameTutorials`, `gameinvert`, `activeContract`, `medevacEnable`, and `disableSave` (only if save is disabled). Reads each setting from the corresponding `Sys.*Enabled()` accessor when present.

### ClosePauseScreen(oPauseMenu)

Closes the menu: releases focus, calls the movie's `saveProfile` ActionScript callback, pauses/unloads the SWF, removes child widgets, restores the HUD, exits pause sound state, and re-shows the ammo/health counters for `nTime = 3`s (`GuiShowAmmoCounter`/`ShowAllCounters` via `MrxGuiBase.SentEvent`). If tutorials were on at open but off now, calls `MrxTutorialManager.HideMessage(true)`. Assigned as `oPauseMenu.Close`.



### SetUserSaveEnabled(oPause, bEnable)

Enables or disables user save functionality in the pause menu based on the provided boolean flag `bEnable`.



### HandleStateChangeEvent(oWidget, sStateName, sStateAction)

- **Description**: Handles state change events for the pause screen widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `sStateName`: The name of the state that changed.

  - `sStateAction`: The action associated with the state change (e.g., "Enter", "Exit").

- **Behavior**: 

  - If the widget is an imposter or if the state name is not "Pause", it returns early.

  - If the state action is "Enter", it opens the pause screen.

  - If the state action is "Exit", it closes the pause screen.

  - Finally, it calls `MrxGuiBase.ChangeScreenResolution()`.



### HandleInitializationEvent(oWidget, tUnused)

- **Description**: Handles initialization events for the pause screen widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `tUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Sets the widget to use immortal events.

  - Retrieves and stores the menu child widget in the custom data.

  - Sets the first child widget to fullscreen.

  - Closes the pause screen.

  - Removes and then adds the `GuiStateChangeEvent` handler for the widget.

  - Initializes an empty table for HUD states.



### _Initialize(oPauseMenu)

- **Description**: Initializes the pause menu widget.

- **Parameters**:

  - `oPauseMenu`: The pause menu instance.

- **Behavior**:

  - Sets the pause menu to use immortal events.

  - Marks the pause menu as active.

  - Creates and adds a background image widget to the pause menu.

  - Creates and adds a map flash widget to the pause menu.

  - Initializes various properties for the map flash widget.

  - Assigns methods `Open`/`Close`/`SetUserSaveEnabled` to the pause menu widget.

  - Binds `"ControllerInput"` → `_HandleInput`.

  - Sets the map flash's movie name to `"pause_menu"` (`oMapFlash.CustomData.sFile`).

  - Loads the `"pause_graphic"` texture asset via `Pg.LoadAsset`.

  - Closes the pause menu (starts hidden).



### _FinishLoad(oPauseMenu)

- **Description**: Finishes loading the pause menu widget.

- **Parameters**:

  - `oPauseMenu`: The pause menu instance.

- **Behavior**:

  - Marks the pause menu as having a flash and not loading.

  - Binds the movie's action events: `quitGame` → `_HandleQuitEvent`, `closePause` → `_HandleCloseEvent`, `messageMedEvac` → `_ConfirmMedEvacEvent`, `messageButton` → `_HandleMedEvacEvent`.

  - Pauses the map flash.



### _HandleToggleEvent(oPauseMenu, tUnused)

- **Description**: Handles toggle events for the pause menu.

- **Parameters**:

  - `oPauseMenu`: The pause menu instance.

  - `tUnused`: Unused parameter (likely a placeholder).

- **Behavior**:

  - Toggles the active state of the pause menu. If active, it closes; otherwise, it opens.



### _HandleInput(oPauseMenu, tInput)

- **Description**: Handles input events for the pause menu.

- **Parameters**:

  - `oPauseMenu`: The pause menu instance.

  - `tInput`: Input data.

- **Behavior**:

  - Passes the input event to the map flash widget's event handler.



### _HandleCloseEvent(oMapFlash)

- **Description**: Handles close events for the map flash widget.

- **Parameters**:

  - `oMapFlash`: The map flash widget instance.

- **Behavior**:

  - If the pause menu is active, requests the game state to return to "ingame" and closes the pause menu.



### _HandleQuitEvent(oMapFlash)

- **Description**: Handles quit events for the map flash widget.

- **Parameters**:

  - `oMapFlash`: The map flash widget instance.

- **Behavior**:

  - Requests the game state to unload and quits the game. Then, closes the pause menu.



### _ConfirmMedEvacEvent(oMapFlash)

- **Description**: Confirms a medical evacuation event.

- **Parameters**:

  - `oMapFlash`: The map flash widget instance.

- **Behavior**:

  - Formats the cost of medical evacuation and displays a confirmation message with options to proceed or cancel.



### _HandleMedEvacEvent(oMapFlash, sButton)

- **Description**: Handles the response to the medical evacuation confirmation.

- **Parameters**:

  - `oMapFlash`: The map flash widget instance.

  - `sButton`: The button pressed in the confirmation message ("1" for yes, other values for no).

- **Behavior**:

  - If the "yes" button is pressed, performs a medical evacuation and requests the game state to return to "ingame".



### HandleImposterInitializationEvent(oWidget, tEvent)

- **Description**: Handles initialization events for an imposter widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `tEvent`: Event data.

- **Behavior**:

  - Sets the first child widget to fullscreen.

  - Hides the widget and disables input reception.

  - Disables all child widgets.



### HandleImposterStateChangeEvent(oWidget, sStateName, sStateAction)

- **Description**: Handles state change events for an imposter widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `sStateName`: The name of the state that changed.

  - `sStateAction`: The action associated with the state change (e.g., "Enter", "Exit").

- **Behavior**:

  - If the widget is not an imposter or if the state name is not "Pause", it returns early.

  - If the state action is "Enter", it shows the widget and enables input reception, also enabling all child widgets.

  - If the state action is "Exit", it hides the widget and disables input reception, also disabling all child widgets. It then sends an imposter shell event.



### HandleImposterInputEvent(oWidget, tEvent)

- **Description**: Handles input events for an imposter widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `tEvent`: Event data.

- **Behavior**:

  - If the widget is receiving input and a specific button press is detected, requests the game state to return to "ingame".



### HandleImposterEvent(oWidget, tEvent)

- **Description**: Handles general events for an imposter widget.

- **Parameters**:

  - `oWidget`: The widget instance.

  - `tEvent`: Event data.

- **Behavior**:

  - Sets the enabled state of the imposter based on the event's `bOn` flag.



### The `_LTI*` settings bridge (thin forwarders to `LTILibName`)

The pause movie exposes video/input/audio/camera options; the module has one Lua handler per movie event, and each is a **thin forwarder** that calls the matching `LTILibName.*` engine function (the game's options/settings library). They carry no logic beyond dispatch, so they're grouped here rather than documented one-by-one:

- **`_LTIFscommand(oFlash, sFuncName)`** — the catch-all dispatcher: a big `if sFuncName == "..."` chain that maps a movie-supplied command string to the corresponding `LTILibName.LTI*` call (video enter/switch-mode/next-res/prev-res/next-refresh/prev-refresh/apply/cancel/advance, general/KM/joystick input enter/apply/default/cancel/exit, etc.).
- **`_LTIEnter(oFlash, iNumber)`** — `"1"/"2"/"3"` → `LTIVideoEnter`/`LTIVideoAdvanceEnter`/`LTIInputGeneralEnter`.
- **`_LTIVideo(oFlash, iNumber)`** — `"2".."8"` → `LTIVideoSwitchMode`/`NextRes`/`PrevRes`/`NextRefresh`/`PrevRefresh`/`ApplyChanges`/`Cancel`.
- **Value setters** (pass the arg straight through): `_LTIVideoSetGamma(fNumber)`, `_LTIVideoSwitchOpt1(iNumber)`, `_LTIInputGeneralInvertMouse(iNumber)`, `_LTIInputGeneralMouseSense(fNumber)`, `_LTIInputGeneralJoySense(fNumber)`, `_LTIInputGeneralRumble(bBoolean)`, `_LTIInputKMChangeInput(iNumber)`, `_LTIOverBoundResponse(iNumber)`, `_LTIInputJoystickChangePrimary(iNumber)`, `_LTIInputJoystickChangeInput(iNumber)`, `_LTIJoystickOverBoundResponse(iNumber)`, `_LTIPauseItemChanged(iNumber)`, `_LTICamera(iNumber)`.
- **No-arg actions**: `_LTIVideoAdvanceEnter`, `_LTIVideoAdvanceDefault`, `_LTIInputGeneralEnter`, `_LTIInputKMEnter/ApplyChanges/Default/CancelInput/Exit`, `_LTIInputJoystickEnter/ApplyChanges/Cancel/Default/Exit` — each calls the same-named `LTILibName.*` function.

Only `_LTIFscommand`, `_LTIVideoSetGamma`, `_LTIVideoSwitchOpt1`, `_LTIInputGeneralRumble`, `_LTIInputKMChangeInput`, `_LTIOverBoundResponse`, `_LTIInputJoystickChangePrimary`, `_LTIInputJoystickChangeInput`, `_LTIJoystickOverBoundResponse`, `_LTIPauseItemChanged`, and `_LTICamera` are actually bound as movie event handlers in `_FinishPauseOpen`; the rest are reached through `_LTIFscommand`'s string dispatch.



## Events

**There are no `Event.*` (engine event) subscriptions in this file.** The previous draft's event list
invented names — none of `GuiStateChangeEvent`/`InitializationEvent`/`ToggleEvent`/etc. exist as `Event.*`
constants here. Everything is one of two widget-level mechanisms:

- **GUI-system widget events**, bound by name from the layout ([MrxGuiPauseLayout](mrxguipauselayout)) or via
  `oWidget:SetEventHandler(...)`: `GuiGameStateChange` → `HandleStateChangeEvent`, `GuiInitialization` →
  `_Initialize`, `TogglePAUSE` → `_HandleToggleEvent`, `ImposterShellEvent` → `HandleImposterEvent`, and
  `ControllerInput` → `_HandleInput`. `HandleInitializationEvent` also re-binds `GuiStateChangeEvent` →
  `HandleStateChangeEvent` on the widget.
- **Scaleform/ActionScript flash events**, bound via `oFlash:SetFlashEventHandler(...)` in `_FinishLoad` and
  `_FinishPauseOpen`: `quitGame`, `closePause`, `messageMedEvac`, `messageButton`, plus the `LTI*` /
  `PauseItemChanged` / `LTICamera` setting events (see the settings bridge above).

`HandleStateChangeEvent` is the real open/close trigger: it fires when the engine enters/exits the `"Pause"`
game state (`"Enter"` → `OpenPauseScreen`, `"Exit"` → `ClosePauseScreen`), then calls
`MrxGuiBase.ChangeScreenResolution()`.

## Notes for modders

- **Retheme via the `"pause_menu"` movie.** Almost the entire menu is Scaleform. To change layout/appearance
  you edit that movie (and keep its ActionScript entry points — `controllerDisplay`, `videoSubtitles`,
  `gameRumble`, `gameTutorials`, `gameinvert`, `activeContract`, `medevacEnable`, `disableSave`,
  `saveProfile`, `onlineMessage`, `onlineMessageClose` — and dispatch the `quitGame`/`closePause`/`LTI*`
  events). Lua just wires state in and forwards options out.
- **`tControlMap` is the controls legend.** Edit `Init()`'s per-context tables to change which buttons show
  which labels on the pause screen; the `jet` context uses raw English strings while every other context uses
  `[SHELL.Controls.*]` localization tokens.
- **`SetUserSaveEnabled(oPause, bEnable)`** is the public lever to grey out saving (e.g. during a mission);
  it sets `bSaveDisabled`, which drives the `disableSave` callback on open.
- **Med-evac flow**: `messageMedEvac` → `_ConfirmMedEvacEvent` shows an `onlineMessage` confirm dialog and
  latches `_bMedEvac`; the movie's `messageButton` → `_HandleMedEvacEvent` runs the evac only if that latch is
  set and the button was `"1"` (yes), calling `MrxPlayer.MedEvac()` and returning to `"ingame"`.
- **Imposter path** (`HandleImposter*`): a stripped placeholder pause used when the full menu shouldn't run
  (e.g. shell/loading). `HandleImposterEvent` flips `bImposterEnabled`, which makes `HandleStateChangeEvent`
  early-out so the two paths don't both fire. Pressing `BUTTON_PAD2_D` in imposter mode just requests
  `"ingame"`.
- **`_HandleQuitEvent` quits to desktop** (`Sys.RequestGameState("unloading")` + `Net.QuitGame()`) — this is
  the movie's "Quit Game" button, not a mission abort.