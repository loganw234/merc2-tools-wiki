---
title: MrxGuiHudMessage
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud, message]
verified: true
verified_note: 'deeper pass: CORRECTED imports (source imports MrxGui/MrxGuiBase/MrxGuiManager/MrxHqManager — MrxUtil is NOT imported); rewrote Events section (no ObjectHibernation/PlayerInput/PlayerJoined — the real calls are Event.Create/CreatePersistent(Event.TimerRelative | Event.Button) + Event.Delete); surfaced the Scaleform .swf movie names (fanfare_contract/mission/wager/support_unlocked/new_contact/…_businesscard, text_effect) and the _tEventTitles/_tEventTextures/_tEventSounds/_tEventTextureWidths tables; documented module dimension globals'
---

# MrxGuiHudMessage

*Module: mrxguihudmessage.lua*

## Overview
The `MrxGuiHudMessage` module drives the game's on-screen **messages and fanfares** — the full-screen contract/mission/wager payout fanfares, "new contact / new shop item / new landing zone" unlock pop-ups, business-card reveals, big "COMPLETED"/"FAILED" stamps, sliding two-line text fanfares, and the "classy text" effect. It is heavily **Scaleform-backed**: the big fanfares are `MrxGui.FlashWidget`s that load `.swf`/`.gfx` movies and are driven through ActionScript callbacks (`CallActionScriptCallback`, `SetFlashEventHandler`). Simpler messages use native `MrxGui.ImageWidget`/`TextWidget`s.

There is one shared "flash" fanfare at a time — `_gFanfareFlashWidget` is a module global, and `CreateFanfare` returns `false` if one is already active.

