---
title: ChiCon001
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 1
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# ChiCon001

## Overview
A China story contract: rescue a captured VIP ("PartyOfficial") from a hotel, subdue and release the
prisoner, then escort them on foot to a dropoff point. An optional bonus objective — destroy three nearby
buildings — pays a $50,000 bonus (doubled to $50,000 per player in co-op). Ambient AI "skirmish" vehicles
are routed into nearby scripted firefights for atmosphere, and the player is granted a free
`ChiCon001_RocketArtillery` support for the mission's duration.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxSubtitle`, `DangerousBuilding`, `MrxChiCon001Rescue`, `MrxVoSequence`, `MrxSupportData`
  (imported twice in a row — a harmless duplicate `import()` call), `MrxFactionManager`, `MrxMusic`

`MrxFactionManager` and `MrxChiCon001Rescue` have no visible call site in this file (no
`MrxFactionManager.*` call, and no child created with `sModuleName = "MrxChiCon001Rescue"`) — both
imports appear unused here.

## Instance pattern
A native `MrxTaskContract` subclass. Module-level globals: `BldgDeathCount` (bonus-building kill count),
`uTarget` (the VIP's GUID), `oActionObjectve` (the release-objective child, note the typo'd name), and
`eChiVipDamage` (a one-shot half-health VO trigger).

## Functions
### `LoadAssets(self, tSaveData)`
Adds the `vz_state_chicon001`/`Vz_state_ChiCon001_Pristine` layers, then signals `AssetsLoaded`.

### `Activated(self)`
Calls the base `MrxTaskContract.Activated`, removes the pre-mission layers, arms death events on the
three bonus-building targets, plays the opening VO (`FionaVo`), creates the VIP release objective, arms a
prisoner-death and half-health VO trigger, and sets up the bonus-building destroy objective and freebie
support.

### `FionaVo(self)`
Plays a staggered banter/threat VO sequence a few seconds after activation (including switching to threat
music), plus a proximity-triggered VO line near one of the bonus buildings.

### `SetUpFirefights(self)`
Orders three "ChineseSkirmish" vehicle drivers onto preset firefight paths. **Called incorrectly**: see
Notes — the call site evaluates this function immediately rather than registering it as an event
callback.

### `SubdueTarget(self, uTarget)`
Plays a VO line and shows a health bar over the VIP once they wake.

### `ReleaseTarget(self, uTarget, tObjects)`
Switches to "kickass" music, tags the VIP as a `"Prisoner"`, and creates the `MrxTaskObjectiveDeliver`
child to escort them to the dropoff.

### `DisplayLifeBar(self, uGuid, nOldHealth)`
Computes a health percentage/color from its `uGuid`/`nOldHealth` arguments but then calls
`MrxUtil.DisplayHealthBar` on the module-level `uTarget` global instead of `uGuid` — the computed
percentage/color are never used. **No call site found anywhere in this file**; appears to be dead,
half-finished code.

### `DestroyAlliedBldgSetup(self)`
Creates the optional `MrxTaskObjectiveDestroy` child for the three bonus buildings, wiring `BonusComplete`
on completion.

### `BonusCompleteVO(self)`
Plays a VO line for the first, second, or third bonus building destroyed.

### `BonusComplete(self)`
Plays the bonus-complete VO and pays a $50,000 bonus (per player in co-op).

### `SpawnPatrols(self, sVeh, sPoint, sPath)`
Spawns a vehicle at a named point and arms a hibernation trigger that sends it down a path via
`ReinforcementPatrol` once it wakes.

### `ReinforcementPatrol(self, sVeh, sPath)`
Sends a spawned vehicle's driver down a path at low priority/low haste.

### `PrisonerUnrescued(self)`
Sets a cancel message and cancels the contract after the prisoner dies.

### `PrisonerUndelivered(self)`
Sets a different cancel message and cancels the contract if the delivery objective is abandoned.

### `Cleanup(self)`
Clears the HUD objective-tray slots, removes the freebie support, marks the mission layers for removal,
stops the special music, stops the VIP's health bar, and calls the base `MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectDeath` — each of the three bonus buildings dying increments `BldgDeathCount` and plays a
  VO line; the VIP dying triggers `PrisonerUnrescued`.
- `Event.ObjectHibernation` — the VIP waking triggers `SubdueTarget`.
- `Event.Boundary` — entering `LineRegion_Firefights` is *intended* to trigger `SetUpFirefights` (see
  Notes — this registration looks broken).
- `Event.ObjectHealthLessThan` — the VIP dropping below half health plays a one-shot VO warning.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **Likely bug in the firefight trigger**: `Activated` registers the boundary event as
  `self:_CreateEvent(Event.Boundary, {...}, SetUpFirefights({self}))` — calling `SetUpFirefights({self})`
  directly as part of building the argument list, rather than passing `SetUpFirefights` as a function
  reference with a separate `{self}` args table (the pattern used everywhere else in this corpus). In
  practice this means `SetUpFirefights` runs immediately, synchronously, at activation time — not when the
  player enters `LineRegion_Firefights` — and the event registration itself ends up with a `nil` callback
  and no args table.
- `DisplayLifeBar` is dead code with a parameter/global mismatch (computes from its arguments, then acts
  on a different global) — don't use it as a reference for how health-bar display normally works here;
  see `SubdueTarget`'s plain `MrxUtil.DisplayHealthBar(self, uTarget, 0, true, 0)` call instead.
- Bonus payout is a flat $50,000 (per player in co-op), same shape as [AllCon001](allcon001)'s VIP bonus
  but a fixed amount rather than scaled by count.
