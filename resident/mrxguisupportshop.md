---
title: MrxGuiSupportShop
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, support]
verified: true
verified_note: 'deeper pass: re-confirmed the GetHudState() no-arg bug against mrxguimanager.lua (GetHudState(uPlayerGuid) returns _tHudStates[uPlayerGuid], so no-arg → nil → HUD never hidden, bRestoreHud path dead); added the sFlashFile="store" movie, LTILibName.ChangeShellState(true) side-effect (never reverted), AddShopItem arg layout, and cross-links; Events/functions/dialog-fallback all still accurate'
---

# MrxGuiSupportShop

*Module: mrxguisupportshop.lua*

## Overview
The `MrxGuiSupportShop` module is responsible for managing the in-game support shop interface. It handles both a Flash-based graphical user interface (GUI) and a fallback dialog box if the Flash file is unavailable. The module manages adding items to the shop, setting callbacks for various events, and handling the opening and closing of the shop interface.

## Inheritance
- Inherits from: `none` — base/utility module
- Imports: [MrxGui](mrxgui) (FlashWidget/AddWidget), [MrxGuiBase](mrxguibase) (control focus), [MrxPmc](mrxpmc) (cash/fuel/support quantities), [MrxSupportData](mrxsupportdata) (`tSupportData`, `IsSupportEquippable`), [MrxGuiDialogBox](mrxguidialogbox) (the fallback menu), [MrxGuiManager](mrxguimanager) (HUD toggle)

This is the parallel of [MrxGuiGarage](mrxguigarage) (which uses the `"garage"` movie and the same `Create`→`AddItem`→`SetCallback`→`Commence` lifecycle); the shop's equipped-support handoff talks to the [MrxGuiPda](mrxguipda) widget by name.

