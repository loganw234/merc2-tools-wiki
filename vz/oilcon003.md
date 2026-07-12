---
title: OilCon003
parent: Oil Company Contracts & Jobs
grand_parent: VZ Modules
nav_order: 3
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# OilCon003

## Overview
An Oil Company minor/side story contract (VO keys read `MinorContract-Oil03`): talk to an OC VIP, then
deliver him by vehicle to a drop point within a shrinking time limit, chased by a `MrxFactionManager`
custom pursuit that escalates with `GetNumCompletions()`. The cash bonus decays through two time
thresholds, and a trio of polling functions bark VO reactions to reckless driving, vehicle damage, and the
VIP taking damage.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxFactionManager`, `MrxVoSequence`

## Instance pattern
A native task-framework subclass — `self`-based lifecycle overrides, not the `Inheritable`/`uGuid` pattern.
Module-level globals: `nBonusMult` (3/2/1, stepped down by the two time-warning functions), `nBaseReward`
(set per difficulty tier), `nDudeHealth`/`nVehHealth` (previous-tick snapshots the polling VO functions diff
against each call).

## Functions
### `Activated(self)`
Seeds `nBonusMult = 3` and the health snapshots, then creates a `MrxTaskObjectiveAction` ("talk to the
VIP") with completion routed to `DeliverDude`.

### `DeliverDude(self, uTalked)`
Picks time limit, reward decay thresholds, difficulty tier, and drop destination purely from
`self:GetNumCompletions()` (first run vs. one prior completion vs. two-plus), then creates the actual
`MrxTaskObjectiveDeliver` (time-limited, `uStartAttachedToPlayer = uTalked`), arms the two reward-decay
timers (`TimeWarningFirst`/`Second`), the pursuit start/stop proximity triggers, and locks the action-level
music at intensity 3 for the drive.

### `TimeWarningFirst(self)` / `TimeWarningSecond(self)` / `Complete(self)`
Each warning drops `nBonusMult` by one step, replays a random OC-exec VO line, and rewrites the HUD tray
cash-bonus text. `Complete` (overriding the base) pays out `nBaseReward * nBonusMult` to both players
before calling `MrxTaskContract.Complete(self)`.

### `StartPursuit(self, nPurLevel)` / `ClearPursuit(self)`
Three hardcoded `MrxFactionManager.SetCustomPursuit` tables (tier 1: jeep-only; tier 2: jeep+APC; tier 3:
jeep+tank), applied to the `"VZ"` faction guid. Mirrors the same tiered-pursuit shape seen in
[GurCon003](gurcon003), but against `"VZ"` instead of `"OC"`.

### `SpeedVO(self)` / `DamageVehicleVO(self)` / `ResetDamageVehVO(self)` / `DamageVO(self)`
Three independent self-rescheduling polling loops (each re-arms its own short `TimerRelative` every call),
diffing the current vehicle speed/health/VIP health against the previous reading to decide whether to bark
a reactive VO line — speeding over 30, more than 7 damage in one tick, or any drop in the VIP's own health.

### `Cleanup(self)`
Clears the custom pursuit lock and the HUD tray bonus slot, then calls `MrxTaskContract.Cleanup(self)`.

## Events
`Event.ObjectDeath` (VIP killed — cancels), `Event.ObjectProximity` (VZ warning near the VIP, pursuit
start/stop near the route endpoints), `Event.TimerRelative` (the two reward-decay timers and all three
polling-VO self-reschedules).

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not
[Contract Framework](../contract-framework/) — see [VZ Modules](../vz/) for the general
native-vs-framework explanation and
[Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
different, ephemeral system instead of hooking into this one directly.
- The "snapshot last tick, diff against current, re-arm a short timer regardless of outcome" shape
  (`SpeedVO`/`DamageVehicleVO`/`DamageVO`) is a reusable way to get reactive ambient VO out of a value that
  has no dedicated engine event of its own (there's no `Event.ObjectSpeedThreshold`, for instance) —
  polling on a timer is the fallback.
