---
title: GurCon001
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 1
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# GurCon001

## Overview
A Guerilla story contract centered on an assault against a VZ-held island fortress complex. The player
lands on a beach (with a mid-mission checkpoint), fights through to destroy a castle/fortress, a tower,
and a bridge, then optionally wipes out a barracks compound for a cash bonus. Two VZ "Jammer" APCs and the
fortress/bridge/tower deaths each trigger a follow-up helicopter counter-attack, and a boundary trigger
launches a scripted jeep/truck convoy against the player en route.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `DangerousBuilding`, `MrxSubtitle`, `MrxVoSequence`, `MrxSupportData`, `Munitions`, `MrxTransit`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides via the engine's mission system, not
the `Inheritable`/`uGuid` object pattern. Module-level state (shared globals, not per-instance fields):
`BeachCheckPointEventWest`/`East`/`Mid` (event handles — only `West` is ever actually assigned, in
`AddBeachCheckpoints`; `East`/`Mid` stay `nil` for the life of the file), `BuildingsDestroyed` (declared
`= 0` but never read or incremented anywhere in this file — looks like a leftover from
[GurCon002](gurcon002), which uses the same field name heavily), and `tHelosSpawned` (array of spawned
helicopter GUIDs, used by `Cleanup` to remove any that aren't currently player-occupied).

## Functions
### `LoadAssets(self, tSaveData)`
Loads the mission's world-state layers. Builds an 8-entry `tLayersToAdd` and passes it to
`MrxLayerManager.Add`, then immediately reassigns `tLayersToAdd` to a *different*, 4-entry list that is
never used within this function — but **is** read later, since it's a bare global: `Cleanup` iterates
`tLayersToAdd` to mark layers for removal, so it ends up removing the second (overwritten) list, not the
one actually added. Worth knowing if you're tracing which layers this contract touches.

### `Activated(self)` / `Start(self)`
`Activated` calls `MrxTaskContract.Activated(self)`, resets `ObjectivesDestroyed`, and waits for the local
player to wake from hibernation before calling `Start`. `Start` sets up VO triggers (`_SetupVO`), arms a
boundary-triggered scripted convoy (`_SetupVZAttack`), either places beach checkpoints or (if the
`BeachReached` flag is already set from a prior checkpoint) removes two pre-placed soldiers, arms the
helicopter counter-attacks (`_SetupHeloAttacks`), and kicks off the main objective (`DestroyCastle`).

### `DestroyCastle(self)` / `ObjectiveDestroyed(self)`
Creates three `MrxTaskObjectiveDestroy` children in parallel — fortress, tower, bridge — each calling the
shared `ObjectiveDestroyed` callback on completion. `ObjectiveDestroyed` counts them and fires milestone VO
at 1, 2, and 3; the third also chains into a VO sequence that ends by calling `self.Complete`. If the
optional barracks bonus was already completed on a prior run (`BonusCompleted` flag), `DestroyCastle`
skips straight to `KillBarracks` instead of re-offering `SetupBonusObj`.

### `SetupBonusObj(self)` / `KillBarracks(self)`
`SetupBonusObj` is the optional "destroy the barracks" bonus objective (cash bonus + `BonusCompleted` flag
+ checkpoint on completion). `KillBarracks` is the checkpoint-recovery path: instead of re-running the
objective, it just insta-kills each barracks building the moment it wakes from hibernation.

### Dead code: `_MissionComplete`, `SetUpMunitionsObjective`, `_CompletedMunitions`, `_DestroyedMunitions`
None of these four functions are called from anywhere else in the file. `_MissionComplete` duplicates what
`ObjectiveDestroyed`'s third-milestone branch already does inline. `SetUpMunitionsObjective` (an optional
"protect 3 Rocket Artillery crates" bonus, using a `ScriptEvent("MunitionsPickup")` listener) and its two
helpers appear to be an earlier design for the bonus objective that got replaced by the barracks-destroy
bonus and left in place. Treat all four as inert reference code, not part of the live mission flow.

### `_SetupVZAttack()` / `_SpawnVehicleOutOfView(self, sPath, sVehicle, sMode)`
`_SetupVZAttack` is a hardcoded scripted convoy: two jeep drivers and a cargo-truck driver each get a
`PathMove` goal toward the player, with the truck also set to deploy its passengers on arrival.
`_SpawnVehicleOutOfView` is a reusable helper — finds a spawn point out of the player's view along a named
path, spawns the given vehicle template there, and sends its driver down the path once it wakes up; used
by the helicopter counter-attacks below.

### `_SetupHeloAttacks(self)`
Wires five `Event.ObjectDeath` triggers (two Jammer APCs, the fortress, the bridge, the tower), each
spawning a counter-attack helicopter via `_SpawnVehicleOutOfView` and then deleting the *other* pending
death-triggers for the same "wave" — so killing any one of a linked set only spawns one helicopter, not
one per building in that set.

### `_SetupVO(self)` / `AddBeachCheckpoints(self)`
`_SetupVO` arms a handful of one-shot boundary/timer/death-triggered VO barks (shoreline arrival, a 45s
nag, entering the castle grounds, a jammer-driver death reaction). `AddBeachCheckpoints` arms the
beach-boundary trigger that sets the `BeachReached` flag and saves a checkpoint.

### `Cleanup(self)`
Restores dynamic music, deletes the (never-assigned, so effectively no-op) `oCastleMusicOff`/`On` event
handles, marks the (overwritten, 4-entry) `tLayersToAdd` layers for removal, removes any spawned
helicopters that aren't currently ridden by either player, then calls `MrxTaskContract.Cleanup(self)`.

## Events
`Event.ObjectHibernation` (deferred `Awake`/vehicle-ready patterns throughout), `Event.Boundary` (shore
arrival, VZ attack trigger, castle-grounds VO, beach checkpoint), `Event.ObjectDeath` (jammer/fortress/
tower/bridge deaths driving both the helicopter counter-attacks and VO), `Event.TimerRelative` (the 45s VO
nag), and `Event.ScriptEvent` (`"MunitionsPickup"`, only inside the dead `SetUpMunitionsObjective` code
path).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- The dead functions (`_MissionComplete`, `SetUpMunitionsObjective` and its two helpers) are a useful
  reminder that decompiled source can include abandoned designs — don't assume every defined function is
  reachable at runtime; check what actually calls it.
- `BeachReached` and `BonusCompleted` are the two save/checkpoint flags (`_GetFlag`/`_SetFlag`) that gate
  which branch this contract resumes into after a checkpoint reload.
