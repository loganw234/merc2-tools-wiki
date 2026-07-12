---
title: PmcCon018
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 8
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon018

## Overview
PmcCon018 ("Burnout") is a fixed-position shooting-gallery minigame: both players' real weapons are stripped and stashed on the ground, aim mode is disabled, and each is given a "Practice Laser" freebie weapon instead. The goal is to rack up enough points (60/80/100 depending on replay count) by destroying a large, randomly-selected field of props — cargo trucks, fuel-tank props, jeeps, and explosive barrels, each worth different points — before two scripted "Airstrike" events and a final countdown end the round. It's the first of a small family of near-identical shooting-gallery contracts in this batch (see Notes).

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxPmc`, `MrxSupportData`, `MrxSubtitle`, `MrxVoSequence`, `MrxUtil`, `MrxTimer`, `MrxAchievements`, `MrxState`

## Instance pattern
A native `MrxTaskContract` subclass with bare-global state throughout: point tracking (`CurPoints`, `PointGoal`), weapon snapshots (`tP1Weapons`, `tP2Weapons`, `tLocalP2Weapons`), and the spawned-prop list (`tObjectsToDelete`). Two custom net events (`NETEVENT_SETSTARTUPWEAPONS`, `NETEVENT_RETURNWEAPONS`) synchronize the weapon swap and restoration with a co-op client.

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)`
`LoadAssets` enables the shooting-gallery HUD mode, adds mission layers, and strips player 1's weapons (`_SetupP1Weapons`); once a present player 2 wakes, replicates the same setup to them. `Activated` grants the "Practice Laser" freebie to whichever players are present, temporarily sets Oil Company/PMC faction relation to friendly (+100, restored in `Cleanup`), computes the point goal by replay count, disables aim mode for both players, starts the objective (`_ObjectiveStart`) and the prop field (`_RandomSpread`), and wires a two-stage `"Airstrike"` script-event listener — the second strike arms a final 15-second countdown via `_TimeUp`.

### `_RandomSpread(self)`
Spawns roughly 90 destructible props at pre-placed marker locations: 8 cargo trucks (3 points each), 7 fuel-tank props (5 points), 9 jeeps (2 points), plus randomly-rolled explosive barrels at both the vehicle markers and a dedicated barrel-marker list (1 point each). Each prop is wired to `_AddPoints` on death.

### `_AddPoints(iPoints, self)` / `GetRandomTableIndex(t)`
Adds points, refreshes the HUD point display, and resets an 8-second "time since last hit" window (checked by `AirStrikeVO`).

### `_ObjectiveStart(self)` / `_TimeUp(self)`
Creates the "Burnout" destroy objective (used here more as a HUD/label holder for the points minigame than a literal completion gate) and arms a delayed out-of-bounds boundary watch. `_TimeUp` — reachable only after both airstrikes have fired — completes if the point goal was met, otherwise cancels.

### `_SetupP1Weapons(self)` / `SetP2Weapons()`
Drop each player's current weapons to the ground and disable their physics/reposition them out of the way, so the "Practice Laser" freebie is the only usable weapon.

### `AirStrikeVO(self, InitialPoints)`
After 10 seconds, if no points were gained since the airstrike fired, plays a random "getting impatient" hero VO line.

### `OnPlayerJoined(self, ...)` / `OnPlayerLeft(self, ...)`
Re-snapshots player 2's weapons and re-arms the out-of-bounds watcher on join. On leave, checks **`MrxPmc.GetFreebieQty`** for the laser-guided-bomb freebie and backfills a "missing" airstrike to player 1 if player 2 leaves having had one.

### `Complete(self)` / `Cancel(self)`
Both restore the real weapons via the `NETEVENT_RETURNWEAPONS` net event and `Human.Inventory.SetAllWeapons`, then disable weapons outright (this is a fixed minigame, not free-roam combat). `Complete` additionally grants `ACHIEVEMENT_GONE_SHOOTIN`.

### `Cleanup(self)`
Clears three HUD slots, disables the shooting-gallery HUD mode, deletes `oCancelEvent`/`oMoneyUpdate` (neither is ever assigned anywhere in this file, so these are harmless no-op deletes), removes every spawned prop, restores aim mode and the OC/PMC faction relation, and calls base `MrxTaskContract.Cleanup`.

## Events
- `Event.ScriptEvent` — `"Airstrike"` (twice, nested, to distinguish the first and second strike), `"mpPlayerJoin"`.
- `Event.ObjectDeath` — every spawned prop, feeding `_AddPoints`.
- `Event.Boundary` — the delayed out-of-bounds watch.
- `Event.ObjectHibernation` — gates the weapon-setup replication on player 2 waking.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- **Shared "shooting gallery" scaffolding:** this file and [PmcCon031](pmccon031)/[PmcCon032](pmccon032)/[PmcCon033](pmccon033)/[PmcCon034](pmccon034) all reuse the same skeleton — `NETEVENT_SETSTARTUPWEAPONS`/`RETURNWEAPONS` net events, `_SetupP1Weapons`/`SetP2Weapons`/`_MoveWeapons` to strip and stash real weapons, `Hud.SupportMenu:SetShootingGalleryMode`, and `Complete`/`Cancel` that both restore weapons before disabling them again. If you're modding one of these, it's worth diffing against its siblings rather than assuming any one is the "canonical" version.
- Directly calls **[`MrxPmc`](../resident/mrxpmc)** (`GetFreebieQty`) in `OnPlayerLeft` to fairly redistribute an unused airstrike freebie between co-op players.
- `oCancelEvent`/`oMoneyUpdate` are deleted in `Cleanup` despite never being assigned anywhere in this file — harmless, but not meaningful references either.
