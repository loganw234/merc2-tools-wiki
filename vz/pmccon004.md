---
title: PmcCon004
parent: PMC Contracts & Jobs
grand_parent: VZ Modules
nav_order: 4
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# PmcCon004

## Overview
PmcCon004 is the story contract covering the destruction of Solano's second bunker and the hijack of his escape helicopter. The player destroys the bunker (via a "Nuked" freebie strike, watched for proximity to the target), then hijacks Solano's Mi35 before he can get away, racing a timer once a boundary line region is crossed. Two bridges along the route trigger scripted artillery-strike VO and effects when destroyed. The contract coordinates with a shared `HijackContractManager` so only one hijack-style contract is considered "active" at a time, and pays a large flat bonus if Solano isn't already confirmed dead by the time the contract ends.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `MrxApcDrop`, `MrxUtil`, `MrxPlayer`, `MrxTimer`, `MrxSubtitle`, `HijackContractManager`, `MrxSupportData`, `MrxVoSequence`, `MrxArtilleryAttack`, `MrxMusic`, `MrxFactionManager`, `MrxVerifyManager`

## Instance pattern
A native `MrxTaskContract` subclass, state kept in bare module-level globals. Four custom net events (`NETEVENT_HIJACKSOLANO`, `NETEVENT_ARTILLERYATTACK`, `NETEVENT_KILLBRIDGE`, `NETEVENT_CHANGEATMOSPHERE`) replicate atmosphere changes, artillery-attack VFX, and the Solano-hijack handoff to co-op clients.

## Functions
### `LoadAssets(self, tSaveData)` / `Activated(self)`
`LoadAssets` swaps in the bunker/base/city layers for this contract. `Activated` sets two regions to "warzone" atmosphere (replicated to clients via `NETEVENT_CHANGEATMOSPHERE`), disables a specific VZ attack helicopter's usability, creates the "destroy the bunker" objective (setting the `HijackInitiated` flag and calling `SolanoHijackInit` on completion, or `BunkerIntact` — a fail — on cancel), adds a `"PmcCon004_Nuke"` freebie, listens for a `"Nuked"` script event to call `NukeDetonated`, sets up compound music and bridge-destruction triggers, and registers itself with `HijackContractManager`.

### `NukeDetonated(self, tLoc)`
Checks the strike location's distance to the bunker; close enough kills it directly (with a camera shake), otherwise plays a "missed" VO line and fails via `BunkerIntact`.

### `SetCompoundMusic(self)` / `SetMissionMusic(self)` / `BridgeDestruction(self)`
Boundary-triggered music cues, and two bridge-crossing regions that each play VO and call `MrxArtilleryAttack.Create` at two locations (replicated to clients via `NETEVENT_ARTILLERYATTACK`).

### `DetectBridgeOneProximity` / `TwoProximity` / `ThreeProximity`, `SetUpApcDrop1/2/3`, `ApcDrop`, `_DelayedAPCSpawn`, `DetectHeli1` / `DetectHeli2`, `SpawnHelis`
A whole subsystem for spawning ambush APCs at three bridge crossings and reinforcement helicopters near two check regions — none of these functions is called from anywhere else in this file. As elsewhere in this batch, that may mean they're invoked by level-placed triggers outside this corpus (the same way `NetEventCallback` is invoked by the net layer rather than from in-file code) rather than being dead code; it can't be confirmed from source alone.

### `SolanoHijackInit(self)` / `SolanoObjective(self)` / `SolanoHijackObjective(self)` / `SolanoHijackLayerLoaded(self)` / `SolanoStaging(self)`
The hijack setup: loads a layer, then arms the "go to Solano" delivery objective, a "board the Mi35" enter-vehicle objective, staged explosion/mook-spawn triggers along the approach (`SolanoStaging`), and listens for `"SolanoHijackComplete"`/`"SolanoHijackFailed"` script events to complete/cancel the contract.

### `PlayerEntersDockRegion(self)` / `ProximityCallback(self, tGuid)` / `DockAttack(self, tGuid)` / `NetEventCallback(nEventType, tArgs)`
Detects which player reaches the dock/hijack trigger first (replicating the choice to the other machine via `NETEVENT_HIJACKSOLANO` if it wasn't the local player), then force-exits that player from their current vehicle and puts them into the Mi35 directly.

### `SolanoRace(self)` / `PlayerEntersTimerRegion(self)` / `StartTimeSubtitle(self)` / `OutOfTimeSubtitle(self)`
A 60-second `MrxTimer` started on crossing a timer line region; running out cancels the *active hijack contract* via `HijackContractManager.CancelActiveContract()` rather than calling `self:Cancel()` directly.

### `BunkerIntact(self)` / `SolanoEscaped(self)`
Fail paths — cancel the contract with an appropriate message, the latter via a VO sequence first.

### `Cleanup(self)`
Deletes the atmosphere-replication join event, pays a flat 25,000,000 bonus (split evenly in co-op) if `MrxVerifyManager.GetKilled()` reports zero kills (i.e. Solano wasn't otherwise confirmed dead), removes the nuke freebie, and calls base `MrxTaskContract.Cleanup`.

## Events
- `Event.ScriptEvent` — `"mpPlayerJoin"` (re-broadcast atmosphere state to a joining client), `"Nuked"`, `"SolanoHijackComplete"`/`"SolanoHijackFailed"`.
- `Event.Boundary` — bridge-destruction regions, staging explosion triggers, the hijack timer-start line, ambush region triggers.
- `Event.ObjectHibernation` — gates the watched VZ helicopter's usability once it's awake.
- `Event.ObjectProximity` — the dock/hijack-trigger detection.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract Framework](../contract-framework/) — see [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system instead of hooking into this one directly.

- `HijackContractManager` (used here and cancelled via `HijackContractManager.CancelActiveContract()` in `OutOfTimeSubtitle`) looks like a shared coordinator ensuring only one "hijack" story beat runs at a time across contracts — worth knowing if you're studying how these native missions avoid stepping on each other.
- The APC-drop and heli-reinforcement subsystem (`DetectBridge*Proximity`, `SetUpApcDrop*`, `DetectHeli1/2`, `SpawnHelis`) has no in-file caller — don't assume it fires without external confirmation.
- No direct `MrxPmc` calls in this file; the "PmcCon004_Nuke" freebie is added/removed via `MrxSupportData` instead.
