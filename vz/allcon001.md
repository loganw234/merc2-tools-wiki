---
title: AllCon001
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 1
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# AllCon001

## Overview
An Allied Nation story contract built around a downed plane and two captured VIPs. The player destroys
the wreck of a crashed aircraft in three parts (nose/mid/tail) while two prisoners, `Civ_VIP_1` and
`Civ_VIP_2`, sit in nearby jail sites; talking to and extracting each VIP is optional but pays a large
cash bonus (3,000,000 per VIP saved) on top of the main objective. Ambient patrol boats loop preset paths
in the background for atmosphere. The mission plays out around a region named
`reg_MargaritaChinaFactionZone`, suggesting the crash site sits in the China-controlled part of the map
even though this is an Allied Nation contract.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `MrxVoSequence`, `MrxSupportData`

## Instance pattern
A native `MrxTaskContract` subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid`
object pattern. Contract-wide state lives in plain module-level globals rather than fields on `self`:
`nVipSaved`, `nPlaneParts`, `uFoundVIP2`, `uVIP2Event`, and the objective-child references
(`oVIP1talk`/`oVIP1extract`/`oVIP2talk`/`oVIP2extract`) created by the VIP-related functions.

## Functions
### `LoadAssets(self, tSaveData)`
Swaps in the crash-site layers (`Vz_State_AllCon001`, `vz_State_Margarita_crash`,
`Vz_State_AllCon001_pristine`) after removing the pre-crash layer, then signals `AssetsLoaded`.

### `Activated(self)`
Resets contract state, calls the base `MrxTaskContract.Activated`, sets up the plane-destruction and both
VIP-talk objectives, and arms a boundary trigger (talk-about-VIP1 VO), a proximity trigger (VIP2 reveal),
and four `Event.ObjectHibernation` triggers that send patrol boats down their paths via `BoatPatrol` once
each wakes.

### `RelationSetup(self)`
Sets the VIPs and four `jail_11_i` civilians to neutral relations with China. **Not called anywhere else
in this file** — either invoked externally (e.g. by a level trigger) or a vestigial leftover.

### `BoatPatrol(self, sVeh, sPath)`
Orders a patrol boat's driver onto a `PathMove` goal (`Mode = "Bounce"`) one second after the boat wakes.

### `ObjectivePlane1(self)`
Creates the `MrxTaskObjectiveDestroy` child for the plane's three parts, wires `PartDestroyed` as the
per-part callback, and on completion pays out the VIP bonus (both players get the full amount in net
play) before completing the contract on a 4-second delay.

### `PartDestroyed(self)`
Decrements `nPlaneParts` and plays a VO line pair for 2, 1, or 0 parts remaining.

### `PlayObjectiveMusic(self)`
Starts threat music (or a "kickass" sting once only one plane part is left). **No call site found
anywhere in this file** — appears unused/vestigial.

### `TalkAboutVIP1(self)`
Sets a one-time `MargaritaReached` flag/checkpoint on first call, then plays the VIP1 introduction VO.

### `PlayThreatMusic(self, nEndTime)`
Locks the action-level music at level 3 and schedules an unlock after `nEndTime` seconds.

### `ShowVIP1(self)`
Configures `oVIP1talk` to display (`bDsp = true`). **No call site found anywhere in this file** — unlike
its VIP2 counterpart (`ShowVIP2`), nothing here ever calls it; VIP1's talk objective is simply created
already visible.

### `ObjectiveTalkToVIP1(self)`
Creates the `MrxTaskObjectiveRelease` child for `Civ_VIP_1` and arms a proximity trigger that makes nearby
jail civilians (site 11) cower via `MoveCivs`.

### `ObjectiveVIP1(self, uTalked)`
Creates the `MrxTaskObjectiveExtract` child for `Civ_VIP_1`; on completion increments `nVipSaved` and
plays a VO line; calls `VIP1givesInfo`.

### `MoveCivs(self, nSite)`
Puts the four `jail_<nSite>_i` civilians into the `"Cower"` state.

### `VIP1givesInfo(self)`
If VIP2 hasn't been found yet, cancels the standing VIP2-reveal proximity event, plays a VO exchange, and
schedules `ShowVIP2` ten seconds later.

### `ShowVIP2(self)`
Marks VIP2 as found and configures `oVIP2talk` to display.

### `ObjectiveTalkToVIP2(self)`
Creates the `MrxTaskObjectiveRelease` child for `Civ_VIP_2` (initially hidden, `bDsp = false`, until
`ShowVIP2` reveals it) and arms the equivalent proximity/`MoveCivs` trigger for site 22.

### `ObjectiveVIP2(self, uTalked)`
Creates the `MrxTaskObjectiveExtract` child for `Civ_VIP_2`; on completion increments `nVipSaved` and
plays a VO line.

### `Cleanup(self)`
Calls the base `MrxTaskContract.Cleanup`. No contract-specific teardown of its own.

## Events
- `Event.Boundary` — entering `reg_MargaritaChinaFactionZone` fires `TalkAboutVIP1` (once-only checkpoint
  behavior guarded by the `MargaritaReached` flag).
- `Event.ObjectProximity` — player within 20 of `Civ_VIP_2` reveals VIP2's talk objective; player within
  10 of either VIP triggers `MoveCivs` for the corresponding jail site.
- `Event.ObjectHibernation` — four patrol boats (`patrolBoat_west2`, `patrolBoat_2/3/4`) waking each start
  their `BoatPatrol` loop.
- `Event.TimerRelative` — used throughout for short delays: the 1-second `Ai.Goal` dispatch in
  `BoatPatrol`, the 4-second pause before completing after the plane is destroyed, the threat-music
  unlock in `PlayThreatMusic`, and the 10-second VIP2 reveal delay in `VIP1givesInfo`.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- VIP bonus is a flat 3,000,000 per VIP extracted, paid via `_SetPlayer1Bonus`/`_SetPlayer2Bonus`.
- `RelationSetup`, `PlayObjectiveMusic`, and `ShowVIP1` are all defined but have no call site anywhere in
  this file — treat them as inert unless something outside this file (a level trigger, typically) invokes
  them by name.
- `RelationSetup` calls the bare global `GetGuidByName("China")` where the rest of the file consistently
  uses `Pg.GetGuidByName(...)` — likely just an alternate global alias rather than a bug, but worth
  knowing the two forms coexist in this corpus.