## Instance pattern
Stateless singleton/utility module — plain module-level globals, no `Create`/`OnActivate`/`Awake`/`tInstance` (despite this module's own factory function being named `Create`, it's not the engine's per-`uGuid` instance pattern — see below). It maintains one active shop widget per player, keyed by player GUID, in `_tShopList` (`false` until `Init()` runs). `sFlashFile` (`"store"`) names the SWF asset to load; if this were `nil`/`false`, the module falls back to a plain dialog box (`_CreateShopDialogBox`) instead of the Flash UI everywhere `_RunShop`/`Create` branch on it — though as declared it's always the string `"store"`, so no call path in this file can actually reach the dialog-box fallback branches without external code changing `sFlashFile` first.

Per-shop state lives on each Flash widget's own `CustomData` table (`tItems`, `bLoaded`, `bRunning`, `fCallback`/`tCallbackData`, `fCloseCallback`/`tCloseCallbackData`, `bRestoreHud`, `oBg`, `nCancelIndex` in dialog-fallback mode) — `Create(uPlayerGuid)` builds one such widget and stashes it in `_tShopList[uPlayerGuid]`, attaching several functions (`_AddItemWidget`, `_AddItemFullWidget`, `_SetCallbackWidget`, `_SetCloseCallbackWidget`, `_CommenceWidget`) directly onto the widget instance as methods (`oFlash.AddItem = _AddItemWidget`, etc.) — a lightweight per-widget method-attachment pattern, not `setmetatable`/`__index`-based inheritance.

## Functions
### `Init()`
**Not previously documented** — resets `_tShopList` to an empty table. Standard lifecycle reset, not
something a mod would normally call directly.

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
Runs the support shop interface, either in Flash or as a dialog box, depending on the availability of the Flash file (in practice always the Flash branch, since `sFlashFile` is a hardcoded non-nil string — see Instance pattern). On the Flash path: calls `_SetupShopFlash`, shows/plays the widget, grabs control focus, then conditionally hides the HUD.

`_RunShop` also calls `LTILibName.ChangeShellState(true)` at the end (entering shell/menu UI state) — like [MrxGuiNumericBox](mrxguinumericbox), there is no matching `ChangeShellState(false)` anywhere in this module, so that state flip is not undone here.

**Confirmed bug**: line 210 calls `MrxGuiManager.GetHudState()` with **no argument**. `MrxGuiManager.GetHudState`'s real signature is `GetHudState(uPlayerGuid)` (returns `_tHudStates[uPlayerGuid]`) — called with no argument, `uPlayerGuid` is `nil` inside that function, so it returns `_tHudStates[nil]`, which is always `nil`. The `if MrxGuiManager.GetHudState() then` branch here therefore never executes: `MrxGuiManager.ToggleHud(oFlashWidget:GetOwner(), false)` never runs when the shop opens, and `oFlashWidget.CustomData.bRestoreHud` never gets set to `true`. This also makes the `if oFlash.CustomData.bRestoreHud then MrxGuiManager.ToggleHud(oFlash:GetOwner(), true)` check in `_RemoveFlashFile` permanently dead as a consequence — the shop was presumably intended to hide the HUD while open and restore it on close, but as written it never hides the HUD in the first place.

### `_CreateShopDialogBox(oFlash)`
Creates a fallback dialog box for the support shop if the Flash file is unavailable. Color-codes items by affordability and displays them to the player.

### `_CloseShopDialogBox(oFlash, nSelectedIndex)`
Handles the event when an item is selected in the dialog box. Calls the callback function if an item is bought and cleans up resources.

### `_SetupShopFlash(oFlash)`
Sets up the Flash widget with shop items, stockpile information, and equipped support items via `oFlash:CallActionScriptCallback(...)` (`"AddStockpile"`, `"AddShopItem"` per item, `"AddSupportEquipped"` per equipped slot). Pulls currently-equipped support from the player's PDA widget (`MrxGui.GetWidgetByNameAndOwner("PDA", ...)`, up to 3 slots via `oPda:GetEquippedSupport(n)`) and appends those as extra entries in `oFlash.CustomData.tItems` before building the item list — so items added via `AddItem`/`AddItemFull` plus the player's already-equipped support share the same `tItems` array/index space. For each item, resolves designator display text (`smoke`/`satellite`/`advanced satellite`/`beacon`/`laser`/`flare` → localized strings) by looking up `MrxSupportData.tSupportData[tData.sId].oSupport:GetDesignator()`. Registers the three Flash-bridge event handlers (see Events below), builds a fullscreen dark background widget (`oBg`, alpha 192/255), and re-adds `oFlash` after `oBg` so the background renders behind it.

### `_FlashSupportBoughtCallback(oFlash, sArg)`
Registered as the handler for the `"BuyStockpile"` Flash event (the function name says "Bought", the event name says "BuyStockpile" — same handler, just named differently from its event string). Parses `sArg` for two numbers via `string.gmatch(sArg, "-*%d+")` (item index, quantity), looks up `oFlash.CustomData.tItems[t[1]]`, and if found calls `oFlash.CustomData.fCallback` with the stored `tCallbackData` plus the item's `sId` and the quantity appended.

### `_FlashSupportEquippedCallback(oFlash, sData)`
Handles the event when a support item is equipped in the Flash interface. Updates the PDA with the new equipment.

### `_ParseString(sData)`
Parses a string to extract slot and identifier numbers. Used internally by `_FlashSupportEquippedCallback`.

### `_FlashCloseShopCallback(oFlash, sArg)`
Handles the event when the support shop is closed in the Flash interface. Cleans up resources and calls any close callback functions.

### `_RemoveFlashFile(oFlash)`
Removes the Flash file and associated background widget from the GUI. Restores the HUD if it was previously hidden.

## Events
No `Event.*` calls appear anywhere in this file — there is no `Event.ObjectHibernation`, no `Awake`, no `HideMarker` event of any kind. The real mechanism is the Flash/ActionScript bridge: `oFlash:SetFlashEventHandler(sFlashEventName, fCallback, tArgs)`, registered in `_SetupShopFlash` for three named Flash events:
- `"BuyStockpile"` → `_FlashSupportBoughtCallback` — fired from the SWF when the player buys an item.
- `"equip"` → `_FlashSupportEquippedCallback` — fired when the player equips a support item to a slot; calls `oPda:SetEquippedSupport(sName, nSlot)`.
- `"closeStore"` → `_FlashCloseShopCallback` — fired when the player closes the shop UI; also called directly (not through the Flash bridge) by `Close(uPlayerGuid)`.

Separately, `_SetupShopFlash` *sends* data into the Flash widget (not an event, a one-way call) via `oFlash:CallActionScriptCallback(sName, tArgs)`: `"AddStockpile"`, `"AddShopItem"`, `"AddSupportEquipped"`, and `_FlashCloseShopCallback` sends `"requestClose"` the same way.

## Notes for modders
- Ensure that `Create`, `AddItem`/`AddItemFull`, `SetCallback`/`SetCloseCallback`, and `Commence` are called in that order to manage the shop lifecycle — items and callbacks must be registered before `Commence` runs, since `_RunShop`/`_SetupShopFlash` snapshot `CustomData.tItems` at that point.
- Customize shop items by adding them with `AddItem` (name/cost/stock only) or `AddItemFull` (adds description, texture, "new" flag) — both append into the same `oFlash.CustomData.tItems` list.
- Set callbacks using `SetCallback` and `SetCloseCallback` to handle item purchases and store closures. `fCallback` receives `(...tCallbackData, sId, nQuantity)` on a Flash-mode purchase, or `(...tCallbackData, sName, 1)` on a dialog-fallback purchase — the two paths pass different final arguments (item `sId` vs. `sName`, and a parsed quantity vs. a hardcoded `1`), so a callback meant to handle both modes needs to account for that.
- Be aware that the Flash-based interface requires the three ActionScript callbacks (`AddStockpile`, `AddShopItem`, `AddSupportEquipped`) and the SWF must fire back `BuyStockpile`/`equip`/`closeStore` for the loop to work.
- The intended "hide HUD while shopping" behavior does not currently work — see the confirmed bug under `_RunShop` in the Functions section above (missing `uPlayerGuid` argument to `MrxGuiManager.GetHudState()`).