---
title: MrxShop
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [economy, shop]
verified: true
verified_note: "deeper pass: documented the _ShopSelection affordability gate (nCost <= MrxPmc.GetCashQty()) and its MrxPmc.AddCashQty(-nCost, ...) debit path, surfaced tTypeToIcon, cross-linked economy modules, replaced vacuous modder notes; all functions/imports re-confirmed"
---

# MrxShop

*Module: mrxshop.lua*

## Overview
The `MrxShop` module is responsible for managing the in-game store system, including generating and displaying shop lists, handling item purchases, and maintaining persistence of purchased items. It interacts with various other modules like `MrxFactionManager`, `MrxPmc`, and `WifEquipmentData` to determine prices, availability, and player resources.

## Inheritance
- Inherits from: `none`
- Imports: `WifMissionData`, [`MrxSupportData`](mrxsupportdata), `WifEquipmentData`, [`MrxPmc`](mrxpmc),
  [`MrxUtil`](mrxutil), [`MrxFactionManager`](mrxfactionmanager), [`MrxRewardData`](mrxrewarddata)

## Instance pattern
This is a stateless manager/utility module. It does not follow the per-instance pattern (keyed by `uGuid`). Instead, it maintains global state through `_tGlobalShopList` and `_oVender`.

## Functions
### `Init()`
Initializes the global shop list for each faction by populating `_tGlobalShopList` with default values.

### `Open(oVender, fOnClose, tOnCloseData)`
Opens the shop interface for a given vendor. It sets up the shop UI, applies price scaling, separates items into unlocked and locked categories, sorts them by cost, and handles item selection through `_ShopSelection`.

### `_GetShopList(oVender, sFactionId)`
Generates a list of potential shop items based on the vendor's faction. It retrieves both support and equipment items that can be sold in the shop.

### `_GetPriceScale(oVender)`
Determines the price scale for items in the shop. Returns 1.0 if the vendor has a custom vehicle shop; otherwise, it uses `MrxFactionManager.GetPriceScale` to get the faction's PMC price scale.

### `_ShopSelection(sId, nAmt)`
The purchase handler wired into `Hud.Shop` (see Events). Returns `false` immediately if `sId == "Locked"`.
Otherwise it looks the id up in [`MrxSupportData.tSupportData`](mrxsupportdata#support-item-catalog) (or, failing
that, `WifEquipmentData.GetEquipmentData`), computes `nCost = base * nPriceScale * nAmt`, and applies the
**affordability gate**:

```lua
if nCost <= MrxPmc.GetCashQty() then   -- can afford (a $0 item always passes)
  MrxPmc.AddSupportQty(sId, nAmt, false, nCost)   -- or MrxPmc.AddEquipment(sId)
  MrxPmc.AddCashQty(-nCost, nil, "[Generic.ShopItems]")   -- debit, HUD-updating
  return true
end
```

This single `nCost <= MrxPmc.GetCashQty()` comparison is the whole "can the player buy this?" check — there is
no separate free-item flag. Zeroing an item's `nCashCost`/`nCost` (in `MrxSupportData`/`WifEquipmentData`) makes
`nCost` evaluate to `0`, which always passes the gate, i.e. makes the item free. Note the debit goes through
[`MrxPmc.AddCashQty`](mrxpmc#addcashqty-namt-bmateriel-sreason-bsuppressdisplay) (HUD-updating), not
`Player.SetCash`.

### `_AddPurchasedSupportItem(sId)`
Adds a support item to the list of purchased items for the vendor's faction.

### `_AddPurchasedEquipmentItem(sId)`
Adds an equipment item to the list of purchased items for the vendor's faction.

### `Close()`
Closes the shop interface for the local player.

### `GetIndexedShopList(oVender)`
Generates an indexed list of unlocked status for each item in the shop, used for client-server synchronization.

### `SetIndexedShopList(tIndexedList)`
Sets the indexed list of unlocked status for each item in the shop.

### `GetTotalNumberOfItems(sFaction)`
Returns the total number of items available in the shop for a given faction.

### `GetNumberOfPurchasedItems(sFaction)`
Returns the number of items purchased by players for a given faction.

### `GetNumberOfUnlockedItems(sFaction)`
Returns the number of items unlocked for a given faction.

### `SaveSingleton()`
Saves the current state of `_tGlobalShopList` to persistent storage.

### `LoadSingleton(tData)`
Loads the saved state of `_tGlobalShopList` from persistent storage.

## Events
No `Event.*` references appear anywhere in this file. Shop interaction is wired entirely through
`Hud.Shop` callbacks instead of the engine event system:
- `Hud.Shop:SetCallback({..., fCallback = _ShopSelection, ...})` — routes item purchases to
  `_ShopSelection`.
- `Hud.Shop:SetCloseCallback({..., fCallback = function() ... end, ...})` — an inline anonymous
  function (not a named module function) that clears `_oVender` and invokes the caller-supplied
  `fOnClose`/`tOnCloseData` via `MrxUtil.CallWithOptionalArgs`.

Both callback targets (`_ShopSelection`, the inline closure) are defined in this file, so there's no
undefined-callback issue here.

## Module constants
- `tTypeToIcon` — maps an item's `sType`/`nType` to a HUD icon tag string used as a name prefix, e.g.
  `Airstrike = "[airstrike] "`, `Light = "[vehmlight] "`, `Heavy = "[vehmheavy] "`, `Boat = "[vehboat] "`,
  `Heli = "[vehheli] "`, and `[WifEquipmentData.knTypeFuelTank] = "[fuelsilo] "`. Change these to reswap the
  shop-row icons.

## Notes for modders
- **Make an item free / change its price without touching this file** — prices come from the source data
  tables, not from `MrxShop`. Support prices are `tSupport.nCashCost` in
  [`MrxSupportData`](mrxsupportdata); equipment prices are `tEquipmentData.nCost` in `WifEquipmentData`. The
  faction/vendor multiplier is `nPriceScale` from `_GetPriceScale` (via
  [`MrxFactionManager.GetPriceScale`](mrxfactionmanager)); a vendor with `HasCustomVehicleShop()` forces scale
  `1.0`.
- **The affordability check is `nCost <= MrxPmc.GetCashQty()`** in `_ShopSelection` — a `$0` item always
  passes. There is no separate "unlock = free" path here; a locked item is filtered out earlier (its `sId`
  becomes `"Locked"`, which `_ShopSelection` rejects).
- Item availability (which ids appear at all) is driven by
  [`MrxRewardData.GetAllPotentialShopItems(sFactionId)`](mrxrewarddata) inside `_GetShopList`, and per-item
  unlock state by `MrxSupportData.IsItemUnlocked` / `WifEquipmentData.IsItemUnlocked`.
- On clients (`Net.IsClient()`), unlock status is read from a synced `_tIndexedShopList` (set via
  `SetIndexedShopList`) rather than recomputed locally, and grappling hooks are suppressed from the client
  list. Keep that in mind if you mod shop contents in co-op.