---
title: MrxVerifyManager
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [achievement, target]
verified: true
verified_note: "deeper pass: re-confirmed all functions + no-Event finding + the dead tChangedCallback; documented the real achievement string (ACHIEVEMENT_JUSTICE_FOR_ALL) and that CheckTechnoVikingAchievement never grants (returns bool only), the SetKilledIfNotSet naming trap (sets 'captured', not 'killed'), the '' default status, and the four hardcoded-0 faction getters; cross-linked MrxAchievements and the Player/Pg namespaces"
---

# MrxVerifyManager

*Module: mrxverifymanager.lua*

## Overview
The `MrxVerifyManager` module is responsible for managing and tracking the status of various targets in the game. It handles adding, updating, and removing targets, as well as checking achievements related to target completion. This module also manages callbacks for target status changes and maintains statistics on killed and captured targets.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: [`MrxAchievements`](mrxachievements) — the only import; used to actually grant the achievement.
  GUID↔name lookups go through the engine [`Pg`](../namespaces/pg) namespace (`Pg.GetGuidByName`) and the
  achievement is granted to [`Player`](../namespaces/player)`.GetPrimaryPlayer()`.

## Instance pattern
This is a stateless manager/utility module (module-level globals, no `Create`/`uGuid`/`tInstance` pattern — `Activated()` here is just a plain function, not the `OnActivate`/`Awake` world-object lifecycle). It tracks the following key fields:
- `tTargetListStatus`: A nested table that stores the status of each target, categorized by faction (`All`,
  `Chi`, `Civ`, `Gur`, `Oil`, `Pir`, `Pmc`, `Vza`). **Pre-populated at load** with dozens of named HVT/job
  targets (e.g. `All.AllCon003_HVT`, `Gur.Mendez`, `Pmc.Solano`, `Pmc["PmcCon002 Blanco"]`, and the
  `*Job0NN_Target_NN` sets), each with an initial status of **`""` (empty string), not `"alive"`** — so
  `GetStatus` returns `""` for an untouched target, and the "resolved?" checks throughout compare against
  `"killed"`/`"captured"` specifically. `Civ` and `Vza` are declared but left empty.
- `sSolanoStatus`: The status of the Solano target ("alive", "killed", or "captured"). Starts `"alive"`.
- `tChangedCallback`: A list of callbacks registered via `AddCallback`. Populated but never read or invoked anywhere in this file — no call site iterates it, so it appears to be dead code in this module (or consumed by code outside the decompiled corpus).
- `tTargetGuidList`: A mapping of GUIDs to target names for quick lookup.
- `nKilled` and `nCaptured`: Counters for the number of killed and captured targets, recomputed by `UpdateStats()`.
- `nCount`: Cached total target count, computed once by `GetTotal()` and reused on subsequent calls (starts at `0`, meaning `0 == "not yet computed"` — the count is never legitimately zero since `tTargetListStatus` is pre-populated with dozens of static keys).

## Functions
### `LoadSingleton(tSaveData)`
Loads saved data into the module. If no save data is provided, it does nothing. It logs a debug message and updates the target list status and Solano status from the save data.

### `SaveSingleton()`
Saves the current state of the module to a table. It logs a debug message and returns a table containing the target list status and Solano status.

### `Activated()`
Builds the GUID list for targets when the module is activated.

### `AddTarget(sTargetName, sStatus)`
Adds a new target with the specified name and status. If no status is provided, it defaults to "alive". It updates the target list status and calls functions to update statistics and check achievements.

### `UpdateTarget(sTargetName, sStatus)`
Updates the status of an existing target. If the target's GUID is provided instead of its name, it converts it to the target name. It updates the target list status and calls functions to update statistics and check achievements.

### `_CheckJusticeAchievement()`
Grants the achievement `"ACHIEVEMENT_JUSTICE_FOR_ALL"` (via `MrxAchievements.NetGrantAchievement(..., Player.GetPrimaryPlayer())`)
when `GetCompletedTotal() == GetTotal() - 1` **and** the `AllCon003_HVT` or `ChiCon003_HVT` target is
`"killed"` or `"captured"`. The `- 1` is because the final HVT is the last target and completing it is the
trigger. Called automatically from every status-mutating function (`AddTarget`, `UpdateTarget`,
`SetKilledIfNotSet`, `SetSolanoVerified`).

### `CheckTechnoVikingAchievement()`
Returns `true` when `GetCaptured() == GetTotal() - 1` and the `AllCon003_HVT`/`ChiCon003_HVT` target is
`"captured"` (i.e. everything captured, nothing killed), else `false`. **It only returns a bool — unlike
`_CheckJusticeAchievement`, it never actually grants an achievement.** Something external must call this and
grant the reward itself; no `MrxAchievements.*` call exists in this function.

