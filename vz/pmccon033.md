---
title: PmcCon033
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 11
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon033

## Overview
PmcCon033 is a "pop-up target" shooting-gallery course: armed with an infinite-ammo silver Pistol, the player clears four fixed firing points (3 targets each, framed in-HUD as "Portaits" — a typo preserved from the source), then a final wave of four painting-style targets that physically pop up by opening like a hinged door (`Vehicle.OpenDoor`/`CloseDoor` reused as a pop-up mechanism) before being destroyed. As with [PmcCon032](pmccon032), the timer counts up from zero and the pass/fail check happens once at the end against a target time (1:30/1:00/0:45 by replay count).

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxMultiPageMenu`, `MrxUtil`, `MrxLayerManager`, `MrxShootingGallery`, `MrxVoSequence`, `MrxAchievements`, `MrxMusic`, `MrxState`

## Instance pattern
A native `MrxTaskContract` subclass sharing the shooting-gallery scaffolding described on [PmcCon018](pmccon018#notes-for-modders). Two extra net events (`NETEVENT_TARGETSDOWN`/`NETEVENT_TARGETSUP`, 2/3) replicate the pop-up targets' open/closed state to co-op clients.

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)` / `_SetupObjective(self)`
Sets up the shooting-gallery HUD mode, strips weapons and arms both players with a silver Pistol, opens the four pop-up "painting" targets immediately (replicated via `NETEVENT_TARGETSDOWN`), scales the time-to-beat text by replay count, starts the count-up `MrxTimer`, and moves the player to the first firing point.

### `_DestroyObj1` … `_DestroyObj6` / `_MoveToPoint2` … `_MoveToPoint5`
Five fixed-point stages (3 targets each) followed by a sixth stage (`_DestroyObj6`) against the four pop-up targets, closing them again (`Vehicle.CloseDoor`, replicated via `NETEVENT_TARGETSUP`) before the objective is created. The final stage's completion callback checks the course timer against `nTimeLimit` — under time completes via `CompleteVO`, over it cancels.

### `TempLoadLayers(self)`
Removes the "pop down" layer and adds a "pop up" layer, then calls `_DestroyObj6`. No caller is visible anywhere in this file — the pop-up sequencing that actually runs appears to go through direct `NETEVENT_TARGETSDOWN`/`UP` toggling instead, making this function look unused.

### `PlayMusic(self, nTimeLimit)` / `_CountDownVOSetup(self, nTimeLimit)` / `CompleteVO(self)` / `FailureVO(self)`
Music speed-up and scheduled countdown VO, matching the pattern in [PmcCon032](pmccon032)/[034](pmccon034). `FailureVO` again appends an extra line if `JetCon001` has been completed.

### `_SetupP1Weapons(self)` / `SetP2Weapons()` / `_MoveWeapons(...)`
Strip real weapons and arm both players with the silver Pistol.

### `Complete(self)` / `Cancel(self)` / `Cleanup(self)`
Restore real weapons, grant `ACHIEVEMENT_GONE_SHOOTIN` on `Complete`; `Cleanup` clears HUD slots, disables shooting-gallery mode, stops the course timer, and marks the mission layers for removal.

## Events
- `Event.ObjectDeath` — per-target destruction across all six stages.
- `Event.ObjectHibernation` — the pop-up targets' open animation is triggered once each wakes.
- `Event.TimerRelative` — countdown VO schedule and per-stage celebratory-VO cooldowns.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- Shares its weapon-strip/timer/VO scaffolding with [PmcCon018](pmccon018), [PmcCon031](pmccon031), [PmcCon032](pmccon032), and [PmcCon034](pmccon034) — see PmcCon018's notes. Like PmcCon032/034, the timer counts up against an overall cap with a manual pass/fail check at the end.
- The pop-up targets reusing `Vehicle.OpenDoor`/`CloseDoor` on what are visually paintings/portraits, rather than a dedicated "pop-up target" API, is a good example of the engine's object systems being repurposed for set-dressing rather than a bespoke solution existing for every visual gimmick.
- `TempLoadLayers` has no visible caller — the wiring that's actually active goes through the `NETEVENT_TARGETSDOWN`/`UP` net events instead.
- No direct `MrxPmc` calls in this file.
