---
title: MecCon001
parent: Story & Special Contracts
grand_parent: VZ Modules
nav_order: 3
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# MecCon001

## Overview
`MecCon001` is the recruitment mission for the Mechanic specialist: a monster-truck race against the
clock (with an AI motorcycle opponent in co-op), delivering the truck back to the mechanic's garage at the
end. It shares layers and vehicle-delivery/garage plumbing with [`MecJob`](mecjob) (both load
`vz_state_gua_upperclass_pristine`/`Vz_State_MecJob`), but is its own contract rather than a `MecJob`
subclass. The race is retried on failure via a persisted attempt counter (`giAttempts`) that raises the
goal time on later attempts, and the whole mission is laced with an in-vehicle jump tutorial that's synced
to both co-op players over custom net events.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (→
  [`MrxTaskMission`](../resident/mrxtaskmission) → [`MrxTask`](../resident/mrxtask))
- Imports: [`MrxUtil`](../resident/mrxutil), [`MrxVoSequence`](../resident/mrxvosequence), `MrxApcDrop`,
  `DangerousBuilding`, `MrxTimer`, [`MrxMusic`](../resident/mrxmusic),
  [`MrxTutorialManager`](../resident/mrxtutorialmanager), `MrxGuiInterface`,
  [`MrxPlayState`](../resident/mrxplaystate)

  `MrxApcDrop`, `DangerousBuilding`, `MrxTimer`, and `MrxGuiInterface` are imported but never referenced
  anywhere else in the file (confirmed by direct search) — of this group, only `MrxPlayState`
  (`.GetCurrentMission()`, used once in `NetEventCallback`) is actually called.

## Instance pattern
Native task-framework subclass (`self`-based). Per-`self` fields include `self.uCar`/`self.uBike` (the
race vehicles), `self.inRegion`/`self.outRegion`/`self.garage` (mechanic-HQ geometry), `self.curAiGoal`,
and `self.tOpponents`/`self.bOpponentFinished` (co-op AI opponent tracking). Module-level globals:
`giAttempts` (persisted race-attempt counter, read/written via `_GetFlag("race_cp")`/`_SetFlag`) and the 5
`NETEVENT_*` constants used for co-op sync. `geJumpTutorial` is a bare (undeclared-local) global set by the
client-side tutorial handler in `NetEventCallback`.

## Functions

**Setup**

### `LoadAssets(self, tSaveData)`
Adds 3 layers then calls `_SetupVehicles1`.

### `_SetupVehicles1(self)`
If `_GetFlag("race_cp")` is set (resuming a retried race), respawns the truck/bike at the respawn points
and waits for the truck to wake before `_SetupVehicles2`; otherwise (fresh start) spawns them at the
mission-start points and goes straight to `AssetsLoaded`. Also calls `Net.DoneReloadingLayers()` if
present.

### `_SetupVehicles2(self)`
Only reached on a resumed race. Seats the primary/secondary players in the truck/bike (which vehicle each
player gets depends on the persisted `race_P2` flag — the driver on retry keeps their prior vehicle), and
waits for a driver to be in the truck's seat before calling `AssetsLoaded`.

### `_MyOnPlayerLeft(self, tData)`
Server-only rejoin handler: if the secondary player (previously the truck driver, per `race_P2`) leaves
mid-retry-setup, reassigns the primary player to the truck driver seat instead.

### `Activated(self)`
Calls `MrxTaskContract.Activated(self)` (super call), resolves the garage/in/out regions, watches the
truck and garage for death (→ `MonsterTruckDestroyed`/`GarageDestroyed`), and branches: a resumed race
(`race_cp` set) makes both vehicles vincible again and calls `ObjGoToDestination` directly; a fresh start
plays the mission intro VO (with an extra co-op-only line) ending in `ObjGetInVehicle`. Also plays special
mission music and kills a specific prop gun object (`0xd047d`) once it wakes.

**Tutorial (jump-over-water) sequence**

