---
title: PirCon004
parent: Pirate Contracts & Jobs
grand_parent: VZ Modules
nav_order: 4
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PirCon004

## Overview
PirCon004 is a large, co-op-capable physics cargo-delivery contract: the player hijacks a truck ("PirCon004_OrganTruck") whose bed is loaded with dozens of separately-spawned organ-transplant containers, then drives it cross-country to a delivery point while a `VZ` pursuit triggers past a distance threshold, scripted explosions go off near landmark buildings/pipes along the route, and an ambush truck is spawned near a marked goal. In co-op, the second player is offered a dialog choice partway through to end the run early or press on. The cash reward scales with how many containers survive the trip, with a large flat bonus for a perfect delivery.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxLayerManager`, `DangerousBuilding`, `MrxGui`, `MrxUtil`, `MrxFactionManager`

## Instance pattern
A native `MrxTaskContract` subclass with almost entirely bare-global state: the organ-box location lists (`tOrganBoxes`, `tOrganBoxes02`, and `B`-suffixed co-op copies), the spawned physics props (`tSpawnedItems`), per-truck box counts (`nP1Boxes`/`nP2Boxes`), difficulty scaling (`nPurs`, `nGoal`, `nMod` from `GetCompletions`), and a mission timer (`oMissionTimer`, an `MrxTimer` instance).

## Functions
### `LoadAssets(self)` / `Activated(self)`
`LoadAssets` loads the `VZ_state_PirCon004` layer. `Activated` builds the organ-box location lists, spawns a `_global_containertransplant` prop at each box location (turning static set-dressing into destroyable/losable cargo), disables random building hazards for the mission (`DangerousBuilding.SetRarity("default", "never")`), and creates the "enter the truck" objective leading to `ObjDeliverGoods`.

### `GetPlayers(self)` / `GetCompletions(self)`
`GetPlayers` spawns a second truck for player 2 in co-op. `GetCompletions` sets the pursuit-trigger distance (`nPurs`), minimum-boxes goal (`nGoal`), and reward multiplier (`nMod`) from the completion count (capped at 2).

### `ObjDeliverGoods(self)`
The core delivery objective: starts a countdown `MrxTimer` (7 minutes minus 30s per prior completion), persistent per-truck box-loss checks (`CheckOrganBoxesLost`), several `ObstacleDetonate` scripted explosions near smokestacks/pipes, an `ObstacleTruck` ambush spawn, and the pursuit-trigger/pursuit-warning proximity events feeding `StartPursuit`.

### `StartPursuit(self)`
Locks a `VZ`-faction pursuit via `MrxFactionManager.LockPursuit` once the truck gets far enough from its start point.

### `SetupChaser(self)` / `VZChaseDelay(self, tVZcars)` / `VZChase(self, tVZcars)` / `VZChaseTest(...)`
A second, direct-AI-goal "chaser" vehicle system distinct from the custom-pursuit table used elsewhere. No path in this file's `Activated`/`ObjDeliverGoods` flow actually calls `SetupChaser` or its chain — it appears to be unused, superseded by the `StartPursuit`/`MrxFactionManager` approach that *is* wired up.

### `CheckOrganBoxesLost(self, uVeh, sPlyr)` / `FinalOrganBoxCheck(self)` / `DisplayOrganBoxesLost(self)`
Count "Organ Container" props still on each truck bed (only while the truck is within 65m of the host player, to avoid querying while far away), update the HUD, and play threshold warning VO; cancel if the count drops below the goal.

### `TruckDestroyed(self)`
Plays a failure VO line and cancels. No caller is visible in this file — the objective's own target-death handling (via the base `MrxTaskObjectiveDeliver`/`MrxTaskObjectiveEnterVehicle` classes) may call it by convention, or it may be unused.

### `Delivered(self)` / `ActivateDelivered` / `DeliveryAccept(self)` / `DeliveryDiag(self, uGuid)` / `DisplayDiag()` / `DeliveryDiagAction(self, tOptions, nIndex)` / `FinalTally(self)`
The delivery tally and, in co-op, a dialog-box choice (via `MrxGui.DisplayDialogBox`) offered to whichever player reaches the delivery NPC first — replicated to the other machine via the custom net events below when needed. Reward is a flat 2,000,000-per-player bonus for a perfect delivery, otherwise `(delivered - goal) * 1000 * nMod`.

### `ClearTimer(self)` / `ObstacleDetonate(self, uBuilding, sLoc, sDet, nDist)` / `ObstacleTruck(self)`
Helpers: stopping the mission timer, spawning a double explosion near a building once the truck convoy gets close, and spawning + pathing a VZ ambush truck near a marked goal location.

### `Cleanup(self)`
Stops the timer/music, clears three HUD slots, restores building-hazard rarity, removes spawned props and vehicles (scheduling truck removal on hibernation), clears the pursuit lock, and calls base `MrxTaskContract.Cleanup`.

### `NetEventCallback(nEventType, tArgs)`
Dispatches the two custom net events used by the co-op delivery dialog (`NETEVENT_CLIENTDIAGSHOW`/`NETEVENT_CLIENTDIAGSELECT`), so the choice can be shown/resolved correctly regardless of which player's machine triggered it.

## Events
- `Event.ObjectHibernation` / `Event.TimerRelative` — stagger the organ-box prop spawns after the truck wakes.
- `Event.ObjectProximity` — building detonations, ambush-truck spawn, pursuit trigger/warning, and tanker pre-kill near the player.
- `Event.Boundary` — clears the pursuit lock on entering the end-pursuit region.
- `Event.ObjectDeath` — VO reactions to specific building destructions.
- `Event.ObjectIsReady` — the ambush truck's driver gets an AI goal once ready.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- The `SetupChaser`/`VZChase*` chain and `TruckDestroyed` have no visible caller in this file — treat them as possibly dead code (or invoked by a level-placed trigger outside this corpus, the same way `NetEventCallback` is invoked by the net layer rather than from within the file) rather than assuming they run.
- `DangerousBuilding.SetRarity("default", "never")` at mission start / `SetRarity("all", "default")` in `Cleanup` is a reusable pattern if you want to suppress random building-hazard events for the duration of a custom mission.
- Reward math: `(nFinalGoods - nGoal) * 1000 * nMod` once the goal is beaten, or a flat `2000000 * nPlayers` for a perfect delivery — useful reference points if you're designing a similarly-scaled cargo mission.
