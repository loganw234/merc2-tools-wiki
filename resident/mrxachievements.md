---
title: MrxAchievements
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [achievement, faction]
verified: true
verified_note: "deeper pass: re-confirmed Imports (MrxFactionManager only), Events, and all functions against source; added the tAchievementsList catalog shape + representative nRequiredCount thresholds, flagged that AchievementAddCount_MASTER_HIJACK targets three achievement ids not present in tAchievementsList (so they log 'No such an achievement'), replaced boilerplate modder notes"
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
Adds `+1` to `"ACHIEVEMENT_MASTER_HIJACK"`, `"ACHIEVEMENT_MASTER_5_HIJACK"`, and
`"ACHIEVEMENT_MASTER_10_HIJACK"` for the given players.

{: .note }
> None of those three ids appear in `tAchievementsList`, so each `AchievementAddCount` call falls through the
> not-found branch and logs `"... Failed: No such an achievement."` — i.e. this function currently records
> nothing. If you're adding hijack-mastery achievements, you must also add these ids to `tAchievementsList`.

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

## Achievement catalog

`tAchievementsList` is a flat 41-entry array of `{sName, nRequiredCount}`. `nRequiredCount` is the count
threshold before the achievement unlocks (`Pg.AchievementAddCount` is passed the entry's **0-based index**
`i - 1` as the counter ID). Most are single-shot (`nRequiredCount = 1`); the count-based ones are the
interesting tunables, e.g.:

| Achievement | Required count |
|---|---:|
| `ACHIEVEMENT_NOTHIN_BUT_GOODTIME` | 200 |
| `ACHIEVEMENT_HAIL_AND_KILL` / `_HOLY_SMOKE` / `_LITTLE_SAVAGE` / `_QUICK_OR_DEAD` | 50 |
| `ACHIEVEMENT_SHOOTTHRILL` | 25 |
| `ACHIEVEMENT_ARMAGGEDON` / `_DAMAGE_INC` | 20 |
| `ACHIEVEMENT_HEAVY_METAL_THUNDER` | 10 |
| `ACHIEVEMENT_DIGITAL_MAN` / `_BURN_THE_SKY` | 5 |
| `ACHIEVEMENT_HIGHWAY_TO_HELL` | 3 |

The five max-relation faction achievements (`STAND_UP_AND_SHOUT`, `FOREVER_FREE`, `ISLAND_DOMINATION`,
`LONGING_FOR_FIRE`, `DIRTY_DEEDS`) are the ones [`MrxFactionManager`](mrxfactionmanager) grants on hitting
max relation.

## Notes for modders
- **Grant path**: use `NetGrantAchievement(sName)` for a plain grant (server broadcasts to clients);
  `AchievementAddCount(sName, nDelta, vPlayers, bCustomEvent)` for count-based ones — pass `bCustomEvent = true`
  if you want the delta replicated to remote players.
- **Every function looks the name up in `tAchievementsList` first.** An id not in that table silently no-ops
  (logs `"... Failed: No such an achievement."`). Add your id to the list before granting/counting it.
- **The "turn everyone hostile" achievement** (`ACHIEVEMENT_NO_MORE_MR_NICE_GUY`) is wired via five
  `MrxFactionManager.CreateAttitudeChangeEvent(..., "Hostile")` hooks flipping `nAlliedMood`/`nChinaMood`/
  `nGuerillaMood`/`nOCMood`/`nPirMood` to `1`; it grants only once all five are `1`. Those mood globals are
  never re-set to `0` in this file, so it's effectively a one-way latch per session.
- **`tSupportFilter`** excludes the delivery/pickup support modules from the coop `ACHIEVEMENT_DAMAGE_INC`
  trigger; add a module name there to exclude your custom support from that achievement.