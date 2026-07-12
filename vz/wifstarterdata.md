---
title: WifStarterData
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 12
inherits: none
tags: [data]
verified: false
---

# WifStarterData

## Overview
The static per-faction catalog of every "starter" NPC in the game — the mission-giving character standing
at each faction HQ/outpost who hands out that faction's contracts (distinct from the four PMC-specific
bosses, whose runtime behavior lives in [`WifPmcInterior`](wifpmcinterior) but whose catalog entries are
still defined here alongside everyone else's). ~30 entries total: 5 for Allied Nation, 5 for China, 5 for
Guerilla, 6 for Oil Company, 3 for Pirates, plus the Jet/Mec recruitment bosses and the four PMC starters.
Each entry describes which actor template/hardpoint to spawn, voice bank, FaceFX set, and (for the
roster-card starters) the PDA contact-card text. The actual runtime "starter" object/state machine is
`MrxStarterManager`/`MrxStarter` elsewhere — this file is purely the data those systems are built from.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
Almost entirely static data (~30 top-level tables, one per starter, e.g. `AllStarter0`..`AllStarter4`,
`ChiStarter0`..`ChiStarter4`, `GurStarter0`/`1`/`2`/`4`/`5`, `OilStarter0`..`OilStarter5`,
`PirStarter1`/`3`/`4`, `JetBoss`, `MecBoss`, `PmcBoss`, `HelPmcBoss`, `MecPmcBoss`, `JetPmcBoss`), plus
`_sStarters` (a flat array of all their names, confirmed read directly by
[`MrxStarterManager`](../resident/mrxstartermanager) to enumerate every starter that exists). `Init()`
does perform light one-time mutation on top of that static data — see below — which is enough to make this
a singleton-state module rather than a purely stateless one, even though the vast majority of its content
never changes after load.

## Functions

### `Init()`
Walks every starter grouped by faction and, for any non-boss entry with a `sVoBankName`, builds and
attaches a `tBriefingWrapper` sub-table onto that starter's own data table — a structured set of
`"<VoBankName>.<line>"` VO cue names for greetings (first-time vs. subsequent, by mood), "no jobs"/"job
summary" lines, and goodbyes. Also stamps `sFaction` onto every entry. This mutates the module's own static
tables in place; it's presumably called once at boot before any starter is actually used.

### `GetPlayerVisibleName(sStarterId)`
Returns `_THIS[sStarterId].sPlayerVisibleName`. `_THIS` is an engine-provided self-reference to the current
module's own table — the same role `getfenv()` plays in the `Inheritable` idiom used throughout
`resident/`, confirmed used the same way in `resident/mrxbriefing.lua` and `resident/mrxtask.lua`. Used here
instead of naming the module directly, though functionally equivalent to `WifStarterData[sStarterId]`.
Confirmed called from `resident/mrxunlockfanfare.lua` to show a starter's display name in an unlock
notification.

## Events
None — pure data plus one init-time transform, no event subscriptions.

## Notes for modders
- This file has no `Create`/instance pattern of its own — to actually spawn/interact with a starter at
  runtime, go through [`MrxStarterManager`](../resident/mrxstartermanager), which is what
  [`WifPmcInterior`](wifpmcinterior) and mission scripts actually call
  (`MrxStarterManager.GetStarter(sStarterId)`); this module only supplies the config that manager reads.
- The four PMC-specific bosses (`PmcBoss`/`HelPmcBoss`/`MecPmcBoss`/`JetPmcBoss`) have much sparser entries
  here than the faction starters (no `tActors`/`sHqName` — they're placed and driven by
  [`WifPmcInterior`](wifpmcinterior) itself, not spawned generically the way outpost starters are) but
  still share this same catalog for their `sFaceFxSet`/boolean feature flags
  (`bHintSystem`/`bBribeSystem`/`bTransitSystem`/`bGarageSystem`/`bCustomVehicleShop`) — confirmed from
  source these map to Fiona/Ewan/Eva/Misha respectively.
- Note some faction rosters skip numbers (no `GurStarter3`; Pirates only field `PirStarter1`/`3`/`4`, no
  `0` or `2`) — presumably characters cut or renumbered during development rather than a documentation gap.
