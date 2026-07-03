---
title: MrxPmc
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [economy, support]
verified: true
verified_note: AddCashQty/AddFuelQty/SetFuelCapacity/AddSupportQty/GetSupportQty confirmed by live testing via MrxCheatBootstrap; instance-pattern claim corrected against source (stateless, not per-uGuid)
---

# MrxPmc

*Module: mrxpmc.lua*

## Overview
The `MrxPmc` module manages the player's economy and support items in Mercenaries 2. It handles various aspects such as cash, fuel, support items, freebies, and equipment. The module provides functions to add or remove resources, check quantities, and manage stockpile thresholds.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `MrxFactionManager`

## Instance pattern
**Not a per-`uGuid` instance module** — despite that being the default assumption for most `resident/`
pages, `MrxPmc` has no `Create`/`Awake` pattern anywhere in source. It's a stateless singleton manager
tracking *the* local player's economy (there's only one), called directly like
`MrxPmc.AddCashQty(100000)` with no object/instance argument — confirmed by every real call site in this
corpus, including [`MrxCheatBootstrap`](mrxcheatbootstrap)'s cash/fuel/support dialogs. The `uGuid`
parameters that do appear in this file (e.g. inside `AddFuelTank`/`_OnFuelTankDeath`) refer to a spawned
fuel-tank *prop* in the world, not a per-player instance of this module. It tracks the following key
fields:
- `_ksFuelTank`: A string representing the fuel tank prop template.
- `_tFactionToAssociation`: A table mapping factions to their associated names.
- `_tPluralReasonToSingular`: A table mapping plural reasons to singular reasons for display purposes.
- `_tEvents`, `_tStockpile`, `_tFreebies`, `_tEquipment`, `_tStockpileThresholdInfo`: Tables used to store various data related to the player's economy and support items.
- `_nLatestCount`: An integer used to keep track of the latest count for stockpile change callbacks.
- `_tClientSupportSpendings`: A table tracking client-side support spendings.
- `_knMinFuelCapacity`, `_knMaxFuelCapacity`: Constants defining the minimum and maximum fuel capacities.

## Functions

### Init()
Initializes the player's economy by setting the initial fuel capacity to `_knMinFuelCapacity` and creating a high-score event.

### AddCashQty(nAmt, bMateriel, sReason, bSuppressDisplay)
Adds a specified amount of cash to the player's total. It ensures that the cash does not exceed the hard
ceiling (`knBillion`). If `bSuppressDisplay` is false, it displays the updated cash amount in the HUD.
**Confirmed working, HUD updates** — see [`MrxCheatBootstrap`](mrxcheatbootstrap): `import("MrxPmc");
MrxPmc.AddCashQty(100000)`. Prefer this over the lower-level `Player.AddCash(...)`, which changes the real
value but skips this HUD-refresh trigger, so the on-screen number won't visibly update even though the
value changed underneath it.

### GetCashQty()
Returns the current amount of cash the player has.

