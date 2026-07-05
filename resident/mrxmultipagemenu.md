---
title: MrxMultipageMenu
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, menu]
verified: true
verified_note: high-level pattern was already accurate; added _Display pagination/cancel-index internals, _ChooseOption page-nav vs callback dispatch detail, _knMaxOptionsPerPage field, and two source quirks (undeclared nDefaultOption global, LTILibName not defined anywhere in this corpus)
---

# MrxMultipageMenu

*Module: mrxmultipagemenu.lua*

## Overview
The `MrxMultipageMenu` module is responsible for managing a paginated menu system in the game's user interface. It allows adding options that can span multiple pages, providing navigation between them and handling callbacks when an option is selected.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxGui`

## Instance pattern
This is a stateless manager/utility module — a single global set of tables, not per-`uGuid` (no `Create`/`OnActivate`/`Awake`/`tInstance`). Because state is module-global rather than per-instance, only one multi-page menu can be "in progress" at a time module-wide; a second `Reset()`/`AddOption()`/`Display()` sequence overwrites the first. It tracks the following key fields:
- `_tOptions`: A table of options that do not appear on every page.
- `_tOptionsOnEveryPage`: A table of options that appear on every page.
- `_tOptionsToCallbacks`: A mapping from option names to `{fCallback, tCallbackArgs}` pairs.
- `_tPageOptions`: A temporary table used during menu display to store the current page's options (including "Next page"/"Previous page" entries).
- `_nPages`: The total number of pages required for all options.
- `_sCancelButtonOptionName`: The name of the option bound to the cancel button.
- `_knMaxOptionsPerPage`: Constant, `8`. Caps how many non-"every page" options fit on one page (after subtracting the count of "every page" options).
- `_DialogBox`: The handle returned by `MrxGui.DisplayDialogBox`, or `nil` when no dialog is open. Set in `_Display`, cleared in `Close()` and at the top of `_ChooseOption`'s non-navigation branch.

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
Builds and shows one page of the menu. Resets `_tPageOptions`, then in order: inserts `"Next page"` if `nPage < _nPages`, inserts `"Previous page"` if `nPage > 1`, then fills the remaining slots (`_knMaxOptionsPerPage - nOptionsOnEveryPage`) from `_tOptions` starting at index `(nPage - 1) * nFreeOptions + 1`, stopping early if it hits a `nil` entry. Appends every `_tOptionsOnEveryPage` entry after that. While building the list, if an inserted option's name matches `_sCancelButtonOptionName`, its position in `_tPageOptions` is recorded as `nIndexForCancelButton` (used so the underlying dialog UI can visually bind that slot to the controller's cancel button). Appends `" (Page N/M)"` to the query text when `_nPages > 1`. Calls `LTILibName.ChangeShellState(true)` then `MrxGui.DisplayDialogBox(Player.GetLocalPlayer(), sDisplay, _tPageOptions, nDefaultOption or 1, _ChooseOption, {nPage, sQuery}, nil, nil, nil, nil, nil, nIndexForCancelButton)`, storing the result in `_DialogBox`.

Note: the `nDefaultOption` referenced here is never assigned anywhere in this file — it's an undeclared global, so `nDefaultOption or 1` evaluates to `1` unless some other loaded module happens to set a global of that exact name (no such assignment found elsewhere in the decompiled `resident/` corpus). In practice this argument is effectively always `1`.

### `_ChooseOption(nPage, sQuery, nSelectedIndex)`
The callback passed to `MrxGui.DisplayDialogBox` (bound with `{nPage, sQuery}` as extra args, so it receives `nPage, sQuery, nSelectedIndex`). Looks up `_tPageOptions[nSelectedIndex]`. If it's `"Previous page"` or `"Next page"`, re-invokes `_Display` with `nPage - 1`/`nPage + 1` (query unchanged) — the dialog is not closed for page navigation. Otherwise: clears `_DialogBox` to `nil`, looks up `_tOptionsToCallbacks[sOptionName]`, calls `LTILibName.ChangeShellState(false)`, and if callback data exists, invokes it via `_CallWithOptionalArgs(tCallbackData[1], tCallbackData[2])`.

## Events
No `Event.*` calls appear in this file. User interaction is routed entirely through `MrxGui.DisplayDialogBox`'s callback parameter (`_ChooseOption`), not the `Event` system. `LTILibName.ChangeShellState` (called in `Close()`, `_Display`, and `_ChooseOption`) toggles a shell-active flag around the dialog's lifetime; `LTILibName` itself is not defined anywhere in this file or elsewhere in the decompiled `resident/` corpus — presumably an engine/native-provided global.

## Notes for modders
- Ensure that options are added correctly using `AddOption`, specifying whether they should appear on every page or not.
- Use `BindOptionToCancelButton` to ensure that a specific option's callback is triggered when the cancel button is pressed.
- Customize the menu display by adding appropriate options and callbacks.
- Be aware of the maximum number of options per page (`_knMaxOptionsPerPage`) to avoid overflow.