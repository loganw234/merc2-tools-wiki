---
title: MrxGuiPda
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, pda]
verified: true
verified_note: 'deeper pass: rewrote Events (removed invented Event.ObjectHibernation/Event.PlayerInput; documented the real Event.CreatePersistent(mpPlayerJoin), the 6 Event.Post signals, Event.Create timers, and Net.SendCustomEvent net-events); added movie names (topbar, landingzones), assets (pda_titles), _knBlipLimit=5000, nLogSize=100, the _ksTypeAddFunc/_tPrefix/_tFactionNameLookup tables, and the flash-callback wiring'
---

# MrxGuiPda

*Module: mrxguipda.lua*

## Overview
The `MrxGuiPda` module is responsible for managing the Player Data Assistant (PDA) interface in the game. It handles various PDA operations such as opening and closing the PDA, managing map blips, missions, support items, and database entries. The module also interacts with other modules like `MrxGuiBase`, `MrxPmc`, and `MrxSupportData` to update and display relevant information.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [MrxGuiBase](mrxguibase), [MrxPmc](mrxpmc), [MrxGuiManager](mrxguimanager), `WifVzRegionNames`, [MrxSupportData](mrxsupportdata), [MrxGuiDialogBox](mrxguidialogbox), [MrxSound](mrxsound), [MrxPlayState](mrxplaystate), `WifMissionData`, [MrxGuiHudFactionGauge](mrxguihudfactiongauge), [MrxStatsManager](mrxstatsmanager), [MrxState](mrxstate), and [MrxGui](mrxgui)

## Module constants & assets (high-value knobs)
- **Scaleform movies**: the PDA itself is the movie `"topbar"` (`oMapFlash.CustomData.sFile = "topbar"`); the deploy/transit picker is a separate movie `"landingzones"` loaded by `OpenTransitInterface`.
- **Texture assets** preloaded on init: `Pg.LoadAsset("pda_titles", "texture")`.
- `_knBlipLimit = 5000` — hard cap on map blips (`_PopulateMapDisplay` defaults to half of this when no limit is passed).
- `nLogSize = 100` — max message-log entries kept (`AddLogEntry` trims to this).
- `_ksTypeAddFunc` — maps a support `sType` to the movie's add callback: `Airstrike→AddSupportAirstrike`, `Civilian→AddSupportCivilian`, `Light→AddSupportLight`, `Heavy→AddSupportHeavy`, `Heli→AddSupportHelicopters`, `Boat→AddSupportBoats`, `Supply→AddSupportSupplies`.
- `_tPrefix` — icon-token prefix per support type (`Airstrike→"[airstrike] "`, `Light→"[vehmlight] "`, etc.) prepended to the display name.
- `_tFactionNameLookup` (built in `Init`) — faction code → localized-name token: `AN`,`PR`,`OC`,`GR`,`CH`,`VZ`,`PMC`.
- **Sound cues**: open `"ui_PDA_Open_01_st"` (played 0.5 s after open via a timer), close `"ui_PDA_Close_01_st"`.
- **Net-event ids**: `NETEVENT_SETSELECTEDMISSION = 0`, `NETEVENT_PDAOPEN = 1`, `NETEVENT_PDACLOSE = 2` (used with `Net.SendCustomEvent("MrxGuiPda", ...)`).
- Backdrop: full-screen black `ImageWidget` at alpha `192`.

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: only a one-time `Init()` setup function, no
`OnActivate`/`Create`/`tInstance` registry anywhere in source. This is the one shared PDA interface, not
something spawned per world object. Key fields:
- `_knBlipLimit`: A limit for the number of map blips.
- `_nMissionCount`: A counter for mission IDs.
- `tMapBlips`: Table to store map blips.
- `tMissions`: Table to store missions.
- `tSupportItems`: Table to store support items.
- `tLogEntries`: Table to store log entries.
- `tDossierEntries`: Table to store dossier entries.
- `tHelpEntries`: Table to store help entries.
- `tStatisticCategories`: Table to store statistic categories.
- `tStatisticEntries`: Table to store statistic entries.
- `bActive`: Indicates whether the PDA is currently active.
- `bSuppressed`: Indicates whether the PDA is suppressed.
- `bCooldown`: Indicates whether the PDA is in cooldown mode.
- `nCooldownFrames`: Counter for cooldown frames.
- `oFlash`: Reference to the Flash object used for rendering the PDA interface.

