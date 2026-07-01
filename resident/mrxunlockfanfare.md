---
title: MrxUnlockFanfare
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [hud, fanfare]
---

# MrxUnlockFanfare

*Module: mrxunlockfanfare.lua*

## Overview
The `MrxUnlockFanfare` module is responsible for displaying unlock banners on the HUD when players acquire new items or complete certain game objectives. It handles both individual and batched fanfares, formats messages based on item types, and replicates events across the network.

## Inheritance
- Inherits from: `none`
- Imports: `MrxGui`, `MrxCheatBootstrap`, `MrxFactionManager`, `MrxSupportData`, `WifStarterData`, `MrxStarterManager`, `WifEquipmentData`, `MrxUtil`

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but provides functions to manage unlock fanfares.

## Functions
### `AddUnlockedItem(tItemData)`
Adds an individual unlocked item and displays the corresponding HUD fanfare. If the game is in skip mode, it does nothing. It sends network events for server replication (excluding "outfit" items).

### `AddUnlockedItems(sType, tItems)`
Handles batched unlock items of a specific type. It formats messages for each item, sends network events for server replication, and displays the fanfares on the HUD.

### `_BuildMessage(sType, tItemData)`
A helper function that constructs the message text for the HUD fanfare based on the item type (`sType`) and item data (`tItemData`). It includes faction icons, names, quantities, and other relevant details.

### `SetClientFanfareData(sType, sName, sFactionId, nStarterId, sSupportId, nQty)`
Sets client-side fanfare data for a single unlocked item. It converts support IDs to string indices and calls `AddUnlockedItem` to display the fanfare.

### `SetClientBatchFanfareData(bComplete, sType, sFactionId, sSupportId, nQty, bClear)`
Manages batched client-side fanfare data. It clears previous messages if `bClear` is true, appends new messages, and displays them on completion.

### `ClientHVTFanfare(iFanfareType, sFactionId, sDesc, iInlineIcon, nCompleted, nQuota)`
Handles HVT (High Value Target) capture/kill fanfares. It formats the message with faction icons, descriptions, and progress information, then displays it on the HUD.

## Events
- Listens for network events to handle replicated unlock fanfares.
- Triggers `Hud.EventFanfare:Commence` to display fanfares on the HUD.

## Notes for modders
- Ensure that `AddUnlockedItem` and `AddUnlockedItems` are called appropriately to trigger fanfares.
- Customize fanfare messages by modifying the `_BuildMessage` function or extending it with new item types.
- Be aware of network synchronization, as some items (like "outfit") are excluded from replication.
- Use `ClientHVTFanfare` for handling HVT-related fanfares in a client-server environment.