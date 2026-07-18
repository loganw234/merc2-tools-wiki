---
title: MrxStatsManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [statistics, player progress]
verified: true
verified_note: "deeper pass: completed Imports (added MrxShop/MrxTransit/MrxPmc/MrxStarterManager/MrxAchievements), rewrote Events (real subs are Event.WeaponEvent Stow/Drop/Equip and Event.ObjectInSeat enter/exit via Event.CreatePersistent — no PlayerJoined/ObjectUse/SaveGame/LoadGame), surfaced the GetPercentCompleted weight constants + nTotalToolbox=100 and the credit/debit reason keys; all functions re-confirmed"
---

# MrxStatsManager

*Module: mrxstatsmanager.lua*

## Overview
The `MrxStatsManager` module is responsible for tracking and managing various statistics and progress metrics for the player. It includes counters for completed toolboxes, destroy bounties, credits, debits, fuel usage, deaths, medevacs, retries, transit events, race times, favorite weapons, and vehicles. Additionally, it manages faction names and abbreviations.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxShop`](mrxshop), [`MrxTransit`](mrxtransit), [`MrxVerifyManager`](mrxverifymanager),
  [`MrxFactionManager`](mrxfactionmanager), [`MrxUtil`](mrxutil), [`MrxPmc`](mrxpmc),
  [`MrxStarterManager`](mrxstartermanager), `WifMissionData`, [`MrxAchievements`](mrxachievements)
  (an earlier draft listed only four).

## Instance pattern
**Not per-`uGuid` — a singleton module.** Confirmed: no `OnActivate`/`Create`/`tInstance` registry
anywhere in source. This is one shared, session-wide stats tracker, not something spawned per world
object. Key fields:
- `bActivated`: Indicates whether the module has been activated.
- `tDestroyBty`: Counts of destroyed parts for each faction.
- `nCompletedToolboxes`: Total number of completed toolboxes.
- `tFavWeapon`: Time spent with each favorite weapon.
- `tFavVehicle`: Time spent in each favorite vehicle.
- `sFactionName`: Short player-visible names for each faction abbreviation.
- `nTotalCredit`: Total credit amount.
- `tListOfCredits`: Reasons and amounts of credits earned.
- `nTotalDebit`: Total debit amount.
- `tListOfDebits`: Reasons and amounts of debits incurred.
- `nFuelInAmount`: Total fuel input amount.
- `nFuelOutAmount`: Total fuel output amount.
- `nDeathCounter`: Total number of deaths.
- `nMedevacCounter`: Total number of medevacs.
- `nRetriesCounter`: Total number of retries.
- `nTransitCounter`: Total number of transit events.
- `tBestTimes`: Best times for each mission.

## Completion weights & totals (tunables)

`GetPercentCompleted` (and the identical math inlined in `BuildStats`) is a weighted average of seven progress
categories. The weights and category totals are module-level locals:

| Constant | Value | Category |
|---|---:|---|
| `nContractWeight` | `25` | contracts completed |
| `nRecruitWeight` | `10` | PMC recruits (out of 4) |
| `nShopWeight` | `2` | shop items unlocked |
| `nDestroyWeight` | `3` | faction destroy-bounty parts |
| `nHVTWeight` | `5` | HVTs verified |
| `nToolboxWeight` | `1` | toolboxes collected |
| `nLZWeight` | `3` | landing zones unlocked |

`nTotalWeight` is their sum (`49`); the final result is `math.min(weighted / nTotalWeight, 1)` so it never
exceeds 100%. Other totals: `nTotalToolbox = 100` (toolbox denominator), and `tDestroyBtyTotals` holds the
per-faction destroy targets (`All = 24`, `Gur = 13`, `Oil = 13`, `Pir = 11`, `Chi = 8`; others `0`). Change any
of these to reweight the completion meter.

The **credit/debit reason keys** are also pre-seeded (localization strings): credits include
`[Generic.Contracts]`, `[Generic.Wagers]`, `[Generic.Collectibles]`, `[Generic.Pickups]`; debits include
`[Generic.CopterRepair]`, `[Generic.Collateral]`, `[Generic.Bribes]`, `[Generic.Wagers]`, `[Generic.Medevacs]`,
`[Generic.ShopItems]`, `[Garage.replacefionacar]`, `[Generic.SupportDesignators.Satellite]`. These are the same
`sReason` strings [`MrxPmc.AddCashQty`](mrxpmc#addcashqty-namt-bmateriel-sreason-bsuppressdisplay) forwards here.

## Functions

### Activated()

This function initializes the module if it hasn't been activated yet. It sets `bActivated` to true and populates the `sFactionName` table with short player-visible names for each faction abbreviation obtained from `MrxFactionManager`.

### LoadSingleton(tSaveData)

This function loads saved game data into the module's state. It updates various tables and counters (`tDestroyBty`, `nCompletedToolboxes`, `tFavWeapon`, `tFavVehicle`, etc.) with values from `tSaveData`. It also handles specific logic for loading retries and deaths based on whether the load is a retry.

### SaveSingleton()

This function saves the current state of the module into a table (`tSaveData`). It includes all counters, tables, and data related to player progress, favorite items, and faction-related statistics.

### _GetTableSizeSlow(t)

This helper function calculates the size of a given table by iterating over its keys. It returns the number of elements in the table.

### GetTotalNumContracts()

This function retrieves the total number of contracts available in the game using `WifMissionData.GetNumContracts()` and subtracts one from the result.

### GetTotalNumHVTs()

This function calculates the total number of High Value Targets (HVTs) by calling `MrxVerifyManager.GetTotal()` and subtracting one.

### GetPercentCompleted()

This function computes the overall percentage completion based on various player statistics, including contracts, recruits, shop items, destroy bounties, HVTs, toolboxes, LZ events, favorite weapons, and vehicles. It uses weighted averages for each category to determine the final percentage, ensuring it does not exceed 100%.

### BuildStats(oPda)
This function builds and updates statistics related to the player's progress in the game. It adds various categories and entries to the PDA (Personal Digital Assistant) such as cash, fuel, contracts completed, recruits, shop items unlocked, faction targets destroyed, HVTs verified, toolboxes collected, and landing zones unlocked. The function also calculates a weighted percentage of completion based on these statistics.

### JobDestroyPart(sFaction)
This function increments the count of destroyed parts for a specific faction. It updates the `tDestroyBty` table with the number of parts destroyed by each faction.

### CompleteToolboxPart()
This function increments the count of completed toolboxes. It updates the `nCompletedToolboxes` variable to reflect the total number of toolboxes collected.

### PdaStatistics(oPda)
This function builds and updates statistics related to the player's in-game activities. It adds various categories and entries to the PDA such as favorite weapon, favorite vehicle, outposts captured, credits, debits, fuel usage, deaths, medevacs, retries, transits, and best race times. The function also formats monetary values using `MrxUtil.FormatMoney`.

### AddWeaponTimer()
This function sets up event listeners for weapon-related events (stow, drop, equip) to track the time spent with each favorite weapon. It creates persistent events using `Event.CreatePersistent` and initializes timestamps for the current weapon.

### DeleteWeaponTimer()
This function deletes the event listeners set up by `AddWeaponTimer`. It unregisters the timers using `Event.Delete`.

### TrackWeaponTime(uOwner, uWeapon)
This function tracks the time spent with a specific weapon. It calculates the elapsed time since the last timestamp and updates the favorite weapon's total time if the weapon has the "weapon" label.

### StartWeaponTime(uOwner, uWeapon)
This function starts or resets the timestamp for a specific weapon. If a timestamp already exists, it marks it; otherwise, it creates a new main timestamp.

### UpdateWeaponTime()
This function updates the time spent with the current favorite weapon by calling `TrackWeaponTime` and `StartVehicleTime`.

### SetFavWeaponTime(sWeapon, nTime)
This function updates the total time spent with a specific favorite weapon. It adds the elapsed time to the existing value or initializes it if not present.

### GetFavWeapon()
This function determines the player's favorite weapon based on the total time spent using each weapon. It returns the name of the weapon with the highest usage time.

### AddVehicleTimer()
This function sets up event listeners for vehicle-related events (exit, enter) to track the time spent in each favorite vehicle. It creates persistent events using `Event.CreatePersistent` and initializes timestamps for the current vehicle.

### DeleteVehicleTimer()
This function deletes the event listeners set up by `AddVehicleTimer`. It unregisters the timers using `Event.Delete`.

### TrackVehicleTime(uOwner, uVehicle)
This function tracks the time spent in a specific vehicle. It calculates the elapsed time since the last timestamp and updates the favorite vehicle's total time if the vehicle has the "vehicle" label.

### StartVehicleTime(uOwner, uVehicle)
This function starts or resets the timestamp for a specific vehicle. If a timestamp already exists, it marks it; otherwise, it creates a new main timestamp.

### UpdateVehicleTime()
This function updates the time spent in the current favorite vehicle by calling `TrackVehicleTime` and `StartVehicleTime`.

### SetFavVehicleTime(uVehicle, nTime)
This function updates the total time spent in a specific favorite vehicle. It adds the elapsed time to the existing value or initializes it if not present.

### GetFavVehicle()
This function determines the player's favorite vehicle based on the total time spent using each vehicle. It returns the name of the vehicle with the highest usage time.

### IncreaseOutpostCapturedCounter()
This function increments the counter for outposts captured by the player.

### IncreaseCreditAmount(nAmt)
This function increases the total credit amount by a specified amount. It updates the `nTotalCredit` variable.

### ReasonsForCredits(sReason, nAmt)
This function records the reasons and amounts of credits earned. It updates the `tListOfCredits` table with the specified reason and amount.

### IncreaseDebitAmount(nAmt)
Decreases the total debit amount by a specified amount.

### ReasonsForDebits(sReason, nAmt)
Updates the list of debits for a given reason. If the reason already exists in the list, it decreases the existing debit amount by the specified amount. Otherwise, it adds the new debit amount with a negative sign.

### IncreaseFuelInAmount(nFuel)
Increases the total fuel input amount by a specified amount.

### IncreaseFuelOutAmount(nFuel)
Increases the total fuel output amount by a specified amount.

### IncreaseDeathCounter()
Increments the death counter by one.

### IncreaseMedevacCounter()
Increments the medevac counter by one.

### IncreaseRetriesCounter()
Increments the retries counter by one.

### IncreaseTransitCounter()
Increments the transit counter by one.

### RecordBestTime(sMission, nTime)
Records the best time for a given mission. If the mission does not have a recorded time or if the new time is better than the existing recorded time, it updates the best time for that mission.

## Events

The only real subscriptions are the fav-weapon and fav-vehicle timers, created on demand via
`Event.CreatePersistent` and torn down by their matching `Delete*` functions:

- **`AddWeaponTimer`** → `Event.CreatePersistent(Event.WeaponEvent, {uLocalChar, "Stow"/"Drop"/"Equip"}, ...)`
  — `"Stow"`/`"Drop"` route to `TrackWeaponTime`, `"Equip"` to `StartWeaponTime`. `DeleteWeaponTimer` deletes all three.
- **`AddVehicleTimer`** → `Event.CreatePersistent(Event.ObjectInSeat, {uLocalChar, "Vehicle", "d", "x"/"e"}, ...)`
  — driver-seat exit (`"x"`) → `TrackVehicleTime`, enter (`"e"`) → `StartVehicleTime`. `DeleteVehicleTimer` removes them.

{: .note }
> There are **no** `PlayerJoined`/`PlayerLeft`/`ObjectUse`/`SaveGame`/`LoadGame` event subscriptions — an earlier
> draft invented them. Stats are updated by direct function calls from other modules (e.g.
> [`MrxPmc`](mrxpmc) calls `IncreaseCreditAmount`/`ReasonsForCredits`; [`MrxPlayer`](mrxplayer) calls
> `IncreaseDeathCounter`/`IncreaseMedevacCounter`), and save/load happens through `SaveSingleton`/`LoadSingleton`
> called by the bootstrap, not events.

## Notes for modders

- **Reweight the completion meter** by editing the weight/total constants above — `nTotalToolbox`,
  `tDestroyBtyTotals`, and the seven `n*Weight` locals are the only knobs that decide what "100%" means.
- **Increment counters through the `Increase*`/`Record*` functions**, which is how the rest of the codebase
  feeds this module. There's no event to hook — call the function directly (all are plain globals, so they're
  also overridable if you want to intercept a stat).
- **`GetFavWeapon`/`GetFavVehicle`** rank by accumulated time keyed on `Object.GetLocalizedName`, so two items
  sharing a localized name merge into one bucket. Fine for the stats screen, worth knowing if you query them.
- `LoadSingleton` deliberately skips restoring `nDeaths`/`nRetries` when `Pg.LoadIsRetry()` is true (a mission
  retry shouldn't reset those), unlike a normal load.