## Functions

### NetEventCallback(nEventType, tArgs)
Handles network events related to PDA operations. It logs the event type and processes it accordingly:
- `NETEVENT_SETSELECTEDMISSION`: Sets the selected mission in the PDA.
- `NETEVENT_PDAOPEN`: Posts an event for PDA opening.
- `NETEVENT_PDACLOSE`: Posts an event for PDA closing.

### _PlayDelayedOpenSound(oPda)
Plays a sound when the PDA is opened, if it is active.

### _SetupDelayedOpenSound(fDelay, oPda)
Sets up a timer to play a delayed open sound for the PDA.

### Open(oPda)
Opens the PDA and sets up its various components:
- Checks conditions like whether the PDA is already active or has flash content.
- Handles mission changes and support menu closing.
- Sets up map display, support display, and database display.
- Manages HUD state and player widget settings.
- Posts events for PDA opening and sends network messages if applicable.

### Close(oPda)
Closes the PDA and cleans up its components:
- Unregisters from PDA updates.
- Releases control focus and sets visibility to false.
- Removes widgets and restores HUD state.
- Handles map blips and missions.
- Posts events for PDA closing and sends network messages if applicable.

### _FinishPdaReload(oPda)
Finishes the PDA reload process by calling `_FinishLoad` and resetting some properties.

### _PdaCooldown(oPda)
Handles the cooldown period after the PDA is closed, decrementing the cooldown frames until it reaches zero.

### SetSuppressed(oPda, bSuppress)
Sets or clears the suppression state of the PDA. If suppressed, it closes the PDA if it is active.

### AddMapBlip(oPda, sName, nX, nY, sLabel, sDesc, uGuid, sTexture, sMission, nMeter, bSticky, bTodoList, sFaction, nSortOrder)
Adds a map blip to the PDA with specified properties.

### RemoveMapBlip(oPda, sName)
Removes a map blip from the PDA by name.

### AddMapMission(oPda, sName, sLabel, sDesc, sFaction, sDefaultBlipTexture, sDefaultBlipLabel, bSuppress, bTrackable, nSortOrder)
Adds or updates a mission in the PDA with specified properties.

### RemoveMapMission(oPda, sName)
Removes a mission from the PDA by name and associated map blips.

### UpdateMapMission(oPda, sName, sLabel, sDesc, sFaction, sDefaultBlipTexture, sDefaultBlipLabel, bSuppress, nSortOrder)
Updates an existing mission in the PDA with new properties.

### SetMissionTrackable(oPda, sName, bTrackable)
Sets whether a mission is trackable in the PDA.

### AddLineRegion(oPda, uRegionGuid, nRed, nGreen, nBlue, nAlpha, bInvert)
Adds or updates a line region with specified color and properties.

### _Clamp(n, nMin, nMax)
Clamps a number to be within a specified range.

### RemoveLineRegion(oPda, uRegionGuid)
Removes a line region by its GUID.

### SetSelectedMission(oPda, sName, bForceOnClient)
Sets the selected mission in the PDA. If `bForceOnClient` is true, it forces the change on the client side.

### GetSelectedMission(oPda)
Retrieves the currently selected mission from the PDA.

### SetMissionTrackCallback(oPda, fCallback, tCallbackData)
Sets a callback function for mission changes and associated data.

### SetMissionChangeAllowed(oPda, bAllow)
Sets whether mission changes are allowed on the client side.

### SetFakePlayerLocation(oPda, nX, nY, nZ)
Sets a fake player location in the PDA.

### SetBeaconTutorialMode(oPda, bBeaconTutorialMode)
Sets the beacon tutorial mode for the PDA.

### `_PopulateMapDisplay(oPda, oFlash, bCleanup, nBlipLimit, bHideTertiary)`
- **Description**: Populates the PDA map display with various blips and markers.
- **Parameters**:
  - `oPda`: The PDA object.
  - `oFlash`: The Flash object for rendering the map.
  - `bCleanup` (optional): Boolean indicating whether to perform cleanup operations. Defaults to `true`.
  - `nBlipLimit` (optional): Maximum number of blips to display. If not provided, defaults to half of `_knBlipLimit`.
  - `bHideTertiary` (optional): Boolean indicating whether to hide tertiary blips. Defaults to `false`.

