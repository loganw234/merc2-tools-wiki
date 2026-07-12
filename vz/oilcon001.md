---
title: OilCon001
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 1
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# OilCon001

## Overview
The largest "normal" story contract in the entire corpus (2241 lines, roughly 108 functions) — an
extended warehouse heist and rescue for Universal Petroleum. The player fights into a dockside industrial
complex to rescue a kidnapped OC executive, then personally escorts him between two separate warehouse
offices while he burns incriminating documents inside each ("burn boxes" tick up over time), defending him
through two large scripted assault waves — one culminating in a helicopter air-attack — before walking him
back out to safety. The whole burn-defend loop is driven by four self-contained, reusable helper "classes"
defined inside this same file, not by the native task framework itself.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxUtil`, `MrxApcDrop`, `MrxVoSequence`, `MrxMissionBoundary`,
  `DangerousBuilding`, `MrxSupportData`, `MrxCopterDrop`

## Instance pattern
The contract itself is the usual native task-framework subclass — `self`-based lifecycle overrides, not
the `Inheritable`/`uGuid` pattern. What sets this file apart from the rest of the batch is that it also
defines **four private, in-file "classes"** using Lua's manual `setmetatable(t, self); self.__index = self`
prototype idiom — a third OOP style alongside `Inheritable` (resident/) and the native task framework
(everywhere else in `vz/`):

- **`AttackWaves`** — a reusable scripted-assault *director*. Interprets a data-driven `tCmdList` (a small
  command list / mini-DSL: `"wave"`, `"setpath"`, `"delay"`, `"apc"`, `"call"`) to drive a whole assault
  sequence from a declarative table instead of hardcoded timers, and dynamically scales each wave's vehicle
  composition off a `curThreat`/`kMaxThreat` value that rises when enemy soldiers die and falls when OC
  soldiers die.
- **`HeliAttack`** — manages a pair of attack helicopters: one orbits/loops continuously, one "strafes" the
  nearest player at a time, swapping roles whenever the active attacker dies and escalating (a second
  permanent orbiter joins after six kills).
- **`APCWave`** — a self-respawning troop-carrier: spawns an APC, drives it in, drops its passengers near
  the defense point via `MrxApcDrop`, and queues the next APC once that squad is dealt with.
- **`Executive`** — wraps the kidnapped OC executive NPC itself: hibernation-based pacifism/cower-vs-stand
  state, the "burn box" progress loop (`BurnBox`/`EvaluateProgress`/`BoxCompleted`, milestone VO at
  33%/66%/"one more"), and a HUD progress bar.

These are plain data objects local to this file's closure, constructed with `SomeClass:Create(...)` and
torn down with `:Cleanup()` — not registered with the engine's own object/event system beyond whatever raw
`Event.Create` calls they make internally. Module-level data: `tBurnObjConfigs[1]`/`[2]` (the two burn-site
configs — location names, `boxVal`/`goalVal` progress targets, milestone VO), and `vehInfo` (a shared
template/speed/threat table for jeep/guntruck/truck/apc/tank/heli, used by both `AttackWaves` and
`HeliAttack`).

## Functions
Given the size of this file, related functions are grouped by subsystem rather than listed individually.

### Contract lifecycle and top-level objective flow
`LoadAssets` conditionally keeps or removes a "part 1" layer depending on the `StartSite2` checkpoint flag.
`Activated` builds the `Executive` wrapper around the `oc001_exec` NPC and either resumes directly at
`Obj_Site2_Goto` (if `StartSite2` was already set on a prior checkpoint — also destroying the relevant
gates immediately and disabling faction reporting) or runs the full intro: `FirstWarehouseDestroyedSetup`,
`BuildingDestroyedSetup`, `Obj_GotoRefinery`, and `_SetupConvoy1`. The objective chain from there is linear:
`Obj_GotoRefinery` → `Obj_RescueExec` (kill the VZ squad guarding the executive, or skip straight through if
they're already dead) → `Obj_TalkToExec` → `ExecutiveIntroConversation` → `Obj_Site3_Goto` (deliver the exec
to warehouse 1) → `Obj_Site3_Defend` → `Obj_Site2_Goto` (deliver to warehouse 2, also the direct
checkpoint-resume entry point) → `Obj_Site2_Defend` → `Obj_Site2_Complete` → `ObjReturnExecutive` →
`ObjReturnExecutiveComplete` → `MissionComplete`. `ObjDeliverExec` is the one generic
"deliver-the-executive-somewhere" objective factory reused for all three deliveries (site 3, site 2, and
the final return), parameterized by a small config table — a good example of collapsing three similar
objectives into one function plus data rather than three near-duplicate ones. `Cancel` overrides the base
to give the executive a different death-reaction VO sequence if he's already dead when cancelled; `Cleanup`
tears down whichever attack/heli-attack/executive/mission-boundary objects are still live.

### The `Executive` hostage wrapper
Constructed once in `Activated` with a death callback and (on checkpoint resume only) a retry point;
whether it stands calmly or cowers on first dehibernation depends on which of those two construction paths
was used. `Start` sends it walking toward the site's `returnPoint`; `EnterBuilding` creates the
"defend the office" protect-objective and starts the `BurnBox`/`EvaluateProgress` loop, which ticks
`curProgress` up by `boxVal` (plus any bonus banked from a completed attack wave) every 12 seconds, firing
milestone VO at 33%, 66%, and "one more box" before finishing and calling `ExitBuilding`. One spotted
decompiler-faithful oddity: on the goal-reached branch, `BoxCompleted` assigns `self.curProgres` (missing
the final `s`) instead of `self.curProgress` — harmless, since the function's `retval` is already set
`true` in the same branch regardless, but a genuine typo worth knowing about if you're tracing progress
math by hand.

### The `AttackWaves` director (site 2 and site 3 defenses)
`Obj_Site2_Defend` and `Obj_Site3_Defend` each build a `tAttackData` config (attack paths, spawn points,
defense points, and a `tCmdList` command sequence) and hand it to `AttackWaves:Create`. `ProcessNextCmd`
walks the command list: `"wave"` spawns and tracks a squad via a hidden `MrxTaskObjectiveDestroy`,
`"setpath"` picks which attack path(s) the next wave(s) use (optionally playing a VO line first), `"delay"`
waits (optionally with a "defend this point" sub-objective as the actual gate), `"apc"` hands off to an
`APCWave`, and `"call"` invokes an arbitrary function before immediately continuing. `SpawnOneSquad`/
`SpawnManySquads` pick vehicle composition entirely from the current `curThreat` value against a ladder of
thresholds (10/25/45/65/80/90% of `kMaxThreat`), so the same command list produces a harder or easier wave
depending on how the fight has gone so far. `WaveStagnated` (triggered by a stagnation timer once only one
attacker is left standing for 18 seconds) force-clears the wave rather than waiting indefinitely, so a
single hard-to-find straggler can't soft-lock the sequence. Two site-2-only timers layer on top:
`SetupHeliTimeout`/`HeliTimeout` (forces the current wave to stagnate if the player is taking too long,
guaranteeing `StartHeliAttack` eventually fires) and `TowerDefenseNag`/`TowerDefenseFreebie`/
`TowerDefenseAddFreebie` (a mid-siege supply-drop crate and a nag VO if the player hasn't used their
support calls in a while).

### The `HeliAttack` director (site 2 only)
Started via `StartHeliAttack` partway through the site-2 command list. Spawns two helicopters — one
immediately ordered to attack a random player (`_StartStrafe`), one to loop-orbit
(`_StartOrbit`) — and whenever the active attacker dies, promotes an orbiter to attacker after a short
random delay (`_DelayStrafe`/`_ReturnAttackerToOrbit`) while a fresh orbiter spawns in to replace losses;
a second permanent orbiter joins once the kill count hits 6.

### The `APCWave` director
Spawned by `AttackWaves:SpawnApc`. Finds a spawn point out of view, spawns the configured APC/truck, and
wires it into `MrxApcDrop` (a native drop-off system, not documented in this corpus) via a config table so
the vehicle drives in, drops its squad near the defense point, and removes itself once empty. `DropDone`
creates a small hidden objective tracking that squad's deaths (`nQuota` = squad size minus one, i.e. it
resolves once all but one are down) and queues the next APC (`DelayedSpawn`) once that resolves.

### Staging, banter, and world-state helpers
`_StagingSetup`/`_StagingBeginSequence`/`_StagingSpawnVehicle`/`_StagingStartVehicle` choreograph a small
ambush of scripted, low-health vehicles the player passes early at site 3. `_RabbitSetup`/`_RabbitSpawn`/
`_RabbitStart` spawn a fleeing "getaway car" once the executive leaves the first warehouse's boundary.
`_SetupConvoy1`/`_SetupConvoy2` arm background convoy vehicles to self-remove once they hibernate.
`_OCSavedBanter`/`_PerformBanter` pick a living, non-excluded squad member to speak a banter line — reused
for two back-to-back lines that shouldn't come from the same soldier. `_DestroyGate` waits for a gate
object to wake, then kills it with an explosion effect. `_MoveOCSquad`/`_MoveOCBoatSoldier` reposition
supporting OC AI squads/an NPC as the fight moves between sites. `_MoveSite3OCSquad` is defined but has no
call site anywhere in the file, and references a global `uDefensePoint` that is never assigned in scope —
both suggest genuinely unused, incomplete code rather than a live path.

### Mission-boundary, building-watchdog, and ambience helpers
`CreateMissionBoundaryDelayed`/`CreateMissionBoundary`/`UpdateMissionBoundaryStatus` wrap
`MrxMissionBoundary` with a fixed warn/fail time and radius, giving the player a 75-second grace period
before the "stay near the objective" boundary itself arms. `BuildingDestroyedSetup`/`Warning`/`Cleanup` and
`FirstWarehouseDestroyedSetup`/`FirstWarehouseDestroyed` are a matched pair of watchdogs on the "safe"
buildings (the two burn offices and the initial rescue warehouse): if one of them is destroyed while the
executive happens to be standing inside, he's killed outright (triggering the normal death→cancel flow)
rather than the mission continuing in a broken state. `SoundRegion_Inside`/`Outside` toggle a battle
ambience cue as the player crosses a boundary, each re-arming the other on trigger.

## Events
`Event.ObjectHibernation` (near-universal — vehicle-ready gates, the executive's own
pacifism/animation-state toggle), `Event.ObjectDeath` (attacker deaths driving both `AttackWaves` and
`HeliAttack`'s threat/respawn logic, the two building-watchdog systems, the executive's own death→cancel),
`Event.ObjectProximity` (goal-arrival triggers, banter/VO cues, the `APCWave` drop-off), `Event.TimerRelative`
(wave delays, stagnation timers, the heli-timeout failsafe, mission-boundary delay), `Event.Boundary`
(warehouse-region banter, the rescue mission-boundary itself, ambience region toggling), `Event.ObjectInSeat`
(vehicle hijack/eject detection feeding into `VehicleDestroyed`).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- **This is the best reference file in the corpus for a scripted, wave-based defense/assault sequence.**
  If you're building something similar for a mod, study `AttackWaves`'s command-list interpreter and
  threat-based difficulty scaling before reaching for hardcoded timers — it's a genuinely reusable pattern,
  not mission-specific plumbing.
- `NetEventCallback(nEventId, tArgs)` at the very end of the file is an empty stub — no multiplayer sync
  logic at all, unlike the fuller `NetEventCallback`s in [OilCon002](oilcon002)/[OilCon020](oilcon020).
- Checkpointing hinges on one flag, `StartSite2` (`_GetFlag`/`_SetFlag`), which — uniquely among this
  batch's checkpoint flags — also changes which `Executive:Create` constructor branch runs (retry-point
  "stand calmly" vs. fresh-start "cower"), not just which objective function is called next.
- Treat `_MoveSite3OCSquad` (unused, references an unassigned global) and the `self.curProgres` typo in
  `Executive:BoxCompleted` as decompiler-faithful reproductions of the shipped source, not bugs to fix.
