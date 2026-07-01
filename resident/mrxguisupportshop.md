---
title: MrxGuiSupportShop
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, support]
---

# MrxGuiSupportShop

*Module: mrxguisupportshop.lua*

## Overview
The `MrxGuiSupportShop` module is responsible for managing the in-game support shop interface. It handles both a Flash-based graphical user interface (GUI) and a fallback dialog box if the Flash file is unavailable. The module manages adding items to the shop, setting callbacks for various events, and handling the opening and closing of the shop interface.

## Inheritance
- Inherits from: `none` — base/utility module
- Imports: `MrxGui`, `MrxGuiBase`, `MrxPmc`, `MrxSupportData`, `MrxGuiDialogBox`, `MrxGuiManager`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but maintains a list of active shops (`_tShopList`) keyed by player GUID.

## Functions
### `Create(uPlayerGuid)`
Instantiates a new Flash widget for the support shop and sets up its initial properties. If the Flash file is available, it loads the SWF file; otherwise, it falls back to a dialog box. Returns `true` on success, `false` otherwise.

### `AddItem(uPlayerGuid, sName, nCashCost, nCurrentStock, nMaxStock, bUnlocked, sId, bFuelTank, nFuelQuantity, sRawName)`
Adds an item to the support shop for a specific player. Returns `true` on success, `false` otherwise.

### `_AddItemWidget(oFlash, sName, nCashCost, nCurrentStock, nMaxStock, bUnlocked, sId, bFuelTank, nFuelQuantity, sRawName)`
Internal function to add an item to the Flash widget's custom data. Returns `true` on success, `false` otherwise.

### `AddItemFull(uPlayerGuid, sName, sDesc, sTexture, nCashCost, nCurrentStock, nMaxStock, bUnlocked, sId, bFuelTank, bMarkAsNew, nFuelQuantity, sRawName)`
Adds a full item with additional details to the support shop for a specific player. Returns `true` on success, `false` otherwise.

### `_AddItemFullWidget(oFlash, sName, sDesc, sTexture, nCashCost, nCurrentStock, nMaxStock, bUnlocked, sId, bFuelTank, bMarkAsNew, nFuelQuantity, sRawName)`
Internal function to add a full item to the Flash widget's custom data. Returns `true` on success, `false` otherwise.

### `SetCallback(uPlayerGuid, fCallback, tCallbackData)`
Sets a callback function for when an item is bought in the support shop. Returns `true` on success, `false` otherwise.

### `_SetCallbackWidget(oFlash, fCallback, tCallbackData)`
Internal function to set the callback data for the Flash widget. Returns `true` on success, `false` otherwise.

### `SetCloseCallback(uPlayerGuid, fCallback, tCallbackData)`
Sets a callback function for when the support shop is closed. Returns `true` on success, `false` otherwise.

### `_SetCloseCallbackWidget(oFlash, fCallback, tCallbackData)`
Internal function to set the close callback data for the Flash widget. Returns `true` on success, `false` otherwise.

### `Commence(uPlayerGuid)`
Starts the support shop interface for a specific player. If the Flash file is loaded, it runs the shop; otherwise, it creates a dialog box.

### `_CommenceWidget(oFlash)`
Internal function to commence the support shop interface in the Flash widget.

### `Close(uPlayerGuid)`
Closes the support shop interface for a specific player. Cleans up resources and calls any close callback functions.

### `_FlashLoadedCallback(oFlashWidget)`
Handles the event when the Flash file is loaded. Pauses the widget and runs the shop if it was previously running.

### `_RunShop(oFlashWidget)`
Runs the support shop interface, either in Flash or as a dialog box, depending on the availability of the Flash file.

### `_CreateShopDialogBox(oFlash)`
Creates a fallback dialog box for the support shop if the Flash file is unavailable. Color-codes items by affordability and displays them to the player.

### `_CloseShopDialogBox(oFlash, nSelectedIndex)`
Handles the event when an item is selected in the dialog box. Calls the callback function if an item is bought and cleans up resources.

### `_SetupShopFlash(oFlash)`
Sets up the Flash widget with shop items, stockpile information, and equipped support items. Registers event handlers for buying items, equipping support, and closing the store.

### `_FlashSupportBoughtCallback(oFlash, sArg)`
Handles the event when an item is bought in the Flash interface. Parses the buy event and calls the appropriate callback function.

### `_FlashSupportEquippedCallback(oFlash, sData)`
Handles the event when a support item is equipped in the Flash interface. Updates the PDA with the new equipment.

### `_ParseString(sData)`
Parses a string to extract slot and identifier numbers. Used internally by `_FlashSupportEquippedCallback`.

### `_FlashCloseShopCallback(oFlash, sArg)`
Handles the event when the support shop is closed in the Flash interface. Cleans up resources and calls any close callback functions.

### `_RemoveFlashFile(oFlash)`
Removes the Flash file and associated background widget from the GUI. Restores the HUD if it was previously hidden.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for custom event `HideMarker` to remove objectives for hidden objects.

## Notes for modders
- Ensure that `Create`, `AddItem`, and `Commence` are called appropriately to manage the shop lifecycle.
- Customize shop items by adding them with `AddItem` or `AddItemFull`.
- Set callbacks using `SetCallback` and `SetCloseCallback` to handle item purchases and store closures.
- Be aware that the Flash-based interface may require specific ActionScript callbacks to function correctly.