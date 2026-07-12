---
title: PmcCon002
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 2
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon002

## Overview
PmcCon002 sends the player to an oil rig to find an informant, "Blanco," hiding in the rig office. The office turns out to be booby-trapped — entering it triggers a hero-specific cutscene followed by an explosion that knocks the player down — after which Blanco flees by helicopter and must be tracked down and captured (or killed) before the player destroys the oil rig itself. Capturing Blanco alive pays a bonus on top of the base reward. The rig or the specific office building section being destroyed before the player gets there both fail the contract.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxState`, `MrxSubtitle`, `MrxCinematic`, `MrxGui`, `DangerousBuilding`, `MrxLayerManager`, `MrxVoSequence`, `MrxUtil`

## Instance pattern
A native `MrxTaskContract` subclass, state kept in bare module-level globals (`uOilRig`, `uBuildingA`, `oOfficeObjective`, `oVerifyBlanco`, `oTauntTimer`, etc.) rather than fields on `self`.

## Functions
### `Activated(self)` / `Start(self)`
`Activated` waits for the local player to wake, then `Start` creates the "Find Blanco" action objective on the rig office, watches the oil rig for death (`Failure` on death) and a specific office floor section's health via `SetupOfficeEvent`, and plays intro banter.

### `SetupOfficeEvent(self)`
Watches `floor02.piece1b`'s health on the office building; if it drops below 1, calls `Failure`.

### `Failure(self, sReason)`
On `"rig"`, cancels the office objective, runs a transient `Cleanup(true)` pass (props/sound only, not the full contract teardown), and plays a failure VO sequence ending in `self.Cancel`.

### `Cleanup(self, bContinue)`
Removes the minimap objective marker if set, silences the oil rig's alarm siren/light across several tagged objects, removes Blanco's context action and corpse if present, and — only when `bContinue` is falsy — calls the real `MrxTaskContract.Cleanup`. This dual-purpose design lets `PlayOfficeCinematic`/`Failure` reuse it for mid-mission scene cleanup without ending the task.

### `PlayOfficeCinematic(self, uCharacter)`
Runs a transient `Cleanup(true)`, deletes the office health-watch event, then — via `MrxState.Enter/Exit(MrxState.STATE_WAITFORGAME, ...)` — plays a hero-specific cutscene (`"10_BRV_" .. heroLetter`, defaulting to `"M"` for any hero not M/J/C) through `Hud.Cinematic`, then teleports the hero to an exit point and schedules `ExplodeHero`.

### `ExplodeHero(uCharacter)`
Spawns a force explosion and a C4-style particle effect at a marked location, then knocks the hero down shortly after — the office's booby trap paying off.

### `SpawnBlanco(self, uCharacter)` / `RunBlancoRun(self, uCharacter)`
Re-arms the alarm, turns on `DangerousBuilding` hazards for three rig sections, spawns two VZ transport helicopters near the camera, then loads a layer and creates the "Verify Blanco" objective (faction `"Gur"` — Blanco reads as a Guerrilla-aligned informant rather than VZ or Oil Company). Capturing him alive pays 1,000,000 to each player; subduing/destroying him instead just stops his taunts and continues to `StartDestroyRig`.

### `OKVO(self)` / `PlayBlancoTaunt(self)` / `StopBlancoTaunt(self)`
Flavor dialogue and Blanco's periodic taunt lines while he's being chased, on a re-arming timer until the verify objective resolves.

### `StartDestroyRig(self)` / `RigIsDead(self)`
Creates the "destroy the oil rig" objective (auto-completing if the rig is somehow already dead); on destruction, waits 24s, removes the rig's pristine layer, and completes via VO.

## Events
- `Event.ObjectHealth` — the office floor-section health watch (`SetupOfficeEvent`).
- `Event.ObjectDeath` — the oil rig death watch (`oRigDeath`, deleted once `PlayOfficeCinematic` runs).
- `Event.ObjectHibernation` — `Activated` waits for the local player to wake before starting.
- `Event.TimerRelative` — `PlayBlancoTaunt`'s re-arming taunt timer, `ExplodeHero`'s knockdown delay, `RigIsDead`'s post-destruction pause.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- `Cleanup(self, bContinue)`'s dual-purpose "tidy the scene now, end the task later (or never)" pattern is worth copying if you need to reuse teardown logic (siren/marker/corpse cleanup) both mid-mission and at real completion without duplicating it.
- Blanco's faction id is `"Gur"` (Guerrilla) — a good example of a contract's antagonist/target not sharing the contract's own faction prefix (`Pmc`).
- No direct `MrxPmc` calls in this file; the 1,000,000-per-player capture bonus is set through `self:_SetPlayer1Bonus`/`_SetPlayer2Bonus` on the base `MrxTaskContract`, paid out by the framework rather than this file touching cash directly.
