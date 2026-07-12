---
title: VzaCon001
parent: Story & Special Contracts
grand_parent: VZ Modules
nav_order: 1
inherits: MrxTaskContract
tags: [contract]
verified: false
---

# VzaCon001

## Overview
`VzaCon001` is the game's opening mission. `xQ!L.lua`'s `LoadSingleton` defaults a fresh game's
`sMissionId` to `"VzaCon001"` whenever no `_sSkipToMissionName` override is set, which is what makes this
the mission a brand-new save actually starts in. It runs the whole prologue arc: both co-op heroes board a
starting boat, approach a beach, fight through two gated checkpoints (with a satellite-airstrike targeting
minigame available throughout), pick up dropped weapons/vehicles via helicopter supply drops, and finish by
rescuing Carmona. `LoadAssets` branches on two persisted checkpoint flags (`VZ001CP01`, `VZ001CP02`) so a
save loaded mid-mission resumes at the right layer/state instead of replaying the boat intro every time.

## Inheritance
- Inherits from: [`MrxTaskContract`](../resident/mrxtaskcontract) (→
  [`MrxTaskMission`](../resident/mrxtaskmission) → [`MrxTask`](../resident/mrxtask)). Unlike most native
  engine globals (`Object`, `Event`, `Player`), `MrxTaskContract` does have decompiled source in this
  corpus and is already documented — see that page for the shared checkpoint/fanfare/reward machinery
  `Activated`/`Cleanup` here build on.
- Imports: [`MrxGuiManager`](../resident/mrxguimanager), `MrxSubtitle`,
  [`MrxVoSequence`](../resident/mrxvosequence), `MrxClusterBomb`,
  [`MrxSupportData`](../resident/mrxsupportdata) (imported twice — lines 6 and 14 of the file, a harmless
  duplicate `import()`), [`MrxFactionManager`](../resident/mrxfactionmanager), `MrxState`,
  [`MrxSupport`](../resident/mrxsupport), [`MrxTutorialManager`](../resident/mrxtutorialmanager),
  [`MrxAchievements`](../resident/mrxachievements), `MrxGuiSatellite`,
  [`MrxCopterDrop`](../resident/mrxcopterdrop)

  `MrxGuiManager`, `MrxSubtitle`, `MrxClusterBomb`, `MrxState`, and `MrxGuiSatellite` are imported but never
  referenced anywhere else in the file (confirmed by direct search) — most likely leftovers from an earlier
  draft. Notably, the satellite-targeting minigame this file implements (the `AirstrikeMinigame*` functions
  below) never touches the imported `MrxGuiSatellite` at all; its real UI hook is
  `Hud.Satellite:SetTutorialText(...)` plus raw `Event.ScriptEvent` names like
  `"Satellite Targetting Start"`.

## Instance pattern
Native task-framework subclass (`self`-based), following the base [`MrxTask`](../resident/mrxtask)
pipeline `Activate -> LoadAssets -> AssetsLoaded -> Activated`. State lives partly on `self` (via
`_SetFlag`/`_GetFlag`, `_CreateEvent`) and partly as bare module-level globals shared across callbacks:
`_tPlayers` (boat-boarding tracker), `iInsideMinigame`, `iGate`, `tSquad`, `uGate`, and a scattering of `o*`
globals (`oGetToBeach`, `oWaitForWeapon`, `oBeachEncounter`, `oDestroyGate`, `oKillVillageGuards`,
`oWaitForCar`, `oGetToThirdWaypoint`, `oGetToFourthWaypoint`, `oRescueCarmona`, etc.) that each hold a
reference to whichever child objective task is currently active — mostly write-once by the function that
creates them, read only by that same objective's own completion/cancel callback.

## Functions

**Setup & lifecycle**

### `LoadAssets(self, tSaveData)`
Overrides the framework step between `Activate` and `AssetsLoaded`. Branches on `_GetFlag("VZ001CP02")` /
`_GetFlag("VZ001CP01")`: a fresh game adds all pristine/checkpoint layers and calls `SetStartupWeapons()`
before `StandardSetup`; a save at either checkpoint removes the layers for earlier stages instead and skips
straight to `AssetsLoaded`. Uses `MrxLayerManager.Remove(tLayersToRemove, MrxLayerManager.Add, {...})` —
removal's completion callback is what triggers the add.

### `StandardSetup(self)`
Fresh-game-only path (reached only when neither checkpoint flag is set). Waits for the starting boat
(`VzaCon001_StartingBoat`) to wake, then (local `_PutPlayersInBoat`) fills every player's primary weapon's
reserve ammo, stands them up, and seats player 1 as driver / player 2 as passenger, registering an
`Event.ObjectInSeat` "entered" watch per player wired to `EnsureHeroesInBoat`. Also calls
`MrxStatsManager.DeleteVehicleTimer()`/`AddVehicleTimer()` on the server — without its own
`import("MrxStatsManager")` anywhere in this file, presumably relying on it already being loaded globally
by whatever else imports it.

