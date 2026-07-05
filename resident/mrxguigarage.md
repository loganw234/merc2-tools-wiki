---
title: MrxGuiGarage
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, pda]
verified: true
verified_note: 'deeper pass: added sFlashFile="garage" movie name, the AddStockpile/AddSupport* ActionScript callbacks + sType routing, the vehicleSelect/closePDA flash events, the black-backdrop dim (0,0,0,192); flagged that oFlash.SetCloseCallback = _SetCloseCallbackWidget references an UNDEFINED function (resolves nil)'
---

# MrxGuiGarage

*Module: mrxguigarage.lua*

## Overview
`MrxGuiGarage` drives the **garage / vehicle-support screen** — the full-screen PDA panel where you spend cash to stock vehicles and support. It is a thin Lua wrapper around a **Scaleform movie named `"garage"`** (`sFlashFile = "garage"`): Lua collects the item list and stockpile numbers, hands them to the movie via ActionScript callbacks, and listens for the movie's selection/close events. The lifecycle is a fixed four-step call sequence: `Create` → `AddItem` (repeat) → `SetCallback` → `Commence`.

## Inheritance
- Inherits from: `none`
- Imports: [MrxGui](mrxgui) (FlashWidget/AddWidget/RemoveWidget), [MrxGuiBase](mrxguibase) (control focus), [MrxPmc](mrxpmc) (cash/fuel quantities), [MrxSupportData](mrxsupportdata), [MrxGuiDialogBox](mrxguidialogbox), [MrxGuiManager](mrxguimanager) (HUD toggle)

## Instance pattern
Manager module keyed by player. State lives in the module global `_tGarageList[uPlayerGuid] = oFlash`; each open garage is one `FlashWidget` whose per-screen state (`tItems`, callbacks, `bLoaded`/`bRunning`/`bRestoreHud`) is on that widget's `CustomData`. `Init()` must run once to set `_tGarageList = {}` (it starts as `false`). Only one garage per player at a time — `Create` returns `false` if one already exists for that player.

## Module constants
- `sFlashFile = "garage"` — the Scaleform movie name loaded via `oFlash:SetSwfFile(sFlashFile, _FlashLoadedCallback, {oFlash})`. This is the single biggest knob: swap it to point at a different `.gfx` movie. If `sFlashFile` were falsy the module short-circuits to a "loaded, no visuals" state.
- Panel width: half-width `283.33334` centered at x=320 (so ~566 px wide, full 480 height).
- Dim backdrop behind the movie is a black `ImageWidget` at alpha `192` (`SetColor(0,0,0,192)`).

## Functions
### `Create(uPlayerGuid)`
Creates a new garage screen for the player. Builds the `FlashWidget`, loads the `"garage"` SWF, attaches the per-widget methods (`AddItem`/`SetCallback`/`SetCloseCallback`/`Commence`), positions it, and stores it in `_tGarageList`. Returns `true` on success, `false` if `uPlayerGuid` isn't `userdata` or a garage already exists for that player.

{: .warning }
> `Create` runs `oFlash.SetCloseCallback = _SetCloseCallbackWidget`, but **`_SetCloseCallbackWidget` is never defined anywhere in this file** — so `oFlash.SetCloseCallback` ends up `nil`. Calling `oFlash:SetCloseCallback(...)` would error. There is no top-level `SetCloseCallback(uPlayerGuid, ...)` wrapper either. Use `SetCallback` (which is invoked on both vehicle-select and PDA-close) for close handling.

### `AddItem(uPlayerGuid, sId, sName, sDescription, sType, nCurrentStock, nMaxStock, sIcon, bNew)`
Adds an item to the garage screen for the specified player. The item details include ID, name, description, type, stock quantities, icon, and a flag indicating if it's new.

### `_AddItemWidget(oFlash, sId, sName, sDescription, sType, nCurrentStock, nMaxStock, sIcon, bNew)`
Internal helper function to add an item widget to the flash object. Validates input types and inserts the item data into the custom data table of the flash widget.

