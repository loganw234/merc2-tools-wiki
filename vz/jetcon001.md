---
title: JetCon001
parent: Story & Special Contracts
grand_parent: VZ Modules
nav_order: 2
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# JetCon001

## Overview
`JetCon001` is the recruitment mission for the Jet-pilot specialist. `wifbriefingdata.lua`'s `Intros.Jet`
entry (`sTitle = "[Briefing.Intro.JetPmcBoss]"`) is the briefing shown before this contract starts, framed
as a PMC-boss-style recruitment intro rather than a faction contract. The mission itself is a
bunker-buster escort/defense: the player extracts 3 "bunker buster" ordnance crates while surviving a
beach ambush, an AA-jeep counterattack, and a helicopter attack run, then uses the recovered bunker
busters to destroy a VZ bunker. Completing it (`MrxSupportData.SetJetPilotRecruited(true)`, set in
`Activated`) is what unlocks the Jet specialist.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (→
  [`MrxTaskMission`](../resident/mrxtaskmission) → [`MrxTask`](../resident/mrxtask))
- Imports: `MrxSubtitle`, [`Munitions`](../resident/munitions), [`MrxVoSequence`](../resident/mrxvosequence),
  [`MrxPmc`](../resident/mrxpmc), `MrxAi`, [`MrxSupportData`](../resident/mrxsupportdata)

  `MrxSubtitle` and `MrxAi` are imported but never referenced anywhere else in the file (confirmed by
  direct search) — every AI-goal call in this file goes through the plain [`Ai`](../namespaces/ai)
  namespace (`Ai.Goal({...})`), not the imported `MrxAi` wrapper.

## Instance pattern
Native task-framework subclass (`self`-based). Module-level (not per-`self`) state shared across
callbacks: `oExtractBB`/`oDestroyBunker` (references to the two `MrxTaskObjective`-family child tasks),
`nBBExtracted` (bunker busters collected so far, 0-3), `nCallbackID` (the stockpile-change callback handle
from `MrxPmc.SetStockpileChangeCallback`), and `NETEVENT_SETBBQTY = 0` (this contract's one custom
net-event ID, used to sync the bunker-buster count to clients).

## Functions

### `LoadAssets(self, tSaveData)`
Adds 3 layers (`Vz_State_JetCon001`, `_Pristine`, `_CP01`) then calls `AssetsLoaded`.

### `Activated(self)`
Calls `MrxTaskContract.Activated(self)` (super call), marks the Jet pilot recruited, disables the
`JetCon001_ScrambleCopter` vehicle, and arms all 4 region triggers (`BeachRegionActivate`,
`AASiteRegionActivate`, `BBWarningRegionActivate`, `BunkerIslandRegionActivate`). Then branches on
checkpoint flags: `JC001CP02` resumes with all 3 bunker busters already collected and goes straight to
`DestroyBunker`; `JC001CP01` resumes mid-extraction via `ExtractBB`; a fresh start also arms the checkpoint
and travel-music regions and plays the mission's intro VO sequence.

### `CheckpointRegionActivate(self)` / `CheckpointActivate(self)`
Arms a region-enter trigger that (once, guarded by `_GetFlag`) sets `JC001CP01` and calls `_Checkpoint`.

### `BeachRegionActivate(self)` / `BeachAssault(self)`
Arms a region trigger that sends a tank AI down a supply-beach ambush path.

### `AASiteRegionActivate(self)` / `AASiteRegionAssault(self)`
Arms a region trigger that plays a VO warning and sends the AA-site jeep's driver down an attack path at
high priority/haste.

### `BBWarningRegionActivate(self)` / `BBWarningVO(self)`
Arms a region trigger that plays a single VO warning line as the player nears the bunker-buster crates.

### `CopterAttackRegionActivate(self)` / `CopterSpawn(self)` / `CopterMove(self)` / `CopterAttack(self)`
A 4-step chain: region entry adds the `Vz_State_JetCon001_CopterAttack` layer, which (once loaded) sends
the spawned attack helicopter down a one-way path, which on path completion sets it to directly attack the
player. Only armed once all 3 bunker busters are extracted (see `BBPickup` below).

### `BunkerIslandRegionActivate(self)` / `BunkerIslandArrive(self)`
Arms a region trigger that re-enables the `JetCon001_ScrambleCopter` and sends a jeep on bunker-island
patrol.

### `NearBunkerRegionActivate(self)` / `NearBunkerVO(self)`
Arms a region trigger (near the bunker) that plays the laser-designator usage hint VO.