### `EnsureHeroesInBoat(self, uOccupant)`
Per-player callback from the seat-entry watch above. Marks `_tPlayers[uOccupant] = true`; once every
tracked player has entered, stops camera blending for all players and calls `self:AssetsLoaded()` (letting
the framework continue on to `Activated`).

### `Activated(self)`
Calls `MrxTaskContract.Activated(self)` (super call) first. Disables faction attitude reporting, wires up a
handful of standing region/script-event triggers for the whole mission (tutorial-hide on boat exit/death,
music stop near the heli-kill region, Carmona weapon drop, broken-bridge/handbrake/grenade/tank-switch
hints, both satellite-minigame script events), then branches on checkpoint flags to resume at
`DeliverTank`, `GetToFirstWaypoint`, or (fresh start) `BoatApproach` + `SetupAirstrikeEvent`. Ends by
forcing night atmosphere on `rgn_atmo_carmonaislandrain` and syncing `NETEVENT_CLIENTSETUP` to clients.

### `OnPlayerJoined(self, iPlayerId, uPlayerGuid, uCharGuid)`
Re-sends `NETEVENT_CLIENTSETUP` so a player joining a co-op session mid-mission gets the same
startup-weapons/atmosphere setup the host received in `Activated`.

### `NetEventCallback(nEventId, tArgs)`
Handles `NETEVENT_CLIENTSETUP` on clients: waits for the local character to wake, then calls
`SetStartupWeapons()` and re-applies the night-rain atmosphere setting.

### `SetStartupWeapons()` / `FillWeapon(uGuid)`
Module-level (no `self`) helpers. Gives the local character a Carbine/Grenade/C4 loadout, then waits for
the primary weapon to wake before topping off its reserve ammo.

**Beach approach & first gate**

### `BoatApproach(self)`
Starts a 0.1s timer into `GetToBeach` — effectively an immediate next-frame call.

### `GetToBeach(self)`
Switches off dynamic music for a scripted cue, creates a `MrxTaskObjectiveDeliver` child
([`MrxTaskObjectiveDeliver`](../resident/mrxtaskobjectivedeliver)) sending the player to the beach, with an
intro VO sequence.

### `BoatCheck(self)`
If the starting boat is still player-controlled, begins a custom tutorial (enter/exit prompt) and waits for
the player to exit before `DropInWeapon`; otherwise calls `DropInWeapon` immediately.

### `DropInWeapon(self)`
Hides the tutorial message, plays VO, and calls `MrxCopterDrop.Create` to spawn a supply-drop helicopter
carrying a weapon crate, then waits 3s before `WaitForWeapon`.

### `WaitForWeapon(self, uCargo)` / `FailSafe(self)`
Creates a `MrxTaskObjectiveDeliver` child waiting for the dropped weapon crate to reach the drop point
(`tOnComplete` → `BeachGuardsCheck`, `tOnCancel` → `FailSafe`), and sets up the melee-bash tutorial trigger
around it. `FailSafe` plays a VO and force-completes the objective if it gets cancelled instead.

### `MeleeBashTuteSetup(self, uCargo)` / `MeleeBashTute(self)` / `RemoveBashTute(self)`
Proximity-triggers a "melee to open the crate" tutorial message near the weapon drop, and removes it (and
force-completes `oWaitForWeapon`) once the crate object dies.

### `BeachGuardsCheck(self)` / `KillBeachGuards(self)`
Checks whether any of the 4 named beach-guard soldiers are still alive; if so, creates a
`MrxTaskObjectiveDestroy` ([`MrxTaskObjectiveDestroy`](../resident/mrxtaskobjectivedestroy)) child to clear
them (with a VO intro and a proximity-triggered shoot/reload tutorial via `SetupShowShootTutorial`), else
skips straight to `DestroyGateSetup`.

### `SetupShowShootTutorial(self)` / `ShowShootTutorial(self)`
Proximity trigger near the first gate that shows shoot/reload tutorial text, followed 10s/12s later by a
zoom/switch-weapons tutorial.

### `DestroyGateSetup(self)` / `DestroyGateSetupVO(self)` / `DestroyGate(self)`
Destroys the first gate (`vza001_gate`) via a `MrxTaskObjectiveDestroy` child if it's still alive (else
skips straight to `PostGate`), alongside VO and the grenade-hint teardown.

### `GatedPDAObjectiveSetup(self)` / `GatedPDAObjective(self)` / `DestroyGateSetupTwo(self)`
A PDA-open tutorial gate: shows a "open your PDA" hint, waits for the real `"PDA Open"`/`"PDA Close"`
script events, then plays follow-up VO and proceeds to `DestroyGateSetupTwo` (more VO, the support-menu
tutorial, freebies, and a confirmation flyby, all timer-delayed).