## Inheritance
- Inherits from: none — base/utility module
- Imports (via [`import()`](../glossary#importname)): `MrxGui`, `MrxGuiBase`, `MrxGuiManager`, `MrxHqManager` — see [MrxGui](mrxgui), [MrxGuiBase](mrxguibase), [MrxGuiManager](mrxguimanager), [MrxHqManager](mrxhqmanager). It also calls the [Net](../namespaces/net), [Player](../namespaces/player), [Sys](../namespaces/sys), [Sound](../namespaces/sound), [Object](../namespaces/object), and [Gui](../namespaces/gui) namespaces, plus the internal `_GuiInternal` and `Pda` singletons and `LTILibName.ChangeShellState`.

{: .note }
> The earlier draft listed `Imports: MrxGui, MrxUtil`. **`MrxUtil` is not imported.** The real import list is the four modules above. Corrected.

## Instance pattern
**Stateless module + module-global singletons + per-widget `CustomData`.** No `tInstance`/metatable pattern. The active flash fanfare lives in the module global `_gFanfareFlashWidget` (plus `_gFullscreenFadeWidget` for the black slow-mo fade); everything else is per-widget `CustomData`. The `_ev*` locals (`_evSkip`, `_evLSLeft`, `_evLSRight`, `_evSelect`) hold live event handles for teardown by `_DeleteFanfareEvents`.

### Module constants & tunables
- **Default geometry/timing**: `nGlobalWidth = 256`, `nGlobalHeight = 128`, `nX = 320`, `nY = 340`, `nMagnification = 5` (the zoom-in scale factor for `ShowMessage`), `nAnimationTimeLength = 0.1`, `nLifeTime = 3` (default on-screen seconds), `nFadeTime = 1`. `nGlobalWidth`/`Height`/`nX`/`nY` are **overwritten at runtime** by `HandleInitialization` from the announcement widget's authored size/position.
- **Fanfare Scaleform movies** (`.swf`/`.gfx`, chosen by `sType` in `CreateFanfare`): `fanfare_contract`, `fanfare_mission`, `fanfare_wager`, `fanfare_support_unlocked`, `fanfare_new_contact`, and `fanfare_new_contact_<faction>_businesscard` (faction must be one of `an`/`ch`/`oc`/`gr`/`pr`). The classy-text effect uses the `text_effect` movie.
- **Event-fanfare lookup tables** (keyed by event `sType`, used by `ShowEventFanfare`/`GetEventFanfareTitle`):
  - `_tEventTitles`: localized title tokens (`[Fanfare.Common.NewContact]`, `[Fanfare.Common.NewShopItem]`, `[Fanfare.Common.NewStockpileItem]`, `[Fanfare.Common.NewLandingZone]`, `[Fanfare.Common.HvtCaptured]`, `[Fanfare.Common.HvtKilled]`, `[Fanfare.Common.NewBounties]`, `[Fanfare.Common.NewOutfit]`, `[Fanfare.Common.NewHighScore]`).
  - `_tEventTextures`: icon texture per type (`unlockables_newcontact`, `unlockables_newshopitem`, `unlockables_newstockpileitem`, `unlockables_landingzone`, `unlockables_hvtcaptured`, `unlockables_hvtkilled`, `unlockables_newbounties`, `unlockables_newoutfit`, `unlockables_leaderboardupdated`).
  - `_tEventSounds`: `ui_signal_ding` for most, `ui_signal_generic` for `hvtcapture`/`hvtkill`.
  - `_tEventTextureWidths`: per-type pixel widths (398/456/512/512/432/365/428/370/512).
  - `_knTextQueueFadeTime = 0.5` — cross-fade time between queued event-fanfare text lines.
- **Classy-text geometry**: `_nClassyTextWidth = 566.6667`, `_nClassyTextHeight = 33.333336`.
- **Fonts**: `Init()` loads `fanfare_36`; text fanfares use font `fanfare_36`, event fanfares `english_18`.

## Functions

### CreateFanfare(sType, sFaction)
Creates a new fanfare widget based on the specified type (`contract`, `mission`, `wager`, `support`, `contact`, or `card`) and faction. It initializes the widget with necessary properties and sets up event handlers for input and loading completion.

### SetFanfareCompleteCallback(fCallback, tCallbackData)
Sets a callback function that will be called when the fanfare completes. The callback can include additional data passed through `tCallbackData`.

### SupportFanfareAddItem(sTexture, sItemName, sFaction, sContactName, sBlipName)
Adds an item to the support fanfare widget with specified texture and details. This function is used to populate the items in a support-related fanfare.

### SupportFanfareCommence()
Starts the support fanfare if it is ready to begin. It checks if the loading is complete before starting the fanfare.

### _SupportLoadCompleteCallback(oWidget)
Internal callback function that marks the support widget as loaded and starts the fanfare if it is ready.

### _BeginSupportFanfare(oWidget)
Begins playing the support fanfare by setting its visibility and triggering a scroll-out effect after 3 seconds.

### _ScrollOutFanfare(oWidget)
Handles the scroll-out effect of the fanfare, calling an action script callback and scheduling the widget's deletion.

### ContactFanfareCommence(sTexture, sContactName, sFaction)
Starts the contact fanfare with specified texture and details. It checks if the loading is complete before starting the fanfare.

### _ContactLoadCompleteCallback(oWidget)
Internal callback function that marks the contact widget as loaded and starts the fanfare if it is ready.

### _BeginContactFanfare(oWidget)
Begins playing the contact fanfare by setting its visibility and triggering a scroll-out effect after 3 seconds.

### CardFanfareSetParameters(sTitle, sName, sJobTitle, sPhone1, sPhone2, sEmail, nDisplayTime)
Sets parameters for the business card fanfare, including title, name, job title, contact information, and display time. It marks the card as ready if all required fields are provided.

### CardFanfareCommence()
Starts the business card fanfare if it is ready to begin. It checks if the loading is complete before starting the fanfare and sends network events if applicable.

### _CardLoadCompleteCallback(oWidget)
Internal callback function that marks the card widget as loaded and starts the fanfare if it is ready.

### _BeginCardFanfare(oWidget)
Begins playing the business card fanfare by setting its visibility, calling an action script callback to start the fanfare, and scheduling cleanup events.

### _ContinueCardFanfare(oWidget)
Continues the business card fanfare by calling an action script callback and scheduling the end of the fanfare based on the display time.

### _EndCardFanfare(oWidget)
Ends the business card fanfare by calling an action script callback to conclude the fanfare.

### _CleanupCardFanfare(oWidget)
Cleans up the business card fanfare by scheduling its deletion after a short delay.

### SetFanfareParameters(sProfileName1, sProfileName2, sCancelMsg, bAllowRetry)
Sets parameters for contract or mission fanfares, including profile names, cancel message, and retry option. It ensures that only valid types are set.

### AddFanfareLineItem(sDescription, nValue, sType, nPlayer)
Adds a line item to the contract or wager fanfare with specified description, value, type, and player index. It checks for valid input and ensures that the cancel message is not set.

### CommenceFanfare(nSlowdownDuration)
Starts the fanfare by locking HQ, sending network events if applicable, setting up time dilation effects, and preparing the fanfare widget for display. It also handles UI state changes like disabling the HUD and PDA.

### NetClientCloseFanfare()
Closes the fanfare on the client side by stopping sound callbacks, closing the fanfare, and ending it.

### _SlowdownUpdate(oWidget, nDeltaTime)
Handles the time dilation effect during the fanfare, updating the time scale and fade widget's alpha value accordingly. It triggers the beginning of the fanfare when the time scale reaches zero.

### _LoadCompleteCallback(oWidget)
Internal callback function that marks the main widget as loaded and starts the fanfare if it is ready.

### _BeginFanfareFlash(oWidget)
This function initializes the fanfare flash sequence for a given widget. It checks if the loading is complete and proceeds to close any pause screens, set invincibility for the local player, initialize the fanfare, create a timer event for an initial delay, and get control focus.

### _InitializeFanfareFlash(oWidget)
This function initializes the fanfare flash by setting up various properties of the widget. It changes the shell state, sets visibility and pauses the widget, calls action script callbacks to initialize the fanfare with player data, and sets up event handlers for closing, retrying, and continuing the fanfare.

### _ContinueFanfare(oWidget)
This function handles the continuation of the fanfare by calling an action script callback to make the fanfare buttons appear.

### _InitialDelay(oWidget)
This function makes the widget visible and plays it after a short delay.

### _SkipFanfare(oWidget)
This function sets up event listeners for skipping the fanfare based on player input. It creates events for button presses that trigger the `_EndFanfare` function.

### _RetryEvents(oWidget)
This function sets up persistent event listeners for retrying the fanfare using left stick inputs and selection buttons. It sends flash inputs to handle these actions.

### OnPlayerJoined()
This function handles the event when a player joins the game. If there is an active fanfare flash widget, it sends a specific input to the widget.

### _DeleteFanfareEvents()
This function deletes various persistent events related to the fanfare flash sequence.

### _EndFanfare(oWidget, sEnd)
This function ends the fanfare flash by handling cleanup tasks such as deleting events, releasing control focus, and calling callbacks. It also unlocks all HQs if necessary.

### _DeleteFanfareWidget(oWidget)
This function deletes the fanfare widget, removes it from the GUI, and calls any callback functions associated with it. It also handles restoring certain game states like PDA suppression and scope enabling.

### _HandleFanfareInput(oWidget, tEvent)
This function handles input events for the fanfare flash by calling a custom handler defined in the widget's custom data.

### ShowTextFanfare(uPlayerGuid, sLine1, sLine2, nEnterTime, nDisplayTime, nFadeTime, fCallback, tCallbackData)
This function creates and displays a text-based fanfare with two lines of text. It sets up animations for entering, displaying, and fading out the text, and calls a callback function when the fanfare is done.

### _TextFanfareDone(oTextFanfare, fCallback, tCallbackData)
This function handles the completion of a text fanfare by calling the provided callback function and cleaning up the widget.

### _TextDelay(oWidget, oTextFanfare, nDelayTime, nFadeTime)
This function sets up a delay before fading out the text in a text fanfare.

### _TextFadeout(oWidget, oTextFanfare, nFadeTime)
This function handles the fade-out animation of the text in a text fanfare.

### _TextDelete(oWidget, oTextFanfare)
This function removes and deletes the animated widget from the text fanfare.

### ShowEventFanfare(sType, vText, fCallback, tCallbackData)
- **Description**: Displays an event fanfare message on the HUD.
- **Parameters**:
  - `sType`: Type of the event (used to determine the icon texture).
  - `vText`: The text to display, can be a string or a table of strings for sequential display.
  - `fCallback`: A callback function to execute after the fanfare completes.
  - `tCallbackData`: Data to pass to the callback function.

### _EventFanfareFinishAppear(oFanfare)
- **Description**: Handles the appearance animation completion of an event fanfare.
- **Parameters**:
  - `oFanfare`: The fanfare widget instance.

### _EventFanfareProcessTextQueue(oInfo)
- **Description**: Processes the text queue for sequential display in the event fanfare.
- **Parameters**:
  - `oInfo`: The text widget instance.

### _EventFanfareContinueTextFade(oInfo)
- **Description**: Continues the fade animation for the next text in the queue.
- **Parameters**:
  - `oInfo`: The text widget instance.

### _EventFanfareFinishDisplay(oFanfare)
- **Description**: Handles the display animation completion of an event fanfare.
- **Parameters**:
  - `oFanfare`: The fanfare widget instance.

### _EventFanfareComplete(oFanfare)
- **Description**: Completes the event fanfare by removing the widget and executing the callback.
- **Parameters**:
  - `oFanfare`: The fanfare widget instance.

### GetEventFanfareTitle(sType)
- **Description**: Retrieves the title for a given event type.
- **Parameters**:
  - `sType`: Type of the event.

### HandleInitialization(oWidget, tUnused)
- **Description**: Handles initialization of a widget by setting its translucency and scheduling removal.
- **Parameters**:
  - `oWidget`: The widget instance.
  - `tUnused`: Unused parameter (likely for future expansion).

### ShowCompletedMessage(uPlayerGuid, fZoomCompleteCallback, fFadeCompleteCallback)
- **Description**: Displays a completed message on the HUD.
- **Parameters**:
  - `uPlayerGuid`: GUID of the player to show the message to.
  - `fZoomCompleteCallback`: Callback function for when the zoom animation completes.
  - `fFadeCompleteCallback`: Callback function for when the fade animation completes.

### ShowFailedMessage(uPlayerGuid, fZoomCompleteCallback, fFadeCompleteCallback)
- **Description**: Displays a failed message on the HUD.
- **Parameters**:
  - `uPlayerGuid`: GUID of the player to show the message to.
  - `fZoomCompleteCallback`: Callback function for when the zoom animation completes.
  - `fFadeCompleteCallback`: Callback function for when the fade animation completes.

### ShowMessage(uPlayerGuid, sTextureName, fZoomCompleteCallback, fFadeCompleteCallback, nXLocation, nYLocation, sHorizontalAnchor, sVerticalAnchor, nMessageWidth, nMessageHeight, nMessageDisplayTime, vSoundEffect)
- **Description**: Displays a message on the HUD with specified parameters.
- **Parameters**:
  - `uPlayerGuid`: GUID of the player to show the message to.
  - `sTextureName`: Name of the texture for the message.
  - `fZoomCompleteCallback`: Callback function for when the zoom animation completes.
  - `fFadeCompleteCallback`: Callback function for when the fade animation completes.
  - `nXLocation`, `nYLocation`: Coordinates for the message location.
  - `sHorizontalAnchor`, `sVerticalAnchor`: Anchor points for the message.
  - `nMessageWidth`, `nMessageHeight`: Dimensions of the message.
  - `nMessageDisplayTime`: Duration to display the message.
  - `vSoundEffect`: Sound effect(s) to play with the message.

### AnimationFinishCallback(oWidget)
- **Description**: Handles the completion of an animation for a widget.
- **Parameters**:
  - `oWidget`: The widget instance.

### HandleUpdateEvent(oWidget, nTimeSinceLastUpdate)
- **Description**: Updates the display time remaining for a widget and handles removal if necessary.
- **Parameters**:
  - `oWidget`: The widget instance.
  - `nTimeSinceLastUpdate`: Time since the last update event.

### RemovalCallback(oWidget)
- **Description**: Handles the removal of a widget after its fade animation completes.
- **Parameters**:
  - `oWidget`: The widget instance.

### Init()
- **Description**: Initializes the module by loading necessary fonts.

### HandleClassyTextInit(oWidget)
- **Description**: Initializes a widget for displaying classy text.
- **Parameters**:
  - `oWidget`: The widget instance.

### DisplayClassyText(oWidget, sText, nX, nY, nDuration, nScale, sHorizAnchor, sVertAnchor, sJustification, bExpand)
- **Description**: Displays classy text on the HUD with specified parameters.
- **Parameters**:
  - `oWidget`: The widget instance.
  - `sText`: The text to display.
  - `nX`, `nY`: Coordinates for the text location.
  - `nDuration`: Duration to display the text.
  - `nScale`: Scale of the text.
  - `sHorizAnchor`, `sVertAnchor`: Anchor points for the text.
  - `sJustification`: Justification of the text.
  - `bExpand`: Whether to expand the text.
- **Not previously documented:** clamps `nX`/`nWidth`/`nY`/`nHeight` to stay on-screen using a tiny
  `Clamp(n, nMin, nMax)` helper defined *inside this function's own body* (without `local`, so — like a
  couple of other modules on this wiki — it's technically a global, just one only ever called from here).

### _ClassyTextLoadCompleteCallback(oText, sText, nDuration, sJustification, bExpand)
- **Description**: Handles the completion of loading a classy text widget.
- **Parameters**:
  - `oText`: The text widget instance.
  - `sText`: The text to display.
  - `nDuration`: Duration to display the text.
  - `sJustification`: Justification of the text.
  - `bExpand`: Whether to expand the text.

### _HandleClassyTextEnd(oText)
- **Description**: Handles the end of a classy text widget by scheduling its deletion.
- **Parameters**:
  - `oText`: The text widget instance.

### _DeleteClassyText(oText)
- **Description**: Deletes a classy text widget from the HUD.
- **Parameters**:
  - `oText`: The text widget instance.

## Events

{: .warning }
> The earlier draft listed `Event.ObjectHibernation`, `Event.PlayerInput`, and `Event.PlayerJoined` — **none of these appear in the source.** Removed. (`OnPlayerJoined()` here is an engine *lifecycle callback*, not an `Event.PlayerJoined` subscription.)

The real engine-event usage in this file (see [Event](../namespaces/event)):
- **`Event.Create(Event.TimerRelative, {nSeconds[, bRealtime]}, fCallback, tData)`** — the workhorse for all scheduled steps: fanfare scroll-out (3s), card fanfare stages, widget deletion delays, the announcement auto-remove (0.5s in `HandleInitialization`), and the text-fanfare done timer. Fire-and-forget one-shots.
- **`Event.Create(Event.Button, {uPlayer, sButton, "press", true}, fCallback, tData)`** and **`Event.CreatePersistent(Event.Button, ...)`** — bound in `_SkipFanfare` (skip on `cancel`/`selection`) and `_RetryEvents` (left-stick `lsleft`/`lsright` and `selection`/`cancel` mapped to `_GuiInternal.SendFlashInput`). Button choice depends on `Sys.IsConfirmOnCircle()`.
- **`Event.Delete(handle)`** — `_DeleteFanfareEvents` tears down the stored `_ev*` handles.
- **Widget event handlers** (not engine events): `SetEventHandler("GuiUpdate", _SlowdownUpdate)` drives the slow-mo dilation; `SetEventHandler("GuiUpdate", HandleUpdateEvent)` counts down a message's on-screen time.
- **Flash/ActionScript handlers** (Scaleform, not engine events): `SetFlashEventHandler("closeFanfare"/"Retry"/"FanfareCountUpComplete"/"FanfareOff"/"close", ...)` and `SetEventHandler("ControllerInput", _HandleFanfareInput)`.

## Notes for modders

- **Fanfare build sequence** (contract/mission/wager): `CreateFanfare(sType, sFaction)` → `SetFanfareParameters(...)` and repeated `AddFanfareLineItem(...)` → optional `SetFanfareCompleteCallback(...)` → `CommenceFanfare(nSlowdownDuration)`. `CommenceFanfare` locks all HQ ([`MrxHqManager.LockAllHq`](mrxhqmanager)), starts a time-dilation slow-mo (via `_SlowdownUpdate`), hides the HUD, suppresses the PDA, and disables sniper scope; `_EndFanfare` reverses all of that and `MrxHqManager.UnlockAllHq()`s. If you spawn a fanfare, make sure it can reach `_EndFanfare` or the HUD/PDA/HQ stay locked.
- **Support / contact / card fanfares** each have a `*Commence` entry point that only actually plays once the SWF's `bLoadingComplete` fires (the `*LoadCompleteCallback` re-checks `bReadyToStart`). So calling `SupportFanfareCommence`/`ContactFanfareCommence`/`CardFanfareCommence` before the movie finishes loading is safe — it defers.
- **Multiplayer**: many entry points call `Net.SendEvent_*` when `Net.IsServer()` (`Net.SendEvent_Fanfare`, `Net.SendEvent_CardFanfare`, `Net.SendEvent_TextFanfare`, `Net.SendEvent_ShowMessage`, `Net.SendEvent_CloseFanfare`) to mirror the fanfare to clients. See [Net](../namespaces/net).
- **`ShowMessage` tunables**: it zooms an image in from `nMagnification` (×5) scale to normal over `nAnimationTimeLength`, holds for `nMessageDisplayTime` (default `nLifeTime` = 3s; pass a negative time to hold indefinitely), then fades over `nFadeTime`. `ShowCompletedMessage`/`ShowFailedMessage` are thin wrappers using textures `global_gui_completed` / `global_gui_failed`. `vSoundEffect` may be a single cue string or a table of them.
- **`ShowEventFanfare(sType, vText, ...)`**: `sType` must be a key of `_tEventTextures` or it silently returns. `vText` can be a string or a table of strings shown sequentially (each held `max(1.5, 4/count)`s, cross-faded by `_knTextQueueFadeTime`).
- **Business-card faction codes**: only `an`, `ch`, `oc`, `gr`, `pr` are valid (case-insensitive) — any other faction makes `CreateFanfare("card", ...)` return `false`.

{: .note }
> **Real bug in `ShowMessage` (server→client path):** the `Net.SendEvent_ShowMessage(...)` call passes `nGlobalTime` for height and `nMessageDisplayTime or nLifeTime` positionally in a way that references the undefined global `nGlobalTime` (there is no such variable — the module defines `nGlobalHeight`/`nLifeTime`). On a dedicated-server non-local target this passes `nil` for the height argument. Local display (the common path) is unaffected. Also note `_DeleteFanfareWidget` sets `bSupressedPda` (typo) instead of clearing `bSuppressedPda`.

- **Decompiler artifacts**: `DisplayClassyText` defines its `Clamp(n, nMin, nMax)` helper *inside* its own body without `local`, so it leaks as a global — harmless, only called from here. Several `*LoadCompleteCallback`s share the same defer-until-loaded shape.