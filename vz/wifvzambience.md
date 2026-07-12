---
title: WifVzAmbience
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 13
inherits: none
tags: [world-flow, ambience]
verified: false
---

# WifVzAmbience

## Overview
A small, generic boundary-triggered ambient-sound-cue system: cross into a named world boundary volume and
it cues an ambience sound stream; cross back out and it stops that stream. It's the same
enter/exit-boundary-crossing architecture used by [`WifVzAtmosphere`](wifvzatmosphere) and
[`WifVzRegionNames`](wifvzregionnames), just wired to `Sound.CueAmbience`/`Sound.StopAmbience` instead of
sky presets or one-time VO lines.

**Confirmed from source: `tBoundaryList` ships completely empty.** It's declared as `{}` at the top of the
file, and nothing anywhere else in this corpus (checked by direct search) ever inserts a boundary
name/ambience-stream pair into it. `Start()` (called once at boot from [`xQ!L`](xql)) faithfully iterates
`pairs(tBoundaryList)` and would set up a boundary-crossing event for each entry — but since the table has
zero entries, that loop currently does nothing. As shipped, this module is fully wired and functional but
entirely inert.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
Singleton module-level state, though minimal: `tBoundaryList` is the one piece of state (a plain data
table intended to map a boundary object name to an ambience stream name), declared empty and never
populated anywhere in this corpus. Not per-`uGuid`.

## Functions

### `Start()`
Iterates every entry in `tBoundaryList` and calls `SetupBoundaryEvent(uBoundaryGuid, sAmbienceStream,
"any")` for each — `Pg.GetGuidByName(sBoundary)` resolves the configured boundary name to a live object
first. Called once at boot by [`xQ!L`](xql)'s `_GameplaySetup_LoadWorldState`. With `tBoundaryList` empty,
this is currently a no-op in practice.

### `SetupBoundaryEvent(uBoundaryGuid, sAmbienceStream, sAction)`
Registers an `Event.Boundary` watch for the local player crossing `uBoundaryGuid` in direction `sAction`
(`"any"`, `"enter"`, or `"exit"`), calling `CrossedBoundary` with the stream name when it fires. Guarded on
`uBoundaryGuid` being non-nil — a boundary name that didn't resolve to a live object is silently skipped.

### `CrossedBoundary(sAmbienceStream, uPlayerGuid, uBoundaryGuid, sAction)`
The crossing callback: on `"enter"` cues the ambience stream (`Sound.CueAmbience`) and re-arms itself
watching for `"exit"`; on `"exit"` stops the stream (`Sound.StopAmbience`) and re-arms watching for
`"enter"` again — a self-perpetuating enter/exit toggle, the same pattern `WifVzAtmosphere` and
`WifVzRegionNames` both use.

## Events
- `Event.Boundary` — the only event type this module uses, registered/re-registered per `tBoundaryList`
  entry by `SetupBoundaryEvent`, alternating between watching for `"enter"` and `"exit"` each time it
  fires.

## Notes for modders
- **This system is a ready-made hook for ambient sound**, just missing data. To use it: either add entries
  directly to `tBoundaryList` (`sBoundaryName = sAmbienceStreamName`) before `Start()` runs, or call
  `WifVzAmbience.SetupBoundaryEvent(Pg.GetGuidByName("some_boundary"), "some_stream_name", "any")` directly
  at runtime — the underlying machinery (event wiring, enter/exit toggling) is already correct and doesn't
  need to be touched.
- No `SaveSingleton`/`LoadSingleton` — unlike [`WifVzBoundary`](wifvzboundary) and
  [`WifVzRegionNames`](wifvzregionnames), this module carries no persisted state, consistent with it never
  actually holding any live data as shipped.
- It's only ever `import()`-ed by [`xQ!L`](xql) (confirmed by corpus-wide search) — nothing else in the
  game currently talks to this module at all.
