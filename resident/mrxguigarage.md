---
title: MrxGuiGarage
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, pda]
---

# MrxGuiGarage

*Module: mrxguigarage.lua*

## Overview
The `MrxGuiGarage` module is responsible for managing the garage screen in the game's user interface. It handles the creation, display, and interaction with the garage UI, including adding items to the garage list, setting callbacks for user actions, and managing the visibility of the garage screen.

## Inheritance
- Inherits from: `none`
- Imports: `MrxGui`, `MrxGuiBase`, `MrxPmc`, `MrxSupportData`, `MrxGuiDialogBox`, `MrxGuiManager`

## Instance pattern
This is a stateless manager/utility module. It does not follow the per-instance object pattern and instead manages garage screens for players through a global list `_tGarageList`.

## Functions
### `Create(uPlayerGuid)`
Creates a new garage screen instance for the specified player. Initializes the flash widget, sets its properties, and adds it to the global garage list.

### `AddItem(uPlayerGuid, sId, sName, sDescription, sType, nCurrentStock, nMaxStock, sIcon, bNew)`
Adds an item to the garage screen for the specified player. The item details include ID, name, description, type, stock quantities, icon, and a flag indicating if it's new.

### `_AddItemWidget(oFlash, sId, sName, sDescription, sType, nCurrentStock, nMaxStock, sIcon, bNew)`
Internal helper function to add an item widget to the flash object. Validates input types and inserts the item data into the custom data table of the flash widget.

### `SetCallback(uPlayerGuid, fCallback, tCallbackData)`
Sets a callback function for user actions in the garage screen for the specified player. The callback can be used to handle events like selecting a vehicle or closing the PDA.

### `_SetCallbackWidget(oFlash, fCallback, tCallbackData)`
Internal helper function to set the callback and associated data on the flash object. Validates the callback type and stores it in the custom data table of the flash widget.

### `Commence(uPlayerGuid)`
Starts the garage screen for the specified player. Initializes the garage UI by setting up the flash file, adding items, and handling user interactions.

### `_CommenceWidget(oFlash)`
Internal helper function to commence the garage screen. Sets a flag indicating that the garage is running and calls the internal function to run the garage if the flash file is loaded.

### `Init()`
Initializes the module by setting up the global garage list `_tGarageList`.

### `_FlashLoadedCallback(oFlashWidget)`
Internal callback function triggered when the flash file for the garage screen is loaded. Sets a flag indicating that the flash file is loaded and calls the internal function to run the garage if it was previously running.

### `_RunGarage(oFlashWidget)`
Internal helper function to run the garage screen. Sets up the flash widget with stockpile data, adds items based on their type, sets event handlers for user actions, and manages the visibility of the garage screen.

### `_SetupGarageFlash(oFlash)`
Sets up the flash widget for the garage screen by calling ActionScript callbacks to add stockpile data and items, setting event handlers for user interactions, and managing the background image.

### `_EndCallback(oFlash, sArg)`
Internal callback function triggered when a vehicle is selected in the garage screen. Ends the garage session by removing the flash file, releasing control focus, and calling the user-defined callback if set.

### `_CloseCallback(oFlash)`
Internal callback function triggered when the PDA is closed in the garage screen. Calls the end callback with no argument to handle the close action.

### `_RemoveFlashFile(oFlash)`
Internal helper function to remove the flash file for the garage screen. Restores the HUD state, removes the flash widget and background image from the UI, and deletes them.

## Events
- Listens for `Event.TimerRelative` to call `_RemoveFlashFile` after a delay when ending the garage session.

## Notes for modders
- Ensure that `Create`, `AddItem`, `SetCallback`, and `Commence` are called appropriately to manage the garage screen lifecycle.
- Customize the garage items by providing appropriate details when calling `AddItem`.
- Use `SetCallback` to handle user actions in the garage screen, such as selecting a vehicle or closing the PDA.
- Be aware that the module manages global state through `_tGarageList`, so ensure proper cleanup and initialization of this list.