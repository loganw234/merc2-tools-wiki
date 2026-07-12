---
title: PmcCon031
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 9
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon031

## Overview
PmcCon031 is a multi-stage shooting-gallery contract at the PMC compound: move to a firing point, destroy a set of decorative statues (first with an emplaced machine gun, then a recoilless rifle, then a grenade launcher), then finish with a car-launch gauntlet where vehicles fling in from fixed points and must be destroyed within a 9-second window each (up to 4 misses trigger negative hero VO). The whole run is against a countdown timer (4:00/2:30/1:30 depending on replay count) that pauses briefly for a 5-second bonus window on certain hits. Destroying either pair of emplaced turrets (machine gun or grenade launcher) early cancels the mission.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxMultiPageMenu`, `MrxUtil`, `MrxLayerManager`, `MrxShootingGallery`, `MrxVoSequence`, `MrxTimer`, `MrxAchievements`, `MrxMusic`, `MrxState`

## Instance pattern
A native `MrxTaskContract` subclass sharing the "shooting gallery" scaffolding described on [PmcCon018](pmccon018#notes-for-modders) — weapon-strip/restore net events, `_SetupP1Weapons`/`SetP2Weapons`, and a countdown `MrxTimer` (`self.CourseTimer`) with rescheduled VO/music cues (`_CountDownVOSetup`/`_FixTimers`) whenever the timer gets a bonus pause. Course-specific state (`tStatueTargets`, `tGrenadeStatueTargets`, `NumCars`, `CarsMissed`) is bare module-level globals.

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)` / `_SetupObjective(self, nTimeLimit, nQuota)`
Sets up the shooting-gallery HUD mode and weapon strip, arms a delayed out-of-bounds cancel, scales the time limit/target time-to-beat by replay count, starts a **counting-down** `MrxTimer` (`nStartTime = nTimeLimit`, ticking to 0), plays course music, and watches the player's health plus four emplaced-turret death events — losing 2 of either the grenade-launcher or machine-gun turrets cancels the mission via `Cancel`.

### `_MoveToMG(self)` / `_DestroyStatues(self)` / `StatueKilled(self, iGuid)` / `Obj_MGStatues_StatueKilled(self)`
Move-to-point objective, then a machine-gun statue-destruction objective built from ~49 named columns (quota computed by counting how many are still alive). A parallel "fake" destroy objective (`oFakeMachineGunObj`) exists purely to control the world-space vs. radar blip display, switching modes once only 5 statues remain.

### `_MoveToRR(self)` / `_SpawnCar(self)` / `_CarHit(self)`
Move to the recoilless-rifle point, then the car-launch gauntlet: spawns one of four "Fling" cars on a rotating schedule, gives each a 9-second destroy window (missing it cancels that car's objective and counts toward `CarsMissed`, with negative hero VO at 4 misses), and rewards a hit with a 5-second timer pause (`_CarHit`, via `_FixTimers`) before continuing to the next car or moving on to the grenade-launcher point.

### `_MovetoGL(self)` / `_DestroyStatuesGL(self)` / `StatueKilledGrenade(self, iGuid)`
Move to the grenade-launcher point, then a second, larger statue-destruction objective (~50 named columns, quota reduced by 5 to leave a small buffer), again with a "fake" blip-only objective layered on top and a display-mode switch at 10 remaining.

### `PlayMusic(self, nTimeLimit)` / `_CountDownVOSetup(self, nTimeLimit)` / `_FixTimers(self)` / `CompleteVO(self)` / `TimeUp(self)`
Music speed-up partway through, scheduled countdown VO lines (5/15/30 seconds remaining), a re-scheduler (`_FixTimers`) that shifts all of the above whenever the course timer gets paused for a bonus, and the completion/failure VO pickers.

### `_SetupBorderWeapons(uBorderName, uWeaponName, self)`
Calls `MrxShootingGallery.RemoveWeapons` but has no visible caller anywhere in this file — likely unused.

### `Complete(self)` / `Cancel(self)` / `Cleanup(self)`
Restore real weapons via the net event, grant `ACHIEVEMENT_GONE_SHOOTIN` on `Complete`, and (in `Cleanup`) delete every spawned car, disable the shooting-gallery HUD mode, restore aim mode, re-add the shared `"vz_state_pmc"` layer, and call base `MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectDeath` — the four emplaced-turret watches, each spawned car, and per-statue kill counters (used to trigger celebratory VO in small bursts).
- `Event.ObjectHealth` — the player's own health, for damage-warning VO.
- `Event.ObjectProximity` — the persistent weapon-retrieval watch (`_evMoveWeapons`) that re-hides dropped weapons if a player wanders back near them.
- `Event.Boundary` — the delayed out-of-bounds cancel.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- Shares its weapon-strip/timer/VO scaffolding with [PmcCon018](pmccon018), [PmcCon032](pmccon032), [PmcCon033](pmccon033), and [PmcCon034](pmccon034) — see PmcCon018's notes for the pattern overview. This file's `CourseTimer` counts *down* from the time limit to 0 (failing via `TimeUp` at zero); contrast [PmcCon032](pmccon032)/[033](pmccon033)/[034](pmccon034), which count *up* from 0 against an overall cap and check "did you beat the target time" manually at the end.
- No direct `MrxPmc` calls in this file.
