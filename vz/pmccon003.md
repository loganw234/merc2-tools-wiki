---
title: PmcCon003
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 3
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon003

## Overview
PmcCon003 is a large, multi-phase story contract covering the assault on Solano's bunker and the immediate PMC counter-attack that follows: fly out by taxi helicopter, deploy a Bunker Buster strike on the bunker, race back to base against a helicopter-wave pursuit, defend the PMC compound from an armored assault (with an optional second tank wave), then track down and extract the target "Carmona" as he flees by jeep and helicopter. It supports resuming from saved flags (`BunkerBusterDeployed`, `BoardedLuckyLady`, `PMCRaceComplete`, `PMCDefenseComplete`) so the mission picks up at the right phase after a save/reload.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxLayerManager`, `MrxVoSequence`, `MrxState`, `MrxSupportData`, `MrxSupportManager`, `MrxMusic`, `MrxSupport`, `WifPmcInterior`, `MrxSupportTransit`, `MrxPmc`, `WifVzBoundary`, `DangerousBuilding`

## Instance pattern
A native `MrxTaskContract` subclass with bare-global state throughout: the PMC building handle (`uPMCguid`), Carmona's tracking handles (`uCarmona`, `uCarmonaJeep`, `uCarmonaHeli`), an escape path list (`tEscapePaths`), and various per-phase objective handles (`oBustBunker`, `oDestroyAttackers`, `oGetCarmona`, etc.).

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)`
`LoadAssets` swaps in phase-appropriate layers based on saved flags. `Activated` sets up the region boundary via `WifVzBoundary.SetupBoundaryPMCCON003`, makes the bunker invincible until the strike is properly delivered, manages the "Copter" support recruit's availability/cooldown, and branches to the correct phase entry point based on saved flags — or, on a fresh start, sends the player to board the `PMC003_EwanTaxi` helicopter.

### Phase 1 — Bunker Buster (`TransitTeleport`, `BunkerBuster`, `BBDeployed`, `VODeployedBB`, `FailedToBust`)
`TransitTeleport` flies the taxi to a drop point via `MrxSupportTransit`, then `BunkerBuster` grants a "Bunker Buster" freebie support item and creates the "deploy it on the bunker" destroy objective. `BBDeployed` (fired by a `Busted` script event) checks the strike location against the bunker via `MrxUtil.GetDistanceToObject`: close enough completes the objective; too far, with no stock left (checked via **`MrxPmc.GetSupportQty`/`GetFreebieQty`**), fails the contract through `FailedToBust`.

### Phase 2 — Race back (`PMCRace`, `LoadPMCAttack01`)
A 600-second `MrxTaskObjectiveDeliver` back to the compound, backed by a helicopter-wave pursuit (`StartHeliPursuit`/`Pg.StartHeliWaveSpawner`) and distance-banded VO lines; running out of time (while still alive) cancels the contract.

### Phase 3 — Defend the PMC (`ClearPMCGrounds`, `ClearPMCGrounds_Wave2`, `TankAttackPMC`, `TankBustPMCWall`, `_PMCHealthBar`)
Destroy 4 named AMX tanks attacking the compound while a health bar tracks the PMC building itself (auto-fails the objective if the building's health hits zero first); if a second wave of tanks/APCs is still alive, `ClearPMCGrounds_Wave2` sends them punching through the compound walls via `TankBustPMCWall` before the phase can finish. `WifPmcInterior.SetEntranceLock(true)` locks the HQ interior menu for the duration.

### Phase 4 — Capture Carmona (`EnterPMC`, `CinematicCarmonaPMC`, `SpawnCarmona`, `GetCarmona`, `MountUpCarmona`, `DriveCarmonaToHeli`, `DriveCarmonaTimeOut`, `ExitAttempted`, `CarmonaStoppedAtDestn`, `SwitchCarmonaToHeli`, `HeliWaitForCarmona`, `CarmonaHeliEscape`)
After a cutscene, a "Verify Carmona" objective (faction `"Oil"`) tracks him as AI paths him along a sequence of escape-path segments in his jeep, then switches him to a helicopter once he reaches the end — each step retried on a timeout if the AI goal doesn't report success. A custom `VZ` pursuit (`StartPursuit`/`StopPursuit`) runs for the duration of the chase.

### Region-triggered ambushes (`BunkerApproachRegionActivate`, `Bunker_Approach_Attack01`, `BunkerTankAmbushRegionActive`, `BunkerTankAmbush01`, `AngelFallsBridgeRegionActivate`, `AngelFallsBridgeAmbush`)
Three boundary regions along the route, each pathing a specific named ambush unit (helicopter or tank) toward the player once triggered.

### `Cleanup(self)`
Stops the pursuit and heli-wave spawner, re-enables the "Copter" recruit, removes the Bunker Buster freebie, removes the taxi, stops the PMC health bar, unlocks the HQ interior (`WifPmcInterior.SetEntranceLock(false)`), marks the phase layers for removal (and the pre-mission "lived-in" layers for re-addition), and calls base `MrxTaskContract.Cleanup`.

## Events
- `Event.Boundary` — the three ambush regions, plus the health-bar region pair (enter/exit toggles `_PMCHealthBar`'s display).
- `Event.ObjectHealthLessThan` — cancels the tank-clearing objective early if the PMC building's health hits the watched threshold.
- `Event.ScriptEvent` — `"Busted"` (bunker-buster strike confirmation).
- `Event.ObjectInSeat` — detects Carmona boarding his getaway helicopter.
- `Event.ObjectHibernation` — gates tank AI goals on the tanks actually being awake.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- This is one of the few files in this batch that directly calls **[`MrxPmc`](../resident/mrxpmc)** (`GetSupportQty`/`GetFreebieQty` in `BBDeployed`) to check whether the player has a Bunker Buster strike left in stock or as a freebie before failing the "deploy it correctly" check — a concrete example of a native contract reading the player's support-item economy.
- The four-phase structure (with per-phase save flags gating `LoadAssets`/`Activated` branching) is a solid reference if you're trying to understand how a single native contract file spans what feels like several distinct missions.
- `MountUpCarmona`'s escape-path retry logic (`DriveCarmonaToHeli`/`DriveCarmonaTimeOut`) is a good template for a "make an AI walk a specific path, retry on failure, then hand off to the next step" pattern.
