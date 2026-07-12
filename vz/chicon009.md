---
title: ChiCon009
parent: China Contracts & Jobs
grand_parent: VZ Modules
nav_order: 5
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# ChiCon009

## Overview
A China minor/side contract: acquire a locked "ZBD2000" APC, rendezvous with the player's current
position, then escort a spawned civilian ambulance (shown with a health bar) along a preset path to a
dropoff — all under an overall countdown timer that fails the contract if it expires. The ambulance dying
or hibernating too far from the player also fails the contract, each with its own distinct cancel
message. Like the other race/escort minor contracts in this batch, the timer and escort haste tighten on
replay via `self:GetNumCompletions()`.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxTaskObjectiveDeliver`, `MrxLayerManager`, `MrxTimer`, `MrxSubtitle`, `MrxAchievements`,
  `MrxMusic`

`MrxAchievements` has no visible call site in this file (unlike [ChiCon008](chicon008), where the
equivalent import *is* used) — appears unused here.

A module-level `tDestroyLocs` table (eight `"TargetN"` names) is declared but never read anywhere in this
file — the proximity VO triggers in `FionaChiCon009Vo` reference `"Target1"`/`"Target4"` as literal
strings instead of indexing this table. Dead data, the same shape as `AntiAir`'s `_tLockOnUpdates` field
noted elsewhere in this wiki.

## Instance pattern
A native `MrxTaskContract` subclass. Module-level globals: `oTimer` (the `MrxTimer` countdown instance),
`civAmbulance` (the spawned ambulance GUID), and `self.eDeath` (the ambulance-death event handle).

## Functions
### `Activated(self)`
Calls the base `MrxTaskContract.Activated`, plays special mission music, removes the pre-mission layer,
locks the APC, resolves the time limit from prior completions, starts an `MrxTimer` countdown (failing
via `OutOfTime` if it runs out), plays the opening VO, creates the `MrxTaskObjectiveEnterVehicle` child
for acquiring the APC, arms a seat-enter shortcut that completes that objective early, and calls
`FionaChiCon009Vo`/`AmbulanceSetup`.

### `RendezvousAmbulance(self)`
Creates the `MrxTaskObjectiveDeliver` child that brings the player to the ambulance's rendezvous point.

### `AmbulanceTemp(self)`
Reschedules `AmbulanceSetup` ten seconds later. **No call site found anywhere in this file.**

### `AmbulanceSetup(self)`
Spawns the civilian ambulance at its named spawn point.

### `AmbulanceObjective(self)`
Shows the ambulance's health bar, creates the escort `MrxTaskObjectiveDeliver` child and a second,
purely-cosmetic `MrxTaskObjective` child that just blips the dropoff location, arms a proximity-based
early-complete trigger, arms an ambulance-death cancel trigger, sends the ambulance down its path (haste
scaling with completion count), and arms VO triggers for the ambulance falling behind or hibernating.

### `PlayAmbulanceMusic(self)`
Plays the `"mu_fac_oc_kickass_01"` special music cue.

### `FionaChiCon009Vo(self)`
Arms two proximity-triggered VO lines near `"Target4"`/`"Target1"`.

### `VehicleDeath(self)`
Sets a cancel message and plays a cancel VO. **No call site found anywhere in this file.**

### `VehicleUnentered(self)`
Sets a cancel message and cancels the contract if the APC-acquire objective is cancelled — wired via
`tOnCancel` on `oAcquireTankObjective`.

### `MineActive(self)`
Sets a cancel message and cancels the contract if the rendezvous objective is cancelled.

### `OutOfTime(self)`
Sets a cancel message and cancels the contract when the countdown timer runs out.

### `AmbulanceDestroyed(self)`
Sets a cancel message and cancels the contract if the escort objective is cancelled.

### `AmbulanceAbandoned(self)`
Sets a cancel message and cancels the contract immediately (no VO sequence, unlike the other cancel
paths).

### `Cleanup(self)`
Restores the pre-mission layer, stops the countdown timer, stops the ambulance's health bar and removes
it if still valid, stops the special music, and calls the base `MrxTaskContract.Cleanup`.

## Events
- `Event.ObjectInSeat` — entering/exiting the APC's `"D"`/`"E"` seat states completes the acquire
  objective early (see Notes on the seat-state casing).
- `Event.ObjectProximity` — the ambulance nearing its dropoff completes the escort objective; the player
  falling too far behind the ambulance plays a VO warning; two target-proximity triggers play VO lines.
- `Event.ObjectHibernation` — the ambulance hibernating plays a VO line and calls `AmbulanceAbandoned`.
- `Event.ObjectDeath` — the ambulance dying cancels the escort objective.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **Possible case-mismatch**: the APC seat-enter shortcut in `Activated` filters on `"D"`/`"E"` (uppercase),
  where every other seat-state filter seen across this batch (e.g. [AllCon008](allcon008),
  [ChiCon008](chicon008)) uses lowercase `"d"`/`"e"`. If this engine's seat-state filter strings are
  case-sensitive, this event would never actually fire, and the APC-acquire objective would only ever
  complete through whatever other path exists — worth live-testing rather than assuming either way from
  source alone.
- `tDestroyLocs` (an 8-entry `Target1`..`Target8` table) is declared at module scope but never read —
  dead data, not wired to anything in this file.
- `AmbulanceTemp` and `VehicleDeath` are both defined with no call site anywhere in this file.
- The escort-completion VO reuses `Fiona-In-Mission-Contract-Pmc01-10` — the same generic "you won" line
  seen in [ChiCon008](chicon008)'s race completion.
