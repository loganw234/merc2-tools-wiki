---

title: MrxGuiHudActionHijack

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, hud]
verified: true
verified_note: 'deeper pass: re-confirmed all 8 functions + the four sprite-mapping tables against source; clarified this uses native MrxGui.ImageWidget/SpriteWidget (not Scaleform .gfx); surfaced the full button-texture constant list and the "countdown_circle"/"icon_hijack_glow"/"icon_fail" clip names; confirmed zero Event.* calls'

---



# MrxGuiHudActionHijack



*Module: mrxguihudactionhijack.lua*



## Overview

The `MrxGuiHudActionHijack` module drives the "Action Hijack" HUD widget — the on-screen button prompt shown during the quick-time hijack minigame (press/mash a button before a countdown ring expires). It shows the correct controller-button sprite, animates a countdown ring, plays press/mash/recover/error sound cues, and shows a fail icon on failure.

It is built on the **native GUI widget framework** ([MrxGui](mrxgui) / [MrxGuiBase](mrxguibase)), not Scaleform `.gfx` movies: `_HandleInitialization` constructs `MrxGui.ImageWidget`/`MrxGui.SpriteWidget` children and drives them with `SetTexture`/`PlayAnimation`/`SetClockAnimation`. See the [Gui](../namespaces/gui) namespace for the texture-loading and controller-query primitives it calls (`Gui.LoadTexture`, `Gui.IsXboxController`).



## Inheritance

- Inherits from: `none — base/utility module`

