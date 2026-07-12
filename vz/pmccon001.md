---
title: PmcCon001
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 1
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon001

## Overview
PmcCon001 is the story contract where Solano's men raid the player's own PMC headquarters villa. It walks through investigating the villa (gates close behind the player, cutting off retreat), hijacking a tank to smash back out through the garage, and fighting off two waves of VZ entourage troops before they flee. It supports resuming mid-mission from saved flags (`HijackInitiated`, `VillaReached`) so a save/reload during the mission picks back up at the right stage instead of restarting.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxVoSequence`, `MrxFactionManager`, `MrxCinematic`, `MrxTutorialManager`, `MrxAchievements`, `MrxMusic`

## Instance pattern
A native `MrxTaskContract` subclass. Module-level constants include `ksBarExitBuilding`/`ksBarExitCameraLocation` and `tPmcDoors` (the PMC HQ's named exterior gate/door objects, used for HUD-radar cleanup in `Cleanup`). Two custom net events (`NETEVENT_SETSTARTUPWEAPONS`, `NETEVENT_MOVECOLLISION`) replicate the mission's setup steps to a joining co-op client.

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)` / `ActivateMission(self)`
`LoadAssets` swaps in the mission's layers, conditionally including a "villa soldiers" layer if the `HijackInitiated` flag isn't already set, then calls `SetStartupWeapons`. `Activated` just calls `ActivateMission`, which watches three HQ buildings for death (auto-cancelling if any are destroyed), sets the interior atmosphere to "warzone," disables two road AI lanes, and branches on saved flags: `HijackInitiated` jumps straight to the villa interior; `VillaReached` jumps to `KillSolanoEntourage01`; otherwise it runs the full intro (banter, VZ jeep pursuit region, gate closer, banter region, replicated startup weapons, `PmcInvulnerable`, disabled faction reporting).

### `SetStartupWeapons()`
Gives the local player a fixed loadout (Assault Rifle, C4, Grenade) and maxes the primary weapon's reserve ammo.

### `VZJeepPursuitRegionActivate(self)` / `JeepPursuit01(self)` / `StopPursuit(self)`
Boundary-triggered custom `VZ` jeep pursuit along the approach road, cleared on reaching a second boundary region.

### `SetupGateCloser(self)` / `GateCloser(self)` / `GateOpener(self)` / `CheckFrontDoor(self)`
`GateCloser` shuts the PMC HQ's entrances and the mid-compound gate once the player enters a wide region around the villa — cutting off the easy way back. `GateOpener`/`CheckFrontDoor` re-open those same doors later, once the mission no longer needs the player walled in (called from `GoToVillaInterior02`, once inside).

### `SetupGoToObjective(self)` / `KillSolanoEntourage01(self)` / `GoToVillaInteriorLayerLoad(self)` / `GoToVillaInterior(self)` / `GoToVillaInterior02(self)` / `ObjectInSightCheck(self)`
A chain of "go to X" delivery objectives leading progressively deeper into the villa, interspersed with a "kill Solano's entourage" (5 named HVTs) destroy objective. `GoToVillaInterior02` sets the `HijackInitiated` save flag/checkpoint and calls `NetSafeMoveInvisibleCollision` + `GateOpener`.

### `NetSafeMoveInvisibleCollision()` / `ClientMoveCollision()` / `NetEventCallback(nEventId, tArgs)`
Moves an invisible collision blocker out of the way once (replicated to clients via `NETEVENT_MOVECOLLISION`), so players who join or reconnect after the move still get it applied.

### `LoadTank(self)` / `GarageSmash(self)` / `ActionHijackTank(self)` / `RideDragonAchievement(self, uTank)`
The tank-hijack centerpiece: waits for a named column to be visible, then loads a hijack-tutorial layer and — once the `PMC001_EntourageScorpion` tank wakes — calls `ActionHijackTank`. **Note:** `LoadTank` passes this as `ActionHijackTank(self)` rather than `ActionHijackTank, {self}`, so `ActionHijackTank` actually runs immediately when `LoadTank` fires rather than being deferred to the tank's wake event; the hibernation event ends up registered with `ActionHijackTank`'s return value (`nil`) as its callback, which is a no-op. `ActionHijackTank` itself smashes the garage entrance, disables normal tank entry so hijacking has to go through a dedicated "Hijack the Tank" objective, and grants `ACHIEVEMENT_RIDE_DRAGON` to whoever's driving once boarded.

### `KillSolanoEntourage02Load(self)` / `KillSolanoEntourage02(self)` / `Wave01(self)` / `SetUpWave02(self)` / `Wave02(self)` / `RunAndFleeInTerror(self)`
Two staged AI reinforcement waves (named NPCs pathed to positions) forming a 10-target `VZ`-labeled destroy objective; once cleared, survivors are sent fleeing and the contract completes.

### `SetUpBanterRegion(self)` / `Banter(self)` / `SetupCourtyardPanic(self)`
Boundary-triggered flavor dialogue. `SetupCourtyardPanic` has no visible caller in this file.

### `PmcInvulnerable(self)`
An empty function — it's called from `ActivateMission` but its body does nothing. Whatever invulnerability effect this was meant to apply isn't present in this file as decompiled.

### `Cleanup(self)`
Force-exits all players from any vehicle seat, clears HUD radar objectives for the HQ doors, marks a long list of mission layers for removal, resets VZ/PMC faction relation to fully hostile (-100), re-enables faction reporting, restores the default atmosphere, and calls base `MrxTaskContract.Cleanup`.

## Events
- `Event.Boundary` — jeep-pursuit start/stop, gate-closer trigger, and the banter region.
- `Event.ObjectDeath` — cancels the contract if any of the three watched HQ buildings dies.
- `Event.ObjectHibernation` — door open/close sequencing, tank wake, entourage NPC waves.
- `Event.ObjectInSeat` — completes the tank-hijack objective directly if the player enters the driver seat (in addition to the objective's own completion path).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- This contract is set at the player's own PMC headquarters (`tPmcDoors` are the HQ's own exterior gates) but doesn't call the `MrxPmc` economy API directly — see [`MrxPmc`](../resident/mrxpmc) for how the player's cash/fuel/equipment system works elsewhere in the corpus.
- `PmcInvulnerable` is a no-op despite being called at a point where you'd expect invulnerability to be applied — don't assume the player is actually protected during the intro just because this function exists and is called.
- `LoadTank`'s `ActionHijackTank(self)` vs. `ActionHijackTank, {self}` distinction matters if you're tracing exactly when the hijack objective becomes available — as written, it fires immediately rather than gated on the tank's hibernation-wake event.
- `SetupCourtyardPanic` and `Pmc01FionaVOComplete` have no visible caller in this file; treat as possibly unused rather than assuming they run.