### `_MissionSortLessThan(tMission1, tMission2)`
- **Description**: Compares two missions based on their sort order.
- **Parameters**:
  - `tMission1`: The first mission table.
  - `tMission2`: The second mission table.

### `HandleBeaconCheck(oFlash, sArgs)`
- **Description**: Handles beacon check events by verifying player position and updating the flash UI accordingly.
- **Parameters**:
  - `oFlash`: The Flash object for rendering the map.
  - `sArgs`: String containing arguments related to the beacon check.

### `_DisplayRegions(oPda, nXOffset, nYOffset)`
- **Description**: Displays regions on the PDA map.
- **Parameters**:
  - `oPda`: The PDA object.
  - `nXOffset` (optional): X offset for region display. Defaults to `0`.
  - `nYOffset` (optional): Y offset for region display. Defaults to `0`.

### `_DisplayRegion(oFlash, uRegion, nId, sColor, nAlpha, nXOffset, nYOffset, bInvert)`
- **Description**: Displays a single region on the PDA map.
- **Parameters**:
  - `oFlash`: The Flash object for rendering the map.
  - `uRegion`: GUID of the region to display.
  - `nId`: Unique identifier for the region.
  - `sColor`: Color of the region.
  - `nAlpha`: Alpha transparency of the region.
  - `nXOffset` (optional): X offset for region display. Defaults to `0`.
  - `nYOffset` (optional): Y offset for region display. Defaults to `0`.
  - `bInvert`: Boolean indicating whether to invert the region.

### `_HandleTrackEvent(oMapFlash, sId)`
- **Description**: Handles track events by setting the selected mission and invoking a callback if available.
- **Parameters**:
  - `oMapFlash`: The Flash object for rendering the map.
  - `sId`: Identifier of the mission to track.

### `_HandleUntrackEvent(oMapFlash, sMission)`
- **Description**: Handles untrack events by clearing the selected mission and invoking a callback if available.
- **Parameters**:
  - `oMapFlash`: The Flash object for rendering the map.
  - `sMission`: Identifier of the mission to untrack.

### `_HandleMissionCancel(oFlash, sUnused)`
- **Description**: Handles mission cancellation by canceling the current mission.
- **Parameters**:
  - `oFlash`: The Flash object for rendering the map.
  - `sUnused`: Unused parameter.

### `HandleMarkerUpdate(oPda, tEvent)`
- **Description**: Updates the marker position on the PDA map and posts an event.
- **Parameters**:
  - `oPda`: The PDA object.
  - `tEvent`: Event data containing the new marker position.

### `HandleMarkerClear(oPda, tEvent)`
- **Description**: Clears the marker position on the PDA map and posts an event.
- **Parameters**:
  - `oPda`: The PDA object.
  - `tEvent`: Event data containing the cleared marker position.

### `OpenTransitInterface(oPda, tZones, fCallback, tCallbackData)`
- **Description**: Opens the transit interface for managing landing zones.
- **Parameters**:
  - `oPda`: The PDA object.
  - `tZones`: Table of landing zone data.
  - `fCallback`: Callback function to be invoked upon completion.
  - `tCallbackData`: Data to pass to the callback function.

### `_FinishTransitInterfaceLoad(oTransit, oParentPda, tZones)`
- **Description**: Finishes loading the transit interface by populating it with blips and setting up event handlers.
- **Parameters**:
  - `oTransit`: The transit interface object.
  - `oParentPda`: The parent PDA object.
  - `tZones`: Table of landing zone data.

### `_LandingZoneLessThan(tData1, tData2)`
- **Description**: Compares two landing zones based on their sort order.
- **Parameters**:
  - `tData1`: The first landing zone data table.
  - `tData2`: The second landing zone data table.

### `_RemoveTransitInterface(oPda)`
- **Description**: Removes the transit interface and cleans up associated resources.
- **Parameters**:
  - `oPda`: The PDA object.

### _RemoveTransitInterfaceDelayed(oTransit)
Removes the transit interface by setting its SWF file to `nil` and deleting it.

### _InvokeCallbackSuccess(oTransit, sNumber)
Posts an event for a successful transit interface interaction. Invokes the callback with success status.

