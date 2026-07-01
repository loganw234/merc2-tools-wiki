---
title: MrxMultipageMenu
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, menu]
---

# MrxMultipageMenu

*Module: mrxmultipagemenu.lua*

## Overview
The `MrxMultipageMenu` module is responsible for managing a paginated menu system in the game's user interface. It allows adding options that can span multiple pages, providing navigation between them and handling callbacks when an option is selected.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGui`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `_tOptions`: A table of options that do not appear on every page.
- `_tOptionsOnEveryPage`: A table of options that appear on every page.
- `_tOptionsToCallbacks`: A mapping from option names to their associated callbacks and arguments.
- `_tPageOptions`: A temporary table used during menu display to store the current page's options.
- `_nPages`: The total number of pages required for all options.
- `_sCancelButtonOptionName`: The name of the option bound to the cancel button.

## Functions
### `_CallWithOptionalArgs(fFunction, tArgs)`
A helper function that calls a given function with optional arguments. If `tArgs` is provided, it unpacks and passes them; otherwise, it calls the function without arguments.

### `Init()`
Initializes the module by resetting all internal state tables and counters.

### `Reset()`
Resets the module to its initial state by calling `Init()`.

### `Close()`
Closes the current dialog box if one is open, changes the shell state to false, and clears the `_DialogBox` reference.

### `BindOptionToCancelButton(sOptionName)`
Binds a specified option name to the cancel button. This ensures that when the cancel button is pressed, this option's callback will be triggered.

### `AddOption(sOptionName, fCallback, tCallbackArgs, bEveryPage, bBindToCancelButton)`
Adds an option to the menu with an associated callback function and arguments. If `bEveryPage` is true, the option appears on every page; if `bBindToCancelButton` is true, it binds the option to the cancel button.

### `Display(sQuery)`
Displays the paginated menu based on the current options. It calculates the number of pages needed and calls `_Display(1, sQuery)` to show the first page.

### `_Display(nPage, sQuery)`
A private function that constructs and displays a specific page of the menu. It handles navigation options ("Next page" and "Previous page") and ensures that options bound to the cancel button are correctly positioned.

### `_ChooseOption(nPage, sQuery, nSelectedIndex)`
Handles the selection of an option from the displayed menu. If the selected option is a navigation option, it updates the current page; otherwise, it triggers the associated callback for the selected option.

## Events
- Listens for user input through `MrxGui.DisplayDialogBox` to handle option selections and page navigation.

## Notes for modders
- Ensure that options are added correctly using `AddOption`, specifying whether they should appear on every page or not.
- Use `BindOptionToCancelButton` to ensure that a specific option's callback is triggered when the cancel button is pressed.
- Customize the menu display by adding appropriate options and callbacks.
- Be aware of the maximum number of options per page (`_knMaxOptionsPerPage`) to avoid overflow.