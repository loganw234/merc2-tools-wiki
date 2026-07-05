---
title: MrxStarter
parent: Missions & Tasks
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [briefing, mission, starter]
verified: true
verified_note: corrects the Instance pattern (class-factory via Create(mModule, self), the same
  prototype-inheritance pattern as MrxTask — not per-uGuid); confirms IsBoss/AddBriefing/SetPendingContract/
  End's exact mechanism from building and debugging a real custom contract end to end — see the
  [Custom Contract deep dive](../deep-dives/custom-contract).
---

# MrxStarter

*Module: mrxstarter.lua*

## Overview
The `MrxStarter` module is responsible for managing the briefing process, handling missions, and maintaining various state related to player interactions with NPCs (Non-Player Characters). It provides functionality to set up and manage briefings, track mission acceptance, and handle special case greetings. This module is crucial for initializing and managing NPC interactions in the game.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGui`, `MrxTask`, `MrxUtil`, `MrxLayerManager`, `MrxHqManager`, `MrxPlayState`, `MrxState`, `WifPmcInterior`, `WifBriefingData`, `WifMissionData`, `MrxUnlockFanfare`, `WifMissionFlow`, `MrxSoundBanks`, `MrxTransit`

## Instance pattern
**Not per-`uGuid` — this is the same class-factory pattern as [`MrxTask`](mrxtask), confirmed directly from
`Create`'s exact body:**

```lua
function Create(mModule, self)
  self = self or {}
  setmetatable(self, {__index = mModule})
  self._tBriefings = {}
  self:_SetBriefingCount(0)
  return self
