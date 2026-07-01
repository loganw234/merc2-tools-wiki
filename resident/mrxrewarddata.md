---
title: mrxrewarddata
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [reward, economy]
---

# mrxrewarddata

*Module: mrxrewarddata.lua*

## Overview
The `mrxrewarddata` module manages reward configurations and dispenses rewards for various game events, missions, and milestones. It handles cash, fuel, mood, support, equipment, and stockpile rewards, as well as custom rewards and wager data. The module also provides functions to generate human-readable descriptions of rewards and handle network-related events.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxUtil`, `WifEquipmentData`, `MrxFactionManager`

## Instance pattern
This is a stateless utility module (no per-instance pattern). It tracks the following key fields:

- `_tCashReward`: A table of cash rewards keyed by reward tier names.
- `_tFuelReward`: A table of fuel rewards keyed by reward tier names.
- `_tMoodReward`: A table of mood rewards keyed by reward tier names.
- `_tRewards`: A large data table containing reward configurations for various missions and events.
- `gtAllSupport`: Cached lists of potential support items for factions.
- `gtAllEquipment`: Cached lists of potential equipment items for factions.
- `_bPrintRewardType`: A boolean flag to control whether reward types are printed in generated strings.

## Functions

### Init()

Initializes the reward data by normalizing support/equipment/stockpile item tuples and setting up back-references to missions and factions.

### GetRewards(uMissionId, uFactionId)

Retrieves the rewards for a given mission ID and faction ID. Returns a table containing the cash, fuel, and mood rewards.

### DispenseRewards(uMissionId, uFactionId)

Dispenses the rewards for a given mission ID and faction ID to the player or relevant faction.

### GrantRewardKey(uPlayerGuid, sRewardKey)

Grants a reward key to the specified player GUID. This function is likely used to unlock specific rewards or items.

### NetEventCallback(uEventId, uPlayerGuid, tData)

Handles network events related to rewards. The `uEventId` specifies the type of event, and `tData` contains additional data relevant to the event.

### GetWagerData(iPercentage, iMin, iMax)

Calculates wager data based on a percentage and minimum/maximum values. Rounds the result to the nearest 1000.

### Init()
Initializes the reward data by iterating through each reward entry in `_tRewards`. For each reward, it sets the mission ID and faction ID based on the reward key. It also processes support, equipment, and stockpile items to ensure they are properly formatted as tables and assigns default values if necessary.

### GetRewards(sRewardKey)
Retrieves the reward data associated with the given `sRewardKey` from `_tRewards`.

### GetAllPotentialShopItems(sFactionId)
Generates lists of potential support and equipment items that can be sold in shops for a specific faction. It caches these lists in `gtAllSupport` and `gtAllEquipment` to avoid redundant calculations.

### DispenseRewards(tRewards, bDisableFanfares)
Dispenses the rewards specified in `tRewards`. This includes adding cash and fuel to the player's PMC account, changing faction attitudes, unlocking support and equipment items, and updating stockpile quantities. If `bDisableFanfares` is set to true, fanfare notifications for unlocked items are disabled.

### DispenseAllRewards()
Dispenses all rewards in `_tRewards` by calling `DispenseRewards` on each entry with fanfares disabled.

### GetRewardKeyFromHash(uNameHash)
Retrieves the reward key associated with a given hash value from `_tRewards`.

### NetEventCallback(nEventId, tArgs)
Handles network events. If the event ID matches `EVENT_GRANTREWARDKEY`, it retrieves the reward key and calls `GrantRewardKey` to grant the reward.

### GrantRewardKey(sRewardKey, nCashOverride)
Grants the reward associated with `sRewardKey`. On the server, it sends a custom network event to clients. On the client, it dispenses the rewards, optionally overriding the cash amount if provided.

### EnableCashRewardHalving(bEnable)
Enables or disables halving of cash rewards based on the boolean value `bEnable`.

### SaveSingleton()
Saves the wager data for each reward in `_tRewards` to a table `tSaveData`. Only rewards with a wager are saved.

### LoadSingleton(tSaveData)
Loads the wager data from `tSaveData` into `_tRewards`, updating the corresponding entries.

### GetWagerData(tRewards)
Calculates and returns the wager data for the given reward. It computes the wager amount based on the player's current cash, the reward's percentage-based wager, and any minimum or maximum wager constraints.

### GenerateRewardString(sMissionId)
Generates a string representation of the rewards associated with a specific mission ID. This includes cash, fuel, support items, equipment items, stockpile quantities, and custom rewards.

### AddCustomReward(sMissionId, sCustomReward)
Adds a custom reward to the list of rewards for a specific mission ID.

### _GenerateStringFromRewardData(tRewards, sPrependedString, sAppendedString)
Generates a string representation of the reward data. It formats each type of reward (cash, fuel, support, equipment, stockpile) into a readable string and appends any custom strings provided.

### `_GetPrintableSupportString(sSupportId)`
This function takes a support ID (`sSupportId`) and returns a printable string representation of the support. It retrieves the support data from `MrxSupportData.tSupportData` using the provided ID. If the support data exists and has a name, it constructs a return string with the support's name. Optionally, if `_bPrintRewardType` is true, it appends a markup code based on the support type (e.g., `[airstrike]`, `[supply]`). If no valid support data or name is found, it returns `nil`.

### `_GetPrintableEquipmentString(sEquipId)`
This function takes an equipment ID (`sEquipId`) and returns a printable string representation of the equipment. It retrieves the equipment data using `WifEquipmentData.GetEquipmentData(sEquipId)`. If `_bPrintRewardType` is true, it checks the type of the equipment:
- For fuel tanks (`knTypeFuelTank`), it returns a formatted string with `[fuelsilo]` and `[Generic.FuelSilo]`.
- For grappling hooks (`knTypeGrapplingHook`), it returns the player-visible name using `WifEquipmentData.GetPlayerVisibleName(sEquipId)`.
If no valid equipment data or type is found, it returns the original equipment ID.

### `_FormatMilestoneString(tMilestoneData, sSingle, sPlural)`
This function formats a milestone string based on the provided milestone data (`tMilestoneData`). It extracts the milestone number and key from `tMilestoneData`, retrieves the corresponding reward data using `GetRewards(sMilestoneKey)`. If no valid reward data is found, it returns `nil`.

It constructs a prepend string based on whether the milestone is singular or plural. If `_bPrintRewardType` is true, it formats the suffix using `_FormatMilestoneSuffix`. It then appends a checkmark (`[check1]` for completed milestones, `[check0]` for incomplete) and generates the reward data string using `_GenerateStringFromRewardData`.

### `_FormatMilestoneSuffix(sSuffix, nNumber)`
This function formats a milestone suffix by appending a number to a given suffix. It checks if both `sSuffix` is a string and `nNumber` is a number. If valid, it returns a formatted string in the form `[suffix:number]`. Otherwise, it returns `nil`.

### `_FormatLevelMilestoneString(tMilestoneData)`
This function formats a level milestone string based on the provided milestone data (`tMilestoneData`). It extracts the milestone key from `tMilestoneData`, retrieves the corresponding reward data using `GetRewards(sMilestoneKey)`. If no valid reward data is found, it returns.

It constructs a prepend string with `[Generic.Level]` followed by the milestone number. It then appends a checkmark (`[check1]` for completed milestones, `[check0]` for incomplete) and generates the reward data string using `_GenerateStringFromRewardData`.

## Events

- **Event.NetCustom (EVENT_GRANTREWARDKEY)**: This module listens for this event to handle granting rewards based on a custom network event. When triggered, it retrieves the reward key and calls `GrantRewardKey` to grant the associated rewards.

## Notes for modders

1. **Call-order requirements**: Ensure that `Init()` is called before any other functions in this module to properly initialize the reward data.
2. **Pitfalls**:
   - Modifying `_tRewards` directly can lead to unexpected behavior if not handled carefully, as changes may affect game mechanics.
   - Be cautious when overriding cash rewards using `GrantRewardKey`, as it can impact player economy balance.
3. **Tunables**: The module uses several tunable values such as wager percentages and minimum/maximum wager constraints. Modifying these values can affect the reward system's behavior.
4. **Decompiler artifacts**:
   - Some local variables in functions like `NetEventCallback` may appear unused or are assigned but never read, which is a decompiler artifact and should be ignored.