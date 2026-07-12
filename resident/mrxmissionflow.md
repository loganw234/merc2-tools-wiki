---
title: mrxmissionflow
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mission, flow]
verified: true
verified_note: 'deeper pass: rewrote the fabricated Events section (source has NO Event.MissionUnlock/
  MissionDestroy/PlayerAcceptMissions/etc. subscriptions — grep-confirmed zero Event.Create for those; the
  only real Event.* here are two mpPlayerJoin Event.CreatePersistent handles in SetGrapple/VehicleDisguise,
  plus the NETEVENT_* custom-event constants dispatched via NetEventCallback); documented the file-vs-module
  name (file mrxmissionflow.lua, called as WifMissionFlow); Instance pattern + UnlockMission/
  GetMissionStartLocations mechanism re-confirmed against source.'
---

# mrxmissionflow

*Module: mrxmissionflow.lua*

## Overview
The `mrxmissionflow` module is responsible for managing the mission flow in the game. It handles various aspects of missions, including enabling/disabling mission flow, tracking active missions, awarding keys, refreshing mission states, and updating the PDA with mission details. This module also manages network-related settings such as grapple and vehicle disguise functionality.

{: .note }
> **File name vs. module name:** the source file is `mrxmissionflow.lua`, but the module registers itself as
> `WifMissionFlow` — every call site in the corpus (and this page) uses `WifMissionFlow.X`, and the module's
> own recursive calls reference `WifMissionFlow.` too. Treat `mrxmissionflow` and `WifMissionFlow` as the
> same module.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
**Not per-`uGuid` — this is a singleton module, confirmed directly: there is no `Create` factory function
anywhere in this file**, unlike [`MrxTask`](mrxtask)/[`MrxStarter`](mrxstarter)'s class-factory pattern. All
state is module-level. In particular, **`_tActiveMissions` is keyed by mission name (a string), not a world
object GUID** — confirmed from source: `_tActiveMissions[sMissionName] = {oMission = oMission}`. This is
the table a custom mission's `fOnActivate` callback (config-driven, called with zero arguments — see
[`MrxTask`](mrxtask)) has to read to get its own live `MrxTask` instance, since it isn't passed one
directly: `WifMissionFlow._tActiveMissions.<sMissionName>.oMission`, confirmed populated synchronously by
`UnlockMission` (below), well before activation ever fires.

It tracks the following key fields:
- `_bEnable`: A boolean flag to enable or disable the mission flow.
- `_tMyFlowData`, `_tActiveMissions`, `_tCulledBindings`, `_sTrackedMissionName`, `_tMissionsToRepeat`, `_fRefreshCallback`, `_tRefreshCallbackArgs`: Tables and variables used to track various aspects of missions, such as active missions, culled bindings, tracked mission names, and deferred key awards.
- `_bCheckpointSaveMode`, `_bCurrentlyRefreshing`, `_bGrappleEnabled`, `_bVehicleDisguiseEnabled`, `_bResourceCountersEnabled`, `_bPersistentRetry`, `_bSkipToMissionReached`, `_nBlockingSequences`, `_oParent`, `_sLastCompletedContractName`, `_tDeferredKeyAwards`, `_tFlowData`, `_tRetryLocations`: Additional flags and tables used for managing mission flow, including checkpoint save mode, current refreshing state, network-related settings, and retry locations.

## Functions

### EnableFlow(bEnable)
Enables or disables the mission flow based on the boolean argument `bEnable`.

### Reset(bResetMore)
Resets various module-level states and tables. If `bResetMore` is true, it resets additional flags and variables related to mission flow.

### _TrackMission(sTrackedMissionName)
Tracks or untracks a mission by its name. It updates the `_sTrackedMissionName` variable and enables or disables tracking for the specified mission.

### CleanupAllActiveMissions()
Cleans up all active missions by iterating through `_tActiveMissions` and calling `Cleanup()` on each mission's parent container.

### SetFlowData(tFlowData)
Sets the flow data table `_tFlowData` with the provided `tFlowData`. It also logs the number of bindings in the new flow data.

### SetMissionParent(oParent)
Sets the parent object for missions using the provided `oParent`.

### SetPreContractSaveFunction(fPreContractSave)
Sets a pre-contract save function `_fPreContractSave` that will be called before saving contracts.

