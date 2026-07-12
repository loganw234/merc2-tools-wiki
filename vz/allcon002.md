---
title: AllCon002
parent: Allied Nation Contracts & Jobs
grand_parent: VZ Modules
nav_order: 2
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# AllCon002

## Overview
A large Allied Nation story contract: the siege of Caracas's China-held MLRS/AA position. Three
sequential stages — destroy three MLRS launchers (`Obj1_A/B/C`) while they bombard a tracked landmark
called "Caracas" (health shown as a HUD bar), destroy three river boats providing anti-air cover once the
launchers are down, then hunt down three fleeing "Turncoat" officers to verify the position is secure. The
contract layers on a simulated artillery barrage aimed at the player while inside a strike region, ambient
randomized aircraft flybys, and multiplayer-synced smoke/particle effects. Save flags (`BoatsKilled`,
`MLRSkilled`) let the contract resume mid-siege after a reload instead of restarting from stage one.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (a real `resident/` module — see that page for the base class's own behavior)
- Imports: `DangerousBuilding`, `MrxSubtitle`, `MrxVoSequence`, `MrxSupportData`, `MrxFactionManager`

Four module-level constants (`NETEVENT_STARTEMITTERS = 0`, `NETEVENT_STARTPLUMES = 1`,
`NETEVENT_CLEANSMOKE = 2`, `NETEVENT_AIRSTRUCK = 3`) are custom net-event IDs used with
`Net.SendCustomEvent`/`NetEventCallback` to mirror particle effects and fake artillery hits to remote
clients in co-op.

## Instance pattern
A native `MrxTaskContract` subclass, `self`-based with an explicit "super" call pattern. Contract state
lives in module-level globals rather than on `self`: `nCaracasLife` (the tracked HP value), `nAAalive`,
`bBombard` (0/1/2 escalation state), `nStrikeFrequency`, `nDamMod`, `uAirstrikeOn`, `_tSmokeParticleObjects`
(spawned smoke-plume tracking, for cleanup), and several standing event handles
(`eAirstrikes`/`eAirstrikes2`/`eDamageCarac`/`eBoatDamage`/`eDisplay1-3`).

## Functions
### `LoadAssets(self, tSaveData)`
Adds/removes the Caracas-siege layer set, branching on the `BoatsKilled`/`MLRSkilled` save flags so a
resumed contract loads the correct mid-siege layer state.

### `NetEventCallback(eventId, tArgs)`
Remote-client dispatcher for the four `NETEVENT_*` IDs, routing to `Pop`, `Plumes`, `SmokeClean`, or
`AirStriked`.

### `Activated(self)`
Resets contract state, starts `Flybys`, schedules `SetupANTalker` after 15s, and resumes at the correct
stage (`Obj4_Verify`, `Obj3_BoatAA`, or `DestroyMLRS`) based on the save flags.

### `DestroyMLRS(self)`
Stage 1 setup: creates the `MrxTaskObjectiveDestroy` child for the three MLRS launchers, staggers
`Obj1_Bombard` starts, watches each launcher for sinking, and arms the boundary that turns the simulated
artillery barrage on.

### `LauncherSunk(self, uSinkingVeh)`
Kills a sinking launcher five seconds after it starts sinking.

### `Obj3_BoatAA(self)`
Stage 2 setup: escalates the bombardment rate/damage (`bBombard = 2`, `nDamMod = 1`), starts a 30-second
persistent Caracas-damage timer, triggers the bridge/river-assault setup, and creates the
`MrxTaskObjectiveDestroy` child for the three river boats.

### `BoatDestroyed(self)`
Plays a VO line when two, then one, boats remain.

### `Obj4_Verify(self)`
Stage 3 setup: idles the "Turncoat" AI, arms a proximity trigger that starts it fleeing, clears the
HUD health-bar slots, and creates the `MrxTaskObjectiveDestroy` child for the three Turncoat officers.

### `OfficerDown(self)`
Plays a VO line when two, then one, officers remain.

### `RunAway(self, nSegment)`
Sends the Turncoat AI down the next `Pa_RunMan_<n>` path segment.

### `RunAwayCheck(self, nSegment, Guid, State)`
`Ai.Goal` PathMove callback: retries `RunAway` on failure, otherwise arms proximity events (spotted /
too-close) for the next flee segment.

### `SpottedHim(self, nRunAway)`
Re-triggers `RunAway` if the player can currently see the Turncoat, otherwise polls again in 2s.

### `AADestroyed(self)`
Plays a VO line when two, then one, MLRS launchers remain.

### `AlliedSpeaks(self, tAlliedTalk)`
Cycles through three canned Allied-soldier VO lines, resetting and re-polling every 20s.

### `SetupANTalker(self)`
Finds nearby Allied soldiers via `Pg.FastCollectHumans` to speak an `AlliedSpeaks` line, retrying every
15s if none are found.

### `AirstrikeThePlayer(self)`
Repeats `MPShelling` on an `nStrikeFrequency`-second timer while `uAirstrikeOn` is set.

### `AirstrikesOff(self)`
Clears `uAirstrikeOn` and re-arms the boundary-enter trigger for the strike region.

### `AirstrikesOn(self)`
Sets `uAirstrikeOn`, plays a one-time warning VO, arms the boundary-exit trigger, and starts
`AirstrikeThePlayer`.

### `Obj1_Bombard(self, sLauncher)`
Orders a launcher's driver to lock the turret and attack a fixed fire target; while bombardment is
active, schedules `ShellCaracas` and reschedules itself every 26s.

### `Obj1_StopBombard(self, sLauncher)`
Returns a launcher's driver to Idle and reschedules `Obj1_Bombard`.

### `SetupWreck(self)`
Arms hibernation triggers that kill five named bridge-segment pieces once each wakes, and delays
`BoatDelay` by 4s.

### `WreckBridge(self, uPiece)`
Kills a bridge-segment piece object.

### `BoatDelay(self)`
Arms hibernation triggers on the three river boats to start their attack run once each wakes.

### `StartRiverAttack(self, nBoat)`
Delays `PathMoveBoat` per boat (staggered by boat index times 4s) once a boat is awake and has a live,
non-player driver.

### `PathMoveBoat(self, nBoat, uBoatCapn)`
Sends a river boat down its attack path via `Ai.Goal`.

### `RiverAttack(self, nBoat, uBoatCapn, State)`
PathMove callback: retries `PathMoveBoat` on failure; on success, anchors the boat, orders an `Attack`
goal on a fire target, and arms a stop timer plus a recurring Caracas-damage timer.

### `RiverAttackStop(self, nBoat, uBoatCapn)`
Returns a boat to Idle and re-arms the next attack cycle 15s later.

### `ShellCaracas(self, sLauncher)`
Damages Caracas and pops nine staggered impact-particle effects along a launcher's pop-location chain via
`MPpop`.

### `MPpop(self, sPopLoc)`
Spawns (and net-syncs to remote clients) one airstrike-distance particle if its named pop-location object
is awake.

### `Pop(uPopX, uPopY, uPopZ, uPopper)`
The actual `Pg.Spawn("global_particle_airstrike_distance", ...)` — the remote-client half of `MPpop`'s
net sync (called directly by `NetEventCallback`), or the local half when called from `MPpop` itself.

### `DisplayCaracasHealth(self)`
Flashes HUD slot 1 red/white and writes a colored `[bar<N>]` health-bar string to HUD slot 2 from
`nCaracasLife` (green above 60, yellow above 25, red below).

### `DamageCaracas(self)`
Subtracts `nDamMod` HP, triggers smoke plumes and VO at specific HP thresholds (98/90/44/24/18), and at 3
HP or below sets a cancel message and force-cancels the contract 4.5s later.

### `MPplumes(nPlumeID)`
Spawns (and net-syncs) a smoke-plume particle at a named `Loc_Smoke_<n>` location if it's awake.

### `Plumes(uPlumeX, uPlumeY, uPlumeZ, nPlumeID)`
The actual smoke-plume spawn, tracked in `_tSmokeParticleObjects` for later cleanup.

### `AirStriked(uStrikeLoc, uSeeStrike, uEncounter)`
Computes a camera-relative "incoming shell" impact point scaled by the player's current speed, then
schedules `TriggerFallingMissile` for each of `nShells`.

### `MPShelling(uStrikeLoc, uSeeStrike, uEncounter)`
Calls `AirStriked` locally and mirrors it to remote clients via `NETEVENT_AIRSTRUCK`.

### `TriggerFallingMissile(tData, uPlayer)`
Spawns the actual falling ordnance via `Airstrike.SpawnOrdnance`.

### `Flybys(self)`
Picks a random ambient aircraft flyby from a hardcoded template table and spawns it, repeating every 15s.

### `SmokeClean(self)`
Removes every particle object tracked in `_tSmokeParticleObjects`.

### `Cleanup(self)`
Restores the pre-contract staging layers, cancels the outstanding HUD/health-bar timer events, mirrors a
smoke cleanup to remote clients, and calls the base `MrxTaskContract.Cleanup`.

## Events
- `Event.TimerRelative` — used pervasively for staggered starts, cooldowns, and repeating loops (bombard
  cycles, river-attack cycles, HUD flashes, flyby repeats, etc.).
- `Event.ObjectPhysicsEvent` — `"VehicleSinking"` on each of the three MLRS launchers fires `LauncherSunk`.
- `Event.ObjectProximity` — five `loc_Rockets_i` triggers (range 65) fire `MPShelling` for the simulated
  artillery; separate proximity events drive the Turncoat flee/spot logic.
- `Event.Boundary` — `Reg_AllCon002_Strikes` enter/exit toggles the simulated-artillery state
  (`AirstrikesOn`/`AirstrikesOff`).
- `Event.ObjectHibernation` — bridge-segment pieces and river boats waking trigger their respective
  setup chains.

## Notes for modders
This is the native `MrxTaskContract`/`WifMissionData` mission system, not [Contract
Framework](../contract-framework/) — see [Contract.Register &
Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a different, ephemeral system
instead of hooking into this one directly.

- **The `NETEVENT_*`/`Net.SendCustomEvent`/`NetEventCallback` pattern** here is a reusable recipe for
  mirroring ambient VFX (particles, fake artillery) to remote co-op clients from a host-authoritative
  contract — worth studying if you need synced cosmetic effects.
- **HUD health-bar trick**: `DisplayCaracasHealth` writes `[red]`/`[white]`/`[bar<N>]`-tagged strings
  directly into `Hud.ObjectiveTray` slots — a simple way to show a non-objective progress bar in the
  objective tray.
- **Apparent targeting bug in `AirStriked`**: inside the `if uStrikeLoc then` branch, the code declares a
  *new* `local tData = {}` to hold location-specific target coordinates, which shadows the outer `tData`
  instead of overwriting it — so that inner table is discarded when the block ends, and the
  location-specific coordinates never actually reach the `Event.Create(... TriggerFallingMissile ...)`
  call below. In practice this reads as if the simulated strike always falls back to the generic
  camera-relative aim point, even when a named `loc_Rockets_<encounter>_<i>` target exists. This is a
  scoping bug in the original logic, not a decompiler artifact — the shadowing would behave identically
  in the original source.
- **Tunables**: `bBombard` (0 = stopped, 1 = stage-1 rate, 2 = stage-2 rate) and `nDamMod` (per-tick
  Caracas damage) are the pacing levers; HP thresholds for smoke/VO beats are hardcoded (98/90/44/24/18/3).
