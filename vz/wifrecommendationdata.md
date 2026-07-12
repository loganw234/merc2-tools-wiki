---
title: WifRecommendationData
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 11
inherits: none
tags: [data]
verified: false
---

# WifRecommendationData

## Overview
A static per-mission "recommended loadout" catalog — for about 25 contracts across every faction, a small
table of support-item id -> suggested quantity (e.g. `OilCon001 = {gl = 1, extgl = 1,
upcombatairpatrol = 2}`). `MrxBriefing` and `MrxMissionFlow` both call into this module to render that
recommendation as a formatted, icon-annotated checklist on the mission briefing/PDA screen,
cross-referencing what the player already owns and where they could still buy the rest.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxFactionManager`](../resident/mrxfactionmanager), [`MrxPmc`](../resident/mrxpmc),
  [`MrxRewardData`](../resident/mrxrewarddata), [`MrxShop`](../resident/mrxshop),
  [`MrxSupportData`](../resident/mrxsupportdata)

## Instance pattern
Stateless utility/data module. `_tRecommendations` is a static, read-only lookup table (confirmed: never
written to anywhere in this file, only ever indexed by mission id) — nothing here is per-`uGuid` or
mutated at runtime.

## Functions

### `HasRecommendations(sMissionId)`
`true` if `sMissionId` has an entry in `_tRecommendations`, else `false`. The gate `MrxBriefing` checks
before bothering to render a recommendation section at all.

### `GenerateRecommendationString(sMissionId)`
Builds the full multi-line recommendation string for a mission: one formatted line per recommended
support item (via `_FormatLineItem`), plus a second return value `bAllInStock` — `true` only if the player
already has enough of *every* recommended item. Returns nothing if the mission has no entry.

### `_FormatLineItem(sSupportId, nQty)`
Per-item line formatter: looks up the item's player-visible name and type via
[`MrxSupportData`](../resident/mrxsupportdata) (bailing out silently if either lookup fails), prepends a
markup icon code for its type (`Airstrike`/`Supply`/`Light`/`Heavy`/`Civilian`/`Boat`/`Heli`), appends which
of the six factions currently stock it in their shop (checking
[`MrxShop`](../resident/mrxshop)/[`MrxRewardData`](../resident/mrxrewarddata) per faction), and finally
prefixes a checked/unchecked checkbox plus `"<nQty> x "` based on whether
[`MrxPmc`](../resident/mrxpmc)'s current stock (`GetSupportQty`) already meets the recommended quantity.
Returns the formatted string and whether this specific item is fully stocked.

## Events
None — purely a data lookup + string-formatting module, no event subscriptions.

## Notes for modders
- To add or change a recommendation, edit `_tRecommendations[sMissionId]` — it's a plain
  `{sSupportId = nQty, ...}` table, keyed by whatever ids [`MrxSupportData`](../resident/mrxsupportdata)
  recognizes.
- Only ~25 missions have entries; any mission id not present here just gets no recommendation section
  shown, rather than an error — `HasRecommendations`/`GenerateRecommendationString` both handle the
  missing-entry case gracefully.
- The "sold by" faction-icon line only appears if at least one of the six shop-owning factions
  (`Pmc`/`Oil`/`Gur`/`Pir`/`All`/`Chi`) currently has that item unlocked for sale
  (`MrxShop.GetNumberOfUnlockedItems(sFactionId) > 0`) — a mission recommending an item nobody sells yet
  just won't show a "sold by" line for it.