- Imports: `MrxGui` (via [`import("MrxGui")`](../glossary#importname))



## Instance pattern

This is a stateless manager/utility module (no per-instance tables). It tracks the following key fields:



- **Sound Variables**: Defines sound cues for different actions, such as `_ksPressSound`, `_ksErrorSound`, `_ksMashSound`, and `_ksRecoverSound`.

- **Joystick Table**: Reassigns and extends the `Joystick` table from `MrxGui` to include specific button mappings for various controller inputs.

- **Controller Sprite Texture Mapping**: A table mapping joystick button IDs to their corresponding sprite texture names for PC controllers.

- **_ControllerSpriteTextureMapping**: Maps joystick button constants to texture names for standard controllers.

- **_ControllerXboxSpriteTextureMapping**: Maps joystick button constants to texture names for Xbox controllers.

- **_ControllerSpriteData**: Provides sprite data (likely coordinates or dimensions) for each joystick button on standard controllers.

- **_ControllerXboxSpriteData**: Provides sprite data for each joystick button on Xbox controllers.



The module manages the display and behavior of action hijack HUD elements, including button prompts, fail icons, and timer animations. It also handles sound effects associated with player actions.



## Functions



### ShowButton(uGuid, nButton, nTime, nRepeatTime, nXPosition, nYPosition, nTranslucency, bShowSparks, nElapsedTime, bFillTimer, bClockwise, bIsRecovery, bShowTimer, nScale)

- **Purpose**: Displays a button prompt overlay with various customizable options such as position, animation, and sound effects.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.

  - `nButton`: Identifier for the button to display.

  - `nTime`: Duration of the countdown timer.

  - `nRepeatTime`: Time for repeating animations.

  - `nXPosition`, `nYPosition`: Position on the screen.

  - `nTranslucency`: Transparency level.

  - `bShowSparks`: Boolean to show spark animations.

  - `nElapsedTime`: Elapsed time for the timer.

  - `bFillTimer`: Boolean to fill the timer clockwise or counterclockwise.

  - `bClockwise`: Boolean indicating the direction of the timer.

  - `bIsRecovery`: Boolean to indicate recovery mode.

  - `bShowTimer`: Boolean to show the timer.

  - `nScale`: Scale factor for the widget.



### HideButton(uGuid)

- **Purpose**: Hides the button prompt overlay and stops any animations or sounds associated with it.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.



### ShowFail(uGuid, nDuration)

- **Purpose**: Displays a fail icon and plays an error sound when the player fails an action hijack.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.

  - `nDuration`: Duration for which the fail icon is visible.



### GetElapsedTime(uGuid)

- **Purpose**: Retrieves the elapsed time of the countdown timer for a specific button prompt overlay.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.

- **Returns**: The elapsed time or `nil` if the widget is not found.



### SetDisplayVisible(uGuid, bVisible)

- **Purpose**: Sets the visibility of the entire action hijack display and stops any animations or sounds.

- **Parameters**:

  - `uGuid`: Unique identifier for the GUI widget.

  - `bVisible`: Boolean to set the visibility.



### SetDisplayButton()

- **Purpose**: This function is deprecated and does nothing.



### SetDisplayMashAnimation()

- **Purpose**: This function is deprecated and does nothing.



### _HandleInitialization(oWidget)

- **Purpose**: Initializes the action hijack display by creating and positioning various GUI elements such as buttons, timers, fail icons, and spark animations.

- **Parameters**:

  - `oWidget`: The GUI widget to initialize.

## Events

This file contains zero `Event.*` / `Event.Create(...)` references — grepped and confirmed. It is driven entirely by direct function calls (`ShowButton`, `HideButton`, `ShowFail`, etc.) made by other modules against the "Action Hijack" widget looked up via `MrxGui.GetWidgetByNameAndOwner("Action Hijack", uGuid)`. The only GUI-framework hook in the file is `_HandleInitialization(oWidget)`, which by naming convention is wired as a widget `EventHandlers.GuiInitialization` callback in whatever layout file defines the "Action Hijack" widget (not in this file) — this is a widget-level event handler key, not an `Event.*` engine constant.

## Notes for modders

(call-order requirements, pitfalls, tunables, decompiler artifacts)

- **No per-instance lifecycle**: this is a stateless utility module — there is no `OnActivate`/`Awake`/`OnDeactivate` in this file, and no `tInstance` registry. All state lives in `CustomData` on the "Action Hijack" widget itself (per-player, since widgets are looked up by owner GUID), set up once by `_HandleInitialization` when the widget initializes.
- **Call order**: `_HandleInitialization` must run (via the widget's `GuiInitialization` handler) before `ShowButton`/`HideButton`/`ShowFail`/etc. are called, since those functions read `oActionHijackDisplay.CustomData.oButton/oTimer/oFail/oSparkL/oSparkR` which `_HandleInitialization` creates.
- **Pitfalls**: `ShowButton` returns silently (no-op) if `_ControllerSpriteTextureMapping[nButton]`, `_ControllerSpriteData[nButton]`, `_ControllerXboxSpriteTextureMapping[nButton]`, or `_ControllerXboxSpriteData[nButton]` is missing for the given `nButton` — only the button IDs explicitly populated in the four mapping tables (D-pad, stick directions, melee, reload) are supported; passing an unmapped `Joystick.BUTTON_*` constant silently fails and logs `"No data for given action hijack buttons"` via `Debug.Printf`.
- **Sound cue constants** (change the audio feedback): `_ksPressSound = "ui_HUD_Minigame_Press_Button"`, `_ksErrorSound = "ui_HUD_Minigame_Error"`, `_ksMashSound = "ui_HUD_Minigame_Tap_Button_lp"` (looping), `_ksRecoverSound = "ui_HUD_Minigame_Tap_Button_Recover_lp"` (looping). Played via `Sound.CueSound(0, ...)` / stopped via `Sound.StopSound(0, ...)` — see [Sound](../namespaces/sound).
- **Timer / button textures** (change the visuals): the countdown ring uses `"countdown_circle"` when `bShowTimer` is true, or `"icon_hijack_glow"` when false; the fail overlay is `"icon_fail"`; sparks are `"icon_sparks_left"`/`"icon_sparks_right"`. Every controller sprite is loaded by `_HandleInitialization` via `Gui.LoadTexture(...)`: standard prompts `icon_hijack_button_{A,B,X,Y}`, `icon_hijack_joystick_{up,down,left,right,leftright}`, `Use_Melee`, `Use_Reload`; Xbox variants prefix `icon_hijack_xbox_*` and `xbox_Use_Melee`/`xbox_Use_Reload`. Which sprite a `nButton` maps to is set in the four `_Controller*SpriteTextureMapping` / `_Controller*SpriteData` tables — the sprite-data entries are `{nFrameW, nFrameH, nUOffset, nVOffset, nTexW, nTexH}`.
- **Xbox vs. standard**: `ShowButton` picks the Xbox texture set at runtime when `Gui.IsXboxController()` returns true (see [Gui](../namespaces/gui)); otherwise the standard set.
- **Tunables via caller**: the `nTime`/`nRepeatTime`/`nScale`/`nTranslucency` (default `190`) arguments to `ShowButton` control countdown duration, button-flash repeat rate, size, and opacity — these are passed in by the calling minigame code, not fixed here.
- **Deprecated stubs**: `SetDisplayButton()` and `SetDisplayMashAnimation()` are empty except for a `Debug.Printf("Deprecated.")` call — calling them does nothing.
- **Decompiler Artifacts**: The module may contain unused locals or duplicate table keys as artifacts of the decompilation process (e.g. `Joystick = MrxGui.Joystick` immediately overwritten by a literal `Joystick = {...}` table two lines later). These should not affect functionality but are noted for clarity.