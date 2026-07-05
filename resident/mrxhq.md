---
title: mrxhq
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [hq, briefing, ui]
verified: true
verified_note: "deeper pass: rewrote the Events section (no Event.BriefingModuleLoaded/PlayerEnteredHQ/PlayerExitedHQ constants exist — the real sub is Event.CreatePersistent(Event.ContextAction) in SetPortal plus TimerRelative timers; module posts parkingLotStart), pinned the fixed interior spawn pos {3750,450,-3840} and 50-unit draw-distance default, described _tAssetPreload; all functions/Imports re-confirmed"
---

# mrxhq

*Module: mrxhq.lua*

## Overview
The `mrxhq` module is responsible for managing the HQ portal in the game. It handles various aspects such as briefing modules, UI displays, faction attitudes, and player interactions within the HQ interior. The module ensures that the HQ portal behaves correctly based on player state, mission availability, and faction relationships.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxFactionManager`, `MrxGui`, `MrxGuiBootstrap`, `MrxHqManager`, `MrxLayerManager`, `MrxStarterManager`, `MrxUtil`, `MrxTransit`, `MrxPlayState`, `WifFreePlay`, `WifMissionData`, `WifMissionFlow`, `WifVzBoundary`, `MrxSound`, `WifHqData`, `MrxState`, and `MrxTutorialManager`

## Instance pattern
**Not per-`uGuid`** — same class-factory pattern used elsewhere in `resident/`: `Create(mModule, self)` is
`self = self or {}; setmetatable(self, {__index = mModule}); return self`, no `tInstance` registry. It
tracks the following key fields:
- `bLocked`: Indicates whether the HQ portal is locked.
- `inside`: Boolean indicating if players are inside the HQ interior.
- `starter`: The starter object associated with the HQ portal.
- `name`: Name of the HQ portal.
- `radarIcon`: Radar icon for the HQ portal.
- `atmosphere`: Atmosphere settings for the HQ interior.
- `drawDistance`: Draw distance for the HQ portal.
- `buildingName`: Name of the building where the HQ is located.
- `faction`: Faction associated with the HQ portal.
- `respawn`: Boolean indicating if respawning is enabled.
- `lockStatusMessage`: Message displayed when the HQ portal is locked.

## Functions

### NetSafeBriefingModuleLoaded(mModule)
- **Description**: This function is called when the briefing module is loaded. It sets up the briefing assets and exits the `STATE_WAITFORGAME` state.
- **Parameters**:
  - `mModule`: The briefing module that was loaded.

### NetSafeLoadAssets1()
- **Description**: This function dynamically imports the `MrxBriefing` module and calls `NetSafeBriefingModuleLoaded` when it is loaded.
- **Parameters**: None

### NetSafeLoadAssets()
- **Description**: This function enters the `STATE_WAITFORGAME` state and then calls `NetSafeLoadAssets1`.
- **Parameters**: None

### NetSafeUnloadAssets()
- **Description**: This function unloads the briefing assets by calling the unload method on `_NetSafeBriefingModule`, removes the module, and sets `_NetSafeBriefingModule` to nil.
- **Parameters**: None

### Create(mModule, self)
- **Description**: This function creates a new instance of the module with default values for locked, inside, starter, name, radar icon, atmosphere, draw distance, building name, faction, respawn, and lock status message.
- **Parameters**:
  - `mModule`: The module to create an instance of.
  - `self`: The instance being created (optional).

### SetName(self, sName)
- **Description**: This function sets the name of the instance.
- **Parameters**:
  - `sName`: The new name for the instance.

### GetName(self)
- **Description**: This function returns the name of the instance.
- **Parameters**: None

### SetLock(self, bLocked)
- **Description**: This function sets whether the instance is locked.
- **Parameters**:
  - `bLocked`: A boolean indicating if the instance should be locked.

### IsLocked(self)
- **Description**: This function returns whether the instance is locked.
- **Parameters**: None

### GetRadarIcon(self)
- **Description**: This function returns the radar icon of the instance.
- **Parameters**: None

### GetAtmosphere(self)
- **Description**: This function returns the atmosphere of the instance.
- **Parameters**: None

### GetDrawDistance(self)
- **Description**: This function returns the draw distance of the instance, defaulting to 50 if not set.
- **Parameters**: None

### GetEntryLocations(self)
- **Description**: This function returns the entry locations of the instance.
- **Parameters**: None

### GetBuildingName(self)
- **Description**: This function returns the building name of the instance.
- **Parameters**: None

### GetFaction(self)
- **Description**: This function returns the faction of the instance, if a starter is set.
- **Parameters**: None

### SetRespawn(self, bEnable)
- **Description**: This function sets whether the instance should respawn.
- **Parameters**:
  - `bEnable`: A boolean indicating if respawning should be enabled.

### GetRespawn(self)
- **Description**: This function returns whether the instance is set to respawn.
- **Parameters**: None

### NetSafeAddHqPdaBlip(nHqIndex, bSticky, nFactionIndex, sBlipLabel, tMissions, bStarterIsBoss, bUnlocked)
- **Description**: This function adds a PDA blip for the HQ portal.
- **Parameters**:
  - `nHqIndex`: The index of the HQ.
  - `bSticky`: A boolean indicating if the blip should be sticky.
  - `nFactionIndex`: The index of the faction.
  - `sBlipLabel`: The label for the blip.
  - `tMissions`: A table of missions.
  - `bStarterIsBoss`: A boolean indicating if the starter is a boss.
  - `bUnlocked`: A boolean indicating if the HQ is unlocked.

### GetMissionDesc(tMissions)
- **Description**: This function generates a description for the given missions.
- **Parameters**:
  - `tMissions`: A table of mission names.

### AddHqPdaBlip(sBlipName, uBlippedObject, sPdaTexture, bSticky, sFaction, sBlipLabel, tMissions, bStarterIsBoss, nLandingZone, sLockStatusMessage)
- **Description**: This function adds a PDA blip for the HQ portal with detailed information.
- **Parameters**:
  - `sBlipName`: The name of the blip.
  - `uBlippedObject`: The GUID of the object being blipped.
  - `sPdaTexture`: The texture for the PDA icon.
  - `bSticky`: A boolean indicating if the blip should be sticky.
  - `sFaction`: The faction associated with the blip.
  - `sBlipLabel`: The label for the blip.
  - `tMissions`: A table of missions.
  - `bStarterIsBoss`: A boolean indicating if the starter is a boss.
  - `nLandingZone`: The landing zone index.
  - `sLockStatusMessage`: The lock status message.

### NetSafeRemoveHqPdaBlip(nHqIndex)
- **Description**: This function removes the PDA blip for the HQ portal.
- **Parameters**:
  - `nHqIndex`: The index of the HQ.

### RemoveHqPdaBlip(sBlipName)
- **Description**: This function removes a PDA blip by name.
- **Parameters**:
  - `sBlipName`: The name of the blip to remove.

### RefreshUiDisplay(self)
- **Description**: This function refreshes the UI display for the HQ portal, updating radar and PDA blips based on various conditions such as faction attitude, mission availability, and player state.
- **Parameters**:
  - `self`: The instance being refreshed.

### SetPortal(self, bEnable, sActionDisplay)
Enables or disables the HQ portal based on the `bEnable` flag. If enabling, it checks faction attitudes and content availability to determine if the portal should be unlocked. It updates context actions, HUD icons, and markers accordingly. If disabling, it removes all associated context actions, tutorial messages, and markers.

### AddStarter(self, tStarter)
Adds a starter object to the HQ portal. If a starter is already assigned, it logs an error message. Otherwise, it assigns the new starter and refreshes the UI display if necessary.

### RemoveStarter(self, tStarter)
Removes a starter object from the HQ portal if it matches the currently assigned starter. Logs an error message if the removal fails.

### GetStarter(self)
Returns the currently assigned starter object for the HQ portal.

### GlobalEnter(bPmc)
Handles global actions when entering the HQ interior. It disables faction reporting, sets interior mode, toggles HUDs, and makes players invincible. It also plays entry sounds and processes marked layers.

### GlobalExit()
Handles global actions when exiting the HQ interior. It re-enables faction reporting, resets interior mode, toggles HUDs, and restores player invincibility settings. It also plays exit sounds and restores camera settings.

### _OnEnter(self)
Called when a player enters the HQ portal. If already inside, it returns early. Otherwise, it disables faction reporting, sets internal state, and starts loading the interior.

### _LockedOnEnter(self)
Handles the locked entry scenario for the HQ portal. It shows a tutorial message based on the lock status and schedules its removal after 5 seconds.

### HideTutorialMessage(self)
Deletes any scheduled tutorial message hide event and hides the tutorial message.

### _CompleteOnEnter(self)
Completes the interior loading process by entering the game state, refreshing UI displays, stopping nag messages, and loading interior assets. It also sets up briefing modules and teleports players to designated hardpoints.

### _LoadInterior(self)
Loads the interior layers and spawns the HQ interior actor at a specified position. It sets up callbacks for further initialization steps.

### _OnInteriorLoad(self)
Handles the completion of interior loading by initializing the starter, enabling hero weapons, changing atmosphere settings, and teleporting players to designated hardpoints.

### _BriefingModuleLoaded(self, mModule)
Sets the briefing module for the HQ portal and loads necessary assets. It also assigns the briefing module to the starter object.

### _KickoffStarter(self, nSignal)
Handles signals indicating different stages of interior loading completion. Once all stages are complete, it starts the starter mission.

### ExitBegin(self)
Initiates the process of exiting the HQ interior by calling global exit functions, unloading layers and assets, and resetting internal state.

### ExitEnd(self)
Completes the exit process by accepting missions, setting up transit points, and resetting session data. It also calls any unload callbacks and refreshes UI displays.

### _ToggleHuds(bEnable)
Toggles HUDs for all players based on the `bEnable` flag.

### Unload(self)
Unloads layers, removes interior assets, and unloads the starter object associated with the HQ portal.

## Events

The real event **subscription** is the portal's enter-prompt, created in `SetPortal`:

- **`Event.CreatePersistent(Event.ContextAction, {0, uGuid}, fCallBackFunc, {self})`** — fires when the player
  triggers the portal's context action; routes to `_OnEnter` when unlocked or `_LockedOnEnter` when locked
  (which shows a lock-status tutorial message). Deleted whenever the portal is re-configured or disabled.

The module also uses one-shot **`Event.TimerRelative`** timers for the locked-message auto-hide (5 s in
`_LockedOnEnter`), the exit sequence (2 s in `ExitEnd`), and the "all load stages done" kickoff (1 s in
`_KickoffStarter`), and it **posts** `Event.Post("parkingLotStart", {entrance, parkingLotPoint, heliPoint})`
in `ExitEnd` after accepting missions.

{: .note }
> There is no `Event.BriefingModuleLoaded`/`Event.PlayerEnteredHQ`/`Event.PlayerExitedHQ` — an earlier draft
> invented those. Entry/exit are driven by the context-action subscription above and by direct calls
> (`_OnEnter` → `_CompleteOnEnter`; `ExitBegin`/`ExitEnd`). Briefing loading uses `dynamic_import("MrxBriefing", ...)`,
> not an event.

## Module constants & tunables
- `_tAssetPreload` — the briefing asset manifest preloaded for the HQ: per-hero briefing **animations**
  (Chris/Jennifer/Mattias plus generic Male/FemaleStarter idle/greeting/spiel/goodbye sets), facefx animation
  sets, and the `"vo_job_heros"` wavebank/soundbank. Passed to `MrxBriefing`'s load/unload asset calls.
- Interior spawn position is the fixed literal `{3750, 450, -3840}` in `_LoadInterior` (via
  `MrxUtil.SpawnActor(..., "HqInterior", ...)`).
- `GetDrawDistance()` defaults to `50` (used in `Graphics.Camera.SetNearFar(0, 0.3, drawDist, 0)`).
- Radar/PDA blip icons switch to `sRadarIconLocked`/`sPdaIconLocked` when the HQ is locked; HUD marker icon
  sets differ for boss-starter HQs (`HUD_HQ_*`) vs regular starters (`HUD_Outpost_*`), with `_locked` variants.

## Notes for modders

- **Portal lock/unlock is faction-attitude driven.** `RefreshUiDisplay`/`SetPortal` unlock a mutable-faction HQ
  only when relation to `"Pmc"` is `>= "Neutral"` (regular) or `>= "Friendly"` (boss starter) — see
  [`MrxFactionManager.TestAttitude`](mrxfactionmanager). Boss HQs also require free-play and available content.
- **Entering an HQ is a global mode switch**: `GlobalEnter`/`GlobalExit` disable faction reporting, flip
  `WifVzBoundary` interior mode, toggle HUDs, disable/enable hero weapons, and set/clear invincibility on every
  player. If you script anything during an HQ visit, expect those to be in effect.
- Server-authoritative: `RefreshUiDisplay` early-returns on clients; blips are replicated via
  `Net.SendEvent_AddHqPdaBlip`/`Net.SendEvent_RemoveHqPdaBlip` and marker objectives via `Net.SendEvent_Add/RemoveMarkerObjective`.
- Decompiler note: `NetSafeLoadAssets1`'s `mModule` param is unused (artifact).