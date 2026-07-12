---
title: GurCon002
parent: Guerilla Contracts & Jobs
grand_parent: VZ Modules
nav_order: 2
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# GurCon002

## Overview
A Guerilla story contract set around a town plaza in Merida. The player destroys three marked buildings
(commercial, residential, "projects") without letting a nearby church die in the crossfire, then pushes the
fight to the church itself and defends it through a large scripted siege — waves of tanks, APCs, and two
helicopter troop drops timed out to roughly five minutes — before hunting down and verifying the kill on a
named VZ HVT, "Mendez." Building-attached AI spawners are tuned live via `DangerousBuilding`/
`Ai.TweakAttachedSpawners`, and special combat music swaps in and out based on which boundary region the
player is standing in.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `DangerousBuilding`, `MrxLayerManager`, `MrxUtil`, `MrxTimer`, `MrxPmc`,
  `MrxSupportData`, `MrxVoSequence`, `MrxMusic`, `mrxclusterbomb`, `mrxfuelairbomb`, `mrxcratedelivery`,
  `mrxtankbuster`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` pattern.
Heavy use of bare (non-`local`) globals for module state: `BuildingsDestroyed`, `TankNum`,
`DamageOnHibernate`, `ChurchLifeVO50`/`ChurchLifeVO15`, `uChurchGuid`, and roughly a dozen named event
handles (`uChurchHealthEvent`, `uChurchDeath`, `oDefendChurchObj`, `DirectionVO1`-`5`, `TracingVO1`-`3`,
`CountDownEvent`, etc.) set throughout `Start`/`SetupDestroyObjective`/`DefendChurch`.

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)` / `Start(self)`
Standard layer-load, then wait-for-local-player-awake, then branch on saved flags: `ChurchDefended` skips
straight to `KillCaptain` (the whole siege already happened), `AllBuildingsDestroyed` skips straight to
`MoveToChurch`, otherwise `SetupDestroyObjective` runs the mission from the start.

### `SetupDestroyObjective(self)`
Creates the three-building `MrxTaskObjectiveDestroy` (per-part VO via `BuildingDestroyedVO`, cancel routes
to `self.Cancel`), sets a bonus objective unless a prior `BonusFailed` flag says otherwise
(`_SetupBonusObjective`), and arms two church watchdogs: an `Event.ObjectHealth` trigger that spawns a
"don't hurt the church" advisory objective, and an `Event.ObjectDeath` trigger that fails the contract
outright if the church dies here. `SetupChurchObjective` (a 60s-timer wrapper around `MoveToChurch`) is
defined but has no call site anywhere else in the file — dead code.

### `CheckCompletion(self)` / `MoveToChurch(self)`
`CheckCompletion` (the three-building destroy callback) sets the `AllBuildingsDestroyed` checkpoint flag
and VO-chains into `MoveToChurch`, a `MrxTaskObjectiveDeliver` to the church that leads into `DefendChurch`
on completion.

### `DefendChurch(self)`
The siege setup. Clears the two building-watchdog events, removes any stray invisible VZ tanks
(`_RemoveTanks`), disables Guerilla-faction infraction penalties for the duration
(`Ai.SetInfractionMultiplier(..., 0)`), and arms an `Event.ObjectHibernation` watch on the church with an
**empty callback body** — a no-op as written, likely a decompiler-faithful reproduction of a
never-finished hook rather than working logic. Creates the `DefendChurch` protect-objective (a large
`fOnCancel` tears down nine separate VO/timer event handles), starts special "kickass" music, and fires off
roughly twenty hardcoded `Event.TimerRelative` calls between t=20s and t=300s that spawn tanks/APCs
(`_SpawnTankOutOfView`), two helicopter troop drops (`_GurHeloDrop`), and timed VO barks — a fully
scripted, non-reactive siege timeline rather than a reusable wave-director class (contrast with
[OilCon001](oilcon001)'s `AttackWaves`).

### `DisplayCountdownBar(self, prog)`
Also started from `DefendChurch`. This is the actual win condition for the siege: a repeating 15s timer
that adds 5 to `prog` and rewrites a HUD tray progress bar each tick, and — once `prog` hits 100 — directly
calls `oDefendChurchObj:Complete()`. The defend phase's success condition is elapsed time (twenty ticks x
15s = 300s), not a kill count; the progress bar isn't just decorative, it *is* the timer.

