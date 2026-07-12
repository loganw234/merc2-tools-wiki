---
title: PmcCon032
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 10
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon032

## Overview
PmcCon032 is an "easy" shooting-gallery course: armed with an infinite-ammo Grenade Launcher, the player moves through 5 firing points, destroying 3 targets at each of the first three, 21 sniper statues at the fourth, and 6 more at the fifth, all against a displayed time-to-beat (2:30/1:20/1:00 depending on replay count). Unlike [PmcCon031](pmccon031)'s hard countdown, this course's timer counts *up* from zero and the pass/fail check — did you finish before the target time — happens once, manually, when the final statue group is cleared.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxMultiPageMenu`, `MrxUtil`, `MrxLayerManager`, `MrxShootingGallery`, `MrxVoSequence`, `MrxTimer`, `MrxAchievements`, `MrxMusic`, `MrxState`

## Instance pattern
A native `MrxTaskContract` subclass sharing the shooting-gallery scaffolding described on [PmcCon018](pmccon018#notes-for-modders). Course-specific state is bare module-level globals (`Counter`, `tTargets`, `bAllDead`, `self.CourseTimer`).

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)` / `_MoveToPoint1(self, nTimeLimit)`
Sets up the shooting-gallery HUD mode and weapon strip (arming the player with an infinite-ammo Grenade Launcher instead of the usual sidearm), scales the time-to-beat text by replay count, arms a delayed out-of-bounds cancel, plays music, and starts a **count-up** `MrxTimer` (`nStartTime = 0, nStopTime = 600`) before moving the player to the first firing point.

### `_DestroyObj1` … `_DestroyObj5` / `_MoveToPoint2` … `_MoveToPoint5`
Five sequential move-to-point-then-destroy stages, each targeting a small named set of props (3 targets each for stages 1-3, 21 `PMC011_SniperStatue18` columns for stage 4, 6 targets for stage 5). Each destroy stage plays a random celebratory VO line once enough targets die in a short window (via a per-stage `Counter`). The final stage (`_DestroyObj5`) checks `MrxTimer.GetTime(self.CourseTimer) < nTimeLimit` — under the target time completes via `CompleteVO`, over it cancels.

### `PlayMusic(self, nTimeLimit)` / `_CountDownVOSetup(self, nTimeLimit)` / `CompleteVO(self)` / `FailureVO(self)`
Music speed-up, scheduled countdown VO lines (including a hero-specific "getting impatient" line near the end via `uCountdownHero`), and the completion/failure line pickers. `FailureVO` also appends an extra line if the player has already completed `JetCon001` (a small piece of cross-contract state awareness).

### `_SetupP1Weapons(self)` / `SetP2Weapons()` / `_MoveWeapons(...)`
Strip real weapons to the ground and arm both players with the Grenade Launcher instead.

### `Complete(self)` / `Cancel(self)` / `Cleanup(self)`
Restore real weapons via the net event, grant `ACHIEVEMENT_GONE_SHOOTIN` on `Complete`. `Cleanup` clears HUD slots, disables the shooting-gallery HUD mode, re-adds the shared `"vz_state_pmc"` layer, and stops the course timer.

## Events
- `Event.ObjectDeath` — per-target destruction across all five stages.
- `Event.ObjectHealth` — damage-warning VO.
- `Event.Boundary` — the delayed out-of-bounds cancel.
- `Event.TimerRelative` — the countdown VO schedule and the per-stage celebratory-VO cooldown windows.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- Shares its weapon-strip/timer/VO scaffolding with [PmcCon018](pmccon018), [PmcCon031](pmccon031), [PmcCon033](pmccon033), and [PmcCon034](pmccon034) — see PmcCon018's notes. This file's timer counts *up* against an overall cap, with the actual pass/fail check done manually against `nTimeLimit` at the end (contrast PmcCon031's hard countdown-to-zero).
- `FailureVO`'s check for `WifMissionFlow.HasKey("JetCon001")` is a small example of one contract's flavor text depending on another contract's completion state.
- No direct `MrxPmc` calls in this file.
