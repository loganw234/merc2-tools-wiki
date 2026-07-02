---
title: MrxRewardData
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [reward, economy]
---

# MrxRewardData

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

## Reward catalog

**Captured by live runtime dump** -- see [Snippets](../snippets) for the general table-dumping approach. 213 entries in `_tRewards`, grouped by faction prefix and collapsed by default (this page would be enormous otherwise). "Support items" is a count, not a list -- see the source excerpt below for what that field actually looks like for a couple of representative entries. "Custom reward" is a raw localization string key, same convention as everywhere else in this wiki -- unresolved, since there's no string table available.

One thing the live dump surfaces that static source-reading wouldn't make obvious: several `nCash` values (e.g. `AllCon008`'s 1,000,000) are references to a lookup table (`_tCashReward.chapter_two_medium` and similar) in source, not literal numbers -- the table below shows the real, resolved value.

<details markdown="1">
<summary>All (33 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `AllCon001` | 10,000,000 | 0 | [AllCon001.Terms.reward] |
| `AllCon002` | 5,000,000 | 0 | - |
| `AllCon003` | 25,000,000 | 0 | [AllCon003.Terms.Reward] |
| `AllCon008` | 1,000,000 | 0 | - |
| `AllCon008_Milestone1` | - | 1 | - |
| `AllCon008_Milestone2` | - | 1 | - |
| `AllCon008_Milestone3` | - | 1 | - |
| `AllCon050` | 1,000,000 | 3 | - |
| `AllCon052` | 1,000,000 | 2 | - |
| `AllCon053` | 1,000,000 | 2 | - |
| `AllJob002_Milestone1` | 1,000,000 | 2 | - |
| `AllJob002_Milestone10` | 10,000,000 | 1 | - |
| `AllJob002_Milestone2` | 1,250,000 | 0 | - |
| `AllJob002_Milestone3` | 1,500,000 | 1 | - |
| `AllJob002_Milestone4` | 2,000,000 | 0 | - |
| `AllJob002_Milestone5` | 2,500,000 | 1 | - |
| `AllJob002_Milestone6` | 3,000,000 | 0 | - |
| `AllJob002_Milestone7` | 4,000,000 | 0 | - |
| `AllJob002_Milestone8` | 5,000,000 | 1 | - |
| `AllJob002_Milestone9` | 7,000,000 | 0 | - |
| `AllJob003_Milestone1` | - | 1 | - |
| `AllJob003_Milestone2` | - | 1 | - |
| `AllJob003_Milestone3` | - | 1 | - |
| `AllJob003_Milestone4` | - | 1 | - |
| `AllJob003_PerTarget` | 50,000 | 0 | - |
| `AllJob020_Milestone1` | - | 1 | - |
| `AllJob020_Milestone2` | - | 1 | - |
| `AllJob020_Milestone3` | - | 1 | - |
| `AllJob020_Milestone4` | - | 1 | - |
| `AllJob020_Milestone5` | - | 1 | - |
| `AllJob020_Milestone6` | - | 1 | - |
| `AllJob020_Milestone7` | - | 1 | - |
| `AllJob020_PerTarget` | 500,000 | 0 | - |

</details>

<details markdown="1">
<summary>AllChi (1 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `AllChiIntro` | - | 13 | - |

</details>

<details markdown="1">
<summary>Chi (34 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `ChiCon001` | 5,000,000 | 0 | - |
| `ChiCon002` | 10,000,000 | 0 | - |
| `ChiCon003` | 25,000,000 | 0 | [AllCon003.Terms.Reward] |
| `ChiCon008` | 1,000,000 | 0 | - |
| `ChiCon008_Milestone1` | - | 0 | - |
| `ChiCon008_Milestone2` | - | 1 | - |
| `ChiCon008_Milestone3` | - | 1 | - |
| `ChiCon009` | 1,000,000 | 0 | - |
| `ChiCon009_Milestone1` | - | 1 | - |
| `ChiCon009_Milestone2` | - | 1 | - |
| `ChiCon009_Milestone3` | - | 1 | - |
| `ChiCon050` | 1,000,000 | 3 | - |
| `ChiCon051` | 1,000,000 | 3 | - |
| `ChiCon053` | 1,000,000 | 2 | - |
| `ChiJob002_Milestone1` | 1,000,000 | 1 | - |
| `ChiJob002_Milestone10` | 10,000,000 | 1 | - |
| `ChiJob002_Milestone2` | 1,250,000 | 0 | - |
| `ChiJob002_Milestone3` | 1,500,000 | 0 | - |
| `ChiJob002_Milestone4` | 2,000,000 | 0 | - |
| `ChiJob002_Milestone5` | 2,500,000 | 1 | - |
| `ChiJob002_Milestone6` | 3,000,000 | 0 | - |
| `ChiJob002_Milestone7` | 4,000,000 | 0 | - |
| `ChiJob002_Milestone8` | 5,000,000 | 0 | - |
| `ChiJob002_Milestone9` | 7,000,000 | 0 | - |
| `ChiJob003_Milestone1` | - | 0 | - |
| `ChiJob003_Milestone2` | - | 0 | - |
| `ChiJob003_Milestone3` | - | 1 | - |
| `ChiJob003_Milestone4` | - | 1 | - |
| `ChiJob003_PerTarget` | 50,000 | 0 | - |
| `ChiJob020_Milestone1` | - | 1 | - |
| `ChiJob020_Milestone2` | - | 1 | - |
| `ChiJob020_Milestone3` | - | 2 | - |
| `ChiJob020_Milestone4` | - | 1 | - |
| `ChiJob020_PerTarget` | 500,000 | 0 | - |

</details>

<details markdown="1">
<summary>Gur (38 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `GurCon001` | 850,000 | 0 | [GurCon001.Terms.BonusPayment] |
| `GurCon002` | 750,000 | 0 | [GurCon002.Terms.BonusPayment] |
| `GurCon003` | 300,000 | 0 | [GurCon003.Objectives.bonus] |
| `GurCon003_Milestone1` | - | 0 | - |
| `GurCon003_Milestone2` | - | 1 | - |
| `GurCon003_Milestone3` | - | 1 | - |
| `GurCon005` | 300,000 | 1 | - |
| `GurCon050` | 300,000 | 2 | - |
| `GurCon052` | 300,000 | 1 | - |
| `GurCon053` | 300,000 | 3 | - |
| `GurIntro` | - | 3 | - |
| `GurJob001_Milestone1` | - | 1 | - |
| `GurJob001_Milestone2` | - | 1 | - |
| `GurJob001_Milestone3` | - | 0 | - |
| `GurJob001_Milestone4` | - | 1 | - |
| `GurJob001_Milestone5` | - | 1 | - |
| `GurJob001_PerTarget` | 5,000 | 0 | - |
| `GurJob002_Milestone1` | 150,000 | 1 | - |
| `GurJob002_Milestone10` | 1,500,000 | 1 | - |
| `GurJob002_Milestone2` | 200,000 | 0 | - |
| `GurJob002_Milestone3` | 250,000 | 0 | - |
| `GurJob002_Milestone4` | 300,000 | 0 | - |
| `GurJob002_Milestone5` | 400,000 | 0 | - |
| `GurJob002_Milestone6` | 500,000 | 0 | - |
| `GurJob002_Milestone7` | 700,000 | 0 | - |
| `GurJob002_Milestone8` | 1,000,000 | 1 | - |
| `GurJob002_Milestone9` | 1,250,000 | 0 | - |
| `GurJob006_Milestone1` | - | 0 | - |
| `GurJob006_Milestone2` | - | 0 | - |
| `GurJob006_Milestone3` | - | 0 | - |
| `GurJob006_Milestone4` | - | 1 | - |
| `GurJob006_PerTarget` | 5,000 | 0 | - |
| `GurJob020_Milestone1` | - | 1 | - |
| `GurJob020_Milestone2` | - | 1 | - |
| `GurJob020_Milestone3` | - | 1 | - |
| `GurJob020_Milestone4` | - | 1 | - |
| `GurJob020_Milestone5` | - | 1 | - |
| `GurJob020_PerTarget` | 300,000 | 0 | - |

</details>

<details markdown="1">
<summary>Mec (1 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `MecCon001` | - | 1 | - |

</details>

<details markdown="1">
<summary>Oil (36 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `OilCon001` | 995,000 | 0 | - |
| `OilCon002` | 500,000 | 2 | - |
| `OilCon003` | 300,000 | 0 | - |
| `OilCon003_Milestone1` | - | 1 | - |
| `OilCon003_Milestone2` | - | 1 | - |
| `OilCon003_Milestone3` | - | 0 | - |
| `OilCon005` | 300,000 | 0 | - |
| `OilCon005_Milestone1` | - | 1 | - |
| `OilCon005_Milestone2` | - | 1 | - |
| `OilCon005_Milestone3` | - | 1 | - |
| `OilCon020` | - | 0 | [OilCon020.Objectives.CustomReward] |
| `OilCon021` | 25,000 | 0 | - |
| `OilCon050` | 300,000 | 3 | - |
| `OilCon051` | 300,000 | 2 | - |
| `OilCon052` | 300,000 | 2 | - |
| `OilJob004_Milestone1` | - | 0 | - |
| `OilJob004_Milestone2` | - | 0 | - |
| `OilJob004_Milestone3` | - | 0 | - |
| `OilJob004_Milestone4` | - | 1 | - |
| `OilJob004_PerTarget` | 5,000 | 0 | - |
| `OilJob008_Milestone1` | - | 0 | - |
| `OilJob008_Milestone2` | - | 0 | - |
| `OilJob008_Milestone3` | - | 1 | - |
| `OilJob008_Milestone4` | - | 1 | - |
| `OilJob008_Milestone5` | - | 1 | - |
| `OilJob008_PerTarget` | 100,000 | 0 | - |
| `OilJob011_Milestone1` | 150,000 | 0 | - |
| `OilJob011_Milestone10` | 1,500,000 | 1 | - |
| `OilJob011_Milestone2` | 200,000 | 0 | - |
| `OilJob011_Milestone3` | 250,000 | 0 | - |
| `OilJob011_Milestone4` | 300,000 | 0 | - |
| `OilJob011_Milestone5` | 400,000 | 1 | - |
| `OilJob011_Milestone6` | 500,000 | 0 | - |
| `OilJob011_Milestone7` | 700,000 | 0 | - |
| `OilJob011_Milestone8` | 1,000,000 | 1 | - |
| `OilJob011_Milestone9` | 1,250,000 | 0 | - |

</details>

<details markdown="1">
<summary>Pir (35 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `PirCon001` | 100,000 | 0 | - |
| `PirCon001_Milestone1` | - | 1 | - |
| `PirCon001_Milestone2` | - | 2 | - |
| `PirCon001_Milestone3` | - | 2 | - |
| `PirCon002` | 20,000 | 0 | - |
| `PirCon002_Milestone1` | - | 1 | - |
| `PirCon002_Milestone2` | - | 1 | - |
| `PirCon002_Milestone3` | - | 1 | - |
| `PirCon003` | 30,000 | 0 | - |
| `PirCon003_Milestone1` | - | 1 | - |
| `PirCon003_Milestone2` | - | 1 | - |
| `PirCon003_Milestone3` | - | 1 | - |
| `PirCon004` | 300,000 | 0 | - |
| `PirCon004_Milestone1` | - | 1 | - |
| `PirCon004_Milestone2` | - | 1 | - |
| `PirCon004_Milestone3` | - | 1 | - |
| `PirCon051` | 300,000 | 2 | - |
| `PirCon052` | 300,000 | 2 | - |
| `PirIntro` | - | 4 | - |
| `PirJob012_Milestone1` | 100,000 | 1 | - |
| `PirJob012_Milestone10` | 1,000,000 | 1 | - |
| `PirJob012_Milestone2` | 125,000 | 0 | - |
| `PirJob012_Milestone3` | 150,000 | 1 | - |
| `PirJob012_Milestone4` | 175,000 | 0 | - |
| `PirJob012_Milestone5` | 200,000 | 1 | - |
| `PirJob012_Milestone6` | 250,000 | 0 | - |
| `PirJob012_Milestone7` | 300,000 | 0 | - |
| `PirJob012_Milestone8` | 500,000 | 1 | - |
| `PirJob012_Milestone9` | 750,000 | 0 | - |
| `PirJob020_Milestone1` | - | 1 | - |
| `PirJob020_Milestone2` | - | 1 | - |
| `PirJob020_Milestone3` | - | 1 | - |
| `PirJob020_Milestone4` | - | 1 | - |
| `PirJob020_Milestone5` | - | 1 | - |
| `PirJob020_PerTarget` | 100,000 | 0 | - |

</details>

<details markdown="1">
<summary>Pmc (34 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `PmcCon001` | 0 | 0 | - |
| `PmcCon002` | 650,000 | 0 | - |
| `PmcCon003` | 0 | 0 | - |
| `PmcCon004` | 25,000,000 | 1 | - |
| `PmcCon013` | - | 0 | - |
| `PmcCon015` | - | 0 | - |
| `PmcCon015_Milestone1` | - | 0 | - |
| `PmcCon015_Milestone2` | - | 0 | - |
| `PmcCon015_Milestone3` | - | 0 | - |
| `PmcCon016` | - | 0 | - |
| `PmcCon016_Milestone1` | - | 0 | - |
| `PmcCon016_Milestone2` | - | 0 | - |
| `PmcCon016_Milestone3` | - | 0 | - |
| `PmcCon018` | - | 0 | - |
| `PmcCon018_Milestone1` | - | 0 | - |
| `PmcCon018_Milestone2` | - | 0 | - |
| `PmcCon018_Milestone3` | - | 0 | - |
| `PmcCon031` | - | 0 | - |
| `PmcCon031_Milestone1` | - | 0 | - |
| `PmcCon032` | - | 0 | - |
| `PmcCon032_Milestone1` | - | 0 | - |
| `PmcCon033` | - | 0 | - |
| `PmcCon033_Milestone1` | - | 0 | - |
| `PmcCon034` | - | 0 | - |
| `PmcCon034_Milestone1` | - | 0 | - |
| `PmcJob001_Milestone1` | - | 1 | - |
| `PmcJob001_Milestone2` | - | 1 | - |
| `PmcJob001_Milestone3` | - | 1 | - |
| `PmcJob001_Milestone4` | - | 1 | - |
| `PmcJob001_Milestone5` | - | 1 | - |
| `PmcJob001_Milestone6` | - | 1 | - |
| `PmcJob001_Milestone7` | - | 1 | - |
| `PmcJob001_Milestone8` | - | 1 | - |
| `PmcJob001_Milestone9` | - | 1 | - |

</details>

<details markdown="1">
<summary>Vza (1 entries)</summary>

| Key | Cash | Support items | Custom reward |
|---|---:|---:|---|
| `VzaCon001` | 0 | 0 | - |

</details>

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