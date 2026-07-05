---
title: FriendlyGate
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [ai, gate]
verified: true
verified_note: 'deeper pass: re-confirmed the bare _tGates[uGuid] pattern and every function; rewrote Events to enumerate all real subscriptions (near/far Event.ObjectProximity 20m/40m, two Event.ObjectHealth gate-arm nodes, Event.ObjectDeath, Event.TimerRelative, the MrxFactionManager attitude wrapper); added a Module constants section (radii, filter string, part names, per-faction VO lines, attitude thresholds); flagged the top-level tFactions local as DEAD code and fixed the old Notes that referenced a non-existent _tFactions table'
---

# FriendlyGate

*Module: friendlygate.lua*

## Overview
The `FriendlyGate` module manages the behavior of gates that open based on proximity to friendly or allied vehicles. It checks for nearby valid candidates (hero or faction-vehicles) and opens if any are present and not locked, with attitude-gated conditions for the player. The gate also has a far-edge re-check at 40m.

## Inheritance
- Inherits from: none — base/utility module
- Imports: [`MrxFactionManager`](mrxfactionmanager) (attitude tests + faction abbreviations),
  [`MrxUtil`](mrxutil) (`GetFaction`), [`MrxVoSequence`](mrxvosequence) (the guard's "gate opening" voice line)

## Instance pattern
**Not the `Inheritable`/rich-instance pattern, and not a class-factory either** — confirmed from source: a
plain module-level table, `_tGates[uGateGuid]`, with no `Create`/`Delete`/`setmetatable` anywhere. There's
also a module-level `Init()`/`Deinit()` pair (both empty here) and `SaveSingleton`/`LoadSingleton` for
persisting the lock table, alongside the per-gate `OnActivate`. Each activated gate gets a sub-table entry in
`_tGates`, not a full instance object with inherited methods. It tracks the following key fields:
- `_tLockedGates`: A table to store locked gate GUIDs.
- `_tGates`: A table to manage gate-specific data, including proximity events, attitude change events, candidate vehicles, and filter settings.

## Functions
### `Init()`
Empty in this file — no module setup happens here.

### `Deinit()`
Empty in this file — no teardown happens here.

### `LockGate(uGateGuid, bLock)`
Sets or clears a gate's lock state in `_tLockedGates`. If the gate is already registered, it evaluates candidates again.

### `IsGateLocked(uGateGuid)`
Checks if a gate is locked by looking up its GUID in `_tLockedGates`.

### `OnActivate(uGateGuid)`
Called when the gate instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGateGuid)`
Initializes the gate's behavior, including setting lights and creating proximity and attitude change events. It also registers death events for specific parts of the gate.

### `OnDeath(uGateGuid, uNodeGuid)`
Handles the gate's death by calling `OnDeactivate`.

### `OnDeactivate(uGateGuid)`
Cleans up all events and data associated with the gate when it is deactivated.

### `CreateProxEvent(uFilter, uGateGuid)`
Creates a proximity event for the gate to detect nearby vehicles within 20m.

### `_EvaluateCandidates(uGateGuid, bApproaching, vObjects)`
Evaluates candidate vehicles approaching or leaving the gate's proximity. It updates the list of candidates and opens/closes the gate based on conditions.

### `_RemoveCandidate(uGateGuid, uGuid)`
Removes a vehicle from the list of candidates by deleting associated events.

### `_ChangeState(uGateGuid, bOpen)`
Changes the open state of the gate, playing a voice-over if it opens for the first time and updating lights accordingly.

### `_TestAttitude(sGateFaction, uPlayerCharGuid)`
Tests the attitude between the gate's faction and the player character to determine if the gate should open.
Uses `MrxFactionManager.GetPerceivedFaction`/`GetFactionAbbrev` and `MrxFactionManager.TestAttitude(...,
">=", sTargetAttitude)`. The threshold is `"Friendly"` normally, but relaxes to `"Neutral"` when the
character reads as PMC (and additionally requires `MrxFactionManager.IsAttitudeMutable(sGateFactionAbbrev)`)
— so a PMC player only needs the gate faction to be neutral-or-better, not friendly.

### `SaveSingleton()`
Returns `_tLockedGates` so the engine can persist which gates are locked across save/load. Only the lock
table is saved — live proximity/candidate state in `_tGates` is rebuilt on activation.

### `LoadSingleton(tLockedGates)`
Restores `_tLockedGates` from a saved table (if one is passed). This is why a locked gate stays locked after
loading a save.

## Events
- **Creates** `Event.ObjectHibernation` (`OnActivate`) to call `Start` when the gate leaves hibernation.
- **Creates** the near `Event.ObjectProximity` (`CreateProxEvent`): fires when a filter-matching object comes
  within `< 20`m, calling `_EvaluateCandidates(uGateGuid, true)`.
- **Creates** a per-candidate far `Event.ObjectProximity` (`> 40`m) so a candidate that drives away is
  re-evaluated, plus a per-candidate `Event.ObjectDeath` so killed candidates are dropped.
- **Creates** two `Event.ObjectHealth` listeners (`< 1` health on nodes `piece1a_propattach00` and
  `piece1a_propattach01`) so destroying either gate arm calls `OnDeath` → `OnDeactivate`.
- **Creates** a one-shot `Event.TimerRelative` `{2}` in `Start` to set the initial light state.
- **Creates** a persistent attitude-change event via
  `MrxFactionManager.CreatePersistentAttitudeChangeEvent({sFactionAbbrev, "Pmc"}, _EvaluateCandidates, ...)`
  so the gate re-evaluates when PMC's standing with the gate's faction changes (this is a
  `MrxFactionManager` wrapper, not a raw `Event.*` constant).
- `OnActivate`/`OnDeactivate`/`OnDeath` are engine lifecycle callbacks, not `Event.*` subscriptions.

## Module constants & tunables
- Proximity radii: open trigger `< 20`m (near), re-check trigger `> 40`m (far) — both inline literals in
  `CreateProxEvent`/`_EvaluateCandidates`.
- Object filter: `"Hero||(" .. sFaction .. "&&Vehicle)"` — the gate opens for the hero, or for a vehicle of
  the gate's own faction (built with `ObjectFilter.Create`/`SetFilter`).
- Destructible gate-arm nodes: `"piece1a_propattach00"` and `"piece1a_propattach01"` (health `< 1` kills the
  gate).
- Vehicle parts toggled for lights: `"LightFront"` (green/open) and `"LightBrake"` (red/closed).
- Attitude threshold: `">= Friendly"` for most factions, relaxed to `">= Neutral"` for PMC (see
  `_TestAttitude`).
- Guard voice lines on first open (`_ChangeState`), by gate faction: `Allied`
  `"AlliedSoldier01.Misc.GateYes01"`, `China` `"ChinaSoldier01.Misc.GateYes01"`, `Guerilla`
  `"GurSoldier01.Misc.GateYes01"`, `OC` `"OCSoldier01.Misc.GateYes01"`, `VZ`
  `"GurSoldier01.Misc.GateYes01"` — played at priority `MrxVoSequence.knPriorityFreeplay` on the nearest
  living soldier found within `25`m via `Pg.FastCollectHumans`.

{: .note }
> The module-level `local tFactions = {"VZ", "Allied", "China", "Guerilla", "OC", "Pirate", "PMC", "Civ"}`
> declared at the top of the file is **dead** — it is never read anywhere in `friendlygate.lua`. (An earlier
> version of this page told modders to edit a non-existent `_tFactions` table; there is no `_tFactions`, and
> the real `tFactions` local does nothing.)

## Notes for modders
- Use `LockGate(uGateGuid, bLock)` to force a gate closed regardless of who is near — the lock state persists
  across saves (`SaveSingleton`/`LoadSingleton`).
- Tune who opens the gate by editing the filter string (`"Hero||(faction&&Vehicle)"`) or the attitude logic
  in `_TestAttitude`; tune *when* by changing the `20`m/`40`m proximity radii.
- Attitude re-evaluation is driven through [`MrxFactionManager`](mrxfactionmanager) — changing PMC's standing
  with the gate faction at runtime will open/close eligible gates automatically.
- The `tFactions` local at the top of the file is dead code (see note above) — do not rely on or edit it.