### `_FindFactionFromName(sName)`
Finds the faction abbreviation associated with a target name by searching through the target list status.

### `BuildGuidList()`
Populates `tTargetGuidList` as a `uGuid → sTargetName` map by resolving every target name through
`Pg.GetGuidByName`. **Gotcha:** it computes `oldCount`/`newCount` with the `#` length operator on
`tTargetGuidList`, but that table is keyed by GUID (an arbitrary/opaque handle, not a 1..N array), so `#`
returns `0` regardless of contents. Those two locals are therefore meaningless — see `FindTargetFromGuid`,
which relies on them.

### `FindTargetFromGuid(uGuid)`
Returns the target name for a GUID, rebuilding the list once and retrying if not found. **Because it
compares `#tTargetGuidList` before/after `BuildGuidList` (both effectively `0`, per the gotcha above),
`oldCount ~= newCount` is never true — so the retry-recursion branch is dead**; a genuinely-unknown GUID
falls straight through to `return nil` rather than retrying. Not fatal (the direct-lookup path still works
once the map is built), but the intended "rebuild and try again" self-heal doesn't actually fire.

### `AddCallback(sTargetName, fCallback, tArgs)`
Adds a callback function to be executed when a target's status changes. It converts the target's GUID to its name if necessary and inserts the callback into the `tChangedCallback` table.

### `UpdateStats()`
Updates the counters for killed and captured targets by iterating through the target list status.

### `GetStatus(sTargetName)`
Retrieves the current status of a target by name. If the target's GUID is provided instead of its name, it converts it to the target name.

### `GetKilled()`
Returns the number of killed targets by updating statistics first.

### `GetCaptured()`
Returns the number of captured targets by updating statistics first.

### `CountCompleted(tTargets)`
Counts the number of completed (killed or captured) targets in a given list of targets.

### `GetCompletedTotal()`
Returns the total number of completed (killed or captured) targets by updating statistics first.

### Per-faction total/completed getters
Sixteen near-identical accessors, two per faction (`GetTotalFaction<F>` / `GetCompleted<F>` for
`F` ∈ `ALL, CHI, CIV, GUR, OIL, PIR, PMC, VZA`). The "total" variant counts entries in
`tTargetListStatus.<Faction>`; the "completed" variant delegates to `CountCompleted(tTargetListStatus.<Faction>)`.

{: .warning }
> **Two of these are hardcoded stubs, not live counts.** `GetTotalFactionVZA`/`GetTotalFactionCIV` always
> `return 0`, and `GetCompletedVZA`/`GetCompletedCIV` always `return "0"` — **a string, not a number.** The
> other twelve return real integers. So the return *type* is inconsistent across the family (number for the
> live ones, `"0"` string for the two stubbed factions), which will bite anything doing arithmetic on the
> result. This matches the empty `Civ`/`Vza` buckets in `tTargetListStatus`.

### `GetTotal()`
Returns the total number of targets across all factions. It caches the count to avoid recalculating it repeatedly.

### `SetKilledIfNotSet(sTargetName)`
Despite the name, this sets the status to **`"captured"`** (not `"killed"`) when the target's current
status is unset, `""`, or `"alive"`. Then updates stats and checks the Justice achievement. Treat the name
as misleading — read it as "mark this target resolved (as captured) if it isn't already."

### `SetSolanoVerified()`
Updates the status of the Solano target based on whether any targets have been killed. It sets the Solano status accordingly, updates the target list status, and checks achievements.

## Events
No `Event.*` calls appear anywhere in this file. `Activated()` (line 90) is presumably invoked by native/engine code (name suggests an activation hook) but has no visible `Event.Create` wiring in this module. All other lifecycle here (target status updates, achievement checks) is driven by direct function calls, not engine events.

## Notes for modders
- Statuses are the strings `"killed"`, `"captured"`, `"alive"`, or `""` (the load-time default). Every
  "is this resolved?" check compares against `"killed"`/`"captured"` — set exactly those, not e.g. `"dead"`.
- `AddTarget`/`UpdateTarget` accept either a name (string) or a GUID (userdata) as the first argument; a
  GUID is resolved to a name via `FindTargetFromGuid`. `UpdateTarget` silently returns if `sStatus` is nil.
- Only the "Justice for All" achievement is granted here (string `"ACHIEVEMENT_JUSTICE_FOR_ALL"`). The
  "Techno Viking" path (`CheckTechnoVikingAchievement`) only *reports* eligibility — whatever grants that
  reward lives elsewhere.
- `AddCallback` is effectively inert in this module: it appends to `tChangedCallback`, but nothing here
  ever iterates or fires that table. Don't rely on registered callbacks being invoked by this file.
- `GetCompletedVZA`/`GetCompletedCIV` return the **string** `"0"`; the other faction getters return
  numbers — don't feed these into arithmetic without normalizing.