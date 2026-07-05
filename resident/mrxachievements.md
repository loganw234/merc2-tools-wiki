---
title: MrxAchievements
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [achievement, faction]
verified: true
verified_note: rewrote Events section — the EVENT_* names are custom net-event type constants dispatched through NetEventCallback/Net.SendCustomEvent, not Event.* engine constants; only real Event.* reference in the file is Event.ScriptEvent via Event.CreatePersistent in FactionMoodAchievements. All 12 top-level functions were already documented; no additions needed there.
---

# MrxAchievements

*Module: mrxachievements.lua*

## Overview
The `MrxAchievements` module is responsible for managing and tracking player achievements in the game. It handles granting achievements, adding counts to achievements, checking if an achievement has been granted, and processing support events that may trigger certain achievements. Additionally, it manages faction mood changes that can unlock specific achievements.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxFactionManager`

## Instance pattern
This is a stateless singleton/utility module — no `inherit()`, no `getfenv():Create()`, no `tInstance`/
`uGuid`-keyed instances anywhere in the file. All state is plain module-level globals:
- `tSupportUsed`, `tSupportUsedInCoop`: tables tracking used support types (declared at module scope but
  only ever read/written via `SaveSingleton`/`LoadSingleton` in this file — `ProcessSupportEvent` reads
  and writes `tSupportUsedInCoop` directly by support name).
- `tSupportFilter`: a static lookup table of support-module names (`MrxSupportTransit`,
  `MrxBoatDelivery`, `MrxCrateDelivery`, `MrxSoldierDelivery`, `MrxSupportCopterDelivery`,
  `MrxSupportPickup`) that are excluded from triggering the coop "damage inc" achievement.
- `tAchievementsList`: a static array of `{sName, nRequiredCount}` entries for every achievement in the
  game — used as the source of truth by `GetNameFromHash`, `AchievementGrant`, `AchievementAddCount`, and
  `AchievementIsGranted` (matched by `sName`, with the achievement's list index passed to
  `Pg.AchievementAddCount`/`Pg.AchievementIsGranted` as a 0-based counter ID via `i - 1`).
- `EVENT_GRANTACHIEVEMENT`, `EVENT_ACHIEVEMENTGRANT`, `EVENT_ACHIEVEMENTADDCOUNT`: integer constants
  (0, 1, 2) used as the custom net-event type tag dispatched through `Net.SendCustomEvent(...)` and
  received via `NetEventCallback` — **not** `Event.*` engine event constants (see Events below).
- `nAlliedMood`, `nChinaMood`, `nGuerillaMood`, `nOCMood`, `nPirMood`: set as bare globals (no
  declaration/initialization visible in this file) inside the closures created by
  `FactionMoodAchievements`, one per faction, flipped to `1` when that faction turns hostile to the PMC.

## Functions
### `GetNameFromHash(nameHash)`
Converts a hash value to the corresponding achievement name. Returns the achievement name if found, otherwise logs an error message and returns `nil`.

### `NetEventCallback(nType, tArgs)`
Handles network events related to achievements. It processes different types of events (`EVENT_GRANTACHIEVEMENT`, `EVENT_ACHIEVEMENTGRANT`, `EVENT_ACHIEVEMENTADDCOUNT`) and calls the appropriate functions based on the event type.

### `NetGrantAchievement(sAchievementName, vPlayers)`
If `vPlayers` is not provided, grants directly via `Net.GrantAchievement(sAchievementName)` and, if this
is the server, broadcasts `EVENT_GRANTACHIEVEMENT` to all clients. If `vPlayers` is provided (a table of
GUIDs, or a single userdata GUID wrapped into a one-element table; returns early for any other type),
splits the list into local vs. remote via `Player.IsLocal`, grants locally if any local player is in the
list, and — if any remote player is present and this is the server — broadcasts `EVENT_GRANTACHIEVEMENT`.

### `GetLocalRemote(vPlayers)`
Determines whether the specified players are local or remote. Returns two boolean values indicating if there are local and remote players.

### `AchievementGrant(sAchievementName, vPlayers)`
Grants an achievement to the specified players. It checks if the achievement exists in the list and updates it using `Pg.AchievementAddCount`.

### `AchievementAddCount(sAchievementName, nDeltaCount, vPlayers, bCustomEvent)`
Adds a count to an achievement for the specified players. It checks if the achievement exists in the list and updates it using `Pg.AchievementAddCount`. If `bCustomEvent` is true, it sends a network event.

### `AchievementIsGranted(sAchievementName)`
Looks up `sAchievementName` in `tAchievementsList`; if found, returns whatever
`Pg.AchievementIsGranted(sAchievementName, i - 1, tAchievement.nRequiredCount)` reports (`true`/`false`).
If the name isn't in the list at all, logs `"AchievementIsGranted(...) Failed: No such an achievement."`
and returns `false` — the error log fires only for an unrecognized achievement name, not merely an
ungranted one.

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
- **`Event.ScriptEvent`** (the only real `Event.*` constant referenced in this file) — registered via
  `Event.CreatePersistent(Event.ScriptEvent, {"SupportUsed", function() return true end},
  ProcessSupportEvent)` inside `FactionMoodAchievements`. Fires `ProcessSupportEvent` for every
  `"SupportUsed"` script event, unconditionally (the filter function always returns `true`).
- **Custom net events, not `Event.*` constants:** `NetEventCallback(nType, tArgs)` is this module's
  handler for `Net.SendCustomEvent("MrxAchievements", ...)` messages, dispatching on the integer type tag
  `EVENT_GRANTACHIEVEMENT` (0), `EVENT_ACHIEVEMENTGRANT` (1), or `EVENT_ACHIEVEMENTADDCOUNT` (2). These
  are this module's own constants, wired through the engine's generic custom-net-event mechanism — they
  are not `Event.Create`/`Event.*` engine event registrations.
- **`MrxFactionManager.CreateAttitudeChangeEvent`** (called 5 times in `FactionMoodAchievements`, once per
  faction: `All`/`Gur`/`Chi`/`Oil`/`Pir` vs `Pmc` going `Hostile`) is a call into another module's API, not
  an `Event.*` constant either — each callback flips that faction's mood global to `1` and grants
  `"ACHIEVEMENT_NO_MORE_MR_NICE_GUY"` once all five moods are `1`.
- No other `Event.Create`/`Event.CreatePersistent` calls exist in this file. There is no
  `OnActivate`/`OnDeactivate`/`OnDeath` in this module — it's a pure logic/utility singleton, not a
  world-object script.

## Notes for modders
- Ensure that `NetGrantAchievement` is called appropriately to grant achievements to players.
- Use `AchievementAddCount` to add counts to achievements and check if they have been granted using `AchievementIsGranted`.
- Customize the list of achievements in `tAchievementsList` as needed, but be cautious with achievement names to avoid conflicts.
- Be aware that faction mood changes can trigger specific achievements, so consider how these might interact with your mod's gameplay.