### `KillCaptain(self)` / `_SetupSoccerMusic(self)`
`KillCaptain` sets the `ChurchDefended` checkpoint flag, stops the siege music, spawns the named HVT
"Mendez" and a `MrxTaskObjectiveVerify` on him, completing the contract once he's confirmed dead.
`_SetupSoccerMusic` is a small self-re-arming pattern worth reusing elsewhere: entering a boundary region
starts special music and arms an exit trigger; exiting stops it and arms a re-entry trigger that calls
`_SetupSoccerMusic` again, so the music follows the player in and out indefinitely without leaking events.

### `_SetupBonusObjective(self)` / `_RemoveTanks(self)`
Optional bonus tied to a `ScriptEvent("CollateralDamage")` listener — any collateral damage report zeroes
the bonus, cancels the bonus objective, and sets a `BonusFailed` checkpoint flag. `_RemoveTanks` culls any
non-player-driven VZ tank near the church that also isn't currently visible — general AI-clutter cleanup.

### `SetupDangerousObjBuildings(self)` / `SetupDangerousBuildings(self)`
Two separate spawner-tuning passes: one arms the three destroy-target buildings (per-group Ground/Balcony/
Rooftop spawn lists), the other (run unconditionally from `Start`, even on checkpoint resume) arms
supporting buildings — media booths, barracks tents, a locker room, and the church itself. The latter also
fetches `ProtestSE`/`NE`/`SW`/`NW` building GUIDs that are never referenced again anywhere in the file —
likely leftover from a cut "protesting crowd" set-dressing feature.

### Siege helpers: `_GurHeloDrop`/`BailOut`/`PatrolChurch`, `_SpawnTankOutOfView`/`_AttackChurch`/`_FireOnChurch`
The two vehicle-delivery pipelines behind the siege timeline. Helicopters find an out-of-view spawn point,
land troops, deploy them, then loop-patrol; tanks find an out-of-view spawn point, path to an attack point,
then get an `Attack` goal on the church. `_APCMoveToChurch`'s debug log references an undefined `uActor`
(the parameter is actually `uAPC`) — a harmless copy-paste artifact from `_AttackChurch`, cosmetic only.

### Dead code: `_ChurchDead`, `_SpawnAPCOutOfView`/`_APCMoveToChurch`/`BailOutAPC`, `_DamageOnHibernate` cluster
None of these have a visible call site in this file. `_ChurchDead` duplicates a VO/health-bar flourish that
doesn't appear to be wired to any event. The APC-delivery trio mirrors the helicopter-delivery pipeline but
for ground troops, unused. `_DamageOnHibernate`/`_ChurchDamageTimer`/`_HurtChurch`/`_SetChurchHealth` would
have ticked the church's health down by 250 every 5 seconds while it was hibernated (off-screen) — a
"don't let the player just leave and let the objective rot" mechanic that was apparently cut. Treat all of
these as inert reference code.

### `Cleanup(self)`
Removes the AI exclusion zone, resets `DangerousBuilding` rarity, clears two HUD tray slots, restores the
Guerilla infraction multiplier, stops special music, removes the traffic layer, stops the church health
bar, stops `oTimer` (never assigned anywhere in this file, so this is a guarded no-op), then calls
`MrxTaskContract.Cleanup(self)`.

## Events
`Event.ObjectHibernation` (player-awake gate, vehicle-ready chains, the no-op church-asleep watch),
`Event.ObjectHealth` (church damage thresholds, both the "don't hurt it" advisory and the 50%/10% VO
barks), `Event.ObjectDeath` (church death fail-state, vehicle-driver deaths throughout the siege),
`Event.TimerRelative` (the entire ~20-entry siege timeline plus the countdown-bar ticker),
`Event.Boundary` (soccer-field music region, ambient VO trigger), `Event.ScriptEvent`
(`"CollateralDamage"` for the bonus).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- `ChurchDefended`/`AllBuildingsDestroyed`/`BonusFailed` are the checkpoint flags that decide which phase
  this contract resumes into after a save/reload.
- This file has an unusually large amount of apparently-dead code for its size (four separate unused
  clusters) — worth remembering generally when reading any file in this corpus: a defined function is not
  proof it runs at all.
- The siege timeline (`DefendChurch`) is entirely hardcoded timer offsets, not a reusable director object —
  if you want a scripted wave-based defense for your own mod, [OilCon001](oilcon001)'s `AttackWaves`/
  `HeliAttack` classes are a much better structural reference.
