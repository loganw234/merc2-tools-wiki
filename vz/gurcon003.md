---
title: GurCon003
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 3
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# GurCon003

## Overview
A Guerilla minor/side story contract (its VO keys all read `MinorContract-Gur03`) — deliver a "Piranha"
speedboat down a river course while being chased by a scaling Oil-Company-flagged pursuit, with a
contextual tutorial for the boat's boost button on the player's first run. Difficulty, reward, and even
which state layer is loaded scale up on repeat completions (`GetNumCompletions`), and the race course itself
is a 21-gate `MrxTaskRace` run.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxFactionManager`, `MrxVoSequence`, `MrxTaskRace`, `MrxTutorialManager`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` pattern.
Module-level globals track the boat(s) (`uPiranha`, `uPiranhaB`, `tPiranha`), the current difficulty tier
(`nPurLevel`, chosen once in `Activated` from `GetNumCompletions()`), coop state (`bClientwasIn`), and a
handful of tutorial event handles (`eSteppedOut`, `eTutorialExit`, `eTutorialEnd`).

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)`
`LoadAssets` swaps out three city-state layers for `VZ_State_GurCon003`. `Activated` spawns the primary
Piranha at `GurCon003_deliv`'s transform, spawns a second one for coop (`SetupMPGame`), and picks
`nPurLevel`/`nTimerLevel`/intro VO purely from `GetNumCompletions()` — 0 completions is the tutorial run
(`CreateTutorialTrigger`), 1 and 2+ are progressively harder repeat runs (the 2+ tier also loads an extra
`VZ_State_GurCon003_Med` layer). It then builds the `MrxTaskRace` objective itself (21 `tCourseLocs` gates,
time bonus formulas keyed off `nPurLevel`) and arms a long tail of proximity/death/seat events: background
river-block and "Finder" boats that loop their patrol paths forever, a mine-side VO bark, a mid-course
difficulty retune (`SetTime`), a first-run-only tutorial trigger near gate 20 (`SecondTute`), music-on-board
(`PlayMusic`), boat/contact death cancels, and the pursuit start/end triggers.

### `SetTime(self)`
A second, later tuning pass on the same race objective created in `Activated` — tightens `oRaceObjective`'s
`nAddTime`/`fWidth` further once the player nears gate 40, keyed again by completion count. Illustrates that
a `MrxTaskRace` objective's fields can be adjusted live, mid-race, not just at creation.

### `_SetupBonusObjective(self)` / `CheckBoats(self)`
Optional bonus tracking boat health: an `Event.ObjectHealthLessThan` trigger per Piranha decrements a
counter (`nBonusMP`, seeded higher in coop) until it hits zero, then cancels the bonus objective with VO.

### Tutorial state machine: `CreateTutorialTrigger`, `StartTutorial`, `SetupJumpTutorial`, `SetupTutorialTray`, `TutorialCancel`
A "how to use the boost button" contextual tutorial, armed only on the very first run. Watches for the
player entering/exiting the driver seat, shows the button-tray message once a driver is confirmed present,
watches a left-mouse-button press to dismiss it early, and re-arms itself if the player gets back in.

### `StartPursuit(self, nPurLevel)` / `EndPursuit(self)`
Three hardcoded `MrxFactionManager.SetCustomPursuit` tables (tier 1–3, escalating car/boat rosters),
applied to the `"OC"` faction guid and triggered by proximity to a start marker; `EndPursuit` clears it near
the destination.

### `RiverMovers(self, nBoat)` / `FinderMovers(self, nFinder)`
Two near-identical self-perpetuating background-boat movers: each re-issues its own `PathMove` goal as its
own `Ai.Goal` completion callback, so a boat loops its patrol path indefinitely as long as its driver stays
alive — a simple, reusable "keep this AI vehicle patrolling forever" pattern.

### `MineTalk`, `BoatDestroyed`, `ContactKilled`, `PlayMusic`, `SetupMPGame`
Small one-shot handlers: a proximity VO bark, two cancel routes (boat sunk / escort NPC killed), one-time
special music on first boarding, and the coop setup that spawns the second Piranha and marks
`bClientwasIn`.

### `Cleanup(self)`
Removes both Piranhas (the second only if `bClientwasIn`), stops special music, restores the three
originally-removed city layers, clears the custom pursuit, then calls `MrxTaskContract.Cleanup(self)`.

## Events
`Event.ObjectHibernation` (mover wake-up gates), `Event.ObjectProximity` (mine talk, difficulty retune,
first-run tutorial, pursuit start/end, delivery-block wake triggers), `Event.ObjectInSeat` (board/exit for
music and the tutorial state machine), `Event.ObjectDeath` (boat/contact cancels), `Event.Button`
(left-click tutorial dismissal), `Event.TimerRelative` (tutorial auto-cancel).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- The replay-scaling pattern here (branch entirely on `self:GetNumCompletions()` at `Activated` time to
  pick difficulty/reward/layers) recurs across several minor contracts in this corpus
  ([GurCon005](gurcon005) aside) — worth copying if you want a side-mission that gets harder on repeat.
- `RiverMovers`/`FinderMovers`'s self-re-arming `Ai.Goal` callback pattern is a clean, minimal way to keep
  background AI vehicles patrolling indefinitely without a persistent timer.
