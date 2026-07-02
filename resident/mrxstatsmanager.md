---
title: MrxStatsManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [statistics, player progress]
---

# MrxStatsManager

*Module: mrxstatsmanager.lua*

## Overview
The `MrxStatsManager` module is responsible for tracking and managing various statistics and progress metrics for the player. It includes counters for completed toolboxes, destroy bounties, credits, debits, fuel usage, deaths, medevacs, retries, transit events, race times, favorite weapons, and vehicles. Additionally, it manages faction names and abbreviations.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxFactionManager`, `WifMissionData`, `MrxVerifyManager`, `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
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

- **`Event.PlayerJoined`**: This module listens for this event to initialize player statistics when a new player joins the game.
- **`Event.PlayerLeft`**: This module listens for this event to handle any necessary cleanup or state saving when a player leaves the game.
- **`Event.ObjectUse`**: This module listens for this event to update statistics related to player interactions with objects in the game, such as destroying bounties or completing toolboxes.
- **`Event.WeaponStow`, `Event.WeaponDrop`, `Event.WeaponEquip`**: These events are used by `AddWeaponTimer` and `DeleteWeaponTimer` to track time spent with favorite weapons.
- **`Event.VehicleExit`, `Event.VehicleEnter`**: These events are used by `AddVehicleTimer` and `DeleteVehicleTimer` to track time spent in favorite vehicles.
- **`Event.SaveGame`**: This module listens for this event to save the current state of player statistics when a game is saved.
- **`Event.LoadGame`**: This module listens for this event to load saved player statistics when a game is loaded.

## Notes for modders

1. **Call-order requirements**:
   - Ensure that `Activated()` is called before any other functions in the module to properly initialize the state and faction names.
   - `LoadSingleton(tSaveData)` should be called after loading a save game to restore player statistics.
   - `SaveSingleton()` should be called when saving a game to ensure all current statistics are preserved.

2. **Pitfalls**:
   - Modifying internal tables or variables directly can lead to inconsistent state management. Use provided functions like `IncreaseCreditAmount` and `SetFavWeaponTime` to update statistics safely.
   - Be cautious with event listeners created by `AddWeaponTimer` and `AddVehicleTimer`. Ensure they are properly deleted using `DeleteWeaponTimer` and `DeleteVehicleTimer` to avoid memory leaks or unexpected behavior.

3. **Tunables**:
   - The module uses weighted averages to calculate the overall percentage completion. Modifying these weights can affect how player progress is displayed.
   - Adjusting the logic in functions like `GetPercentCompleted` can change the criteria for determining completion.

4. **Decompiler artifacts**:
   - Some local variables may appear unused or are assigned but never read, which is a decompiler artifact and should be ignored.
   - There might be slight redundancy in operator precedence groupings that do not affect behavior; these can be safely disregarded.