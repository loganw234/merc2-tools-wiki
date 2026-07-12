---
title: PirCon001
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 1
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PirCon001

## Overview
PirCon001 is a jetski race contract for the Pirate faction: the player (and, in co-op, a second player) races a jetski through roughly 30 waypoint checkpoints while a couple of rival pirate speedboats are scripted to converge on and block the course near a trigger point partway through. Finishing grants the "Highway to Hell" achievement, and finishing first in co-op additionally grants "Wheels of Steel." The starting timer shrinks with each repeat completion.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxTaskRace`, `MrxTaskObjectiveDeliver`, `MrxLayerManager`, `MrxMusic`, `MrxAchievements`

## Instance pattern
A native `MrxTaskContract` subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` object pattern. Module-level (bare global) state includes `uPlayer`, `tHurry` (a table of "hurry up" VO lines assigned in `Activated` but never read anywhere else in this file), `nJetskies` (a remaining-jetski counter), and the spawned jetski handles (`oJetski01`/`oJetski02`, `tJetskies`).

## Functions
### `LoadAssets(self)`
Adds the mission's main and staging layers (`VZ_state_PirCon001[_staging]`), then spawns the jetski(s) via `GetJetskis` once those layers are in.

### `Activated(self)`
Calls the base `MrxTaskContract.Activated`, grabs the player handle, builds the (apparently unused) `tHurry` VO table, counts the spawned jetskis, and kicks off `JetskiRace`.

### `JetskiRace(self)`
Creates the actual race objective: an `MrxTaskRace` child with ~30 `PirCon001_checkpointNNN` course locations, a starting timer that shrinks by 2s per prior completion, and achievement grants on `fOnComplete` (`ACHIEVEMENT_HIGHWAY_TO_HELL` always; `ACHIEVEMENT_WHEELS_OF_STEEL` in co-op if there's a winner). Also wires two side events: special music when a player boards the jetski, and `ConvergeShips` once the player nears a "converge" trigger location.

### `ConvergeShips(self, oShipName, oShipPath, nHaste)`
Gives a named enemy boat's driver a one-way `PathMove` AI goal at the given haste. Called twice from the proximity event above, to send two named "Blocking" boats angling across the player's path.

### `VehicleCheck(self)`
Decrements `nJetskies` and cancels the contract if fewer jetskis remain than there are players. No caller is visible anywhere in this file — it may be invoked by `MrxTaskRace` via a naming convention this corpus doesn't show, or it may simply be unused.

### `GetJetskis(self)`
Spawns one jetski per player (two in co-op) at named spawn points, then waits for the first jetski to wake before signaling `AssetsLoaded` — the base `MrxTaskContract`'s own loaded-callback, resolved here purely through the `inherit()` chain since this file never defines `AssetsLoaded` itself.

### `CrowdNoise(self)`
A chained sequence of `PirThug` VO lines played 0.5-1s apart. Like `VehicleCheck`, nothing in this file calls it — likely dead, or triggered externally.

### `Cleanup(self)`
Stops the special music, marks the staging layer for removal, schedules each spawned jetski's removal once it hibernates, and calls the base `MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectHibernation` — `GetJetskis` waits for the first jetski to wake; `Cleanup` waits for each jetski to hibernate before removing it.
- `Event.ObjectInSeat` — boarding a jetski triggers special mission music.
- `Event.ObjectProximity` — nearing the "converge" trigger fires `ConvergeShips` against two named blocking boats.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- `VehicleCheck` and `CrowdNoise` have no visible caller in this file; treat them as possibly dead or externally-invoked rather than assuming they run every playthrough.
- The checkpoint timer (`nStartTime = 8 - completions*2`) and per-checkpoint time bonus (`nAddTime = 8 - completions`) both shrink with repeat plays, so later replays are noticeably tighter.
- `tHurry`'s VO lines are built but never consumed in this file — if you're retuning this contract, that table may be inert.