### _InvokeCallback(oSelf, sNumber, bSuccess)
Invokes a callback function stored in `oSelf.CustomData.fCallback`, passing the success status and number along with any additional data.

### AddSupport(oPda, tData, sKey)
Adds support to the PDA. If the support already exists, it updates it instead. Assigns a unique ID to the new support and inserts it into ordered lists.

### RemoveSupport(oPda, sName)
Removes support from the PDA by name. Updates related data structures and removes items from the equipped support list if necessary.

### UpdateSupport(oPda, tData)
Updates existing support in the PDA with new data. Returns `true` if successful, otherwise `false`.

### GetStockpile(oPda, sName)
Retrieves the stockpile quantity of a specific support item using `MrxPmc.GetSupportQty`.

### _PopulateSupportDisplay(oPda)
Populates the support display in the PDA by calling action script callbacks with support data. Updates stockpile and support data, then iterates through ordered support items to add them to the display.

### _UpdateSupportData(oPda)
Updates support data by iterating through `MrxSupportData.tSupportData` and adding or updating support entries in the PDA.

### _ShowUnusableSupportMessage(oFlash, sArg)
Handles the event of an unusable support item. Displays a message indicating why the support cannot be equipped.

### _HandleEquipEvent(oFlash, sData)
Handles the equip event by parsing the data, updating the equipped support list, and adding or removing items from the support menu accordingly.

### _ParseString(sData)
Parses a string to extract a slot number and an ID. Returns `nil` if parsing fails.

### _HandleUnequipEvent(oFlash, sUnused)
Handles the unequip event (currently empty).

### _GetEquippedSupport(oPda, nSlot)
Retrieves the equipped support item and its icon for a given slot.

### _SetEquippedSupport(oPda, sName, nSlot)
Sets the equipped support item for a given slot. Updates the support menu and related data structures.

### ReadEquippedSupport(oPda)
Reads and returns the currently equipped support items as an array.

### RestoreEquippedSupport(oPda, tSupportData)
Restores equipped support items silently using `_EquipItemSilent`.

### _EquipItemSilent(oPda, nSlot, sName)
Equips a support item silently by updating the support menu and related data structures without triggering network synchronization.

### SetFactionAttitude(oPda, sFaction, sIcon, nAttitude)
Sets or updates the faction attitude for a given faction. If `nAttitude` is negative, it removes the faction's attitude entry.

### AddLogEntry(oPda, sType, sName, sMessage, sColor)
Adds a log entry to the PDA with specified type, name, message, and color. Limits the log size to 100 entries.

### AddDossierEntry(oPda, sTitle, sText, sIcon)
Adds or updates a dossier entry in the PDA with specified title, text, and icon.

### AddHelpEntry(oPda, sTitle, sText, sIcon)
Adds or updates a help entry in the PDA with specified title, text, and icon.

### AddStatisticCategory(oPda, sCategoryName, sIcon)
Adds a new statistic category to the PDA with specified name and icon.

### AddStatisticEntry(oPda, sCategoryName, sText, sData)
Adds or updates a statistic entry in the PDA with specified category, text, and data.

### _UpdateStatisticEntry(oPda, sText, sData)
Updates an existing statistic entry's data.

### _PopulateDatabaseDisplay(oPda)
This function populates the PDA database display by calling various ActionScript callbacks on `oFlash` with different data. It checks online status, multiplayer roles, active profile, faction attitudes, log entries, and other categories of data.

### _Initialize(oPda)
Initializes the PDA widget: sets up `CustomData` tables, creates the black backdrop, adds the `"topbar"` map `FlashWidget`, binds the public methods (see Notes), seeds support from `MrxSupportData.tSupportData`, subscribes `mpPlayerJoin`, and loads the `"pda_titles"` texture. Loads the movie with `_FinishLoadAndClose` (so the PDA starts closed).

{: .warning }
> `_Initialize` binds three methods to functions that **don't exist in this file**: `oPda.SetMissionSticky = SetMissionSticky`, `oPda.SetMarker = SetMarker`, and `oPda.UpdateStatisticEntry = UpdateStatisticEntry`. No such top-level functions are defined here, so those three fields resolve to `nil` and calling e.g. `oPda:SetMarker(...)` would error. (The related real functions are `HandleMarkerUpdate`/`HandleMarkerClear` for markers and `_UpdateStatisticEntry`/`AddStatisticEntry` for stats.) Same dangling-binding pattern as [MrxGuiGarage](mrxguigarage)'s `SetCloseCallback`.

