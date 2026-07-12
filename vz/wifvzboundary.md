---
title: WifVzBoundary
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 15
inherits: none
tags: [world-flow, boundary]
verified: false
---

# WifVzBoundary

## Overview
Owns the single "world boundary" that fences the player into whatever portion of the map the story has
currently unlocked — the invisible wall (plus a Fiona-voiced warning line and static/radio noise) that
keeps you from wandering into content you haven't reached yet. As the critical-path story advances,
`WifMissionFlow` calls into this module to swap which named boundary volume is active (`Boundary00` through
`Boundary02`, roughly one per act/major story beat), and separately maintains a set of always-on
"exclusion" boundaries used for smaller side pockets (e.g. faction HQ compounds) that layer independently
of the one main boundary. It also has an "interior mode" used to suspend all boundary checks while the
player is inside a building interior.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxCheatBootstrap`](../resident/mrxcheatbootstrap), [`MrxVoSequence`](../resident/mrxvosequence)

## Instance pattern
Singleton-state manager. Key module-level fields:
- `_sBoundaryName`: the currently-active main world boundary's object name, or `nil` if none is set. Only
  one can be active at a time — calling `SetupBoundary` always tears down whatever was active first.
- `_tExclusionBoundaries`: a set (`{[sBoundaryName] = true/false}`) of additional named boundaries enabled
  independently of `_sBoundaryName`, keyed by name; stays `nil` until the first `EnableExclusionBoundary`
  call.
- `_bMapBoundariesDrawn`: dedupe flag so the map/radar line isn't redundantly redrawn.

Both `_sBoundaryName` and `_tExclusionBoundaries` are save-game persisted via `SaveSingleton`/`LoadSingleton`
(called from [`xQ!L`](xql)).

## Functions

### Named boundary presets
`SetupBoundaryIntro()`, `SetupBoundary00()`, `SetupBoundaryINTRO_OIL()`, `SetupBoundaryPOST_OIL()`,
`SetupBoundaryPOST_EVA_PRE_PIR()`, `SetupBoundaryPOST_EVA_POST_PIR()`, `SetupBoundaryPMCCON003()`,
`SetupBoundary02()` — each is a fixed-name wrapper over `SetupBoundary`, one per story checkpoint. Only
`SetupBoundary02` requests the `"[Fanfare.BoundaryExpanded]"` message (`bShowMessage = true`); every other
preset passes `false`. Three of them — `SetupBoundaryPOST_EVA_PRE_PIR`, `SetupBoundaryPOST_EVA_POST_PIR`,
`SetupBoundaryPMCCON003` — additionally guard themselves: they skip calling `SetupBoundary` entirely if
`_sBoundaryName` is already `"Boundary02"`, presumably to stop an out-of-order call from regressing an
already-expanded boundary back to a smaller one. Confirmed called from `WifMissionFlow`/`pmccon003.lua` at
the relevant story beats, and from [`xQ!L`](xql) (`SetupBoundaryIntro`) on a brand-new game with no save
data.

### `SetupBoundary(sBoundaryName, bShowMessage)`
The real entry point behind all the named presets above. Removes any existing world boundary first, sets
`_sBoundaryName`, adds the new boundary to every player and draws it on the map, then — if `bShowMessage`
and the player isn't in a cheat/skip-mode session — shows the `"[Fanfare.BoundaryExpanded]"` message box.

### `RemoveWorldBoundary()`
Clears the currently-active main boundary from every player and the map, and clears `_sBoundaryName`. A
no-op if no boundary is currently set.

### `BoundaryCallback(uPlayer, sType, sAction)`
The actual per-player boundary-crossing handler, registered via `Player.SetBoundaryCallback` (not an
`Event.*` registration — a different callback mechanism). On entering the "out of bounds" area, plays one
of Fiona's warning VO lines and cues a static/radio sound effect; on exiting back into bounds, stops the
static and plays a different randomized VO line. A `bVoDelay` flag (10-second cooldown) throttles the
enter-side VO so it can't retrigger every frame while lingering at the edge.

### Exclusion boundaries: `EnableExclusionBoundary(sBoundaryName, bEnable)` / `RemoveExclusionBoundaries()`
`EnableExclusionBoundary` adds or removes one named boundary from every player independently of the main
world boundary, tracking its on/off state in `_tExclusionBoundaries`. `RemoveExclusionBoundaries` disables
every currently-tracked exclusion boundary and clears the table entirely. Confirmed real caller:
`WifMissionFlow` enables `"Boundary_ALHQ_Exclusion"`/`"Boundary_CHHQ_Exclusion"` at specific faction-HQ
story beats.

### `SetInteriorMode(bEnable)`
Toggles every boundary (main + exclusions) off when entering an interior (`bEnable = true`) and back on
when leaving. Also explicitly clears every player's "out of boundary" flag on enable, so nobody gets stuck
flagged as out-of-bounds while inside a building. Confirmed called from
[`MrxHq`](../resident/mrxhq) on HQ interior enter/exit, and from `WifMissionFlow` at a couple of story
beats that move the player indoors.

### `_AddBoundaryToPlayers(bEnable)`
Internal helper: adds/removes `_sBoundaryName`'s boundary object to every connected player, and wires
`BoundaryCallback` when adding.

### Map drawing: `_DrawWorldBoundaryOnMap(bEnable)` / `_DrawBoundaryOnMap(sBoundaryName, bEnable, bInvert)` / `DrawExclusionBoundaryOnMap(sBoundaryName, bEnable)`
`_DrawBoundaryOnMap` is the shared primitive (adds/removes a line region on both `Hud.Radar` and
`Pda.Map`); `_DrawWorldBoundaryOnMap` calls it for the main boundary with `bInvert = true` (shading
*outside* the boundary, appropriate for a "you can't go past here" line) and dedupes via
`_bMapBoundariesDrawn`; the public `DrawExclusionBoundaryOnMap` calls it for a named exclusion boundary
with `bInvert = false` instead (shading the excluded area itself).

### `SaveSingleton()` / `LoadSingleton(tSaveData, bAutoDeactivate)`
Persists `_sBoundaryName` and `_tExclusionBoundaries` (only if set). On load, always clears any existing
boundary/exclusions first, then — unless `bAutoDeactivate` is true — re-applies the saved boundary and
exclusions through the normal `SetupBoundary`/`EnableExclusionBoundary` calls (redrawing everything and
re-adding to players). If `bAutoDeactivate` **is** true, it restores the internal state
(`_sBoundaryName`, `_tExclusionBoundaries`) and the map line only, but does **not** call
`_AddBoundaryToPlayers` — the boundary is tracked and shown on the map but not actually enforced against
players. [`xQ!L`](xql) passes its own `_bPmcRequired` flag as `bAutoDeactivate`, meaning a save loaded
straight into the PMC HQ (no retry checkpoint) restores the boundary bookkeeping but leaves it inactive
until the player actually exits the HQ interior.

## Events
Doesn't use `Event.Boundary` directly (unlike its sibling VZ modules) — boundary crossings are delivered
through `Player.SetBoundaryCallback`/`BoundaryCallback` instead, a different, player-object-level
mechanism.

## Notes for modders
- **Only one main boundary can be active at a time.** Calling any `SetupBoundary*` preset (or
  `SetupBoundary` directly) always tears down whatever was active before setting the new one.
- Exclusion boundaries are independent and additive — you can have the main boundary plus any number of
  named exclusions active simultaneously; they don't interact with each other, unlike the exclusive main
  boundary.
- `SetInteriorMode(true)` is the correct way to suspend boundary enforcement entirely (e.g. for a custom
  interior space) without losing track of what the boundary should be once you call
  `SetInteriorMode(false)` again.
- All public functions here are server-authoritative — every one of them (except the read-only
  `SaveSingleton`) starts with `if Net.IsClient() then return end`, so calling any of them from client-side
  code is silently a no-op.