### `CreateTutorialTrigger(self)` / `StartTutorial(self)` / `SetupJumpTutorial(self)`
A proximity trigger near `mc001.loc.tutorialtrigger` shows the jump-tutorial VO and tray;
`SetupJumpTutorial` picks the in-car or out-of-car tutorial variant depending on whether the truck's driver
is player-controlled.

### `JumpTutorial_OutCar(self, uChar, uVehicle)` / `JumpTutorial_InCar(self, uDriver, uVehicle)`
Toggle pair driven by `Event.ObjectInSeat` enter/exit on the truck: `InCar` arms the right-trigger jump
button watch and (if the tray was already shown) redisplays it; `OutCar` tears down the button watch and
hides the tutorial/tray (including telling clients to hide it, via `NETEVENT_HIDETUT`).

### `SetupTutorialTray(self)`
Shows the button-tray tutorial message locally if the primary player is driving, otherwise tells the
secondary client to show it via `NETEVENT_SHOWTUT`.

### `TutorialComplete(self)` / `TutorialCancel(self)`
`TutorialComplete` stops the tutorial, stops any in-flight VO, and plays a follow-up VO sequence.
`TutorialCancel` tears down all three tutorial-related event handles
(`eJumpTutorial`/`eJumpTutorialProx`/`eJumpTutorialSeat`) and hides the message/tray.

**The race**

### `ObjGetInVehicle(self)` / `ObjDriveAroundBlock(self)`
If the truck already has a player driver, skips straight to `ObjDriveAroundBlock`; otherwise creates a
`MrxTaskObjectiveEnterVehicle` ([`MrxTaskObjectiveEnterVehicle`](../resident/mrxtaskobjectiveentervehicle))
child first. `ObjDriveAroundBlock` plays a VO sequence ending in `SetupJumpTutorial`, and creates the first
`MrxTaskRace` child (a short warm-up loop) that leads to `ObjGoToDestination` on completion.

### `ObjGoToDestination(self)`
Creates a `MrxTaskObjectiveDeliver` ([`MrxTaskObjectiveDeliver`](../resident/mrxtaskobjectivedeliver))
child sending the truck to the mine entrance, leading to `AtRaceStart`.

### `AtRaceStart(self)`
Cancels any pending tutorial, persists the current attempt count and (if the secondary player is driving)
the `race_P2` flag, sets a checkpoint, plays VO, and starts the real race (`StartRace`).

### `StartRace(self)`
The main event: creates the full-course `MrxTaskRace` ([`MrxTaskRace`](../resident/mrxtaskrace)) child
(goal time 45/60/90s depending on `giAttempts`), arms 3 pipe traps, a bridge trap, and 5 proximity VO
warnings along the course, and opens the mine gate. On completion, plays VO and proceeds to
`_CreateDeliverObjective`; on cancel, re-cancels the whole contract if the truck survived.

