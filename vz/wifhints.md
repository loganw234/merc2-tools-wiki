---
title: WifHints
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 9
inherits: none
tags: [world-flow]
verified: false
---

# WifHints

## Overview
`WifHints` is the contextual "ambient VO hint" system for the game's four commentary characters (Fiona,
Ewan, Eva, Misha) — a static pool of one-off VO lines per speaker, each optionally gated by a
faction-attitude condition, plus per-speaker "currently active/unlocked" queues that story/mission code
adds to and removes from as the campaign progresses.

## Inheritance
- Inherits from: none — singleton utility module.
- Imports: `MrxFactionManager`, [`WifFreePlay`](wiffreeplay).

## Instance pattern
Singleton-state manager. `_tActiveHints` (per-speaker array of currently-unlocked hint ids),
`_tLastPlayed` (per-speaker round-robin index into that array), `_tHints` (static data: 4 speakers —
Fiona has 33 hints, Ewan 6, Eva 7, Misha 16).

## Functions
### `HasHint(sSpeaker)`
True if that speaker has at least one active hint that currently passes `_TestHintConstraints`.

### `GetHint(sSpeaker)`
Round-robins through that speaker's active-hint array starting just after `_tLastPlayed[sSpeaker]`,
returning the first one that passes `_TestHintConstraints` (updating `_tLastPlayed` as it goes); returns
nothing if none qualify.

### `_TestHintConstraints(tHintData)`
True unless `tHintData.tFactionAttitudeConstraint` is set, in which case it defers to
`MrxFactionManager.TestAttitude(faction, towardFaction, comparator, attitude)` — e.g.
`{"Gur", "Pmc", ">=", "Friendly"}` for a hint that should only surface once the Guerrillas like the PMC.

### `Reset()`
Clears `_tLastPlayed` only (not `_tActiveHints`) — unlocked hints stay unlocked; only round-robin
position resets.

### `SaveSingleton()` / `LoadSingleton(tSavedActiveHints)`
Save the raw `_tActiveHints` table; load rebuilds both `_tActiveHints` and `_tLastPlayed` from scratch by
replaying `AddActiveHint` for every saved hint id — correctly guarded with
`type(tSavedActiveHints) ~= "table"` (see [`WifBios`](wifbios) for a similar-looking guard elsewhere in
this batch that isn't written correctly).

### `AddActiveHint(sCurrentHint)`
Resolves which speaker owns `sCurrentHint` via `_FindSpeaker`, appends it to that speaker's active list,
and calls `WifFreePlay.StartNag()` — every new hint re-arms the freeplay nag system.

### `RemoveActiveHint(sCurrentHint)`
Removes it from the owning speaker's active list (`table.remove`), clearing the speaker's entry entirely
once empty (using the Lua 5.0-style `table.getn` rather than the `#` length operator used elsewhere in
this same file — harmless here since both agree on a proper array, but an inconsistency worth knowing
about if you're tracing this file's Lua-version lineage).

### `_FindSpeaker(sHint)`
Linear search over `_tHints` for whichever speaker owns `sHint`.

### `UnlockAllHints(sSpeaker)`
Calls `AddActiveHint` for every hint that speaker has, in one shot (used by
[`WifMissionFlow`](wifmissionflow) at story beats like Eva's full introduction).

## Events
None directly — `WifFreePlay.StartNag()` (called from `AddActiveHint`) is what actually arms the
`Event.TimerRelative` chain, inside [`WifFreePlay`](wiffreeplay) itself.

## Notes for modders
- Every hint entry is just `{sCue = "...", tFactionAttitudeConstraint = {...}}` (the constraint is
  optional) — adding a new hint means adding a key under the right speaker in `_tHints` and calling
  `AddActiveHint("YourHintId")` from wherever should unlock it (typically a mission's `fConseq` in
  [`WifMissionFlow`](wifmissionflow)).
- [`WifFreePlay`](wiffreeplay) only ever asks `WifHints.HasHint("Fiona")` — Ewan/Eva/Misha's hint pools
  exist and are unlocked the same way but aren't wired into that particular nag timer; something else (not
  in this file) must be responsible for surfacing them, if anything is.
- `table.getn(...)` in `RemoveActiveHint` is a Lua 5.0-ism still present in this Lua 5.1 codebase —
  functionally fine here (equivalent to `#` on a proper array) but worth knowing if you're pattern-matching
  this file against others for consistency.