### GetFuelQty()
Returns the current fuel amount — a thin wrapper over `Player.GetFuel()`. **Confirmed working by live
testing** (see [Snippets](../snippets#read--give-fuel)).

### AddFuelQty(nAmt)
Adds a specified amount of fuel to the player's total. It ensures that the fuel does not exceed the maximum capacity or fall below zero. It also triggers tutorials for low and no fuel conditions.
**Confirmed working, HUD updates** — see [`MrxCheatBootstrap`](mrxcheatbootstrap): `import("MrxPmc");
MrxPmc.AddFuelQty(1000)`. If the amount would exceed the current capacity, raise it first with
`SetFuelCapacity` (below).

### SetFuelCapacity(nFuelCapacity, bCheat, bDoNotSyncFuel)
Sets the player's fuel capacity to a specified value, ensuring it is within the allowed range (`_knMinFuelCapacity` to `_knMaxFuelCapacity`). If `bDoNotSyncFuel` is false and the current fuel exceeds the new capacity, it adjusts the fuel accordingly.
**Confirmed working by live testing**: `MrxPmc.SetFuelCapacity(9999, true)` raises the cap before adding
fuel past the default maximum.

### AddFuelCapacity(nFuelCapacity)
Adds a specified amount to the player's fuel capacity. If the resulting capacity exceeds the maximum or falls below the minimum, it sets the capacity to the respective limit.

### GetFuelCapacity()
Returns the current fuel capacity of the player.

### AddSupportQty(sName, nAmt, bDspFanfare, nCost)
Adds a specified amount of support items to the stockpile. It updates client-side spending data and triggers fanfare if required. It also checks for support thresholds and refreshes mission details.
**Confirmed working** — `sName` keys come from [`MrxSupportData.tSupportData`](mrxsupportdata#support-item-catalog);
see [`MrxCheatBootstrap`](mrxcheatbootstrap)'s "Give one support item" row and "The Works!" snippet (which
loops every key in the catalog, maxing each one out via this function).

### SetSupportQty(sName, nAmt)
Sets the quantity of a specific support item in the stockpile.

### GetSupportQty(sName)
Returns the quantity of a specific support item in the stockpile. Used alongside `AddSupportQty` and
`tData.nMaxStock` (from `MrxSupportData`) to compute "how much more to add to max this item out" — see
the "The Works!" snippet linked above.

### SetSupportNew(sName, bNew)
Marks a specific support item as new or viewed.

### SetAllSupportViewed()
Marks all support items as viewed.

### IsSupportNew(sName)
Checks if a specific support item is marked as new.

### CheckSupportThreshold(sName)
Checks if the quantity of a specific support item meets any set thresholds and triggers callbacks accordingly.

### SetStockpileChangeCallback(sName, sComparison, nThreshold, fCallback, tCallbackArgs)
Sets a callback function to be triggered when the quantity of a specific support item meets a specified threshold.

### DeleteStockpileChangeCallback(nId)
Deletes a previously set stockpile change callback by its ID.

### AddFreebieQty(sName, nAmt)
Adds a specified amount of freebies to the player's inventory.

### SetFreebieQty(sName, nAmt)
Sets the quantity of a specific freebie in the player's inventory.

### GetFreebieQty(sName)
Returns the quantity of a specific freebie in the player's inventory.

### AddEquipment(sName, bDoNotAddCapacity)
Adds a specified equipment item to the player's inventory. If it is a fuel tank, it may also adjust the fuel capacity and spawn a corresponding object in the world.

### RemoveEquipment(sName)
Removes a specified equipment item from the player's inventory. If it is a fuel tank, it adjusts the fuel capacity and removes the corresponding object from the world.

### HasEquipment(sName)
Checks if the player has a specific equipment item in their inventory.

### DisplayCash(nCash, sReason, nChange)
Updates the HUD to display the current cash amount, the reason for the change, and the change itself.

### MapPluralReasonToSingular(sReason)
Maps a plural reason to its singular form using the `_tPluralReasonToSingular` table.

### DisplayResources(nCashChange, nFuelChange)
Updates the HUD to display both the current cash and fuel amounts, as well as any changes.

### AddFuelTank(sName, bModifyCapacity)
Adds a fuel tank to the player's inventory. If `bModifyCapacity` is true, it adjusts the fuel capacity accordingly. It also spawns a corresponding object in the world.

### RemoveFuelTank(sName)
Removes a fuel tank from the player's inventory, adjusting the fuel capacity and removing the corresponding object from the world.

### _OnFuelTankDeath(uGuid)
Handles the death of a fuel tank by adjusting the fuel capacity and updating internal state.

### GetClientReimburseAmount()
Calculates the amount to reimburse the client based on their support spendings and remaining stockpile items.

### NetClientReimburse()
Reimburses the client with the calculated amount and displays a message in the HUD.

### _CreateHiScoreEvent()
Creates a dummy widget to handle high-score events and updates the leaderboard accordingly.

### _HiScoreUpdated(oDummyWidget, tEvent)
Handles the update of the leaderboard by displaying a fanfare event.

### SaveSingleton()

This function saves the current state of the player's PMC resources and equipment. It retrieves the player's cash, fuel, and equipment status, then constructs a table containing this information. The function returns this table, which can be used to save the game state.

- **Returns**: A table with the following fields:
  - `tEquipment`: A table of equipment names as keys and boolean values indicating if they are pristine.
  - `nCash`: The player's current cash value.
  - `nFuel`: The player's current fuel value.
  - `tStockpile`: The current stockpile data.
  - `tFreebies`: The current freebie data.

### LoadSingleton(tSaveData)

This function loads the player's PMC resources and equipment from a previously saved state. It takes a table `tSaveData` as an argument, which should contain the saved game state. If the save data is valid, it updates the player's fuel capacity, equipment status, cash, fuel, stockpile, and freebie data accordingly.

- **Parameters**: 
  - `tSaveData`: A table containing the saved game state with fields similar to those returned by `SaveSingleton()`.

## Events
This module subscribes to and fires several engine events related to player economy management. The key events include:

- **`Event.PlayerJoined` / `Event.PlayerLeft`**: These events are used to handle changes in the co-op player session, ensuring that the player's economy state is correctly synchronized across players.
  
- **`Event.ObjectDeath`**: This event is triggered when a world object (such as a fuel tank) dies. The module uses this event to adjust the player's fuel capacity and update internal state.

- **`Event.TimerRelative`**: This event is used for various timed operations, such as triggering tutorials for low or no fuel conditions.

## Notes for modders
- **This is the go-to module for economy cheats/mods** — `AddCashQty`/`AddFuelQty`/`AddSupportQty` are all
  confirmed working with correct HUD updates; see [`MrxCheatBootstrap`](mrxcheatbootstrap) for a complete
  worked example including a "max out everything" snippet.
- **Prefer the `MrxPmc.*` functions over the lower-level `Player.SetCash`/`Player.AddCash`** — those change
  the real value but skip the HUD-refresh trigger, so what's displayed won't visibly update.
- `sName` arguments for support-item functions come from
  [`MrxSupportData.tSupportData`](mrxsupportdata#support-item-catalog) keys, not free-form strings.
- When adding or removing equipment (`AddEquipment`/`RemoveEquipment`), fuel tanks specifically also spawn
  or remove a corresponding world object and adjust fuel capacity — not a pure data change.
- Some local variables may appear unused or assigned but never read in the decompiled source — a
  decompiler artifact, not intentional logic.