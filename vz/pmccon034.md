---
title: PmcCon034
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 12
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon034

## Overview
PmcCon034 is a shooting-gallery course armed with an infinite-ammo Anti-Material Rifle: destroy 19 named sniper statues while two independent bonus side-targets keep appearing — a truck-and-statue pair that drives along a path every 43 seconds, and a bust statue winched beneath a helicopter — each granting a 5-second timer-pause bonus if destroyed before it's cleared away. As with [PmcCon032](pmccon032)/[033](pmccon033), the course timer counts up from zero and the pass/fail check happens once at the end against a target time (1:30/1:00/0:30 by replay count).

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxMultiPageMenu`, `MrxUtil`, `MrxLayerManager`, `MrxShootingGallery`, `MrxVoSequence`, `MrxAchievements`, `MrxMusic`, `MrxState`

## Instance pattern
A native `MrxTaskContract` subclass sharing the shooting-gallery scaffolding described on [PmcCon018](pmccon018#notes-for-modders). Bonus-target state (`iTruckTargetNum`, `TruckSpawn`/`StatueSpawn`, `uCargo`, `oStatueTimer`) is bare module-level globals.

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)` / `_SetupObjective(self)`
Sets up the shooting-gallery HUD mode, scales the time-to-beat by replay count, arms a delayed out-of-bounds cancel, starts the count-up `MrxTimer`, and creates the main 19-statue destroy objective. Its completion callback checks the course timer against `nTimeLimit` — under time completes via `CompleteVO`, over it cancels directly (rather than via `FailureVO`). Also kicks off both recurring bonus-target loops (`_CallTruckTarget`, `_AttachStatue`).

### `_SetupP1Weapons(self)` / `SetP2Weapons()`
Strip real weapons, arm both players with the Anti-Material Rifle, and (uniquely in this file) arm the out-of-bounds boundary watch directly inside the P1 weapon-setup function rather than in `Activated`.

### `_CallTruckTarget(self)` / `_TruckTarget(self)` / `_KillTruckStatue(...)`
Every 43 seconds, spawns a truck towing a bust statue along a fixed path; destroying the statue calls `_MinusTime` (a bonus, despite the name) and plays a celebratory VO line, while the truck reaching its destination un-destroyed removes both props and cancels that round's bonus objective via `_KillTruckStatue`.

### `_AttachStatue(self)` / `_DeployWinch(uGuid, uCargo, self)` / `AttachCargo(uGuid, uCargo)`
Spawns a bust statue above a named transport helicopter, deploys its winch, and attaches the statue as cargo once both are awake — creating an optional destroy objective that, on completion, calls `_MinusTime` and re-arms another `_AttachStatue` cycle 10 seconds later.

### `_MinusTime(self)` / `_FixTimers(self)`
Pauses the course timer for a 5-second "bonus time" window (flashed on the HUD) and reschedules every dependent countdown VO/music cue accordingly.

### `PlayMusic(self, nTimeLimit)` / `_CountDownVOSetup(self, nTimeLimit)` / `CompleteVO(self)` / `FailureVO(self)`
Matches the pattern in [PmcCon032](pmccon032)/[033](pmccon033); `FailureVO` again appends an extra line if `JetCon001` is complete.

### `Complete(self)` / `Cancel(self)` / `Cleanup(self)`
Restore real weapons, grant `ACHIEVEMENT_GONE_SHOOTIN` on `Complete`. `Cleanup` removes any in-flight truck/statue/cargo props, resets the transport helicopter's position, clears three HUD slots, stops the course timer, and cancels the statue-respawn timer if pending.

## Events
- `Event.ObjectDeath` — the 19 main statues, plus each spawned truck-statue and winch-statue pair.
- `Event.TimerRelative` — the 43-second truck-spawn loop, the 10-second winch-statue respawn loop, and the countdown VO/music schedule.
- `Event.ObjectHibernation` — gates the winch deployment on both the helicopter and cargo being awake.
- `Event.Boundary` — the delayed out-of-bounds cancel.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- Shares its weapon-strip/timer/VO scaffolding with [PmcCon018](pmccon018), [PmcCon031](pmccon031), [PmcCon032](pmccon032), and [PmcCon033](pmccon033) — see PmcCon018's notes. Like PmcCon032/033, the timer counts up against an overall cap with a manual pass/fail check at the end.
- The two independent recurring bonus-target loops (`_CallTruckTarget` every 43s, `_AttachStatue` every 10s after each is cleared) are a good reference if you want "optional side-targets that keep reappearing throughout a timed course" for your own contract.
- `_MinusTime`'s name is misleading — it doesn't subtract time directly, it pauses the timer for a 5-second grace window and reschedules dependent VO/music cues via `_FixTimers`.
- No direct `MrxPmc` calls in this file.