### UnlockMission(sMissionName, tSaveData, bBlockingSequence)
Unlocks a mission by its name. It performs various checks and configurations to set up the mission, including creating containers and missions, handling briefing, setting rewards, and managing mission states. It also handles special cases like skip mode and wager missions.

**Confirmed real entry point for a custom mission** — not something to build by hand. Looks up
`WifMissionData.tMissionData[sMissionName]`, builds an `MrxTask` container + mission instance (both via
`MrxTask:Create()`), auto-sets `tMissionConfig.tRewards = MrxRewardData.GetRewards(sMissionName)` (a custom
[`MrxRewardData._tRewards`](mrxrewarddata) entry is picked up automatically — confirmed live, no extra
work needed beyond adding the entry), wires wager win/loss settlement into the task's own
`tOnComplete`/`tOnCancel` config lists, and calls a local `_AddBriefingToStarter()` which does
`MrxStarterManager.RequestStarter(sStarter):AddBriefing(sMissionName, sMissionTitle)` —
[`MrxStarter.AddBriefing`](mrxstarter), confirmed to be exactly what makes a mission show up in a
starter's menu. Populates `_tActiveMissions[sMissionName] = {oMission = oMission}` synchronously before
returning, which is how a bare-`MrxTask`-based mission's `fOnActivate` callback (zero arguments, see
[`MrxTask`](mrxtask)) finds its own instance later.

A minimal custom mission calling this needs, at minimum, a `WifMissionData.tMissionData` entry with
`sFactionId`, `sStarter`, and `bContract = true` set by hand (`WifMissionData.Init()`'s automatic
faction/type/number parse of the mission ID already ran before a custom `OnLoad` entry exists, so this
never happens for a mission added after boot) — full worked example in the
[Custom Contract deep dive](../deep-dives/custom-contract).

### DestroyMission(sMissionName)
Destroys a mission by its name. It removes the mission from `_tActiveMissions`, updates the PDA map, sends network events if applicable, and cleans up briefings associated with the mission.

### GetMissionStartLocations(sMissionName)
Retrieves the start locations for a given mission. If the mission has specific start locations defined in `WifMissionData.tMissionData`, it returns those. Otherwise, it calls `GetBriefingStartLocations` to get the briefing start locations.

**Confirmed exact body**: `if tMissionConfig.tStartLocations then return tMissionConfig.tStartLocations end`
— read directly off the mission's own config, no fallback logic beyond that check. This is what
[`WifPmcInterior.Exit()`](../vz/wifpmcinterior) calls to figure out where to teleport the player after accepting a contract.
`tStartLocations` in every real mission is a list of *string* level-marker names (e.g.
`{"OilCon005_Startpoint_01", "OilCon005_Startpoint_02"}`), but
[`MrxUtil.TeleportHeroesToLocations`](mrxutil) (what actually consumes this list) also accepts a plain
`{x, y, z, yaw}` table per player — confirmed from its source, which explicitly branches on
`type(vLocation) == "table"` as a valid case alongside strings/userdata. A custom mission with no placed
level marker can set `tStartLocations = { {2776.8684, -13.8681, -873.5605} }` directly on its
`WifMissionData` entry to pin the exit teleport to a known location instead.

### GetBriefingStartLocations(sMissionName, bGetEntrance)
Retrieves the briefing start locations for a given mission. It first gets the case-sensitive mission ID and then checks if the mission has a starter defined in `WifStarterData`. If the starter is an HQ, it returns the entrance or start points from the HQ data. If the starter is a PMC starter, it returns predefined start points.

### DoesMissionHaveABriefing(sMissionName)
Checks if a given mission has a briefing by verifying if the mission's starter exists in `WifStarterData`.

### AwardKey(sKeyName, vValue)
Awards a key with a specified value. If the current flow is refreshing, it defers the award until the refresh is complete. Otherwise, it increments the value if it already exists or sets it to 1 if it doesn't. It then grants the reward using `MrxRewardData.GrantRewardKey`.

### RemoveKey(sKeyName)
Removes a key from `_tMyFlowData` if it exists.

### HasKey(sKeyName)
Checks if a key exists in `_tMyFlowData`.

### GetKeyValue(sKeyName)
Retrieves the value of a key from `_tMyFlowData`, returning 0 if the key doesn't exist.

### Refresh(fCallback, tCallbackArgs)
Refreshes the mission flow by iterating through bindings defined in `_tFlowData`. If a binding's prerequisite function returns true, it executes the consequence function. It handles deferred key awards and recursively refreshes if any actions were taken.