### `SetCallback(uPlayerGuid, fCallback, tCallbackData)`
Sets a callback function for user actions in the garage screen for the specified player. The callback can be used to handle events like selecting a vehicle or closing the PDA.

### `_SetCallbackWidget(oFlash, fCallback, tCallbackData)`
Internal helper function to set the callback and associated data on the flash object. Validates the callback type and stores it in the custom data table of the flash widget. Passing `fCallback = nil` clears both the callback and its data.

### `SetCloseCallback` (dangling reference — not defined)
`Create` assigns `oFlash.SetCloseCallback = _SetCloseCallbackWidget`, but no function named `_SetCloseCallbackWidget` exists in this module, so the field is `nil`. There is no working close-specific callback API here — see the warning under `Create`.

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
Pushes all data into the movie and wires its events. Calls the ActionScript function `AddStockpile(cash, fuel, fuelCapacity)` (from `MrxPmc.GetCashQty/GetFuelQty/GetFuelCapacity`), then for each queued item calls one of five ActionScript "add" callbacks chosen by `sType`:

| `sType` (lowercased) | ActionScript callback |
| --- | --- |
| `"light"` | `AddSupportLight` |
| `"heavy"` | `AddSupportHeavy` |
| `"helicopters"` | `AddSupportHelicopters` |
| `"boats"` | `AddSupportBoats` |
| anything else / `nil` | `AddSupportCivilian` |

Each is called with `(sId, sName, sDescription, sIcon, nCurrentStock, nMaxStock, 0, bNew or false)`. It then binds the movie's `vehicleSelect` event to `_EndCallback` and its `closePDA` event to `_CloseCallback`, and inserts a black `SetColor(0,0,0,192)` full-screen backdrop behind the movie.

### `_EndCallback(oFlash, sArg)`
Internal callback function triggered when a vehicle is selected in the garage screen. Ends the garage session by removing the flash file, releasing control focus, and calling the user-defined callback if set.

### `_CloseCallback(oFlash)`
Internal callback function triggered when the PDA is closed in the garage screen. Calls the end callback with no argument to handle the close action.

### `_RemoveFlashFile(oFlash)`
Internal helper function to remove the flash file for the garage screen. Restores the HUD state, removes the flash widget and background image from the UI, and deletes them.

## Events
- **Only real `Event.*` call**: `Event.Create(Event.TimerRelative, {0.1, true}, _RemoveFlashFile, {oFlash})` in `_EndCallback` defers the SWF teardown 0.1 s (ignores pause) after the garage closes, so the flash-event callback returns before the widget it's running in is deleted.
- `vehicleSelect` and `closePDA` are **Scaleform/ActionScript events**, bound via `oFlash:SetFlashEventHandler(...)`, not engine `Event.*` types. `vehicleSelect` passes the selected id as `sArg` to `_EndCallback`; `closePDA` calls `_CloseCallback` (which calls `_EndCallback(oFlash, nil)`).

## Notes for modders
- **Lifecycle order matters**: `Init()` once, then per screen `Create` → one or more `AddItem` → `SetCallback` → `Commence`. `Commence` before the SWF finishes loading is fine — `_CommenceWidget` sets `bRunning` and `_FlashLoadedCallback` runs the garage once `bLoaded` is set.
- **Your `fCallback` receives the selected vehicle id** (the `sId` you passed to `AddItem`) appended after your `tCallbackData` entries; on PDA-close it's called with no extra arg. This is the single place to react to a purchase/selection.
- **`sType` picks the movie's category tab** — spell it exactly `"light"`/`"heavy"`/`"helicopters"`/`"boats"` (case-insensitive); anything else lands in the civilian list.
- **Swap `sFlashFile`** to retheme the whole screen, but the replacement movie must expose the same ActionScript entry points (`AddStockpile`, the five `AddSupport*`, and dispatch `vehicleSelect`/`closePDA`).
- Do **not** rely on `SetCloseCallback` — it's wired to an undefined function (see the warning under `Create`).