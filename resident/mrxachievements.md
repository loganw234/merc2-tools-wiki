---
title: MrxAchievements
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [achievement, faction]
---

# MrxAchievements

*Module: mrxachievements.lua*

## Overview
The `MrxAchievements` module is responsible for managing and tracking player achievements in the game. It handles granting achievements, adding counts to achievements, checking if an achievement has been granted, and processing support events that may trigger certain achievements. Additionally, it manages faction mood changes that can unlock specific achievements.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxFactionManager`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `tSupportUsed`: A table to keep track of used support types.
- `tSupportUsedInCoop`: A table to keep track of used support types in coop mode.
- `tSupportFilter`: A filter table for specific support modules that do not trigger achievements.
- `tAchievementsList`: A list of all available achievements with their names and required counts.

## Functions
### `GetNameFromHash(nameHash)`
Converts a hash value to the corresponding achievement name. Returns the achievement name if found, otherwise logs an error message and returns `nil`.

### `NetEventCallback(nType, tArgs)`
Handles network events related to achievements. It processes different types of events (`EVENT_GRANTACHIEVEMENT`, `EVENT_ACHIEVEMENTGRANT`, `EVENT_ACHIEVEMENTADDCOUNT`) and calls the appropriate functions based on the event type.

### `NetGrantAchievement(sAchievementName, vPlayers)`
Grants an achievement to specified players. It checks if the players are local or remote and sends the appropriate network events to grant the achievement.

### `GetLocalRemote(vPlayers)`
Determines whether the specified players are local or remote. Returns two boolean values indicating if there are local and remote players.

### `AchievementGrant(sAchievementName, vPlayers)`
Grants an achievement to the specified players. It checks if the achievement exists in the list and updates it using `Pg.AchievementAddCount`.

### `AchievementAddCount(sAchievementName, nDeltaCount, vPlayers, bCustomEvent)`
Adds a count to an achievement for the specified players. It checks if the achievement exists in the list and updates it using `Pg.AchievementAddCount`. If `bCustomEvent` is true, it sends a network event.

### `AchievementIsGranted(sAchievementName)`
Checks if an achievement has been granted. Returns `true` if the achievement is granted, otherwise logs an error message and returns `false`.

### `AchievementAddCount_MASTER_HIJACK(vPlayers)`
Adds counts to specific achievements related to hijacking missions for the specified players.

### `FactionMoodAchievements()`
Sets up faction mood change events that trigger the "ACHIEVEMENT_NO_MORE_MR_NICE_GUY" achievement when all factions become hostile towards the PMC. It also sets up a persistent event to process support events that may trigger the "ACHIEVEMENT_DAMAGE_INC" achievement.

### `ProcessSupportEvent(tData)`
Processes support events and checks if they should trigger the "ACHIEVEMENT_DAMAGE_INC" achievement. If the support type is filtered or already used in coop, it returns early.

### `SaveSingleton()`
Saves the current state of `tSupportUsed` and `tSupportUsedInCoop` to a table for saving purposes.

### `LoadSingleton(tSaveData)`
Loads the saved state of `tSupportUsed` and `tSupportUsedInCoop` from the provided save data. If no save data is available, it initializes these tables as empty.

## Events
- Listens for custom network events (`EVENT_GRANTACHIEVEMENT`, `EVENT_ACHIEVEMENTGRANT`, `EVENT_ACHIEVEMENTADDCOUNT`) to handle achievement granting and counting.
- Listens for faction mood change events to trigger the "ACHIEVEMENT_NO_MORE_MR_NICE_GUY" achievement.
- Listens for persistent script events (`SupportUsed`) to process support events that may trigger achievements.

## Notes for modders
- Ensure that `NetGrantAchievement` is called appropriately to grant achievements to players.
- Use `AchievementAddCount` to add counts to achievements and check if they have been granted using `AchievementIsGranted`.
- Customize the list of achievements in `tAchievementsList` as needed, but be cautious with achievement names to avoid conflicts.
- Be aware that faction mood changes can trigger specific achievements, so consider how these might interact with your mod's gameplay.