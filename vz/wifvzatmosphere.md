---
title: WifVzAtmosphere
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 14
inherits: none
tags: [world-flow, atmosphere]
verified: false
---

# WifVzAtmosphere

## Overview
Drives the open-world sky/weather preset (`Graphics.Atmosphere.SetSky`) based on which named atmosphere
boundary region the local player is currently standing inside — e.g. an underground cave gets an
`"afternoon"` sky override, Caracas gets its own `"Maracaibo"` preset, and leaving every configured region
reverts to a hardcoded default. Same boundary-crossing architecture as [`WifVzAmbience`](wifvzambience) and
[`WifVzRegionNames`](wifvzregionnames), wired to sky presets instead of sound cues or VO lines.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
Singleton module-level state: `tBoundaryList` maps a boundary object name to a one-argument function
(`function(bEnter) ... end`) that applies the atmosphere setting for that region. Shipped with 4 real
entries:

| Boundary name | Effect on enter |
|---|---|
| `rgn_atmo_GRstripmine` | Empty function body — registered but does nothing |
| `rgn_atmo_GR Cave` | `Graphics.Atmosphere.SetSky("afternoon")` |
| `rgn_atmo_Caracas` | `Graphics.Atmosphere.SetSky("Maracaibo")` |
| `rgn_atmo_PMC Outpost` | `Graphics.Atmosphere.SetSky("afternoon")` |

No `SaveSingleton`/`LoadSingleton` — nothing here is persisted; every session just re-derives the correct
sky from wherever the player physically is when `Start()` runs.

## Functions

### `SetDefaultAtmosphere()`
Sets the sky to `"afternoon"` — the fallback used both at boot and whenever the player leaves every
configured atmosphere region.

### `Start()`
Applies the default atmosphere, then calls `SetupBoundaryEvents()`. Called once at boot by
[`xQ!L`](xql)'s `_GameplaySetup_LoadWorldState`.

### `SetupBoundaryEvents()`
Registers an `"enter"` boundary watch for every entry in `tBoundaryList`. **Defers itself** if
`Sys.IsLoadingOrStreaming` exists and returns true (or the local character doesn't exist yet) —
reschedules via a 2-second `Event.TimerRelative` retry loop until the world/character is actually ready,
rather than registering boundary events against a player that may not exist yet.

### `SetupBoundaryEvent(uBoundaryName, sBoundaryName, sAction)`
Registers a single `Event.Boundary` watch for the local player crossing the named boundary in direction
`sAction`, routing to `CrossedBoundary`. (The parameter naming here is a little confusing in the source
itself — the first parameter is actually the already-resolved `uGuid`, not a name, despite being called
`uBoundaryName`.)

### `CrossedBoundary(sBoundaryName, uPlayerCharacter, uBoundaryGuid, sAction)`
On `"enter"`: looks up and calls this region's atmosphere function with `true`, then re-arms watching for
`"exit"`. On `"exit"`: calls the same function with `false`, then checks whether the player is now outside
*every* configured region (`Object.InsideBoundary` against each in turn) — if so, calls
`SetDefaultAtmosphere()` — then re-arms watching for `"enter"` again.

**Worth noting:** the per-region functions in `tBoundaryList` only ever call `Graphics.Atmosphere.SetSky`
unconditionally — they accept a `bEnter` argument but none of the 4 shipped functions actually branch on
it (each would apply the same `SetSky` call whether invoked with `true` or `false`). In practice this
doesn't matter because `CrossedBoundary`'s own `"exit"` handling separately falls back to
`SetDefaultAtmosphere()` once you're outside all regions — but a modder adding an overlapping region
should be aware the per-region function itself won't revert anything unless written to branch on `bEnter`.

## Events
- `Event.Boundary` — the only event type used for region tracking, alternating `"enter"`/`"exit"`
  registration per region, same pattern as [`WifVzAmbience`](wifvzambience).
- `Event.TimerRelative` — a 2-second self-retry in `SetupBoundaryEvents` while the world is still
  loading/streaming or no local character exists yet.

## Notes for modders
- To add a new atmosphere region: add `["your_boundary_name"] = function(bEnter)
  Graphics.Atmosphere.SetSky("your_preset") end` to `tBoundaryList` before `Start()` runs (or call
  `SetupBoundaryEvent` directly at runtime for a region added later).
- `rgn_atmo_GRstripmine`'s empty function body means entering that specific boundary currently changes
  nothing — confirmed directly from source, not a guess.
- This module doesn't know or care about save/load; it just re-evaluates the player's physical position
  every time `Start()` runs, so nothing needs to be persisted for it to work correctly on reload.
