---
title: MrxUnlockFanfare
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [hud, fanfare]
verified: true
verified_note: "deeper pass: re-confirmed Imports/functions/Events against source; documented the _BuildMessage sType catalog (contact/support/stockpile/landingzone/bounty/outfit) and the ClientHVTFanfare type ids (1=hvtcapture, 2=hvtkill), noted outfit items skip network replication, replaced boilerplate modder notes"
---

# MrxUnlockFanfare

*Module: mrxunlockfanfare.lua*

## Overview
The `MrxUnlockFanfare` module is responsible for displaying unlock banners on the HUD when players acquire new items or complete certain game objectives. It handles both individual and batched fanfares, formats messages based on item types, and replicates events across the network.

## Inheritance
- Inherits from: `none`
- Imports: `MrxGui`, `MrxCheatBootstrap`, `MrxFactionManager`, `MrxSupportData`, `WifStarterData`, `MrxStarterManager`, `WifEquipmentData`, `MrxUtil`

## Instance pattern
This is a stateless manager/utility module (module-level globals, no `Create`/`uGuid` pattern). It tracks two module-level globals used to accumulate a batch before display:
- `tClientMessages`: List of formatted message strings accumulated across `SetClientBatchFanfareData` calls until the batch completes.
- `_ClientBatchType`: The `sType` of the batch currently being accumulated.

## Functions
### `AddUnlockedItem(tItemData)`
Adds an individual unlocked item and displays the corresponding HUD fanfare. If the game is in skip mode, it does nothing. It sends network events for server replication (excluding "outfit" items).

### `AddUnlockedItems(sType, tItems)`
Handles batched unlock items of a specific type. It formats messages for each item, sends network events for server replication, and displays the fanfares on the HUD.

### `_BuildMessage(sType, tItemData)`
Constructs the fanfare text from `tItemData`, branching on `sType`. The recognized types (and what each pulls
from `tItemData`) are:

| `sType` | Message shape |
|---|---|
| `"contact"` | faction icon + starter name (`WifStarterData.GetPlayerVisibleName`) |
| `"support"` | faction icon + support name, or equipment name if it's equipment |
| `"stockpile"` | support name + `" (x <nQty>)"` |
| `"landingzone"` | faction icon (if any) + `tItemData.sName` |
| `"bounty"` | faction icon + faction visible name |
| `"outfit"` | `tItemData.sName` only |

Any other `sType` returns `nil` (no fanfare). Invalid support/equipment ids fall back to the raw id with a
`"(INVALID SUPPORT ID?)"` / `"(INVALID EQUIPMENT ID?)"` marker — handy when debugging a mod that passes a bad
id. Faction visuals come from [`MrxFactionManager.GetInlineIcon`/`GetPlayerVisibleName`](mrxfactionmanager).

### `SetClientFanfareData(sType, sName, sFactionId, nStarterId, sSupportId, nQty)`
Sets client-side fanfare data for a single unlocked item. It converts support IDs to string indices and calls `AddUnlockedItem` to display the fanfare.

### `SetClientBatchFanfareData(bComplete, sType, sFactionId, sSupportId, nQty, bClear)`
Manages batched client-side fanfare data. It clears previous messages if `bClear` is true, appends new messages, and displays them on completion.

### `ClientHVTFanfare(iFanfareType, sFactionId, sDesc, iInlineIcon, nCompleted, nQuota)`
Client-only (early-returns unless `Net.IsClient()`). Displays an HVT (High Value Target) fanfare. `iFanfareType`
`1` → `sType = "hvtcapture"`, `2` → `"hvtkill"`. The text is `<faction icon> <objective inline icon> <sDesc>
(nCompleted/nQuota)`, using [`MrxUtil.GetInlineIconNameByIndex`](mrxutil) for the objective icon.

## Events
No `Event.*` calls appear anywhere in this file. Network replication uses `Net.SendEvent_UnlockFanfare` and `Net.SendEvent_BatchUnlockFanfare` (outbound, server → client) directly, not the `Event` system; the client-side receive path (`SetClientFanfareData`, `SetClientBatchFanfareData`, `ClientHVTFanfare`) is presumably invoked by native/engine networking code, not visible in this file. `Hud.EventFanfare:Commence` is called to display fanfares on the HUD.

## Notes for modders
- **Show a banner**: call `AddUnlockedItem({sType=..., ...})` for one item or `AddUnlockedItems(sType, tItems)`
  for a batch. Both no-op if [`MrxCheatBootstrap.IsSkipModeEnabled()`](mrxcheatbootstrap) — so if your fanfares
  silently don't appear, skip mode is the first thing to check.
- **Add a new fanfare category** by adding a `sType` branch in `_BuildMessage`; an unhandled `sType` yields no
  message and nothing displays.
- **`"outfit"` fanfares are local-only** — `AddUnlockedItem` returns before the `Net.SendEvent_UnlockFanfare`
  call for that type, so costume unlocks never replicate to co-op partners (by design).
- On the server, replication goes out via `Net.SendEvent_UnlockFanfare` (single) /
  `Net.SendEvent_BatchUnlockFanfare` (batch); the matching client entry points are `SetClientFanfareData` /
  `SetClientBatchFanfareData`, invoked by native networking. All display goes through `Hud.EventFanfare:Commence`.