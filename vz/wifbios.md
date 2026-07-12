---
title: WifBios
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 7
inherits: none
tags: [data]
verified: false
---

# WifBios

## Overview
`WifBios` tracks which character/faction dossier entries the player has unlocked for the in-game PDA
database, and holds the static text (title/body/icon key) for each of the game's 22 named dossiers plus a
default placeholder.

## Inheritance
- Inherits from: none — singleton utility module.
- Imports: none.

## Instance pattern
Singleton-state manager. `_tActiveBios` is the set of unlocked dossier ids (keyed `true`); `_tBios` is the
static 24-entry data table (`Default` plus 22 named bios: `BioChris`, `BioJennifer`, `BioMattias`,
`BioAcosta`, `BioAllies`, `BioBlanco`, `BioCarmona`, `BioChina`, `BioDevilbwoy`, `BioEva`, `BioEwan`,
`BioFiona`, `BioJoyce`, `BioMisha`, `BioPeng`, `BioPirates`, `BioPLAV`, `BioRubin`, `BioSolano`, `BioUP`).
Two more module-level fields, `_nNum` and `_sCurrentBio`, are declared but never read or written by any
function in this file — dead fields, the same pattern as `AntiAir`'s `_tLockOnUpdates` elsewhere in this
wiki.

## Functions
### `HasBio()`
True if `_tActiveBios` has at least one entry (counts every key via `pairs()` just to check for
non-emptiness).

### `AddDossierEntry(sCurrentBio)`
Looks `sCurrentBio` up in `_tBios`; if found, marks it active in `_tActiveBios` and forwards the
title/text/icon to `Pda.Database:AddDossierEntry(...)` so it actually shows up in the in-game PDA. Called
directly from story-flow code ([`WifMissionFlow`](wifmissionflow)) and from individual mission scripts —
e.g. `oilcon002.lua` calls `WifBios.AddDossierEntry("BioEwan")` on activation.

### `SaveSingleton()`
Returns `_tActiveBios` directly (not a copy).

### `LoadSingleton(tActiveBios)`
Re-adds every bio flagged `true` in the saved table via `AddDossierEntry` (so it also re-populates the PDA
database on load, not just the internal set). See the guard-logic gotcha below.

## Events
None.

## Notes for modders
- Adding a new dossier just means adding another key to `_tBios` with `sTitle`/`sText`/`sIcon` and calling
  `AddDossierEntry("YourKey")` from wherever should unlock it.
- **Likely bug:** `LoadSingleton`'s second guard is written as:
  ```lua
  if not type(tActiveBios) == "table" then
    return
  end
  ```
  Because `not` binds tighter than `==` in Lua, this parses as `(not type(tActiveBios)) == "table"`.
  `type(...)` always returns a non-empty string, which is truthy, so `not type(tActiveBios)` is always
  `false`, and `false == "table"` is always `false` — **this guard never fires, for any input.**
  [`WifHints`](wifhints)' `LoadSingleton` has the equivalent check written correctly, as
  `type(tSavedActiveHints) ~= "table"`, which is a useful side-by-side if you want to see what this one
  probably meant to say. In practice `LoadSingleton` is only ever called with a table from save data, so
  this doesn't appear to bite in normal use — but it's not the guard the code looks like it's trying to
  write, and a non-table argument here would fall through into `pairs(tActiveBios)` and error instead of
  returning cleanly.
- `_nNum` and `_sCurrentBio` are declared at the bottom of the file but never referenced by any function —
  safe to ignore, likely leftover from an earlier version.
- Saved/loaded from the boot-time save/load conductor ([`xQ!L`](xql)) as part of the overall save state
  (`tActiveBio`).
