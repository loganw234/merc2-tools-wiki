---
title: MrxShop
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [economy, shop]
---

# MrxShop

*Module: mrxshop.lua*

## Overview
The `MrxShop` module is responsible for managing the in-game store system, including generating and displaying shop lists, handling item purchases, and maintaining persistence of purchased items. It interacts with various other modules like `MrxFactionManager`, `MrxPmc`, and `WifEquipmentData` to determine prices, availability, and player resources.

## Inheritance
- Inherits from: `none`
- Imports: `WifMissionData`, `MrxSupportData`, `WifEquipmentData`, `MrxPmc`, `MrxUtil`, `MrxFactionManager`, `MrxRewardData`

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
Handles the purchase of an item from the shop. It calculates the total cost based on the base price, price scale, and quantity, checks if the player has sufficient cash, and updates the player's resources and purchased items accordingly.

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
- Listens for custom events related to shop operations, such as item selection and UI interactions.

## Notes for modders
- Ensure that `Init()` is called during game initialization to set up the global shop list.
- Use `Open` and `Close` to manage the shop interface lifecycle.
- Customize item prices and availability by modifying the relevant data tables in `MrxSupportData` and `WifEquipmentData`.
- Be aware of network synchronization (`Net.IsClient`) when handling client-server interactions for shop items.