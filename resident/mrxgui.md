---
title: MrxGui
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: corrected Events section (UpdateLoadingHint is a widget SetEventHandler binding, not an Event.* constant; file has exactly one real Event.* call); flagged dead _oTimerEvent guard in GlobalFadeFromBlack
---

# MrxGui

*Module: mrxgui.lua*

## Overview
The `MrxGui` module serves as a facade/alias for the Scaleform-based GUI/HUD system in Mercenaries 2. It provides functions to manage various aspects of the user interface, including dialog boxes, numeric input boxes, and global screen fades. This module is crucial for controlling visual elements that interact with players during gameplay.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGuiBase`, `MrxGuiDialogBox`, `MrxGuiNumericBox`, `MrxUtil_Shell`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but rather provides global functions to interact with the GUI system.

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
- Ensure that the `Init()` function is called appropriately to set up GUI-related functionality.
- Use `AddMessage` to display custom messages on the HUD, and `ClearMessages` to clear them.
- Customize fade effects by adjusting parameters in `FadeToColor` and `FadeFromColor`.
- Be aware of the E3/HUD mode toggle and its effect on UI elements when developing modded content.