end
```

`setmetatable(self, {__index = mModule})` — prototype inheritance via metatable, no `tInstance[uGuid]`
registry anywhere in this function. Each real starter (Fiona, Ewan, Misha, Eva, etc.) is one of these
tables, held and looked up by name elsewhere (`MrxStarterManager.RequestStarter(sStarter)`, confirmed used
by [`WifMissionFlow.UnlockMission`](mrxmissionflow) to fetch a starter and call `AddBriefing` on it) — not
indexed by a world-object GUID inside this module itself. It tracks the following key fields:
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
- **Confirmed starter-ID-to-character mapping**: `"PmcBoss"` → `"Fiona"`, `"HelPmcBoss"` → `"Ewan"`,
  `"JetPmcBoss"` → `"Misha"`, `"MecPmcBoss"` → `"Eva"`.

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
- **Confirmed exact body: `return self.bBoss`.** Purely a data flag from `WifStarterData`, not derived from
  the starter ID's name. **`WifStarterData.PmcBoss` (Fiona) does not set `bBoss = true`**, confirmed live —
  talking to her shows the normal multi-option briefing menu rather than the auto-selected-first-entry
  behavior [`_DisplayRootMenu`](mrxbriefing) takes for a starter where `IsBoss()` is true. Don't assume a
  starter ID containing "Boss" implies this returns true.

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
- **Confirmed exact body**: `self._tBriefings[sMissionName] = {sTitle = sMissionTitle, sLevel =
  sMissionLevel}`. This is what makes a mission actually appear in this starter's menu — confirmed live by
  registering a mission directly into `WifMissionData.tMissionData` and calling
  [`WifMissionFlow.UnlockMission`](mrxmissionflow), which calls this internally
  (`_AddBriefingToStarter`) and the new entry showed up in Fiona's menu on the next interaction, no other
  step required. Does **not** set `.tConfig` — that only happens later, in
  [`mrxbriefing.lua`'s `Start()`](mrxbriefing), which aliases this same `_tBriefings` table
  (`_oStarter:GetOfferedBriefings()` below returns this exact table reference, not a copy) and sets
  `.tConfig = WifBriefingData[sMissionName] or {}` on every entry once a briefing session begins.

### RemoveBriefing(self, sMissionName)
- **Description**: Removes a briefing from the starter.
- **Parameters**:
  - `self`: The instance.
  - `sMissionName`: The name of the mission to remove.

### GetOfferedBriefings(self)
- **Description**: Returns the offered briefings for the starter.
- **Confirmed: returns `self._tBriefings` directly, not a copy** — [`mrxbriefing.lua`'s `Start()`](mrxbriefing) aliases its own module-level `_tBriefings` to this exact same table via `_tBriefings = _oStarter:GetOfferedBriefings()`.
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
- **Confirmed why this matters**: [`mrxbriefing.lua`'s `_AcceptOrDeclineMission`](mrxbriefing) only calls
  this when `WifMissionData.IsMissionAContract(sMissionId)` is true for the accepted mission. That in turn
  is a `bContract` field on the mission's `WifMissionData.tMissionData` entry — set automatically by
  `WifMissionData.Init()` for every real mission, but that pass already ran before a custom `OnLoad`
  script's own entry exists, so a custom contract has to set `bContract = true` itself or this call never
  happens, and `WifPmcInterior.Exit()` (which reads `GetPendingContract()` to decide where to teleport the
  player) falls back to the HQ's own default exterior exit instead — confirmed live: skipping this leaves
  the player with no clear way out after accepting.

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
- **Confirmed**: for a PMC starter (`bPmcStarter` true) with a non-`nil` `sLastAcceptedMission`, calls
  `WifPmcInterior.Exit(1, false)` — this is the actual call that teleports the player back out of the HQ
  interior after accepting a mission. Called from [`mrxbriefing.lua`'s `_EndBegin`](mrxbriefing) as
  `_oStarter:End(_tMissionsToBeAccepted, _sLastAcceptedMission)`, the very end of the accept flow. Confirmed
  reached live for a custom contract mission with no real spiel asset, once the two workarounds documented
  on the `mrxbriefing` page were in place.

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

{: .warning }
> **Corrected — the previous version invented this section** (`Event.PlayerJoined`, `Event.PlayerLeft`,
> `Event.MissionAccepted`, `Event.BriefingCompleted`, `Event.HqExitCompleted`). **None exist in the source.**
> The only `Event.*` call in the whole file is a per-asset `Event.Create(Event.TimerRelative, {15, false},
> _AssetLoaded, ...)` inside `Load` — a 15-second load-timeout watchdog per asset, not a lifecycle
> subscription. Everything else (`Activate`/`Deactivate`/`Start`/`End`/`AddBriefing`/…) is driven by direct
> method calls from [`MrxStarterManager`](mrxstartermanager), [`WifMissionFlow`](mrxmissionflow), and
> [`mrxbriefing`](mrxbriefing), not engine events.

## Notes for modders
- **`AddBriefing` is the lever that puts a mission in a starter's menu** (see its entry). The normal path is
  [`WifMissionFlow.UnlockMission`](mrxmissionflow) → `RequestStarter(sStarter):AddBriefing(...)`; you rarely
  call it by hand, but knowing it writes `self._tBriefings[sMissionName]` (and that
  [`mrxbriefing`](mrxbriefing) aliases that exact table) is key to understanding why a mission appears/vanishes.
- **`Load` has a 15-second per-asset timeout.** If a starter's `tAssetPreload`/`tActors`/`sFaceFxSet` names a
  missing asset, the load doesn't hang forever — the watchdog fires `_AssetLoaded(..., true)` and logs
  `"... TIMED OUT"`. Watch for that string if a starter loads with a missing face or actor.
- **`bBoss` gates real behavior** (see `IsBoss`): a boss starter skips greetings and auto-opens its first
  briefing ([`_DisplayRootMenu`](mrxbriefing)), and `Load` pulls its actors from the *first* briefing's
  `WifBriefingData.tActors`. Fiona's `PmcBoss` does **not** set `bBoss`, despite the name — check the actual
  `WifStarterData` entry.
- **Data-driven fields** (all from the `WifStarterData` entry, surfaced by the `Get*`/`Has*` accessors):
  `sHqName`, `bPmcStarter`, `bFemale`, `bBoss`, `bHintSystem`/`bBribeSystem`/`bGarageSystem`/`bTransitSystem`,
  `bShop`/`bCustomVehicleShop`, `sFaceFxSet`, `tCardData`, `sFaction`. These are the customization surface —
  edit the starter's `WifStarterData` entry, not this module.
- **Decompiler artifacts**: `_SetFanfareDisplayed`/`_SetCardDisplayed` and a couple of `Load` locals hold
  unused values; ignore them.