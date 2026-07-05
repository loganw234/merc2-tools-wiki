---
title: MrxMultipageMenu
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, menu]
verified: true
verified_note: 'deeper pass: re-confirmed the full public API (Reset/AddOption/Display) against source and cross-checked it matches the AI Primer + Snippets pages exactly (AddOption param order, ~8-option pagination via _knMaxOptionsPerPage=8, nil-callback-only-safe-on-cancel-option); added a copy-paste usage shape and the module-name casing note (file mrxmultipagemenu → global; primer imports "MrxMultiPageMenu"). _Display/_ChooseOption internals, undeclared nDefaultOption global, and undefined LTILibName still confirmed'
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

## Public API — the exact shape modders use

This is the auto-paginating menu the [AI Primer](../ai-primer) and [Snippets](../snippets) tell modders to
reach for. The three-call `Reset` → `AddOption` (×N) → `Display` sequence below is confirmed against the
game's own callers (`mrxguishell.lua`, `mrxcheatbootstrap.lua`):

```lua
import("MrxMultiPageMenu")
MrxMultiPageMenu.Reset()
MrxMultiPageMenu.AddOption("Say hello", function() Loader.Printf("hi!") end)
MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)  -- nil callback, on every page, cancel-bound
MrxMultiPageMenu.Display("Test Menu:")
```

`AddOption(sOptionName, fCallback, tCallbackArgs, bEveryPage, bBindToCancelButton)` — the parameter order
above is exact and matches how every stock caller invokes it. `tCallbackArgs` is a plain table `unpack`ed into
`fCallback` when the option fires (so `AddOption("Skip", _Skip, {true})` calls `_Skip(true)`).

{: .note }
> **Module name casing:** the file is `mrxmultipagemenu.lua`, but the callable global is `MrxMultiPageMenu`
> (capital **P**) — that's the name every stock `import("MrxMultiPageMenu")` uses, and the name to `import`.
> The engine registers this module under its CamelCase name, not a naive lowercase-of-filename, so don't guess
> `Mrxmultipagemenu`.

## Notes for modders
- **A `nil` callback is only safe on the cancel/close option.** The `"Close this menu"` idiom above passes
  `nil` for `fCallback` *because* it's bound to the cancel button (last two args `true, true`) — `_ChooseOption`
  guards with `if tCallbackData then`, so a `nil` callback simply closes the menu without erroring. Give every
  *other* option a real callback.
- **Only one menu can be live at a time.** State is module-global (see Instance pattern), so a fresh
  `Reset()`/`AddOption`/`Display` sequence overwrites any menu already in progress — always `Reset()` first.
- **Pagination is automatic past `_knMaxOptionsPerPage` (`8`).** You never build pages yourself; add all your
  options and `Display` inserts `"Next page"`/`"Previous page"` entries and the `(Page N/M)` suffix as needed.
  "Every page" options (`bEveryPage = true`) eat into that 8-slot budget on *every* page, so a menu with 2
  every-page options only fits 6 regular options per page.
- **Built on [`MrxGui.DisplayDialogBox`](mrxguidialogbox).** The menu is a native dialog box under the hood
  (see [`mrxguibase`](mrxguibase) for the widget/focus machinery it rides on); this module is just the
  paginating wrapper around it.