### `ShowGateTutorial(self)`
Shows the support-menu tutorial message. Called from several of the gate-related functions above and from
`DestroySecondGate`.

### `PostGate(self)`
Runs after the first gate falls: grants `ACHIEVEMENT_SCHOOLS_OUT`, calls `FirstCheckpoint`, swaps special
music, and after further delays plays `CarmonaInHillsVO` and proceeds to `GetToFirstWaypoint`.

### `CarmonaInHillsVO(self)` / `SprintTutorial(self)`
One-line VO and sprint-tutorial helpers called from `PostGate`/`GetToFirstWaypoint` respectively.

### `FirstGateDestroyedVO(self)`
Defined but **never called anywhere in this file** (confirmed by direct search) — dead code, likely a VO
step from an earlier version of the first-gate sequence that `PostGate`/`CarmonaInHillsVO` replaced.

**Village, waypoints & vehicle drops**

### `GetToFirstWaypoint(self)`
Removes the `VzaCon01_SatBomb` freebie, starts the sprint tutorial and re-arms the airstrike script event,
then creates a `MrxTaskObjectiveDeliver` child to the first waypoint.

### `KillVillageGuards_Failsafe(self)` / `KillVillageGuards(self)` / `SetupDeliverCar(self)`
Checks whether any of the 3 named village guards are alive; if so, fights them via a
`MrxTaskObjectiveDestroy` child before `SetupDeliverCar`, else skips straight to `DeliverCar` with a
shorter VO.

### `DeliverCar(self)` / `WaitForCar(self, uCargo)`
Drops an `M151 Softtop (VZ)` via helicopter and creates a `MrxTaskObjectiveDeliver` child waiting for it to
land — both completing and cancelling route to `GetToSecondWaypoint`.

### `GetToSecondWaypoint(self)` / `DestroySecondGate(self)`
Delivers the player to the second waypoint, then destroys the second gate (`vza001_gate2`) the same way as
the first (or skips to `DeliverTank` if it's already down), setting `iGate = 2` so
`AirstrikeMinigame_GateCheck` (below) knows which gate to re-check.

### `DeliverTank(self)` / `WaitForTank(self, uCargo)`
Drops an `AMX30` tank via helicopter and waits for it to reach the drop point before
`PauseBeforeThirdWaypoint`.

### `PauseBeforeThirdWaypoint(self)` / `GetToThirdWaypoint(self)` / `GetToFourthWaypoint(self)`
A short delay, then two more `MrxTaskObjectiveDeliver` waypoint hops; `GetToThirdWaypoint` also calls
`SecondCheckpoint`.

### `RescueCarmona(self)`
Final objective: grants freebies again and delivers the player to the hotel/win region, completing the
mission (`self.Complete`) on arrival.

**Hints & one-off encounters**

### `GrenadeHint(self)` / `RemoveGrenadeHint(self)` / `TankSwitch(self)` / `HandbrakeTutorial(self)`
Region-triggered contextual tutorial messages (explosives, tank-switch, handbrake — the last two check
`MrxPlayer.IsInVehicle(...)` and pick a controller- or PC-specific message via `Gui.ControllerInUse`).

### `BrokenBridgeEncounter(self)` / `BrokenBridgeEncounterComplete(self)`
Sends an AI-controlled vehicle (`brokenbridge_mook`) down a one-way path on region entry.
`BrokenBridgeEncounterComplete` has an **empty body and is never called** (confirmed by direct search) —
dead code.

### `DropCarmonaWeapons(self)`
Once `Carmona_VzaCon001` wakes, strips and removes all of his weapons.

### `TreeAttack(self)` / `BeachBypass(self)` / `SetMissionMusic(self)`
All three are defined but **never called anywhere in this file** (confirmed by direct search) — most
likely either cut content or hooks meant to be wired from a region/trigger volume's own embedded script
rather than from `vzacon001.lua` directly.

**Airstrike / satellite-targeting minigame**

### `SetupAirstrikeEvent(self)`
Arms the `"Satellite Targetting Start"` script event to call `AirstrikeMinigame`. Re-armed after every
minigame run (success, cancel, or gate-recheck) so it can be triggered repeatedly.

### `AirstrikeMinigame(self)`
Sets `iInsideMinigame = 1`, shows the camera/confirm-target tutorial, and arms the
`"Satellite Minigame Start"` / `"Satellite Targetting Success"` / `"Satellite Targetting Cancelled"` script
events for this run.

### `AirstrikeMinigame_Start(self)` / `AirstrikeMinigame_SuccessVO(self)` / `AirstrikeMinigame_InsideVO(self)`
Tutorial text and VO lines for the minigame's start/success/in-progress states (the VO variants are wired
directly in `Activated`, not through `AirstrikeMinigame` itself).