### SetMissionToRepeat(sMissionName)
Marks a mission to repeat by adding it to `_tMissionsToRepeat`.

### AcceptMissions(tAcceptedMissions, sLastAcceptedMission)
Accepts a list of missions, completing their briefings. If the player is in free play mode, it tracks the selected mission. It disables job tracking for all active missions.

### DisableAllJobTracking()
Disables job tracking for all active missions that are jobs.

### SaveSingleton()
Saves the current state of `_tMyFlowData`, `_tActiveMissions`, and `_tCulledBindings` into a table for later loading.

### LoadSingleton(tSaveData)
Loads saved data from `tSaveData`, restoring `_tMyFlowData`, culling bindings, and unlocking missions.

### GetCaseSensitiveMissionId(sMissionId)
Retrieves the case-sensitive mission ID from `WifMissionData.tMissionData` based on a case-insensitive match.

### SetLastCompletedContractName(sName)
Sets the last completed contract name to `_sLastCompletedContractName`.

### GetLastCompletedContractName()
Returns the last completed contract name.

### EnableAutosave()
Enables mission autosave by setting `_bDoMissionAutosave` to true.

### IsCheckpointSaveModeEnabled()
Checks if checkpoint save mode is enabled.

### EnableCheckpointSaveMode(bEnable)
Enables or disables checkpoint save mode based on the `bEnable` parameter.

### SetRetryLocations(tLocations)
Sets retry locations to `_tRetryLocations`.

### GetRetryLocations()
Returns the current retry locations.

### SetPersistentRetryLocations(tLocations)
Sets persistent retry locations to `_tPersistentRetryLocations`.

### GetPersistentRetryLocations()
Returns the current persistent retry locations.

### SetGrappleEnabled(bEnable)
Enables or disables grapple functionality. It sends a custom event to all players and sets the local state accordingly.

### SetVehicleDisguiseEnabled(bEnable)
Enables or disables vehicle disguise functionality. It sends a custom event to all players and sets the local state accordingly.

### NetEventCallback(nEventId, tArgs)
Handles network events related to grapple and vehicle disguise settings, as well as autosave requests.

### Autosave()
Performs an autosave if the player is in mission mode and not in a wagered mission. It saves the current mission state and triggers a save game request.

### IsGrappleEnabled()
Checks if grapple functionality is enabled.

### IsVehicleDisguiseEnabled()
Checks if vehicle disguise functionality is enabled.

### EnableResourceCounters(bEnable)
Enables or disables resource counters (cash and fuel) on the HUD.

### AreResourceCountersEnabled()
Checks if resource counters are enabled.

### GetMissionStates()
Retrieves the states of all missions, indicating whether they are incomplete, complete, or active.

### _BeginBlockingSequence()
Increments the blocking sequence counter.

### _EndBlockingSequence()
Decrements the blocking sequence counter and performs actions like autosaving or refreshing callbacks if no sequences remain.

### _AttemptSkipModeExit()
Attempts to exit skip mode if it is enabled and all blocking sequences have completed.

### _RefreshComplete()
Executes the refresh callback if set, resetting it afterward.

### AddPdaMissionDetails(sMissionId, tObjectives, bSelectedMission, nLevel)
This function adds mission details to the in-game PDA (Personal Digital Assistant). It takes a mission ID, objectives, a boolean indicating if it's the selected mission, and an optional level number. The function checks if the mission is suppressed in the PDA and returns early if so. If on the client side and a level number is provided, it stores this information. It then builds the mission header and description, retrieves faction and texture details, determines if the mission is a contract, and sets the sort order based on various conditions. Finally, it adds the mission to the PDA map and handles briefing blips for contracts.

### BuildMissionHeader(sMissionId, tObjectives)
This function constructs the header text for a mission in the PDA. If the mission is a contract, it includes the mission title and level (if repeatable). If objectives are provided, it uses the first objective's description. Otherwise, it defaults to the mission title.

### BuildMissionDescription(sMissionId, bPrependHeader, bIncludeRecommendations, tObjectives)
This function builds the detailed description for a mission in the PDA. It can prepend the header text and include recommendations based on parameters. It retrieves faction details, formats the mission terms, objectives, and rewards. If the mission is a contract, it includes objective list headers and inline icons for each objective.