### SendPlayerJoinEvents()
Sends player join events to the server if the current player is the local player. It logs debug information and sends a custom network event with the selected mission index.

### _FinishLoad(oPda)
Finishes loading the PDA by setting up Flash event handlers for various interactions like tracking blips, canceling contracts, equipping/unequipping items, closing the PDA, changing pages, and updating support quick slots.

### _FinishLoadAndClose(oPda)
Calls `_FinishLoad` to finish loading the PDA and then closes it.

### AddPDATargetMarkers(oPda)
Adds target markers for players to the PDA map by iterating through all target marker positions, creating a blip table with relevant data, and adding these blips to the Flash widget.

### UpdatePDATargetMarkers(oPda)
Updates the target markers on the PDA map by iterating through all target marker positions, updating existing blips or removing them if they no longer exist.

### UpdatePlayerMarkers(oPda, uPlayerGuid, i)
Updates a player's marker on the PDA map. It calculates the player's position and rotation, retrieves mission data, and updates the blip with this information.

### UpdateAllPlayerMarkers(oPda)
Updates markers for all players on the PDA map by calling `UpdatePlayerMarkers` for each player. It also handles removing old markers if necessary.

### _HandlePDAUpdateEvent(oPda, nDeltaTime)
Handles periodic updates for the PDA, such as updating target and player markers every second. It also manages input handling to reset analog inputs after a certain number of frames without input.

### _HandleToggleEvent(oPda, tUnused)
Toggles the PDA's active state. If the PDA is active, it closes it; otherwise, it opens it unless another control holder (like the Support Menu) has focus.

### \_HandleInput(oPda, tInput)
This function handles input events for the PDA. It checks if the map mode is active and processes analog stick inputs to control the map's tessellation and movement. If the left analog stick is used, it updates the map's position based on the input values. The function also calls the `ControllerInput` event handler of the map.

### IsAnalog(nValue)
This utility function checks if a given value corresponds to an analog button press by comparing it against predefined joystick button constants for the left and right sticks.

### \_HandleCloseEvent(oMapFlash)
This function handles the close event for the PDA's map flash. It retrieves the parent widget (PDA) and closes it.

### \_HandlePageChangeEvent(oMapFlash, sArg)
This function manages page changes in the PDA's map interface. If the argument is "Map", it sets the map mode to active. Otherwise, it resets the input frame counter and handles left analog inputs to reset the map position.

### \_HandleMapLocationEvent(oMapFlash, sData)
This function processes location data received from the map. It parses the data to extract coordinates, checks if these points are within defined boundaries, and updates the current point of interest (POI) accordingly. If no valid boundary is found, it defaults to "Venezuela".

### Init()
This initialization function sets up global state for the PDA module. It determines whether exiting the PDA on left button press should be enabled based on a configuration check. It also initializes a table `_tFactionNameLookup` that maps faction codes to their corresponding names.

### \_LTIupdateSupportQuickSlot(oFlash, sParm)
This function updates the quick support slot in the PDA's support menu by calling a library function `LTILibName.LTIupdateSupportQuickSlot`.

### EnableQuickSlot(sId)
This function enables a quick support slot in the PDA. It retrieves the PDA widget and the support menu widget, removes any currently equipped support, and adds the new support based on the provided ID. If the support needs equipping, it creates a new support object, sets its properties, and triggers an animation to update the UI.

## Events

Distinguish four real mechanisms — the previous draft's `Event.ObjectHibernation` and `Event.PlayerInput` do **not** exist in this file:

**Real `Event.*` subscriptions (created here):**
- `Event.CreatePersistent(Event.ScriptEvent, {"mpPlayerJoin", <predicate>}, SendPlayerJoinEvents)` — in `_Initialize`, stored in the global `_evPlayerJoin`. Fires `SendPlayerJoinEvents` on the server when a non-local player joins, re-syncing the selected mission. This is the module's one persistent event subscription.

