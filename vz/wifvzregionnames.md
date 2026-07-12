---
title: WifVzRegionNames
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 16
inherits: none
tags: [world-flow, poi]
verified: false
---

# WifVzRegionNames

## Overview
Despite the filename, this isn't a plain name/label lookup table — it's the point-of-interest (POI) system
that shows a map-label popup (`Hud.MapLabel`) the first time the player enters any of ~38 named world
regions (Caracas, Maracaibo, Angel Falls, the various faction HQs, etc.), and for about half of them, plays
one of Fiona's one-time descriptive VO lines the first time you arrive. It also independently toggles the
rarity of "Dangerous Building" random encounters off while inside Caracas specifically, and back on once
you leave.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxPlayState`](../resident/mrxplaystate), [`MrxState`](../resident/mrxstate),
  [`MrxVoSequence`](../resident/mrxvosequence), [`DangerousBuilding`](../resident/dangerousbuilding)

## Instance pattern
Singleton-state manager. `tBoundaryList` is both the static POI catalog *and* mutable state in the same
table: each of its ~38 entries is keyed by a `poi_*` boundary object name, with either an empty table
(label-only, no VO) or `{VO = "Fiona.POI.SomeLine01"}`. Once a POI's VO line has played, this same file sets
`tBoundaryData.bVoPlayed = true` directly on that entry — mutating the "static" catalog table in place to
double as its own played/not-played tracker. `_tBoundaryEvents` is a separate, purely transient table of
live event handles keyed by POI name, rebuilt every `Start()`.

**Confirmed external reader:** `resident/mrxguipda.lua` (the PDA/map GUI) reads
`WifVzRegionNames.tBoundaryList` directly (`for sGuidName, sName in pairs(WifVzRegionNames.tBoundaryList)`)
— so this table's key set doubles as at least part of the PDA's own list of known map locations, not just
this module's private data.

## Functions

### `Start()`
Clears and rebuilds every tracked boundary event from scratch (deletes all of `_tBoundaryEvents` first),
re-registers an `"enter"` watch for every POI in `tBoundaryList`, then calls `SetupDBBoundary()`. Called
once at boot by [`xQ!L`](xql)'s `_GameplaySetup_LoadWorldState`.

### `SetupDBBoundary()` / `DisableDBs()`
A self-perpetuating pair, independent of the POI system above, both watching the single `"DisableDBs"`
boundary object: `SetupDBBoundary` sets `DangerousBuilding` rarity back to `"default"` (re-enabling the
system generally) and arms a watch for entering that boundary, which calls `DisableDBs`; `DisableDBs` sets
rarity to `"never"` (fully suppressing Dangerous Buildings) and arms a watch for exiting the same boundary,
which calls `SetupDBBoundary` again. Net effect: Dangerous Buildings are suppressed specifically while
inside whatever `"DisableDBs"` marks out (Caracas, per the log message text), and restored everywhere else.

### `SetupBoundaryEvent(sBoundaryName, sAction)`
Registers a single `Event.Boundary` watch for the local player crossing the named POI boundary, but only
if that boundary resolves to a real object *and* there isn't already a tracked event for that name — a
guard against double-registering the same POI.

### `CrossedBoundary(sBoundaryName, uPlayerGuid, uBoundaryGuid, sAction)`
On `"enter"`: clears its own tracked event entry, shows the map label (`Hud.MapLabel:Show`) if the
boundary object has a localized name, and — if this POI has a `VO` line, hasn't played it yet, the player
is in freeplay (`MrxPlayState.IsFree()`), and the game isn't in a locked/cutscene state
(`not MrxState.IsLocked()`) — plays that VO line and marks `bVoPlayed = true` so it never repeats. Either
way, re-arms watching for `"exit"`. On `"exit"`: just re-arms watching for `"enter"` again.

### `SaveSingleton()` / `LoadSingleton(tSaveData)`
Persists which POIs have already had their one-time VO played, as a plain array of POI names (not a
`bVoPlayed`-keyed map). `LoadSingleton` walks that array and re-sets `bVoPlayed = true` on the matching
`tBoundaryList` entries so already-visited POIs don't replay their VO after a reload.

{: .warning }
> **Confirmed from source:** `SaveSingleton`'s `tSaveData = {}` is not declared `local` — it's a bare
> assignment, which in Lua creates a real global variable rather than a function-local one. This is a
> genuine source-level quirk, not a decompiler artifact (the identical unlocalized pattern shows up in
> `resident/mrxtask.lua` too, so it isn't unique to this file). It appears harmless in practice — nothing
> else in this corpus reads a global named `tSaveData` — but every call to this function does leak/
> overwrite a global table as a side effect.

## Events
- `Event.Boundary` — every registration in this file, both for the ~38 POIs and the separate
  `"DisableDBs"` pair, alternating `"enter"`/`"exit"` per crossing, same self-perpetuating pattern as
  [`WifVzAmbience`](wifvzambience)/[`WifVzAtmosphere`](wifvzatmosphere).

## Notes for modders
- To add a new POI: add `poi_yourname = {}` (label only) or `poi_yourname = {VO = "Some.Vo.Line"}` (label +
  one-time VO) to `tBoundaryList`, and make sure a boundary object of that exact name exists in the level.
  `Start()` picks up new entries automatically on the next boot/level load — no other wiring needed.
- The `bVoPlayed` flag lives on the same table entry as the POI's static config, and is what's actually
  persisted (indirectly, as a name list) by `SaveSingleton`. If you add a POI at runtime after `Start()`
  has already run, remember to also call `SetupBoundaryEvent` for it yourself.
- The Dangerous-Building suppression (`SetupDBBoundary`/`DisableDBs`) is entirely separate from the POI
  label/VO system even though it lives in the same file and uses the same `Event.Boundary` mechanism —
  don't confuse `"DisableDBs"` for one of the `poi_*` entries.
