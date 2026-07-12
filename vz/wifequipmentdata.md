---
title: WifEquipmentData
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 5
inherits: none
tags: [data]
verified: false
---

# WifEquipmentData

## Overview
`WifEquipmentData` is the static registry of purchasable/ownable PMC equipment — 14 numbered fuel tanks
plus the grappling hook — along with per-faction unlock-state tracking (new/viewed) layered directly onto
that same table at runtime. It's read from extensively by the shop, reward, and PMC-stats systems.

## Inheritance
- Inherits from: none — base data module.
- Imports: none.

## Instance pattern
Singleton-state manager, but unusually the "state" is written directly onto the static data table rather
than kept in a separate instance store: `_UnlockItem`/`SetItemViewed` mutate
`_tEquipment[sId].tUnlockStatus[sFactionId]` in place.

## The `_tEquipment` schema
Top-level constants: `knTypeFuelTank = 1`, `knTypeCostume = 2`, `knTypeGrapplingHook = 3` (the equipment
"type" enum) — note `knTypeCostume` is never actually used by any entry in `_tEquipment` below; costume
unlocks are tracked by an entirely separate system
([`WifPmcInterior`](wifpmcinterior)'s `GetAvailableCostumes`/`SetAvailableCostumes`, driven from
[`WifMissionFlow`](wifmissionflow)'s `_AddHeroCostume`), so this constant looks vestigial within this
file. `_knUnlockStatusNew = 1` / `_knUnlockStatusViewed = 2` is the per-faction unlock-status enum.

`_tEquipment` has 15 entries: `FuelTank1` through `FuelTank14` (`nType = knTypeFuelTank`) plus
`GrapplingHook` (`nType = knTypeGrapplingHook`). Cost and capacity step up partway through the fuel
tanks — `FuelTank1`-`8` cost 100000 for 200 capacity each, `FuelTank9`-`14` cost 250000 for 700 capacity
each:

```lua
FuelTank1 = {
  sName = "[Generic.FuelSilo]",
  sDescription = "[Generic.FuelSiloDescription]",
  sTexture = "support_bombing_run",
  nType = knTypeFuelTank,
  nCost = 100000,
  nFuelCapacity = 200,
  nFuelTankId = 1
},
```

```lua
GrapplingHook = {
  sName = "[weapon.grapple]",
  sDescription = "[Fiona.Grapple01]",
  sTexture = "weapons_grappling",
  nType = knTypeGrapplingHook,
  nCost = 100000
}
```

## Functions
### `GetEquipmentData(sId)`
Plain `_tEquipment[sId]` lookup; every other function in this file calls through this rather than
indexing `_tEquipment` directly.

### `UnlockItem(vId, sFactionId)`
Accepts either a single equipment id or an array of ids (branches on `type(vId)`); delegates each to
`_UnlockItem`.

### `_UnlockItem(sId, sFactionId)`
Creates `tUnlockStatus` on demand and sets it to `_knUnlockStatusNew` only if that faction doesn't already
have an entry — never downgrades an already-`Viewed` status back to `New`.

### `IsItemUnlocked(sId, sFaction)` / `IsItemNew(sId, sFaction)`
Read `tUnlockStatus[sFaction]` — present at all, or `== _knUnlockStatusNew`, respectively.

### `SetItemViewed(sId, sFaction)`
Flips `New` to `Viewed` for that faction.

### `GetPlayerVisibleName(sEquipmentId)`
Returns `sName`.

### `SaveSingleton()`
Saves only each item's `tUnlockStatus` (not the static definitions).

### `LoadSingleton(tData)`
Restores `tUnlockStatus` onto `_tEquipment[sId]` for each saved id, with no existence check on `sId`
first — see gotcha below.

## Events
None.

## Notes for modders
- **Gotcha:** `LoadSingleton` doesn't guard against a saved equipment id no longer existing in
  `_tEquipment` (`_tEquipment[sId].tUnlockStatus = tUnlockStatus` indexes straight into it) — removing or
  renaming an existing entry would break loading any save that had unlocked it. Adding new entries is
  safe; renaming or removing existing ones isn't.
- Heavily consumed by `resident/mrxpmc.lua` (`AddEquipment`/`RemoveEquipment`/`HasEquipment`/
  `AddFuelTank`/`RemoveFuelTank` all branch on `GetEquipmentData(...).nType`), `resident/mrxshop.lua`
  (shop listing), `resident/mrxrewarddata.lua` (reward payout plus `UnlockItem`), `resident/mrxunlockfanfare.lua`
  (unlock-toast text), and `resident/hero.lua`.
- `knTypeFuelTank`/`knTypeGrapplingHook` are the two type values anything branching on `nType` actually
  needs to handle; `knTypeCostume` can likely be ignored unless a future entry starts using it.