### `SpawnOpponent(self, sStartName, fHaste)` / `StartOpponent(self, uBike, fHaste)` / `OpponentAdvancePath(self, uDriver, tPaths, fHaste, iPathIdx)`
Co-op-only AI opponent: spawns an AI-only motorcycle at a start point, then advances it through a fixed
5-point path list one leg at a time (each leg's completion callback advances to the next), setting
`self.bOpponentFinished` once the path list is exhausted.

### `SetupPipeTrap(self, sTriggerPoint, tPipes)` / `TriggerPipeTrap(self, tPipes)` / `SpawnExplosionPipeTrap(self, tPipes)`
Proximity-triggered hazard: kills the named pipe object(s), then (0.1s later) spawns an explosion at each
paired point and syncs it to clients via `NETEVENT_SPAWNEXPLOSION`.

### `SetupBridgeTrap(self)` / `TriggerBridgeTrap(self)`
Proximity trigger near the bridge bomb that plays a single warning VO line (no explosion logic of its own
here beyond the VO).

### `SetupProxVo(self, sPoint, fRange, tVo)`
Generic helper: arms a proximity trigger that plays an arbitrary VO sequence. Used for the 5 course
warnings in `StartRace`.

**Delivery & completion**

### `_CreateDeliverObjective(self)`
Creates the final `MrxTaskObjectiveDeliver` child parking the truck inside the garage, leading to
`_ExitGarage` on completion.

### `_PlayerOutside(self)` / `_PlayerInside(self, uPCharacter)` / `_ExitGarage(self)` / `_VehicleDelivered(self)`
A gate-choreography chain (closed while player is outside, opened once they enter, closed again once they
leave with the truck inside) ending in `_VehicleDelivered`, which — if the truck is actually inside the
garage — closes the gate and waits for `"gateFullyClosed"`/`"gateStuck"` to remove the truck and complete
the mission; otherwise loops back to `_CreateDeliverObjective`.

### `MonsterTruckDestroyed(self)` / `GarageDestroyed(self)`
Fail-state VO + `self.Cancel` if the truck or the garage is destroyed mid-mission.

### `MissionComplete(self)`
Defined but **never called anywhere in this file** (confirmed by direct search) — dead code; the real
completion path is the `CompleteMission` local function inside `_VehicleDelivered`, which calls
`self:Complete()` directly instead of through this wrapper.

### `Complete2(self)`
Calls `MrxTaskContract.Complete2(self)` (super call), then fires a `Hud.EventFanfare` stockpile-reward
banner (grapple weapon).

### `Cleanup(self)`
Hides the tutorial (locally and via `NETEVENT_HIDETUT`), removes the current AI goal if any, force-exits
any local player still riding the truck/bike and fades them out, closes the mine gate, marks
`Vz_State_MecJob`/`VZ_State_MecCon001` for removal, and calls `MrxTaskContract.Cleanup(self)`.

**Co-op networking**

### `NetClientEnterVehicle(uVeh)`
Client-side helper that seats the secondary player in a given vehicle, retrying every 0.2s until the
client is tether-ready and not already in a different vehicle (in which case it exits that one first).

### `NetEventCallback(eventId, tArgs)`
Dispatches all 5 `NETEVENT_*` IDs: enter-vehicle, spawn-explosion (pipe traps), show/hide the jump
tutorial on the secondary client, and relaying client-side tutorial completion back to the active mission
instance (via `MrxPlayState.GetCurrentMission():TutorialComplete()`).

### `ClientTutorialComplete()`
Client-side: clears the local jump-tutorial button watch, hides the message, and tells the server via
`NETEVENT_CLIENTTUTCOMPLETE`.

## Events
- `Event.ObjectHibernation` — vehicle-respawn wake watches, and the one-off prop-gun kill in `Activated`.
- `Event.ObjectInSeat` — driver-seat watches throughout (`_SetupVehicles2`, jump tutorial toggle).
- `Event.ObjectDeath` — truck/garage destruction (fail states).
- `Event.ObjectProximity` — the jump tutorial trigger, pipe/bridge traps, and course VO warnings.
- `Event.Button` — the right-trigger jump-tutorial watch (`JumpTutorial_InCar`).
- `Event.ObjectPhysicsEvent` — `"gateFullyClosed"`/`"gateStuck"` complete the final delivery.
- `Event.ScriptEvent` — `"mpPlayerLeft"`, filtered to non-local players, drives `_MyOnPlayerLeft`.
- `Event.TimerRelative` — pipe-trap explosion delay, and `NetClientEnterVehicle`'s retry loop.

## Notes for modders
- This is the native `MrxTaskContract`/`WifMissionData` mission system, not
  [Contract Framework](../contract-framework/) — see
  [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
  different, ephemeral system instead of hooking into this one directly.
- `giAttempts`/`race_cp` is the retry/difficulty-ramp pattern worth studying if you want a timed objective
  that gets easier or harder based on prior failures.
- The tutorial button-tray logic is fully duplicated for host/client via the `NETEVENT_SHOWTUT`/
  `NETEVENT_HIDETUT`/`NETEVENT_CLIENTTUTCOMPLETE` trio — a reasonable template for any UI hint that must
  show correctly for a non-host co-op player.
- `MissionComplete` is dead code — don't use it as a reference for how completion actually happens; see
  `_VehicleDelivered`'s local `CompleteMission` instead.