**Outbound `Event.Post` signals other systems can listen for:**
- `"PDA Open"` / `"PDA Close"` (payload `{uPlayer}`) — on open/close.
- `"GPS Beacon Set"` / `"GPS Beacon Cleared"` (`{nX, nY}`) — from `HandleMarkerUpdate`/`HandleMarkerClear`.
- `"Transit Interface Open"` / `"Transit Interface Success"` (`{uPlayer}`) — the deploy/landing-zone picker.

**Timers (`Event.Create(Event.TimerRelative, ...)`):**
- delayed open sound (`_SetupDelayedOpenSound`), the `NetEventCallback` retry-in-1s when the PDA widget isn't found yet, transit-interface deferred teardown (0.1 s), and the quick-slot ammo-counter animation (0.2 s).

**Multiplayer sync (`Net.SendCustomEvent("MrxGuiPda", NETEVENT_*, ...)`)** received back by `NetEventCallback`: `NETEVENT_SETSELECTEDMISSION`/`NETEVENT_PDAOPEN`/`NETEVENT_PDACLOSE`.

Everything else is widget-level: `oPda:SetEventHandler("ControllerInput", _HandleInput)` / `"GuiUpdate"` (`_HandlePDAUpdateEvent` while open, `_PdaCooldown` after close), and the many `oMapFlash:SetFlashEventHandler(...)` bindings (`TrackBlip`, `UntrackBlip`, `cancelContract`, `equip`, `unequip`, `closePDA`, `currentPage`, `LTIupdateSupportQuickSlot`, plus `beaconCheck`, `equipFailed`, and for transit `LandingZone`/`closeMap`).

## Notes for modders

- **Retheme is a movie edit.** Nearly the entire PDA is the `"topbar"` Scaleform movie (map, support tabs, database). Lua feeds it data through ActionScript callbacks (`AddStockpile`, the `AddSupport*` family, `AddPdaMapBlips` via `_GuiInternal`, `AddZone`, `AddFactionAttitude`, `AddDatabaseItem`, `addMessageLog`, `addStats`, `SetMarker`, `currentPOI`, `activeContract`, `onlineMessage`, `requestClose`, …) and receives the flash events listed above. Keep those entry points if you replace the movie.
- **Public per-widget API** (methods bound onto the `"PDA"` widget in `_Initialize`, callable as `oPda:Method(...)`): `Open`/`Close`/`SetSuppressed`, the map/mission set (`AddMapBlip`/`RemoveMapBlip`/`AddMapMission`/`RemoveMapMission`/`UpdateMapMission`/`SetSelectedMission`/`GetSelectedMission`/`SetMissionTrackable`/`SetMissionTrackCallback`/`SetMissionChangeAllowed`/`AddLineRegion`/`RemoveLineRegion`), support (`AddSupport`/`RemoveSupport`/`UpdateSupport`/`GetStockpile`/`GetEquippedSupport`/`SetEquippedSupport`/`ReadEquippedSupport`/`RestoreEquippedSupport`), the database (`SetFactionAttitude`/`AddLogEntry`/`AddDossierEntry`/`AddHelpEntry`/`AddStatisticCategory`/`AddStatisticEntry`), plus `SetFakePlayerLocation`, `SetBeaconTutorialMode`, `OpenTransitInterface`. Grab the widget with `MrxGuiBase.GetWidgetByNameAndOwner("PDA", uPlayer)`.
- **Blip coordinates are offset** by `nXOffset = 35`, `nZOffset = 40` before being handed to the movie (world Z maps to map Y). `AddMapBlip` accepts a `uGuid` to auto-follow an object's live position.
- **`AddLogEntry` silently drops** any `sType` that isn't `"dialog"`, `"objective"`, or `"event"`.
- **`SetMissionChangeAllowed` is forced off on clients** — on `Net.IsClient()` it always stores `false` regardless of the argument, since mission selection is server-authoritative (synced via `NETEVENT_SETSELECTEDMISSION`).
- **`_knBlipLimit` (5000)** caps blips; if a level exceeds it the *lowest* sort-order blips are dropped first (the list is built highest-priority-last and truncated from the front).
- **`_HandleMapLocationEvent` falls back to `"Venezuela"`** for the POI name when a point isn't inside any `WifVzRegionNames.tBoundaryList` region.