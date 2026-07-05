---
title: MrxGuiLoadScreen
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, loading screen]
verified: true
verified_note: 'deeper pass: re-confirmed all 10 functions, the 3 SetEventHandler sites, and the external HandleInit/HandleStateChangeEvent wiring against source; surfaced the concrete constants — _gLoadFlashFile="loadingscreen", save-icon texture "global_loading_skull", font "english_18", string [SHELL.LoadSave.Saving], _knSaveIconSize=64/_knSaveIconTime=0.5, and the closeLoadingScreen/leftAnalog ActionScript callbacks'
---

# MrxGuiLoadScreen

*Module: mrxguiloadscreen.lua*

## Overview
The `MrxGuiLoadScreen` module is responsible for managing the loading screen GUI in the game. It handles the initialization, activation, and deactivation of the loading screen, as well as managing input events and animations related to saving icons.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages the loading screen GUI globally.

## Functions
### `HandleInit(oLoadScreen)`
Initializes the loading screen by setting up its properties, adding a Flash widget for rendering, and initializing save icon elements. This function sets the loading screen to use immortal events, fullscreen mode, and adds event handlers for input and state changes.

### `InitSaveIcon()`
**Not previously documented — the "save icon elements" `HandleInit` calls out.** Builds the save-icon
widget tree: a container positioned at `(64, 48)` sized by `_knSaveIconSize`, with a child image widget
inside it, and two animation points (`nOpenPoint`/`nClosePoint`) recording the icon's on/off-screen X
positions for `HandleSaveIconShow`/`HandleSaveIconHide` to animate between.

### `HandleStateChangeEvent(oLoadScreen, tData)`
Handles state change events by activating or deactivating the loading screen based on the `bLoading` flag in the event data.

### `_SetActive(oLoadScreen, bActive)`
Sets the active state of the loading screen. If the screen is being deactivated, it calls a Flash action script callback to close the loading screen and resets various flags. If the screen is being activated, it loads the Flash file if not already loaded and sets up the necessary properties.

### `_CompleteFlashLoad(oLoadScreen)`
Completes the loading of the Flash file by setting the `bFlashLoaded` flag and obtaining control focus for the loading screen.

### `HandleInput(oLoadScreen, tInput)`
Handles input events by updating the analog input state and calling appropriate Flash action script callbacks to handle left analog stick movement.

### `IsAnalog(nValue)`
Checks if a given value corresponds to an analog controller input.

### `_SaveIconAnimationComplete(oIcon)`
Handles the completion of the save icon animation by reversing the texture coordinates and restarting the animation.

### `HandleSaveIconShow(oContainer, tEvent)`
Shows the save icon by setting its visibility and starting the animation sequence.

### `HandleSaveIconHide(oContainer, tEvent)`
Hides the save icon by resetting its animation state and hiding it from view.

## Events
No `Event.*`/`Event.Create(...)` engine-event references appear in this file — confirmed by grep. All wiring uses widget-level `SetEventHandler` (string keys), three confirmed sites:
- `"ControllerInput"` → `HandleInput` (registered on the load-screen widget in `HandleInit`) — handles left-analog passthrough to the Flash file and tessellation-toggle bookkeeping via `nAnalogInputHeld`.
- `"ShowSaveIcon"` → `HandleSaveIconShow` and `"HideSaveIcon"` → `HandleSaveIconHide` (registered on the save-icon container in `InitSaveIcon`).

`HandleInit` and `HandleStateChangeEvent` are not registered by `SetEventHandler` anywhere in this file — they are wired externally via [`mrxguiloadlayout.lua`](mrxguiloadlayout)'s `LocalWidgetList`, which sets the root "Loading Screen" widget's `EventHandlers.GuiInitialization = MrxGuiLoadScreen.HandleInit` and `EventHandlers.LoadStateChange = MrxGuiLoadScreen.HandleStateChangeEvent`.

## Module constants & tunables
- **`_gLoadFlashFile = "loadingscreen"`** — the Scaleform `.gfx` movie loaded as the loading screen. Swap this
  for a different file name to replace the whole loading-screen visual (`_SetActive` loads it lazily on activate).
- **Save-icon texture: `"global_loading_skull"`** — the spinning skull shown while saving (`InitSaveIcon`).
- **Save-icon label: `"[SHELL.LoadSave.Saving]"`** (localization key) in font **`"english_18"`**, positioned right
  of the icon.
- **`_knSaveIconSize = 64`** (px) and **`_knSaveIconTime = 0.5`** (seconds per open/close animation leg) — the
  save-icon geometry and animation speed. The icon container sits at `(64, 48)`.
- **Flash ActionScript callbacks this module calls:** `"closeLoadingScreen"` (on deactivate) and `"leftAnalog"`
  (analog-stick passthrough, with `{nX, nY}`). These are the `.gfx`-side entry points.
- **Analog detection range** (`IsAnalog`): joystick button indices between `BUTTON_L_STICK_L` and
  `BUTTON_R_STICK_D` (9–16) count as analog input.

## Notes for modders
- Replace the loading-screen visual by pointing `_gLoadFlashFile` at a different `.gfx` — everything else
  (activation, control focus, analog passthrough) keeps working around whatever file you load.
- The save icon "flips" by swapping its texture U coordinates each animation cycle (`_SaveIconAnimationComplete`),
  so a symmetric skull texture looks like it's continuously spinning; a non-symmetric replacement will visibly
  mirror.