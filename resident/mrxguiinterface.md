---

title: MrxGuiInterface

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, hud]

verified: true
verified_note: 'deeper pass: rewrote the Events section — the old list (Event.ObjectiveAdded/ObjectiveUpdated/MessageAdded/CinematicStarted/…) is entirely absent from source and was removed; the ONLY real Event.* calls are two Event.Create(Event.TimerRelative) widget-not-ready retries, Event.CreatePersistent(Event.ScriptEvent,{"mpPlayerJoin",…}) co-op resync, and Event.Create(Event.ObjectHibernation) awaiting P2. Added the tObjectiveMessageConfigs color/sound-cue catalog and boundary alpha=160 constant. Instance pattern (singleton) and the sub-namespace coverage re-confirmed'

---



# MrxGuiInterface



*Module: mrxguiinterface.lua*



## Overview

The `MrxGuiInterface` module is a comprehensive interface for managing various aspects of the game's user interface (UI), including the Heads-Up Display (HUD) and the Personal Digital Assistant (PDA). It provides functionalities to manipulate UI elements such as radar objectives, message boxes, support menus, objective trays, map labels, announcements, fanfares, cinematic movies, faction displays, shops, and PDA database entries. The module ensures that these UI components are synchronized across clients in a multiplayer environment.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`, `MrxGuiHudMessage`, `MrxGuiSupportShop`, `MrxGuiTutorial`, `MrxGuiHudFactionGauge`, `MrxTaskObjective`, `MrxUtil`, `MrxBootstrap`, `WifMissionData`, and `MrxSoundCategories`



## Instance pattern

**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry
anywhere in source. This is the single shared UI-plumbing hub for the whole game session, not something
spawned per world object. Key fields:

- **HudInterface**: Exposed as `_G.Hud` and contains sub-tables like `Radar`, `MessageBox`, `SupportMenu`, `ObjectiveTray`, etc.

- **PdaInterface**: Exposed as `_G.Pda` and manages PDA-related functionalities such as support items, faction attitudes, log entries, help entries, dossier entries, statistic categories, and statistic entries.



The module also maintains internal state for fanfare queues, subtitle buffers, and other UI components. It ensures that all UI updates are synchronized across clients to maintain a consistent user experience in multiplayer scenarios.



## Functions



### HudInterface.Radar:AddObjective(tArgs)

Adds an objective to the radar for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and then adds the objective to each widget. If the current player is a server and net-syncing is not disabled, it sends a network event to add the radar objective.



### HudInterface.Radar:UpdateObjective(tArgs)

Updates an existing objective on the radar for specified players. Similar to `AddObjective`, it calls `_GetWidgetsForPlayers` to get the relevant widgets and updates the objective in each widget. If the current player is a server and net-syncing is not disabled, it sends a network event to update the radar objective.



### HudInterface.Radar:RemoveObjective(tArgs)

Removes an objective from the radar for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and removes the objective from each widget. If the current player is a server and net-syncing is not disabled, it sends a network event to remove the radar objective.



### HudInterface.Radar:AnimateObjectiveSize(tArgs)

Animates the size of an objective on the radar for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and animates the size of the objective in each widget.



### HudInterface.Radar:AnimateObjectiveAlpha(tArgs)

Animates the alpha (transparency) of an objective on the radar for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and animates the alpha of the objective in each widget.



### HudInterface.Radar:AnimateObjectiveSonar(tArgs)

Animates a sonar effect for an objective on the radar for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and applies the sonar animation to the objective in each widget.



### HudInterface.Radar:UnanimateObjective(tArgs)

Stops any animations associated with an objective on the radar for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and stops the animations of the objective in each widget.



### HudInterface.Radar:AddLineRegion(tArgs)

Adds a line region to the radar for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and adds the line region to each widget.



### HudInterface.Radar:RemoveLineRegion(tArgs)

Removes a line region from the radar for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and removes the line region from each widget.



### HudInterface.MessageBox:AddMessage(tArgs)

Adds a message to the message box for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and adds the message to each widget, returning a table of message IDs.



### HudInterface.MessageBox:ModifyPendingMessage(tArgs)

Modifies an existing pending message in the message box for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and modifies the message in each widget.



### HudInterface.MessageBox:RemovePendingMessage(tArgs)

Removes a pending message from the message box for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and removes the message from each widget.



### HudInterface.MessageBox:Clear(tArgs)

Clears all messages from the message box for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and clears the messages in each widget.



### GetMessageTypeFromHash(uStringHash)

Retrieves the message type string from a given hash by iterating over `tObjectiveMessageConfigs`.



### DisplayObjectiveMessage(bDisplay, sInlineIcon, sMsgType, sShortDesc, sGroupId, fCallback, tCallbackArgs)

Displays an objective message based on the provided parameters. It handles client-server synchronization and manages message display logic, including sound cues and callback functions.



### HudInterface.SupportMenu:AddItem(tArgs)

Adds an item to the support menu for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and adds the item to each widget.



### HudInterface.SupportMenu:RemoveItem(tArgs)

Removes an item from the support menu for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and removes the item from each widget.



### HudInterface.SupportMenu:SetShootingGalleryMode(tArgs)

