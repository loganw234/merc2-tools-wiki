---
title: MrxGuiBootstrap
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
---

# MrxGuiBootstrap

*Module: mrxguibootstrap.lua*

## Overview
The `MrxGuiBootstrap` module is responsible for initializing and managing the Scaleform GUI/HUD system in the game. It handles loading GUI files, creating and deleting player HUDs, toggling the visibility of the HUD, and setting up callbacks for GUI events.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGuiBase`, `MrxGui`, `MrxGuiManager`, `MrxUtil`, `MrxGuiShellBootstrap`, `MrxGuiInterface`

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state.

## Functions
### `Init()`
Called during the initialization phase of the game. Loads the pause screen GUI file and sets up a callback for when the pause screen is loaded. Also, sets an exit multiplayer callback function.

### `Deinit()`
Not implemented or used in this module.

### `_PauseScreenLoaded(PauseScreenModule)`
A private function called when the pause screen GUI file is successfully loaded. It closes the pause screen and stores the pause screen module for later use.

### `ToggleHud(uGuid, bVisible, sContext)`
Toggles the visibility of the HUD for a given player GUID (`uGuid`). The `bVisible` parameter determines whether to show or hide the HUD, and `sContext` provides additional context for the operation.

### `CreatePlayerHud(uPlayerGuid)`
Creates a new GUI for the specified player GUID (`uPlayerGuid`) using the `MrxGuiManager`.

### `DeleteHud(uPlayerGuid)`
Deletes the GUI associated with the specified player GUID (`uPlayerGuid`) using the `MrxGuiManager`.

### `DeleteAllHuds()`
Deletes all created GUIs using the `MrxGuiManager`.

### `GetNumberOfPlayersFromShellSelection()`
Returns the number of players selected in the shell (likely referring to the multiplayer selection screen).

### `SetSatelliteOverlay(uPlayer, bOn, sFaction)`
Toggles the satellite overlay for a given player (`uPlayer`). The `bOn` parameter determines whether to enable or disable the overlay, and `sFaction` specifies the faction associated with the overlay.

### `SetOnGuiLoadedFunc(fFunc, tArgs)`
Sets a callback function (`fFunc`) that will be called when the GUI is fully loaded. The `tArgs` table contains any arguments that need to be passed to the callback function.

## Events
- Listens for custom event `_PauseScreenLoaded` to handle pause screen loading.
- Sets an exit multiplayer callback using `MrxGuiShellBootstrap.SetExitMultiplayerCallback`.

## Notes for modders
- Ensure that `Init` and `Deinit` are called appropriately during the game's lifecycle.
- Use `ToggleHud`, `CreatePlayerHud`, and `DeleteHud` to manage player HUDs dynamically.
- Customize the GUI behavior by setting up appropriate callbacks using `SetOnGuiLoadedFunc`.
- Be aware that modifying the satellite overlay may affect multiplayer gameplay.