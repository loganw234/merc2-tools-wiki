---
title: MrxStarter
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [briefing, mission, starter]
---

# MrxStarter

*Module: mrxstarter.lua*

## Overview
The `MrxStarter` module is responsible for managing the briefing process, handling missions, and maintaining various state related to player interactions with NPCs (Non-Player Characters). It provides functionality to set up and manage briefings, track mission acceptance, and handle special case greetings. This module is crucial for initializing and managing NPC interactions in the game.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxTask`, `MrxUtil`, `MrxLayerManager`, `MrxHqManager`, `MrxPlayState`, `MrxState`, `WifPmcInterior`, `WifBriefingData`, `WifMissionData`, `MrxUnlockFanfare`, `WifMissionFlow`, `MrxSoundBanks`, `MrxTransit`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `_tBriefings`: A table to store briefings.
- `_nBriefingCount`: An integer count of briefings.
- `_bActive`: A boolean indicating if the starter is active.
- `_uGuid`: The GUID of the actor associated with this starter.
- `_bFanfareDisplayed`: A boolean indicating if the fanfare has been displayed.
- `_bCardDisplayed`: A boolean indicating if the card has been displayed.
- `_tOldBriefings`: A table to store old briefings.
- `_tIntros`: A table to manage intros.
- `_tMissionsToBeAccepted`: A table of missions to be accepted.
- `_sLastAcceptedMission`: The last accepted mission name.
- `_sPendingContractId`: The ID of the pending contract.
- `_bLoaded`: A boolean indicating if the starter is loaded.
- `_nLoadPending`: An integer count of pending loads.
- `_tQualityRefs`: A table to manage quality references for actors.

## Functions

### Create(mModule, self)
- **Description**: Creates a new instance of the module with the given `mModule` and `self`.
- **Parameters**:
  - `mModule`: The module prototype.
  - `self`: The instance to be created.
- **Returns**: The newly created instance.

### GetName(self)
- **Description**: Returns the name of the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The name as a string.

### GetPmcName(self)
- **Description**: Returns the PMC name associated with the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The PMC name as a string.

### GetActionDisplay(self)
- **Description**: Returns the action display text for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The action display text as a string.

### GetHq(self)
- **Description**: Returns the HQ name associated with the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The HQ name as a string.

### IsBoss(self)
- **Description**: Checks if the starter is a boss.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it's a boss.

### IsPmcStarter(self)
- **Description**: Checks if the starter is a PMC starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it's a PMC starter.

### IsMale(self)
- **Description**: Checks if the starter is male.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it's male.

### HasHintSystem(self)
- **Description**: Checks if the starter has a hint system.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it has a hint system.

### HasBribeSystem(self)
- **Description**: Checks if the starter has a bribe system.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it has a bribe system.

### HasGarageSystem(self)
- **Description**: Checks if the starter has a garage system.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it has a garage system.

### HasTransitSystem(self)
- **Description**: Checks if the starter has a transit system.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it has a transit system.

### GetFaction(self)
- **Description**: Returns the faction associated with the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The faction as a string.

### GetCardData(self)
- **Description**: Returns the card data for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The card data table.

### GetPlayerVisibleName(self)
- **Description**: Returns the player-visible name of the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The player-visible name as a string.

### HasShop(self)
- **Description**: Checks if the starter has a shop or custom vehicle shop.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it has a shop or custom vehicle shop.

### HasCustomVehicleShop(self)
- **Description**: Checks if the starter has a custom vehicle shop.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if it has a custom vehicle shop.

### SetActor(self, uGuid)
- **Description**: Sets the GUID of the actor associated with the starter.
- **Parameters**:
  - `self`: The instance.
  - `uGuid`: The GUID to set.

### GetActor(self)
- **Description**: Returns the GUID of the actor associated with the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The GUID as a string.

### _SetFanfareDisplayed(self, bDisplayed)
- **Description**: Sets whether the fanfare has been displayed.
- **Parameters**:
  - `self`: The instance.
  - `bDisplayed`: A boolean indicating if the fanfare has been displayed.

### FanfareDisplayed(self)
- **Description**: Marks the fanfare as displayed.
- **Parameters**:
  - `self`: The instance.

### HasFanfareBeenDisplayed(self)
- **Description**: Checks if the fanfare has been displayed.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if the fanfare has been displayed.

### _SetCardDisplayed(self, bDisplayed)
- **Description**: Sets whether the card has been displayed.
- **Parameters**:
  - `self`: The instance.
  - `bDisplayed`: A boolean indicating if the card has been displayed.

### CardDisplayed(self)
- **Description**: Marks the card as displayed.
- **Parameters**:
  - `self`: The instance.

### HasCardBeenDisplayed(self)
- **Description**: Checks if the card has been displayed.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if the card has been displayed.

### GetGlobalFaceFxSet(self)
- **Description**: Returns the global face fx set for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The face fx set as a string.

### AddBriefing(self, sMissionName, sMissionTitle)
- **Description**: Adds a briefing to the starter.
- **Parameters**:
  - `self`: The instance.
  - `sMissionName`: The name of the mission.
  - `sMissionTitle`: The title of the mission.

### RemoveBriefing(self, sMissionName)
- **Description**: Removes a briefing from the starter.
- **Parameters**:
  - `self`: The instance.
  - `sMissionName`: The name of the mission to remove.

### GetOfferedBriefings(self)
- **Description**: Returns the offered briefings for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A table of offered briefings.

### _SetBriefingCount(self, nBriefingCount)
- **Description**: Sets the count of briefings.
- **Parameters**:
  - `self`: The instance.
  - `nBriefingCount`: The number of briefings to set.

### _GetBriefingCount(self)
- **Description**: Returns the count of briefings.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The number of briefings as an integer.

### SetBriefingOld(self, sMissionName)
- **Description**: Marks a briefing as old.
- **Parameters**:
  - `self`: The instance.
  - `sMissionName`: The name of the mission to mark as old.

### IsBriefingOld(self, sMissionName)
- **Description**: Checks if a briefing is old.
- **Parameters**:
  - `self`: The instance.
  - `sMissionName`: The name of the mission to check.
- **Returns**: A boolean indicating if the briefing is old.

### GetOldBriefings(self)
- **Description**: Returns the old briefings for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A table of old briefings.

### AddIntro(self, sName)
- **Description**: Adds an intro to the starter.
- **Parameters**:
  - `self`: The instance.
  - `sName`: The name of the intro.

### RemoveIntro(self, sName)
- **Description**: Removes an intro from the starter.
- **Parameters**:
  - `self`: The instance.
  - `sName`: The name of the intro to remove.

### SetViewedIntro(self, sName, bViewed, bRefresh)
- **Description**: Sets whether an intro has been viewed.
- **Parameters**:
  - `self`: The instance.
  - `sName`: The name of the intro.
  - `bViewed`: A boolean indicating if the intro has been viewed.
  - `bRefresh`: A boolean indicating if a refresh is needed.

### HasViewedIntro(self, sName)
- **Description**: Checks if an intro has been viewed.
- **Parameters**:
  - `self`: The instance.
  - `sName`: The name of the intro to check.
- **Returns**: A boolean indicating if the intro has been viewed.

### GetIntros(self)
- **Description**: Returns the intros for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A table of intros.

### HasIntros(self)
- **Description**: Checks if there are any intros.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if there are any intros.

### SetMissionAccepted(self, sMissionName, bAccepted)
- **Description**: Sets whether a mission has been accepted.
- **Parameters**:
  - `self`: The instance.
  - `sMissionName`: The name of the mission.
  - `bAccepted`: A boolean indicating if the mission has been accepted.

### IsMissionAccepted(self, sMissionName)
- **Description**: Checks if a mission has been accepted.
- **Parameters**:
  - `self`: The instance.
  - `sMissionName`: The name of the mission to check.
- **Returns**: A boolean indicating if the mission has been accepted.

### GetMissionsToBeAccepted(self)
- **Description**: Returns the missions to be accepted for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A table of missions to be accepted and the last accepted mission name.

### SetPendingContract(self, sPendingContractId)
- **Description**: Sets the pending contract ID for the starter.
- **Parameters**:
  - `self`: The instance.
  - `sPendingContractId`: The ID of the pending contract.

### GetPendingContract(self)
- **Description**: Returns the pending contract ID for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The pending contract ID as a string.

### IsContractPending(self)
- **Description**: Checks if there is a pending contract.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if there is a pending contract.

### ResetIntraSessionData(self)
- **Description**: Resets the intra-session data for the starter.
- **Parameters**:
  - `self`: The instance.

### HasCriticalPathBriefings(self)
- **Description**: Checks if there are any critical path briefings.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if there are any critical path briefings.

### Activate(self)
- **Description**: Activates the starter.
- **Parameters**:
  - `self`: The instance.

### Deactivate(self)
- **Description**: Deactivates the starter.
- **Parameters**:
  - `self`: The instance.

### IsActivated(self)
- **Description**: Checks if the starter is activated.
- **Parameters**:
  - `self`: The instance.
- **Returns**: A boolean indicating if the starter is activated.

### Start(self)
- **Description**: Starts the briefing process for the starter.
- **Parameters**:
  - `self`: The instance.

### GetBriefingWrapper(self)
- **Description**: Returns the briefing wrapper for the starter.
- **Parameters**:
  - `self`: The instance.
- **Returns**: The briefing wrapper table.

### End(self, tMissionsAcceptedThisSession, sLastAcceptedMission)
- **Description**: Ends the briefing process for the starter.
- **Parameters**:
  - `self`: The instance.
  - `tMissionsAcceptedThisSession`: A table of missions accepted this session.
  - `sLastAcceptedMission`: The last accepted mission name.

### _CompleteHqExit(self, oHq)
- **Description**: Completes the HQ exit process for the starter.
- **Parameters**:
  - `self`: The instance.
  - `oHq`: The HQ object.

### Load(self, fCallback, tCallbackData)
- **Description**: Loads the assets and data required for the starter.
- **Parameters**:
  - `self`: The instance.
  - `fCallback`: A callback function to call after loading.
  - `tCallbackData`: Data to pass to the callback function.

### Unload(self)
This function handles the unloading process for the `mrxstarter` module. It checks if the module is loaded and proceeds to unload various resources, including layers, actors, asset preloads, and face fx sets. The function ensures that all associated objects are removed from the game world and assets are properly unloaded.

### RefreshBriefingRoomDisplay(self)
This function refreshes the briefing room display based on the current HQ name or if it is a PMC starter. It retrieves the HQ object and calls `RefreshUiDisplay` to update the UI accordingly. If no HQ name is found and it is a PMC starter, it refreshes the PMC interior UI.

### SetBriefingModule(self, mModule)
This function sets the briefing module for the `mrxstarter` instance. The briefing module is stored in the `_mBriefingModule` field of the instance.

### SetSpecialCaseGreeting(self, sVo)
This function sets a special case greeting voice-over (VO) for the `mrxstarter` instance. The VO is stored in the `_sSpecialCaseGreeting` field of the instance.

### GetSpecialCaseGreeting(self)
This function retrieves the special case greeting voice-over (VO) set for the `mrxstarter` instance. It returns the value stored in the `_sSpecialCaseGreeting` field.

## Events
- **Event.PlayerJoined**: Listens for when a player joins the session and performs necessary initialization.
- **Event.PlayerLeft**: Listens for when a player leaves the session and handles cleanup or state reset.
- **Event.MissionAccepted**: Listens for when a mission is accepted by the player and updates internal mission tracking.
- **Event.BriefingCompleted**: Listens for when a briefing is completed and performs actions such as marking briefings as old or updating UI displays.
- **Event.HqExitCompleted**: Listens for when an HQ exit process is completed and handles associated cleanup.

## Notes for modders
- **Call-order requirements**: Ensure that `Activate` is called before using any other functions to properly initialize the starter. Similarly, call `Deactivate` when the starter is no longer needed to clean up resources.
- **Pitfalls**: Be cautious with modifying internal state directly; use provided setter and getter functions to maintain consistency.
- **Tunables**: There are no tunable parameters exposed in this module's API for modders. Any customization should be done through the briefing system or other high-level interfaces.
- **Decompiler artifacts**: The function `_SetFanfareDisplayed` and `_SetCardDisplayed` have unused local variables that can be ignored as decompiler artifacts.