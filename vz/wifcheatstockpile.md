---
title: WifCheatStockpile
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 6
inherits: none
tags: [data]
verified: false
---

# WifCheatStockpile

## Overview
`WifCheatStockpile` is a flat lookup table of "expected resources at this point in the campaign" —
support charges, equipment, cash, and fuel — keyed directly by mission id. It exists purely to back the
debug mission-skip cheat: when a developer/tester jumps straight to a given mission, this table tells the
game what to reset the player's stockpile to, so the jump doesn't leave them over- or under-equipped for
that point in the story.

## Inheritance
- Inherits from: none — base data module.
- Imports: none.

Unlike its [`WifMissionData`](wifmissiondata)/[`WifHqData`](wifhqdata) siblings, there's no wrapping
table here — each mission id (`AllCon001`, `ChiCon002`, ...) is a top-level global in this module
directly, not nested under something like `tMissionData`.

## Instance pattern
Pure static data module — no functions at all, no runtime state.

## Functions
None. 38 top-level entries in total: 22 independent records, and 16 that are plain aliases to the exact
same `PmcCon003` table —

```lua
AllCon008 = PmcCon003
AllCon050 = PmcCon003
AllCon052 = PmcCon003
AllCon053 = PmcCon003
AllJob002 = PmcCon003
AllJob003 = PmcCon003
AllJob010 = PmcCon003
AllJob020 = PmcCon003
ChiCon050 = PmcCon003
ChiCon051 = PmcCon003
ChiCon008 = PmcCon003
ChiCon009 = PmcCon003
ChiJob002 = PmcCon003
ChiJob003 = PmcCon003
ChiJob010 = PmcCon003
ChiJob020 = PmcCon003
```

Since Lua assignment doesn't copy tables, all 17 of these ids (the 16 above plus `PmcCon003` itself)
share one underlying table object — mutating one at runtime would mutate all of them.

### Schema
```lua
AllCon001 = {
  tSupport = {
    laserguidedbomb = 3,
    carpetbomb = 1,
    wz10 = 2,
    -- ...
  },
  tEquipment = {"FuelTank01", "FuelTank02", "FuelTank03"},
  nCash = 800000,
  nFuel = 1500
}
```
`tSupport` is a support-id → quantity map (fed to `MrxPmc.AddSupportQty`); `tEquipment` is an array of
equipment id strings (fed to `MrxPmc.AddEquipment`); `nCash`/`nFuel` are absolute amounts, not deltas (see
Notes).

## Events
None.

## Notes for modders
- Read exactly once, from `resident/mrxcheatbootstrap.lua`'s `EnableSkipMode(false, ...)`:
  `WifCheatStockpile[_sSkipToMissionId]` — a plain table index, guarded with `if tExpectedResources then`,
  so skipping to a mission id with no entry here (most Job-type missions, all Vza/Mec/Pir contracts, and
  several late Con missions) silently grants nothing rather than erroring.
- **Likely dead grant:** `tEquipment`'s ids use a zero-padded naming scheme — `"FuelTank01"` through
  `"FuelTank05"` — that doesn't match any real key in [`WifEquipmentData`](wifequipmentdata)'s
  `_tEquipment` table (which uses `FuelTank1`..`FuelTank14`, no leading zero). `MrxPmc.AddEquipment(sName)`
  looks the name up via `WifEquipmentData.GetEquipmentData(sName)` and silently returns if that comes back
  `nil` — so every `tEquipment` grant in this file is presently a no-op; only `tSupport`, `nCash`, and
  `nFuel` actually take effect when skip-jumping.
- `nCash` isn't additive — `EnableSkipMode` zeroes the player's current cash first
  (`MrxPmc.AddCashQty(MrxPmc.GetCashQty() * -1)`) and then adds `nCash`, so it's an absolute reset, not a
  bonus on top of whatever the player already had.
- **Real duplicate-key clobbers** worth knowing if you edit this table: several `tSupport` literals repeat
  a key with a different value later in the same table, and Lua's last-key-wins rule silently keeps the
  later one. For example, `ChiCon002`'s `combatairpatrol` goes from `2` down to `1`, and its `tankbuster`
  goes from `1` up to `3`, purely because a second, generic block of keys was pasted after the
  faction-specific one; `PmcCon002`'s `artillery` (`3` → `1`) and `c4` (`2` → `1`) are clobbered the same
  way. If you're hand-editing one of these tables, check for a repeated key before assuming the first
  value you see is what a player actually gets.
- See [`WifMissionFlow`](wifmissionflow) for the other half of the skip cheat: its
  `GetOriginalFlowData()` entries check the same `MrxCheatBootstrap.IsSkipModeEnabled()` flag to skip
  cutscenes/state-transitions during a skip-jump, while this file supplies the resource reset.
