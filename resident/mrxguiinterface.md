---

title: MrxGuiInterface

parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1


inherits: none

tags: [gui, hud]

---



# MrxGuiInterface



*Module: mrxguiinterface.lua*



## Overview

The `MrxGuiInterface` module is a comprehensive interface for managing various aspects of the game's user interface (UI), including the Heads-Up Display (HUD) and the Personal Digital Assistant (PDA). It provides functionalities to manipulate UI elements such as radar objectives, message boxes, support menus, objective trays, map labels, announcements, fanfares, cinematic movies, faction displays, shops, and PDA database entries. The module ensures that these UI components are synchronized across clients in a multiplayer environment.



## Inheritance

- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`, `MrxGuiHudMessage`, `MrxGuiSupportShop`, `MrxGuiTutorial`, `MrxGuiHudFactionGauge`, `MrxTaskObjective`, `MrxUtil`, `MrxBootstrap`, `WifMissionData`, and `MrxSoundCategories`



## Instance pattern

This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:

- **HudInterface**: Exposed as `_G.Hud` and contains sub-tables like `Radar`, `MessageBox`, `SupportMenu`, `ObjectiveTray`, etc.

- **PdaInterface**: Exposed as `_G.Pda` and manages PDA-related functionalities such as support items, faction attitudes, log entries, help entries, dossier entries, statistic categories, and statistic entries.



The module also maintains internal state for fanfare queues, subtitle buffers, and other UI components. It ensures that all UI updates are synchronized across clients to maintain a consistent user experience in multiplayer scenarios.

```



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



- **Event.ObjectiveAdded**: Triggered when an objective is added to the radar. Listens for this event to call `HudInterface.Radar:AddObjective`.

- **Event.ObjectiveUpdated**: Triggered when an existing objective on the radar is updated. Listens for this event to call `HudInterface.Radar:UpdateObjective`.

- **Event.ObjectiveRemoved**: Triggered when an objective is removed from the radar. Listens for this event to call `HudInterface.Radar:RemoveObjective`.

- **Event.MessageAdded**: Triggered when a message is added to the message box. Listens for this event to call `HudInterface.MessageBox:AddMessage`.

- **Event.MessageModified**: Triggered when an existing pending message in the message box is modified. Listens for this event to call `HudInterface.MessageBox:ModifyPendingMessage`.

- **Event.MessageRemoved**: Triggered when a pending message is removed from the message box. Listens for this event to call `HudInterface.MessageBox:RemovePendingMessage`.

- **Event.MapLabelAdded**: Triggered when a map label is added. Listens for this event to call `HudInterface.MapLabel:Show`.

- **Event.AnnouncementShown**: Triggered when an announcement message is shown. Listens for this event to call `HudInterface.Announcement:Show`.

- **Event.FanfareCompleted**: Triggered when a fanfare completes. Listens for this event to call `_tFanfareQueue:FinishItem`.

- **Event.CinematicStarted**: Triggered when a cinematic movie starts. Listens for this event to call `HudInterface.Cinematic:Show`.

- **Event.CinematicStopped**: Triggered when a cinematic movie stops. Listens for this event to call `HudInterface.Cinematic:Hide`.



## Notes for modders



1. **Call-order requirements**:

   - Ensure that `Init()` is called during the module initialization phase to set up global functions like `TestFlash` and `EndFlashTest`.

   - Functions such as `AddObjectiveToLocalPlayer`, `AddPdaBlipToLocalPlayer`, and `DeletePdaBlipForLocalPlayer` should be called after the player's PDA widget has been initialized.



2. **Pitfalls**:

   - Be cautious with network synchronization functions like `NetClientSetObjectiveTraySlot` and `NetClientFactionSetValue`. Ensure that these are only called on the server to avoid duplication or inconsistencies.

   - When modifying or adding items in the PDA interface, ensure that the widget is properly initialized before making changes.



3. **Tunables**:

   - The duration of fanfare messages can be adjusted by modifying parameters like `nSlowdownDuration` and `nDisplayTime`.

   - Adjusting the fade-in and fade-out times for cinematic movies can enhance visual effects.



4. **Decompiler artifacts**:

   - Some local variables in functions like `NetClientSetObjectiveTraySlot` and `NetClientFactionSetValue` may appear unused or assigned but never read, which is a decompiler artifact.

   - The function `_GetWidgetsForPlayers` has duplicate table keys in some cases, with the last one winning at runtime. This should not affect functionality but should be noted for clarity.