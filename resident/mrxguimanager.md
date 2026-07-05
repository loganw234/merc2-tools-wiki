---
title: MrxGuiManager
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
---

# MrxGuiManager

*Module: mrxguimanager.lua*

## Overview
The `MrxGuiManager` module is responsible for managing the creation, duplication, and lifecycle of various GUI layouts in the game. It handles the loading of master copies of HUD, binoculars, satellite, and PDA layouts, then duplicates these layouts per player. The module also manages the visibility state of the HUD through a sleep/visibility stack and routes events related to the satellite overlay.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGui`, `MrxUtil_Shell`

## Instance pattern
This is a stateless manager/utility module. It does not follow the per-instance object pattern but manages global state for GUI layouts and player-specific GUI instances.

## Functions
### `Init()`
**Not previously documented** — resets the module's four tracking tables (`_tPlayerGuiList`,
`_tPendingList`, `_tHudStates`, `_tPendingHudWidgets`) to empty. Standard lifecycle reset, not something a
mod would normally call directly.

### `CreateGui(uPlayerGuid)`
Called when a new player's GUI needs to be created. Loads master copies of GUI layouts if they haven't been loaded yet, then duplicates these layouts for the given player. Assigns ownership of these layouts to the player and initializes them. If the local player is creating their GUI, it caches certain widgets like `MessageBox`, `Minimap`, `ObjectiveTray`, `SubtitleBuffer`, and `MapLabel`.

### `ToggleHud(uPlayerGuid, bEnable, sContext)`
Toggles the visibility state of the HUD for a given player. Uses a refcounted sleep/visibility stack (`nHudState`) to manage when widgets should be shown or hidden. Context-specific logic is applied to selectively wake specific widgets based on the context (e.g., "briefing", "hijack").

### `_DetoggleWidget(sName, uOwner)`
Private function that wakes up a single widget by name and owner.

### `_DetoggleWidgetRecursive(sName, uOwner)`
Private function that recursively wakes up a widget and all its children by name and owner.

### `_RecursiveWakeup(oWidget)`
Private recursive function that sets a widget and all its children to be awake (not sleeping).

### `GetHudState(uPlayerGuid)`
Returns the current visibility state of the HUD for a given player.

### `AddWidgetToHud(uPlayerGuid, oWidget, bIncludeChildren)`
Adds a widget to the HUD for a given player. If the widget has children and `bIncludeChildren` is true, it recursively adds all children as well.

### `RemoveWidgetFromHud(uPlayerGuid, oWidget, bRemoveChildren)`
Removes a widget from the HUD for a given player. If the widget has children and `bRemoveChildren` is true, it recursively removes all children as well.

### `ToggleSatellite(uPlayerGuid, bEnable, sType, bSuppressMinigame)`
Toggles the satellite overlay state for a given player. Sets up callbacks for map mode changes and sends events to update the satellite progress and state.

### `ApplySatelliteUpdateEvent(uPlayer, nX, nY, nZ, nPercent)`
Private function that sends an event with updated satellite progress information.

### `DoNothing()`
A no-op function used as a placeholder callback.

### `SetSatelliteSuccessCallback(uPlayer, fCallback, tData)`
Sets the success callback for the satellite minigame. This callback is triggered when the satellite designation is successful.

### `SetSatelliteMinigameData(uPlayer, tData)`
Sets the data for the satellite minigame sectors.

### `SetSatelliteCost(uPlayer, nCost)`
Sets the cost of the satellite minigame.

### `DeleteGui(uPlayerGuid)`
Deletes the GUI for a given player by removing and deleting all widgets associated with that player's layouts.

### `DeleteAllGuis()`
Deletes the GUI for all players by calling `DeleteGui` for each player in the list.

### `SetLoadingCompleteCallback(fFunc, tData)`
Sets a callback function to be called when all GUIs have been loaded. If there are already loaded GUIs, it calls the function immediately; otherwise, it stores the callback and data for later use.

### `HudLoaded(oHudModule)`
Called when the HUD layout is loaded. Sets up the master HUD layout.

### `ScopeLoaded(oScopeModule)`
Called when the binoculars (scope) layout is loaded. Sets up the master scope layout.

### `SatelliteLoaded(oSatelliteModule)`
Called when the satellite layout is loaded. Sets up the master satellite layout.

### `PdaLoaded(oPdaModule)`
Called when the PDA layout is loaded. Sets up the master PDA layout.

### `_SetupMasterLayouts(oHud, oSatellite, oScope, oPda)`
Private function that sets up the master copies of GUI layouts once they are all loaded.

### `_AllRequiredModulesLoaded()`
Private function that checks if all required GUI modules have been loaded.

### `_RemoveAndDeleteWidgets(tLayout)`
Private function that removes and deletes all widgets in a given layout.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for custom event `HideMarker` to remove objectives for hidden objects.

## Notes for modders
- Ensure that `CreateGui` is called appropriately to create and initialize player GUIs.
- Use `ToggleHud` to control the visibility of the HUD for players.
- Customize widget behavior by adding or removing widgets using `AddWidgetToHud` and `RemoveWidgetFromHud`.
- Manage satellite overlay state with `ToggleSatellite`, setting callbacks and data as needed.
- Be aware that network synchronization (`bNetSync`) may affect multiplayer behavior.