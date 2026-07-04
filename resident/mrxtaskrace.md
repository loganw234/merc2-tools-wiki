---
title: MrxTaskRace
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: MrxTask
tags: [task, race]
verified: true
verified_note: corrects the Instance pattern (class-factory via the MrxTask family, not per-uGuid) -- see [MrxTask](mrxtask) for the general mechanism.
---

# MrxTaskRace

*Module: mrxtaskrace.lua*

## Overview
The `MrxTaskRace` module is responsible for managing checkpoint-based racing tasks in the game. It handles the creation and management of checkpoints, blips, and tripwires, as well as recording the best race time using `MrxStatsManager`.

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
Handles status changes of target vehicles or characters. Removes completed targets from the list and calls a callback if specified.

### `_DrawTripWire(uGuid, fWidth, r, g, b, bFinish)`
Draws a tripwire for the current checkpoint location with optional finish markers.

### `_DrawRing(uGuid, fWidth, r, g, b, bFinish)`
Draws a ring marker for the current checkpoint location with optional finish markers.

## Events
- Listens for `NETEVENT_MARKLOC`, `NETEVENT_UNMARKLOC`, and `NETEVENT_MARKFINISH` to update blips and markers.
- Listens for custom events related to task status changes.

## Notes for modders
- Ensure that the race configuration includes valid checkpoint locations and target vehicles/characters.
- Customize the width of checkpoints and whether tripwires are used by setting fields like `fWidth` and `bUseTripWires`.
- Be aware that network synchronization may affect multiplayer behavior, especially when marking/unmarking locations.