Sets the shooting gallery mode for the support menu for specified players. It calls `_GetWidgetsForPlayers` to get the relevant widgets and sets the shooting gallery mode in each widget.



### HudInterface.ResourceCounter:SetCash(tArgs) / HudInterface.ResourceCounter:SetFuel(tArgs)

**Not previously documented — a whole sub-namespace missing from this page.** `tArgs` can be a bare number
(just the new value) or a table with `nValue`/`sReason`(cash only)/`nIncrement`; `SetFuel` additionally
accepts `nMax` to render an "X/max" suffix on the widget. Both fetch every matching player's resource-
counter widget via `_GetWidgetsForPlayers` (filtered on `"money"`/`"fuel"` respectively), call `SetValue`
on each, and `Show()` the widget.



### HudInterface.Tutorial:SetText(tArgs) / HudInterface.Tutorial:ShowTutorialForObject(tArgs) / HudInterface.Tutorial:ShowTutorialOnscreen(tArgs)

**Not previously documented — another whole missing sub-namespace.** Thin `_GetWidgetsForPlayers`-driven
wrappers around [`MrxGuiTutorial`](mrxguitutorial): `SetText` just forwards `tArgs.sText` to each matching
tutorial widget's own `SetText`; `ShowTutorialForObject`/`ShowTutorialOnscreen` forward straight to
`MrxGuiTutorial.DisplayTutorialForObject`/`DisplayTutorial` respectively for every player in
`tArgs.vPlayer` (or every player in the session if `vPlayer` isn't a table/single guid).

### HudInterface.Satellite:SetTutorialText(tArgs)

**Not previously documented.** Forwards `tArgs.sText` (defaulting to `" "` if omitted) to `SetHelpText` on
every matching player's satellite-overlay widget.



### HudInterface.ObjectiveTray:SetSlotToText(tArgs)

Sets the text for a specific slot in the objective tray for specified players. It updates local widgets and, if on the server, synchronizes with remote clients.



**Parameters:**

- `tArgs` (table): A table containing:

  - `vPlayer`: The player(s) to update.

  - `nSlot`: The slot number to set text for.

  - `sText`: The text to display.

  - `bDontNetSync`: A boolean indicating whether to skip network synchronization.



### SendSlotText()

Sends the current client-side slot texts to all remote players when a new player joins.



### HudInterface.ObjectiveTray:SetSlotToImage(tArgs)

Sets an image for a specific slot in the objective tray for specified players. It updates local widgets and, if on the server, synchronizes with remote clients.



**Parameters:**

- `tArgs` (table): A table containing:

  - `vPlayer`: The player(s) to update.

  - `nSlot`: The slot number to set image for.

  - `sTexture`: The texture hash of the image.

  - `nWidth`: The width of the image.

  - `nHeight`: The height of the image.



### HudInterface.ObjectiveTray:SetSlotToWidget(tArgs)

Sets a widget for a specific slot in the objective tray for specified players. It updates local widgets.



**Parameters:**

- `tArgs` (table): A table containing:

  - `vPlayer`: The player(s) to update.

  - `nSlot`: The slot number to set widget for.

  - `oWidget`: The widget object to display.



### HudInterface.ObjectiveTray:ClearSlot(tArgs)

Clears a specific slot in the objective tray for specified players. It updates local widgets and, if on the server, synchronizes with remote clients.



**Parameters:**

- `tArgs` (table): A table containing:

  - `vPlayer`: The player(s) to update.

  - `nSlot`: The slot number to clear.



### NetClientSetObjectiveTraySlot(aSlot, aIsImage, aText, aImageHash, aWidth, aHeight)

Sets the objective tray slot on the client side. If the widget is not available, it retries after a delay.



**Parameters:**

- `aSlot`: The slot number.

- `aIsImage`: A boolean indicating if the slot should display an image.

- `aText`: The text to display (if not an image).

- `aImageHash`: The texture hash of the image (if an image).

- `aWidth`: The width of the image (if an image).

- `aHeight`: The height of the image (if an image).



### NetClientClearObjectiveTraySlot(aSlot)

Clears the objective tray slot on the client side.



**Parameters:**

- `aSlot`: The slot number to clear.



### HudInterface.MapLabel:Show(tArgs)

Shows a map label for specified players.



**Parameters:**

- `tArgs` (table): A table containing:

  - `vPlayer`: The player(s) to show the label for.

  - `sLocation`: The location text to display.

  - `nDuration`: The duration to show the label.



### HudInterface.Announcement:Show(tArgs)

Shows an announcement message for specified players.



**Parameters:**

- `tArgs` (table): A table containing:

  - `vPlayer`: The player(s) to show the announcement for.

  - `sTexture`: The texture hash of the announcement image.

  - `fZoomCallback`: A function called when the announcement is zoomed in.

  - `fFadeCallback`: A function called when the announcement fades out.

  - `nX`, `nY`: Position coordinates.

  - `sHorizontalAnchor`, `sVerticalAnchor`: Anchor points for positioning.

  - `nWidth`, `nHeight`: Dimensions of the announcement.

  - `nDuration`: The duration to show the announcement.

  - `vSoundEffect`: Sound effect to play with the announcement.



### Hud.ClassyText:ShowText(tArgs)

Shows a large, centered animated text popup (a Flash `"text_effect"` SWF) for specified players —
confirmed to be a real, fully-wired system (traced through to
[`MrxGuiHudMessage.DisplayClassyText`](mrxguihudmessage)), but **no other script anywhere in the
decompiled corpus actually calls it** — used live for the first time in
[`Fireworks.lua`](../sample-scripts-onkey) (a "Happy 4th of July" banner) — see that page's own
`OnKey` scripts collection.

**Parameters:**

- `tArgs` (table): A table containing:

  - `vPlayer`: The player(s) to show the text to — `nil` targets every player with an active widget of
    this name.

  - `sText` (string): The text to display. Non-string values are silently ignored (`DisplayClassyText`
    returns early if `type(sText) ~= "string"`).

  - `nY`: Vertical position — defaults to `240` if omitted. Horizontal position is not configurable at
    all; `DisplayClassyText` always recenters it itself (`nX = (640 - _nClassyTextWidth) * 0.5`).

  - `nDuration`: Seconds on screen — defaults to `3` if omitted.

  - `sJustification`: Text alignment (`"left"`/`"center"`/etc., default `"left"`). **Also silently
    doubles as the horizontal anchor** — `DisplayClassyText`'s own `sHorizAnchor` parameter gets
    immediately overwritten with whatever `sJustification` resolves to, before `sJustification` even
    gets its own default applied. There's no way to set horizontal anchor and justification
    independently; whichever value you pass as `sJustification` controls both.

  - `sVertAnchor`: Vertical anchor (`"center"`, etc., default `"center"`).

  - `bExpand`: Whether the text box expands to fit content (default `false`).

### _tFanfareQueue:Append(fAction)

Appends an action to the fanfare queue. If the queue is pending, it immediately executes the action; otherwise, it adds it to the queue.



**Parameters:**

- `fAction`: The function to append to the queue.



### _tFanfareQueue:Advance()

Advances the fanfare queue by executing the next action if the queue is not paused and advancing is not already in progress.



### _tFanfareQueue:FinishItem()

Marks the current item as finished and advances the queue.



### HudInterface.FanfareQueue:Append(fAction, ...)

Appends a function with arguments to the fanfare queue. The function will be executed when the queue advances.



**Parameters:**

- `fAction`: The function to append.

- `...`: Additional arguments for the function.



### HudInterface.FanfareQueue.Pause(bPause)

Pauses or resumes the fanfare queue.



**Parameters:**

- `bPause`: A boolean indicating whether to pause the queue.



### HudInterface.FanfareQueue.ClientSetPending(bPending)

Sets the pending state of the client-side fanfare queue.



**Parameters:**

- `bPending`: A boolean indicating the pending state.



### HudInterface.FanfareQueue.ClientPause(bPause)

Pauses or resumes the client-side fanfare queue.



**Parameters:**

- `bPause`: A boolean indicating whether to pause the queue.



### HudInterface.JobFanfare:Complete(tArgs)

Appends a job completion fanfare action to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `fCallback`: A callback function.

  - `tCallbackData`: Data for the callback.



### HudInterface.JobFanfare:Failed(tArgs)

Appends a job failure fanfare action to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `fCallback`: A callback function.

  - `tCallbackData`: Data for the callback.



### HudInterface.Fanfare:Create(tArgs)

Creates a fanfare message of a specified type and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `sType`: The type of fanfare ("contract", "wager", or "mission").

  - `sProfileName1`, `sProfileName2`: Profile names for the fanfare.

  - `sCancelMsg`: Cancel message for the fanfare.

  - `bAllowRetry`: A boolean indicating if retry is allowed.

  - `fCallback`: A callback function.

  - `tCallbackData`: Data for the callback.



### HudInterface.Fanfare:AddItem(tArgs)

Adds an item to a fanfare message and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `sDescription`: The description of the item.

  - `nValue`: The value associated with the item.

  - `sValueType`: The type of the value.

  - `nPlayer`: The player associated with the item.



### Hud.Fanfare:Commence(tArgs)

Commences a fanfare message with a specified slowdown duration and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `nSlowdownDuration`: The duration for slowing down the fanfare.



### HudInterface.SupportFanfare:Create(tArgs)

Creates a support fanfare message and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `fCallback`: A callback function.

  - `tCallbackData`: Data for the callback.



### HudInterface.SupportFanfare:AddItem(tArgs)

Adds an item to a support fanfare message and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `sTexture`: The texture hash of the item.

  - `sItemName`: The name of the item.

  - `sFaction`: The faction associated with the item.

  - `sContactName`: The contact name for the item.

  - `sBlipName`: The blip name for the item.



### HudInterface.SupportFanfare:Commence(tArgs)

Commences a support fanfare message and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - No specific parameters mentioned.



### HudInterface.ContactFanfare:Commence(tArgs)

Commences a contact fanfare message and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `fCallback`: A callback function.

  - `tCallbackData`: Data for the callback.



### HudInterface.CardFanfare:Commence(tArgs)

Commences a card fanfare message with specified parameters and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `sFaction`: The faction associated with the card.

  - `sTitle`: The title of the card.

  - `sName`: The name on the card.

  - `sJobTitle`: The job title on the card.

  - `sPhone1`, `sPhone2`: Phone numbers on the card.

  - `sEmail`: Email address on the card.

  - `nDisplayTime`: The display time for the card.



### Hud.TextFanfare:Commence(tArgs)

Commences a text fanfare message with specified parameters and appends it to the queue.



**Parameters:**

- `tArgs` (table): A table containing:

  - `sLine1`, `sLine2`: Text lines for the fanfare.

  - `nEntranceTime`: The entrance time for the fanfare.

  - `nDisplayTime`: The display time for the fanfare.

  - `nFadeTime`: The fade time for the fanfare.

  - `fCallback`: A callback function.

  - `tCallbackData`: Data for the callback.



### HudInterface.EventFanfare:Commence(tArgs)

Commences an event fanfare message with specified parameters and appends it to the queue. It also logs the event in the PDA database if applicable.



**Parameters:**

- `tArgs` (table): A table containing:

  - `sType`: The type of the event.

  - `vText`: The text or table of texts for the event.

  - `fCallback`: A callback function.

  - `tCallbackData`: Data for the callback.



### HudInterface.Cinematic:Show(tArgs)

Shows a cinematic movie with specified parameters.



**Parameters:**

- `tArgs` (table): A table containing:

  - `sMovie`: The name of the movie to show.

  - `nFadeInTime`: The fade-in time for the movie.

  - `nFadeOutTime`: The fade-out time for the movie.

  - `fCallback`: A callback function.

  - `tCallbackData`: Data for the callback.

  - `bSubtitles`: A boolean indicating if subtitles should be shown.



### HudInterface.Cinematic:Hide()

Hides the currently playing cinematic movie.



### HudInterface.Cinematic:Play()

Plays the currently paused cinematic movie.



### HudInterface.Cinematic:Pause()

Pauses the currently playing cinematic movie.



### NetClientShowMovie(sMovieName, nFadeIn, nFadeOut, bSubtitlesFlag)

Shows a cinematic movie on the client side if it is not already running.



**Parameters:**

- `sMovieName`: The name of the movie to show.

- `nFadeIn`: The fade-in time for the movie.

- `nFadeOut`: The fade-out time for the movie.

- `bSubtitlesFlag`: A boolean indicating if subtitles should be shown.



### NetClientHideMovie()

Hides the currently playing cinematic movie on the client side.



### NetClientIsMovieRunning()

Checks if a cinematic movie is currently running on the client side.



**Returns:**

- A boolean indicating whether the movie is running.



### NetClientIsMovieHiding()

Checks if a cinematic movie is currently hiding on the client side.



**Returns:**

- A boolean indicating whether the movie is hiding.



### HudInterface.CinematicPlaceholder:Show(tArgs)

- **Description**: Shows a cinematic placeholder widget with specified texture, caption, fade-in and fade-out times, callback function, and callback data.

- **Parameters**:

  - `tArgs.sTexture`: The texture to display.

  - `tArgs.sCaption`: The caption text.

  - `tArgs.nFadeInTime`: Time for the widget to fade in.

  - `tArgs.nFadeOutTime`: Time for the widget to fade out.

  - `tArgs.fCallback`: Callback function to be called after the widget is shown.

  - `tArgs.tCallbackData`: Data to pass to the callback function.



### HudInterface.CinematicPlaceholder:Hide(tArgs)

- **Description**: Hides the cinematic placeholder widget.

- **Parameters**:

  - `tArgs`: A table containing any necessary arguments (not used in this implementation).



### HudInterface.FactionDisplay:Show(tArgs)

- **Description**: Shows faction display widgets for specified players with a given duration.

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to show the faction display for.

  - `tArgs.nDuration`: Duration for which the faction display should be shown.



### HudInterface.FactionDisplay:SetValue(tArgs)

- **Description**: Sets the value of a faction gauge for specified players, optionally sending a network message if on the server.

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to set the faction value for.

  - `tArgs.sFaction`: The faction identifier.

  - `tArgs.nValue`: The new value for the faction gauge.

  - `tArgs.bInitialize`: Boolean indicating if this is an initialization call.

  - `tArgs.bForceOnClient`: Boolean to force setting on the client regardless of network state.



### HudInterface.FactionDisplay:SetInsideFactionZone(tArgs)

- **Description**: Sets whether a player is inside a faction zone for specified players.

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to set the faction zone status for.

  - `tArgs.sFaction`: The faction identifier.

  - `tArgs.bInside`: Boolean indicating if the player is inside the faction zone.

  - `tArgs.bInitialize`: Boolean indicating if this is an initialization call.



### HudInterface.FactionDisplay:ConfigureThresholds(tArgs)

- **Description**: Configures the thresholds and names for faction gauges.

- **Parameters**:

  - `tArgs.tLevelThresholds`: Table of level thresholds.

  - `tArgs.tLevelNames`: Table of level names corresponding to the thresholds.

  - `tArgs.sPursuitName`: Name of the pursuit.

  - `tArgs.bDisplayResult`: Boolean indicating if the result should be displayed.



### HudInterface.FactionDisplay:AddMeter(tArgs)

- **Description**: Adds a faction meter for specified players.

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to add the faction meter for.

  - `tArgs.sFaction`: The faction identifier.

  - `tArgs.sTexture`: Texture for the faction meter.



### HudInterface.FactionDisplay:StartTimer(tArgs)

- **Description**: Starts a timer for a faction gauge for specified players.

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to start the timer for.

  - `tArgs.sFaction`: The faction identifier.

  - `tArgs.nDuration`: Duration of the timer.

  - `tArgs.fCallback`: Callback function to be called when the timer ends.

  - `tArgs.tCallbackData`: Data to pass to the callback function.



### HudInterface.FactionDisplay:StartPursuit(tArgs)

- **Description**: Starts a pursuit for a faction gauge for specified players, optionally sending a network message if on the server.

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to start the pursuit for.

  - `tArgs.sFaction`: The faction identifier.

  - `tArgs.nDuration`: Duration of the pursuit.

  - `tArgs.fCallback`: Callback function to be called when the pursuit ends.

  - `tArgs.tCallbackData`: Data to pass to the callback function.

  - `tArgs.bForceOnClient`: Boolean to force setting on the client regardless of network state.



### HudInterface.FactionDisplay:HideMeter(tArgs)

- **Description**: Hides a faction meter for specified players, optionally sending a network message if on the server.

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to hide the faction meter for.

  - `tArgs.sFaction`: The faction identifier.

  - `tArgs.bForceOnClient`: Boolean to force setting on the client regardless of network state.



### HudInterface.FactionDisplay:RemoveMeter(tArgs)

- **Description**: Removes a faction meter for specified players (not implemented in this part).

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to remove the faction meter for.

  - `tArgs.sFaction`: The faction identifier.



### HudInterface.FactionDisplay:RemoveAllMeters(tArgs)

- **Description**: Removes all faction meters for specified players (not implemented in this part).

- **Parameters**:

  - `tArgs.vPlayer`: The player or list of players to remove all faction meters for.



### HudInterface.SubtitleBuffer.AddMessage

- **Description**: Adds a message to the subtitle buffer.

- **Parameters**:

  - `tArgs`: A table containing any necessary arguments (not used in this implementation).



### HudInterface.SubtitleBuffer.ModifyPendingMessage

- **Description**: Modifies a pending message in the subtitle buffer.

- **Parameters**:

  - `tArgs`: A table containing any necessary arguments (not used in this implementation).



### HudInterface.SubtitleBuffer.RemovePendingMessage

- **Description**: Removes a pending message from the subtitle buffer.

- **Parameters**:

  - `tArgs`: A table containing any necessary arguments (not used in this implementation).



### HudInterface.SubtitleBuffer.Clear

- **Description**: Clears all messages from the subtitle buffer.

- **Parameters**:

  - `tArgs`: A table containing any necessary arguments (not used in this implementation).



### Hud.Shop:Create(tArgs)

- **Description**: Creates a shop for a specified player.

- **Parameters**:

  - `tArgs.uPlayer`: The player to create the shop for.



### Hud.Shop:AddItem(tArgs)

- **Description**: Adds an item to a shop for a specified player.

- **Parameters**:

  - `tArgs.uPlayer`: The player to add the item to.

  - `tArgs.sName`: Name of the item.

  - `tArgs.nCashCost`: Cash cost of the item.

  - `tArgs.nCurrentStock`: Current stock of the item.

  - `tArgs.nMaxStock`: Maximum stock of the item.

  - `tArgs.bUnlocked`: Boolean indicating if the item is unlocked.

  - `tArgs.sId`: Unique identifier for the item (optional).

  - `tArgs.bFuelTank`: Boolean indicating if the item is a fuel tank.

  - `tArgs.nFuelQuantity`: Quantity of fuel in the tank (if applicable).

  - `tArgs.sRawName`: Raw name of the item.



### Hud.Shop:AddItemFull(tArgs)

- **Description**: Adds a full item to a shop for a specified player, including detailed description and texture.

- **Parameters**:

  - `tArgs.uPlayer`: The player to add the item to.

  - `tArgs.sName`: Name of the item.

  - `tArgs.sDescription`: Description of the item.

  - `tArgs.sTexture`: Texture for the item.

  - `tArgs.nCashCost`: Cash cost of the item.

  - `tArgs.nCurrentStock`: Current stock of the item.

  - `tArgs.nMaxStock`: Maximum stock of the item.

  - `tArgs.bUnlocked`: Boolean indicating if the item is unlocked.

  - `tArgs.sId`: Unique identifier for the item (optional).

  - `tArgs.bFuelTank`: Boolean indicating if the item is a fuel tank.

  - `tArgs.bMarkAsNew`: Boolean indicating if the item should be marked as new.

  - `tArgs.nFuelQuantity`: Quantity of fuel in the tank (if applicable).

  - `tArgs.sRawName`: Raw name of the item.



### Hud.Shop:SetCallback(tArgs)

- **Description**: Sets a callback function for a shop for a specified player.

- **Parameters**:

  - `tArgs.uPlayer`: The player to set the callback for.

  - `tArgs.fCallback`: Callback function to be called when an event occurs.

  - `tArgs.tCallbackData`: Data to pass to the callback function.



### Hud.Shop:SetCloseCallback(tArgs)

- **Description**: Sets a close callback function for a shop for a specified player.

- **Parameters**:

  - `tArgs.uPlayer`: The player to set the close callback for.

  - `tArgs.fCallback`: Callback function to be called when the shop is closed.

  - `tArgs.tCallbackData`: Data to pass to the callback function.



### Hud.Shop:Commence(tArgs)

- **Description**: Commences a shop session for a specified player.

- **Parameters**:

  - `tArgs.uPlayer`: The player to commence the shop session for.



### Hud.Shop:Close(tArgs)

- **Description**: Closes a shop session for a specified player and logs the action.

- **Parameters**:

  - `tArgs.uPlayer`: The player to close the shop session for.



### PdaInterface:SetSuppressed(tArgs)

**Not previously documented.** A method directly on `PdaInterface` itself (not a sub-table like the others
on this page) — forwards `tArgs.bSuppress` to `SetSuppressed` on every matching player's PDA widget.

### PdaInterface.Map:AddBlip(tArgs) / PdaInterface.Map:RemoveBlip(tArgs)

**Not previously documented — a whole sub-namespace missing from this page**, alongside `AddLineRegion`/
`RemoveLineRegion` documented elsewhere on this page. `AddBlip` forwards a large set of `tArgs` fields
(name, position, label, description, guid, texture, associated mission, meter, sticky/todo-list flags,
faction — defaulting to `"PMC"` — and sort order) to each matching PDA widget's `AddMapBlip`; `RemoveBlip`
just needs `tArgs.sName`. Both also net-sync on the server (unless `tArgs.bDontNetSync`) via
`Net.SendEvent_AddPdaObjective`/`Net.SendEvent_RemovePdaObjective`.

### PdaInterface.Map:AddMission(tArgs) / RemoveMission(tArgs) / UpdateMission(tArgs) / SetSelectedMission(tArgs) / GetSelectedMission()

**Not previously documented.** Thin forwards to each matching PDA widget's own `AddMapMission`/
`RemoveMapMission`/`UpdateMapMission`/`SetSelectedMission` (name, label, description, faction, default
blip texture/label, suppress/trackable flags, sort order, depending on the call). `GetSelectedMission`
is the one read-only accessor in this group — it only looks at the **local** player's widget
(`Player.GetLocalPlayer()`, not `tArgs.vPlayer`) and returns as soon as it finds one.

### PdaInterface.Map:SetMissionTrackable(tArgs) / SetMissionTrackCallback(tArgs) / SetMissionChangeAllowed(tArgs)

**Not previously documented.** Straightforward forwards to each matching widget's own
`SetMissionTrackable`/`SetMissionTrackCallback`/`SetMissionChangeAllowed`.

### PdaInterface.Map:SetFakePlayerLocation(tArgs) / SetBeaconTutorialMode(tArgs)

**Not previously documented.** `SetFakePlayerLocation` forwards `nX`/`nY`/`nZ` to each matching widget's own
`SetFakePlayerLocation` — useful for tutorial/cinematic sequences where the PDA needs to show a location
other than the player's real one. `SetBeaconTutorialMode` forwards `tArgs.bEnable` to `SetBeaconTutorialMode`.



### PdaInterface.Support:UpdateItem(tArgs)

Updates the support item in the PDA interface for specified players. It iterates over widgets associated with the players and calls `UpdateSupport` on each widget with details like name, description, icon, stock, max stock, fuel cost, support object, and type.



### PdaInterface.Support:SetEquippedItem(tArgs)

Sets the equipped support item in the PDA interface for specified players. It iterates over widgets associated with the players and calls `SetEquippedSupport` on each widget with the name and ID of the support item.



### PdaInterface.Support:ReadEquippedSupport(tArgs)

Reads the currently equipped support item from the PDA interface for a specific player. It retrieves the PDA widget for the player and calls `ReadEquippedSupport` to get the equipped support details.



### PdaInterface.Support:RestoreEquippedSupport(tArgs)

Restores the equipped support item in the PDA interface for a specific player. It retrieves the PDA widget for the player and calls `RestoreEquippedSupport` with the support data to restore it.



### PdaInterface.Database:SetFactionAttitude(tArgs)

Sets the faction attitude in the PDA database for specified players. It iterates over widgets associated with the players and calls `SetFactionAttitude` on each widget with details like faction name, texture, and attitude level.



### PdaInterface.Database:AddLogEntry(tArgs)

Adds a log entry to the PDA database for specified players. It iterates over widgets associated with the players and calls `AddLogEntry` on each widget with details like type, name, message, and color.



### PdaInterface.Database:AddHelpEntry(tArgs)

Adds a help entry to the PDA database for specified players. It iterates over widgets associated with the players and calls `AddHelpEntry` on each widget with details like title, text, and icon.



### PdaInterface.Database:AddDossierEntry(tArgs)

Adds a dossier entry to the PDA database for specified players. It iterates over widgets associated with the players and calls `AddDossierEntry` on each widget with details like title, text, and icon.



### PdaInterface.Database:AddStatisticCategory(tArgs)

Adds a statistic category to the PDA database for specified players. It iterates over widgets associated with the players and calls `AddStatisticCategory` on each widget with details like category name and icon.



### PdaInterface.Database:AddStatisticEntry(tArgs)

Adds a statistic entry to the PDA database for specified players. It iterates over widgets associated with the players and calls `AddStatisticEntry` on each widget with details like category, description, and data.



### AddObjectiveToLocalPlayer(name, x, y, z, r, g, b, width, height, texture, uGuid, bSticky, bRotate, bOriented, nSortOrder)

Adds an objective to the local player's minimap. It retrieves the minimap widget for the local player and calls `AddObjective` with details like name, position, color, size, texture, GUID, and other properties.



### AddPdaBlipToLocalPlayer(sName, nX, nY, sLabel, uGuid, nTexture, nMissionIndex, bSticky, nSortOrder)

Adds a PDA blip to the local player's PDA interface. It retrieves the PDA widget for the local player and calls `AddMapBlip` with details like name, position, label, GUID, texture, mission index, and other properties.



### DeletePdaBlipForLocalPlayer(sName)

Deletes a PDA blip from the local player's PDA interface. It retrieves the PDA widget for the local player and calls `RemoveMapBlip` with the name of the blip to delete.



### DeleteObjectiveForLocalPlayer(name)

Deletes an objective from the local player's minimap. It retrieves the minimap widget for the local player and calls `DeleteObjective` with the name of the objective to delete.



### TestFlash(sFile)

Tests a flash file by creating or updating a full-screen Flash widget. If no file is provided, it ends the test. It sets up the Flash widget with the specified SWF file and manages its lifecycle.



### EndFlashTest()

Ends the flash test by removing the Flash widget from the interface and releasing control focus.



### Init()

Initializes the module by adding `TestFlash` and `EndFlashTest` functions to the global namespace for easy access during testing.



### _GetWidgetsForPlayers(vPlayers, sName)

Retrieves widgets associated with specified players or all players if no player list is provided. It filters out widgets without an owner and returns a table of valid widgets.



### NetClientAddBoundary(uBoundary, bInclusion)

Adds a boundary to both the radar and PDA map interfaces on the client side. It sets up the line region with properties like GUID, inclusion flag, color, and alpha.



### NetClientRemoveBoundary(uBoundary)

Removes a boundary from both the radar and PDA map interfaces on the client side by its GUID.



### NetClientFactionSetValue(sFactionName, nLevel)

Sets the value of a faction meter on the client side. It logs the action and updates the faction display with the specified faction name and level.



### NetClientFactionStartPursuit(sFactionName, nTime)

Starts a pursuit for a faction on the client side. It logs the action and initiates the pursuit in the faction display with the specified faction name and duration.



### NetClientFactionHideMeter(sFactionName, nDummy)

Hides a faction meter on the client side. It logs the action and hides the meter in the faction display for the specified faction name.



## Events

This module is **called into** (its sub-namespace methods are invoked directly by mission/task/HUD code and by
`NetClient*` net handlers); it does **not** subscribe to a bank of gameplay events. The complete list of real
`Event.*` calls in the file is small:

- **`Event.Create(Event.TimerRelative, {1}, DisplayObjectiveMessage, {…})`** — `DisplayObjectiveMessage`
  reschedules *itself* after 1 second when the GUI isn't loaded yet (`MrxBootstrap.IsGuiLoaded() ~= true`).
- **`Event.Create(Event.TimerRelative, {2}, NetClientSetObjectiveTraySlot, {…})`** — same idea: retry after 2
  seconds if the `"Objective Tray"` widget doesn't exist yet on a client.
- **`Event.CreatePersistent(Event.ScriptEvent, {"mpPlayerJoin", <filter>}, …)`** — server-only. Used twice, to
  re-broadcast an objective message and the objective-tray slot text to a co-op client when it joins mid-game.
  The filter `function(tData) return Net.IsServer() and not Player.IsLocal(tData[1]) end` restricts it to the
  server firing for a *remote* joiner.
- **`Event.Create(Event.ObjectHibernation, {Player.GetSecondaryCharacter(), "awake"}, …)`** (`SendSlotText`) —
  waits for player 2's character to wake before pushing slot text to them.

{: .note }
> The previous version of this page listed `Event.ObjectiveAdded`, `Event.ObjectiveUpdated`,
> `Event.ObjectiveRemoved`, `Event.MessageAdded`, `Event.MessageModified`, `Event.MessageRemoved`,
> `Event.MapLabelAdded`, `Event.AnnouncementShown`, `Event.FanfareCompleted`, `Event.CinematicStarted`, and
> `Event.CinematicStopped` as subscriptions. **None of these exist in `mrxguiinterface.lua`** — the sub-namespace
> methods (`Radar:AddObjective`, `MessageBox:AddMessage`, `Cinematic:Show`, …) are plain calls, not event
> handlers. They have been removed.

## Objective-message catalog (`tObjectiveMessageConfigs`)

`DisplayObjectiveMessage(bDisplay, sInlineIcon, sMsgType, …)` looks `sMsgType` up in this module-level table.
The keys are the message types, each with a color tag, a hex color (used in the PDA log), a prefix word, a
status word, a priority, and (for non-cancel types) a HUD sound cue. This is the exact set — swap a `sSoundCue`
or `sHexColor` here to restyle every objective toast of that kind:

| `sMsgType`                                   | prefix    | status      | color tag / hex   | priority | sound cue                     |
|----------------------------------------------|-----------|-------------|-------------------|---------:|-------------------------------|
| `add` / `upd` / `cpl` / `ccl`                | Objective | added/updated/completed/cancelled | `[objt]`/`[red]` `FFC800`/`FF0000` | 1 | `ui_HUD_Objective_New`/`_Update`/`_Complete` (none for cancel) |
| `bonus_add` / `bonus_upd` / `bonus_cpl` / `bonus_ccl` | Bonus | (same set) | `[2ndobjt]`/`[red]` `33CC99`/`FF0000` | 2 | (same set) |
| `bty_add` / `bty_upd` / `bty_cpl` / `bty_ccl`| Bounty    | (same set)  | `[2ndobjt]`/`[red]` `33CC99`/`FF0000` | 3 | (same set) |
| `collectible_upd`                            | Collectible | updated   | `[2ndobjt]` `33CC99` | 4 | `ui_HUD_Objective_Update`     |

- Cancel types (`*_ccl`) have **no sound cue** and use red `FF0000`.
- Objective toasts default to a `nDuration` of `5` seconds and `bClearBuffer = true` in `DisplayObjectiveMessage`.

## Module constants & tunables

- **Boundary line-region color: black, alpha `160`** — `NetClientAddBoundary` renders mission-boundary lines as
  `(0,0,0)` at alpha `160` on both the radar and PDA map.
- **Radar objective net-sync defaults** (`Radar:AddObjective`, server path): position `(0,2,0)`, color
  `(255,255,0)` (yellow), size `3×3`, sort order `5`, when the corresponding `tArgs` field is omitted.
- **Sonar/size/alpha animation defaults** (`Radar:AnimateObjectiveSonar`/`Size`/`Alpha`): sonar `4` total blips /
  `1` visible, grow speed `5`; size `2→6` over `2`s; alpha `0→1` over `1`s at speed `0.5`. These are the fallback
  values when you call the animate methods with a bare `sName`.
- **PDA blip default faction: `"PMC"`** and default sort order `5` (`Map:AddBlip`).
- **ClassyText defaults:** vertical position `240`, duration `3`s (always horizontally recentered — see
  `Hud.ClassyText:ShowText` above).

## Notes for modders



- **`_G.Hud` and `_G.Pda` are this module.** `import("MrxGuiInterface")` isn't the usual access path — the file
  publishes itself as the globals `Hud` and `Pda` (also `oPda`), so mission/HUD code just writes
  `Hud.MessageBox:AddMessage{...}` or `Pda.Database:AddLogEntry{...}` directly. Note these are the *resident-module*
  `Hud`/`Pda` tables, distinct from the engine `Hud` namespace used for `Hud.EventFanfare:Commence` in the
  [snippets](../snippets) — that engine `EventFanfare` path is served by
  [`MrxGuiHudMessage`](mrxguihudmessage), which this module also wraps.
- **Almost every method takes one `tArgs` table**, not positional arguments, and is `vPlayer`-aware: pass a single
  player guid, a table of guids, or omit `vPlayer` to target every player who currently owns a widget of that name
  (`_GetWidgetsForPlayers`). Omitting `vPlayer` on a client is the norm for local HUD updates.
- **Server/client split:** methods that mutate shared state (`Radar:AddObjective`, `ObjectiveTray:SetSlotTo*`,
  `FactionDisplay:SetValue`/`StartPursuit`/`HideMeter`, `Map:AddBlip`) net-sync from the server unless you pass
  `bDontNetSync = true`. `FactionDisplay:SetValue`/`StartPursuit`/`HideMeter` are additionally *ignored on a client*
  unless `bForceOnClient = true`. The `NetClient*` functions are the receiving side — don't call them yourself.
- **`RemoveMeter`/`RemoveAllMeters` are empty stubs** (`FactionDisplay:RemoveMeter`/`RemoveAllMeters` have no body);
  use `HideMeter` to take a faction gauge off screen.
- **`_GetWidgetsForPlayers` is the choke point** for every method here — if a HUD update silently does nothing,
  the widget of that exact name (`"Minimap"`, `"MessageBox"`, `"Objective Tray"`, `"PDA"`, `"Faction Display"`,
  `"money"`/`"fuel"`, `"ClassyText"`, …) probably isn't loaded/owned yet for that player.
- **Decompiler artifacts:** a few `NetClient*` helpers have locals that are assigned but never read, and some
  handlers reference a bare `vPlayer`/`tPlayer` that doesn't match the `tArgs.vPlayer` parameter (e.g.
  `Announcement:Show`, `Tutorial:ShowTutorial*`) — these are decompilation glitches, not intended behavior.