### `ExtractBB(self)`
Creates the bunker-buster collection objective ([`MrxTaskObjective`](../resident/mrxtaskobjective), quota
3, targets the 3 named crates), watches all 3 for death (→ `CancelExtractBB`) and for a `"MunitionsPickup"`
script event matching each crate's GUID (→ `BBPickup`), and hides their munitions markers via
[`Munitions.HideMarker`](../resident/munitions).

### `BBPickup(self, nBBindex)`
Increments `nBBExtracted`, syncs the new count to clients via `NETEVENT_SETBBQTY`, then attempts to clear
the death-watch events. **This cleanup looks broken as written**: the guard conditions check
`uBBExtract01`/`02`/`03` (the `MunitionsPickup` script-event handles) but the deletes themselves call
`Event.Delete("uBBDestroyed01")` etc. with a **quoted string literal** rather than the actual
`uBBDestroyed01`/`02`/`03` variables (the real `ObjectDeath` handles set in `ExtractBB`) — likely a
copy-paste slip. Below 3 collected, removes just that one crate from the objective's targets; at 3, arms
the copter-attack sequence, plays VO, and sets the `JC001CP02` checkpoint.

### `CancelExtractBB(self)`
Fires if a bunker-buster crate is destroyed instead of collected: sets the cancel message and cancels the
extraction objective.

### `DestroyBunker(self)`
Arms the near-bunker VO trigger, plays VO, creates the `MrxTaskObjectiveDestroy`
([`MrxTaskObjectiveDestroy`](../resident/mrxtaskobjectivedestroy)) child targeting `JetCon001_Bunker`, and
registers `MrxPmc.SetStockpileChangeCallback("bunkerbuster", "==", 0, ...)` so running out of bunker
busters (rather than destroying the bunker) is handled explicitly.

### `CancelDestroyBunker(self)`
The stockpile-empty callback: waits 12s, then checks whether the bunker is still alive — if so, cancels
the destroy objective (out of ammo); if it happens to already be dead, completes the objective anyway as a
safety net. Note both branches log the same `"...WASTED YOUR LAST BB!!!"` message via `Debug.Printf`, even
in the branch where the bunker is confirmed destroyed — a copy-pasted (harmless) debug string, not a logic
bug.

### `CompleteDestroyBunker(self)` / `FionaCompleteVO(self)`
5-second delay, then a completion VO sequence ending in `self.Complete`.

### `FionaFailVO(self)`
Defined but **never called anywhere in this file** (confirmed by direct search) — dead code; likely
superseded by `CancelDestroyBunker`'s timer-based fail path.

### `Cleanup(self)`
Deletes the stockpile-change callback, un-recruits the Jet pilot flag, removes the CP01 layer, and calls
`MrxTaskContract.Cleanup(self)`.

### `TravelMusicOnRegionActivate(self)` / `StartTravelMusic(self)` / `TravelMusicOffRegionActivate(self)` / `StopTravelMusic(self)`
Locks a fixed "travel" music level between the mission start and the checkpoint region, then unlocks it
once the player reaches the checkpoint.

### `NetEventCallback(nType, tArgs)`
Client-side handler for `NETEVENT_SETBBQTY`: applies the synced bunker-buster count via
`MrxPmc.SetSupportQty`.

## Events
- `Event.Boundary` — the region-enter triggers that drive nearly every set-piece in this mission (beach
  assault, AA site, bunker-buster warning, copter attack, bunker island, near-bunker, checkpoint, travel
  music on/off).
- `Event.ObjectDeath` — watches each bunker-buster crate (`CancelExtractBB`).
- `Event.ScriptEvent` — `"MunitionsPickup"`, filtered per-crate by GUID, drives `BBPickup`.
- `Event.TimerRelative` — `CancelDestroyBunker`'s 12s ammo-check delay and `CompleteDestroyBunker`'s 5s
  completion delay.

## Notes for modders
- This is the native `MrxTaskContract`/`WifMissionData` mission system, not
  [Contract Framework](../contract-framework/) — see
  [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
  different, ephemeral system instead of hooking into this one directly.
- The three checkpoint branches in `Activated` (fresh / `JC001CP01` / `JC001CP02`) are the template to
  follow if you need a similarly multi-stage mission to resume correctly from a save.
- `BBPickup`'s event cleanup and `FionaFailVO` are both confirmed-questionable/dead — see above — don't
  assume everything defined here is either reachable or functioning as named.