### `AirstrikeMinigame_Success(self)`
Clears `iInsideMinigame`, hides the tutorial, and schedules `AirstrikeMinigame_GateCheck` 10s later.

### `AirstrikeMinigame_GateCheck(self)`
Picks the currently-relevant gate from `iGate` (1 or 2) and, if it's still alive, plays a random nag VO
line, calls `AddFreebies`, re-shows the gate tutorial, and re-arms the airstrike script event for another
attempt.

### `AirstrikeMinigame_Cancel(self)`
Re-arms the airstrike script event, clears `iInsideMinigame`, clears the satellite HUD tutorial text, and
re-shows the gate tutorial after 5s.

### `AddFreebies(self)`
Grants the `VzaCon01_SatBomb` freebie. **Its `self` parameter is never read** — three of its four call
sites (`self:_CreateEvent(..., AddFreebies, {"self"})` twice, plus a direct `AddFreebies("self")`) pass the
literal 4-character **string** `"self"` rather than an actual object reference; only the call inside
`AirstrikeMinigame_GateCheck` passes a real `self`. Harmless here since the parameter is unused either way,
but a clear copy-paste artifact rather than intentional.

### `VO_GateNag(Self)`
Defined but **never called anywhere in this file** (confirmed by direct search). Its local `tVO_GateNag`
table is scoped to this function only — it is a *different* variable from the bare `tVO_GateNag`
referenced by `MrxSupport.PlayRandomVOCue(tVO_GateNag)` inside `AirstrikeMinigame_GateCheck`, which reads
an unset global of the same name. As written, that call in `AirstrikeMinigame_GateCheck` passes `nil`
rather than the gate-nag VO lines — the two functions look like they're supposed to share this table but
don't. Also note the parameter is capitalized `Self` here, unlike everywhere else in the file.

**Checkpoints & cleanup**

### `FirstCheckpoint(self)` / `SecondCheckpoint(self)`
One-shot (guarded by `_GetFlag`) checkpoint setters — set `VZ001CP01`/`VZ001CP02` and call `_Checkpoint`
with the matching spawn-point pair.

### `StopTheMusic(self)`
Stops special music on entering `region_killvzaheli`.

### `Cleanup(self)`
Removes the mission's own layers and adds `vz_state_vzacon001_ruined` in their place, removes both
freebies, calls `MrxTaskContract.Cleanup(self)`, re-enables faction reporting, and hides any lingering
tutorial message.

## Events
- `Event.ObjectHibernation` — waits for the starting boat, `Carmona_VzaCon001`, and various dropped
  weapons to wake before acting on them.
- `Event.ObjectInSeat` — per-player boat-boarding watch (`StandardSetup`), boat-exit tutorial teardown
  (`Activated`), and `BoatCheck`'s wait for the player to leave the boat.
- `Event.ObjectDeath` — starting-boat destruction (hides tutorial), weapon-crate death (`RemoveBashTute`).
- `Event.Boundary` — the large family of region triggers (beach, broken bridge, handbrake, grenade, tank
  switch, kill-heli-music region) that drive most of the mission's pacing.
- `Event.ObjectProximity` — melee-bash tutorial, shoot tutorial, first-gate proximity trigger.
- `Event.ScriptEvent` — `"Satellite Targetting Start"`/`"Satellite Minigame Start"`/
  `"Satellite Targetting Success"`/`"Satellite Targetting Cancelled"` drive the airstrike minigame;
  `"PDA Open"`/`"PDA Close"` drive `GatedPDAObjectiveSetup`.
- `Event.TimerRelative` — used throughout for delayed VO/tutorial/objective chaining.

## Notes for modders
- This is the native `MrxTaskContract`/`WifMissionData` mission system, not
  [Contract Framework](../contract-framework/) — see
  [Contract.Register & Lifecycle](../contract-framework/register-and-lifecycle) for why mods use a
  different, ephemeral system instead of hooking into this one directly.
- **This is what a new game actually loads.** If you're testing a mod that patches mission flow or
  `xQ!L.lua`'s boot sequence, `VzaCon001` is the first mission script that runs unless the game is set to
  skip to a different one.
- The checkpoint-flag branch in `LoadAssets`/`Activated` (`VZ001CP01`/`VZ001CP02`) is the pattern to study
  if you need a long mission to resume correctly from a save rather than always replaying from the start.
- Several functions in this file are confirmed-dead (never called): `FirstGateDestroyedVO`,
  `BrokenBridgeEncounterComplete`, `TreeAttack`, `BeachBypass`, `SetMissionMusic`, `VO_GateNag`. Don't
  assume every defined function here is reachable in play.