### RefreshAllPdaMissionDetails()
This function refreshes the PDA mission details for all active missions. It checks if the current context is on the client side and returns early if so. For each active mission, it calls `RefreshPdaDisplay` if available; otherwise, it adds the mission details using `AddPdaMissionDetails`.

### RemovePDAMission(sMissionName)
This function removes a mission from the PDA map. It takes a mission name or index, converts it to a mission ID if necessary, and then removes the corresponding mission entry from the PDA map.

## Events

{: .warning }
> **Corrected — the previous version of this page invented an entire Events list** (`Event.MissionUnlock`,
> `Event.MissionDestroy`, `Event.PlayerAcceptMissions`, `Event.MissionBriefingStart`, `Event.PlayerDeath`,
> `Event.MissionRefresh`). **None of those exist anywhere in the source** (grep-confirmed: zero
> `Event.Create` for any of them). `UnlockMission`/`DestroyMission`/`AcceptMissions`/`Refresh` are plain
> functions called directly by other modules, not event handlers.

The only real `Event.*` usage in this file:

- **Two `Event.CreatePersistent(Event.ScriptEvent, {"mpPlayerJoin", ...})` handles**, created inside
  `SetGrappleEnabled` and `SetVehicleDisguiseEnabled` (stored in `_evSetGrapple` / `_evSetVehicleDisguise`,
  deleted and recreated on each call). Their purpose is to re-send the current grapple / vehicle-disguise
  setting to any player who joins mid-session. The predicate `Net.IsServer() and not Player.IsLocal(tData[1])`
  means only the server acts, and only for a remote (non-local) joiner.

- **Custom network events** are dispatched through `NetEventCallback(nEventId, tArgs)` (the engine routes
  `Net.SendCustomEvent("MrxMissionFlow", ...)` to it — see the
  [Custom Networked Events deep dive](../deep-dives/networking)). The event IDs are module constants:
  `NETEVENT_SETGRAPPLE = 0`, `NETEVENT_AUTOSAVE = 1`, `NETEVENT_SETVEHICLEDISGUISE = 2`. `SetGrappleEnabled`
  / `SetVehicleDisguiseEnabled` broadcast the first/third; `_EndBlockingSequence` broadcasts
  `NETEVENT_AUTOSAVE` after a server autosave so clients autosave in step.

## Notes for modders

1. **`UnlockMission` is the real entry point** — see its section above. A custom mission needs a
   `WifMissionData.tMissionData` entry (with at least `sFactionId`, `sStarter`, `bContract`) and, for cash
   rewards, an [`MrxRewardData`](mrxrewarddata) entry; both are picked up automatically. `SetMissionParent`
   must have been called first (there's an `ASSERT(_oParent)` at the top of `UnlockMission`).

2. **The load hand-off to [`MrxState`](mrxstate):** the mission config's `fOnAssetsLoaded` (wired to a local
   `_OnAssetsLoaded`) calls `MrxState.Exit(STATE_WAITFORSTREAMING)` + `MrxState.Exit(STATE_WAITFORGAME)`, and
   `_OnBriefingComplete` calls `MrxState.Enter(STATE_WAITFORSTREAMING, oMission.Activate, ...)`. These
   Enter/Exit calls are what emit the world-load markers the `loadprobe` tool keys on — if you intercept the
   accept/activate flow, keep these paired or the game stays faded/locked (see the
   [`MrxState`](mrxstate) refcount notes).

3. **`_tActiveMissions` is keyed by mission name** (not GUID) and populated synchronously by `UnlockMission`.
   A bare-`MrxTask`-based mission's zero-arg `fOnActivate` reads its own instance back from
   `WifMissionFlow._tActiveMissions.<sMissionName>.oMission`.

4. **Tunables** (all module-level, all reset by `Reset(true)`):
   - `_bEnable`: master mission-flow gate (`EnableFlow`). `Refresh` early-returns if false.
   - `_bCheckpointSaveMode` (`EnableCheckpointSaveMode`): routes saves through the "retry" checkpoint slot.
   - `_bGrappleEnabled` / `_bVehicleDisguiseEnabled`: replicated player abilities (see Events above).
   - `_bResourceCountersEnabled`: cash/fuel HUD counters (`EnableResourceCounters`).

5. **Decompiler artifacts** to ignore: some locals are assigned but never read; a few literals have duplicate
   keys (only the last wins at runtime); `Reset` sets `_bCurrentlyRefreshing = nil` twice in a row.