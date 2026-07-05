---
title: MrxTaskRace
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTask
tags: [task, race]
verified: true
verified_note: deeper pass — surfaced module constants (kTYPE_GATE/kTYPE_RING, _knWldBlpNearDist=200/_knWldBlpFarDist=300, fWidth default 10, NETEVENT_*); documented that it spawns child MrxTaskObjectiveEnterVehicle + per-checkpoint MrxTaskObjectiveDeliver tasks and records best time via MrxStatsManager; noted the _OnStatusChange decompiler bug (references undefined iGuid/sStatusType)
---

# MrxTaskRace

*Module: mrxtaskrace.lua*

## Overview
`MrxTaskRace` runs a checkpoint race. It marks each course location with a tripwire "gate" or an air "ring",
then spawns a child [`MrxTaskObjectiveDeliver`](mrxtaskobjectivedeliver) objective per checkpoint (deliver
the player/vehicle to the point); reaching the last one finishes the race and records the best time via
[`MrxStatsManager`](mrxstatsmanager). If the race is run in a specific vehicle the player isn't in yet, it
first spawns a child [`MrxTaskObjectiveEnterVehicle`](mrxtaskobjectiveentervehicle) task.

## Module constants & tunables
- `kTYPE_GATE = 1` / `kTYPE_RING = 2` — the two checkpoint marker styles (`sGateType == "ring"` selects
  rings; anything else is a gate/tripwire).
- `_knWldBlpNearDist = 200` / `_knWldBlpFarDist = 300` — world-blip near/far draw distances for the *next*
  checkpoint.
- `fWidth` (config, default `10`) — checkpoint width; `nAddTime` (config) — seconds added to the timer per
  checkpoint cleared.
- `NETEVENT_MARKLOC = 0` / `NETEVENT_UNMARKLOC = 1` / `NETEVENT_MARKFINISH = 2` — custom-net ids for
  syncing checkpoint markers to clients.
- Next-checkpoint blip uses world icon `"HUD_objective_deliverable"` (size `32`) and radar texture
  `"objective_deliverable"` (`8`×`8`).

## Inheritance
- Inherits from: `MrxTask`
- Imports: `MrxGuiHudMessage`, `MrxStatsManager`

## Instance pattern
**Not per-`uGuid` — inherits [`MrxTask`](mrxtask)'s class-factory pattern** (see that page for the general
mechanism), identified by name/lineage rather than a world-object GUID. Key fields tracked via the config
table:
- `fWidth`: The width of each checkpoint.
- `bUseTripWires`: Indicates whether tripwires are used for checkpoints.
- `iGateType`: Type of gate/ring used for checkpoints (`kTYPE_GATE` or `kTYPE_RING`).
- `vTgtInclude`: Target vehicles or characters to include in the race.
- `nAddTime`: Time added to the timer after completing each checkpoint.
- `_tCourseLocs`: List of checkpoint locations.
- `_uWinner`: The player who completed the race.
- `_oTimer`: Timer object for tracking race time.
- `_uTimeStamp`: Timestamp for recording the start and end times of the race.

## Functions
### `NetEventCallback(eventId, tArgs)`
Handles network events related to marking and unmarking checkpoints. It processes `NETEVENT_MARKLOC`, `NETEVENT_UNMARKLOC`, and `NETEVENT_MARKFINISH` events to update blips and markers accordingly.

### `Activated(self)`
Called when the task is activated. Initializes the race configuration, sets default values for width and tripwires, and starts the race if the player is in a controlled vehicle or character.

### `Cleanup(self)`
Cleans up resources used by the race task, such as unmarking locations and removing child tasks.

### `GetWinner(self)`
Returns the GUID of the player who completed the race.

### `_SetupDestination(self)`
Sets up the next checkpoint in the race. Creates a child task for delivering to the current checkpoint location, marks the current and next locations with blips and tripwires, and sends network events if applicable.

### `_GetDspShortDesc(self, nLoc)`
Generates a short description for the current checkpoint or finish line.

### `UnmarkLocation(self)`
Removes blips and markers for the current and next checkpoints. Sends a network event to unmark locations on the server.

### `MarkCurCourseLoc(uGuid, iGateType, fWidth, bFinish)`
Marks the current checkpoint location with a gate or ring and an optional finish marker.

### `MarkNextCourseLoc(uGuid, iGateType, fWidth)`
Marks the next checkpoint location with a gate or ring and adds a world blip for the next checkpoint.

### `UnmarkCourseLoc(tMarkerData)`
Removes all markers (gate, finish, world blip) associated with a checkpoint.

### `_StartRace(self)`
Starts the race by setting up the timer and the first checkpoint. If multiple target vehicles are included, it waits for one to be player-controlled before starting.

### `_FinishRace(self)`
Completes the race by recording the best time using `MrxStatsManager` and marking the task as complete.

### `_OnStatusChange(self, uGuid, sReason)`
Status callback passed to the child objectives. If several target vehicles remain it just drops the
finished/destroyed one from `vTgtInclude`; otherwise it fires config `fVehiclesDestroyedCallback`.

{: .warning }
> This function's fallback branch references `iGuid` and `sStatusType`, which are **not** its parameters
> (they're `uGuid`/`sReason`) — a latent bug carried over from the original code. The forwarded values will
> be `nil`. Don't rely on the args your `fVehiclesDestroyedCallback` receives in that path.

### `_DrawTripWire(uGuid, fWidth, r, g, b, bFinish)`
Draws a tripwire for the current checkpoint location with optional finish markers.

### `_DrawRing(uGuid, fWidth, r, g, b, bFinish)`
Draws a ring marker for the current checkpoint location with optional finish markers.

## Events
No engine `Event.*` subscriptions of its own — `MrxTaskRace` drives everything through child-task callbacks
(`fOnComplete`/`fOnCancel`/`fOnPartComplete` on the spawned Deliver/EnterVehicle objectives) and its inherited
[`MrxTask`](mrxtask) timer. `NetEventCallback` handles the custom-net `NETEVENT_MARKLOC`/`UNMARKLOC`/
`MARKFINISH` messages to sync checkpoint markers to clients — these are custom net events, not `Event.Create`
subscriptions.

## Notes for modders
- **Course setup:** `tCourseLocs` (list of location names), `sGateType` (`"ring"` or gate), `fWidth`
  (default `10`), and a `tTimerParams`/`nAddTime` timer are the main config levers. `vTgtInclude` picks who
  races (defaults to `Player.GetAnyCharacter()`).
- **Best-time recording** only happens if config `sRaceMission` is set (`MrxStatsManager.RecordBestTime`); the
  winner is resolved in the final checkpoint's `fOnPartComplete` and read via `GetWinner`.
- The timer is started manually (`bTaskManualStart = true` is forced) so the clock begins at `_StartRace`,
  not at activation — the "enter the car" phase isn't timed.