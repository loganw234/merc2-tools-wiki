---
title: MrxGuiHudMessage
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud, message]
verified: true
verified_note: corrects the Instance pattern section (singleton, not per-uGuid -- has an Init() setup function but no OnActivate/Create/tInstance anywhere in source)
---

# MrxGuiHudMessage

*Module: mrxguihudmessage.lua*

## Overview
The `MrxGuiHudMessage` module is responsible for managing various types of HUD messages and fanfares in the game. It provides functionality to display different kinds of messages, such as text-based fanfares, event fanfares, and support-related fanfares. The module handles the creation, initialization, and cleanup of these messages, ensuring they are displayed correctly with appropriate animations and callbacks.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxUtil`

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: only a one-time `Init()` setup function, no
`OnActivate`/`Create`/`tInstance` registry anywhere in source. This is one shared HUD message/fanfare
system, not something spawned per world object. Key fields:
- `nGlobalWidth`, `nGlobalHeight`: Dimensions for the fanfare widget.
- `nX`, `nY`: Position coordinates for the fanfare widget.
- `nMagnification`: Magnification factor for the fanfare widget.
- `nAnimationTimeLength`, `nLifeTime`, `nFadeTime`: Time-related parameters for animations and transitions.
- `_gFanfareFlashWidget`, `_gFullscreenFadeWidget`: Global references to the flash and fullscreen fade widgets used in fanfares.
- Various other fields related to specific types of fanfares (e.g., support, contact, card) to store their state and configuration.

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

This module subscribes to and fires several engine events:

- **`Event.ObjectHibernation`**: Listens for object hibernation events to manage fanfare activation and deactivation.
- **`Event.TimerRelative`**: Used for scheduling delays, animations, and other timed events within the fanfares.
- **`Event.PlayerInput`**: Captures player input to handle skipping or retrying fanfares.
- **`Event.PlayerJoined`**: Responds to player join events to manage active fanfare widgets.

## Notes for modders

1. **Call-order requirements**:
   - Ensure that `CommenceFanfare` is called after setting up all necessary parameters and callbacks to ensure proper initialization and display of the fanfare.
   - When adding items or setting parameters for specific types of fanfares (e.g., support, contact, card), make sure these functions are called in the correct order before starting the fanfare.

2. **Pitfalls**:
   - Overwriting global variables such as `nGlobalWidth`, `nGlobalHeight`, etc., can lead to unexpected behavior if other parts of the game rely on these values.
   - Failing to set up necessary event handlers or callbacks can result in incomplete or non-functional fanfares.

3. **Tunables**:
   - Adjusting time-related parameters like `nAnimationTimeLength`, `nLifeTime`, and `nFadeTime` can fine-tune the visual and temporal aspects of the fanfares.
   - Modifying the magnification factor (`nMagnification`) can change the size of the fanfare widgets, affecting their visibility and impact on the player's experience.

4. **Decompiler artifacts**:
   - Some internal functions like `_SupportLoadCompleteCallback`, `_ContactLoadCompleteCallback`, etc., may have unused local variables or redundant operator groupings due to decompiler quirks. These should be treated as noise rather than intentional logic.