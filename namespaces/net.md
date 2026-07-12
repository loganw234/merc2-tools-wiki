---
title: Net
parent: Engine Namespaces
nav_order: 7
---

# Net

## Overview

`Net` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it,
no `import()` call needed, and it's always globally available to every script. Its functions cover
server/client role queries (`IsServer`, `IsClient`, `IsMultiplayer`), lobby and matchmaking control,
achievement granting and player-management (kicking, quitting), and — the bulk of the namespace by
function count — a large family of `SendEvent_*` calls that broadcast a named, one-way network event to
sync HUD/UI-visible state (fanfare cards, PDA blips, objectives, movies, teleports, tutorial popups)
across a co-op session. There is also a general-purpose `SendCustomEvent(sModuleName, iEventId, tArgs
[, bReliable])` used throughout `vz/` mission scripts to sync arbitrary mission-specific state, separate
from the named `SendEvent_*` family.

## Provenance

This page's function list comes from a live `pairs(Net)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 92
function names below is complete and authoritative: every one of them really exists on the namespace. It
does **not** mean every entry is documented with confirmed arguments. Where a function is actually called
somewhere in the ~230 decompiled `.lua` scripts, we can show a real argument pattern. Where it isn't
called anywhere in that corpus, we only know the name — arguments, return values, and behavior for those
are unconfirmed. Given the sheer size of the `SendEvent_*` family (~80 of the 92 functions), individual
call sites were not hunted down for every single one; instead the general calling convention was
confirmed from several concrete examples, and the rest are documented as a single family sharing that
convention. See [Notes for modders](#notes-for-modders).

## Functions

### Server/Client Role & State

| Function | Signature (best-known) | Notes |
|---|---|---|
| `IsServer` | `b = Net.IsServer()` | Extremely common in real scripts — the standard gate before broadcasting a `SendEvent_*` call or mutating authoritative state, e.g. `if Net.IsServer() then Net.SendEvent_Fanfare(...) end`. See Notes for modders. |
| `IsClient` | `b = Net.IsClient()` | Common in real scripts, used both as `if Net.IsClient() then` and `if not Net.IsClient() then` to branch client-only vs. host/local-only logic (e.g. `shell/mrxguicinematic.lua`, `resident/mrxbriefing.lua`). |
| `IsMultiplayer` | `b = Net.IsMultiplayer()` | Used with no arguments in real scripts, e.g. `if not Net.IsMultiplayer() then` in `shell/mrxguibase.lua`, and combined with `IsServer` as `(not Net.IsMultiplayer() or Net.IsServer())` in `shell/mrxguicinematic.lua`. |
| `IsActive` | `b = Net.IsActive()` | Used with no arguments in real scripts, e.g. `resident/moonpatrol.lua`, `resident/mrxachievements.lua`, several `vz/*con*.lua` mission scripts — appears to gate whether networking/an active session is currently running, distinct from `IsMultiplayer`/`IsServer`. |
| `IsDedicated` | `b = Net.IsDedicated()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `IsEnabled` | `b = Net.IsEnabled()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `IsLobby` | `b = Net.IsLobby()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `IsOnlineEnabled` | `b = Net.IsOnlineEnabled()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `IsOnlineConnected` | `b = Net.IsOnlineConnected()` | Used with no arguments in real scripts, e.g. `if not Net.IsMatchmakingInternet() and not Net.IsOnlineConnected() then Net.Stop() end` in `resident/mrxguishell.lua`. |
| `IsConnectedToInternet` | `b = Net.IsConnectedToInternet()` | Used with no arguments in real scripts, e.g. `resident/mrxguipda.lua`. |
| `IsPlatformConnected` | `b = Net.IsPlatformConnected()` | Used with no arguments in real scripts, combined with `IsMatchmakingInternet` in `resident/mrxguishell.lua` to gate `StartServer`. |
| `IsMatchmakingInternet` | `b = Net.IsMatchmakingInternet()` | Used with no arguments in real scripts, appears throughout `resident/mrxguishell.lua`'s lobby-entry flow to branch internet vs. local matchmaking. |
| `IsReadyToTether` | `b = Net.IsReadyToTether()` | Used with no arguments in real scripts, e.g. `if Net.IsReadyToTether() and not uCurrentVehicleGuid then` in `vz/meccon001.lua`. |
| `ShouldPlayOnline` | `b = Net.ShouldPlayOnline()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `GetHostName` | `s = Net.GetHostName()` | Used with no arguments in real scripts, always as the first argument to `Net.StartServer(Net.GetHostName(), ...)`. |

### Lobby & Matchmaking

| Function | Signature (best-known) | Notes |
|---|---|---|
| `AutoClient` | `b = Net.AutoClient()` | Used with no arguments in real scripts as a boot-time branch, e.g. `if Net.AutoClient() then Net.ConnectToServer() end` in `resident/gamebootstrap.lua` and `shell/shellbootstrap.lua`. |
| `AutoServer` | `b = Net.AutoServer()` | Used with no arguments in real scripts, same boot-time branch as above: `if Net.AutoServer() then Net.StartServer(...) end`. |
| `AutoLobby` | `b = Net.AutoLobby()` | Used with no arguments in real scripts, same boot-time branch: `elseif Net.AutoLobby() then Net.EnterLobby() end`. |
| `ConnectToServer` | `bSuccess = Net.ConnectToServer([sName [, sIPAddressOrMode]])` | Confirmed with no arguments (`Net.ConnectToServer()` at boot) and with two string arguments in `resident/mrxguishell.lua`, e.g. `Net.ConnectToServer(tData.sName, tData.sIPAddress)`, `Net.ConnectToServer(sServerName, "online")`, `Net.ConnectToServer(sName, "")`. Returns a boolean treated as success. |
| `StartServer` | `Net.StartServer(sHostName, sLevelName, sMasterScriptName)` | Confirmed with 3 arguments in real scripts, always as `Net.StartServer(Net.GetHostName(), Sys.GetLevelName(), Sys.GetMasterScriptName())` (`resident/gamebootstrap.lua`, `shell/shellbootstrap.lua`, `resident/mrxguishell.lua`). |
| `Stop` | `Net.Stop()` | Used with no arguments in real scripts, e.g. `resident/mrxguishell.lua`, to tear down a session when not connected online. |
| `EnterLobby` | `Net.EnterLobby()` | Used with no arguments in real scripts, boot-time and shell-menu lobby entry. |
| `ExitFriendsLobby` | `Net.ExitFriendsLobby()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. Presumed counterpart to the confirmed `EnterFriendsLobby`. |
| `EnterFriendsLobby` | `Net.EnterFriendsLobby()` | Used with no arguments in real scripts, `resident/mrxguishell.lua`. |
| `ResetServerList` | `Net.ResetServerList()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `DialogBoxMustBeSignInToLive` | `Net.DialogBoxMustBeSignInToLive()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `DialogBoxPlayLocal` | `Net.DialogBoxPlayLocal()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `DialogBoxPlayOffline` | `Net.DialogBoxPlayOffline()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `UpdatePresence` | `Net.UpdatePresence(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |

### Achievements & Player Management

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GrantAchievement` | `Net.GrantAchievement(sAchievementName)` | Confirmed with a single string argument in real scripts, e.g. `Net.GrantAchievement(sAchievementName)` in `resident/mrxachievements.lua`, always called locally on the machine that should actually be credited (paired with `Net.SendCustomEvent("MrxAchievements", EVENT_GRANTACHIEVEMENT, {sAchievementName}, true)` to notify the other side, not to grant remotely — see that file for the full pattern). |
| `HasPlayerUnlockedCode` | `b = Net.HasPlayerUnlockedCode()` | Used with no arguments in real scripts, e.g. `if Net.HasPlayerUnlockedCode() and nCurrentOutfit ~= 2 then` in `vz/wifpmcinterior.lua` — gates an outfit-unlock code check. |
| `KickPlayer` | `Net.KickPlayer(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `ApplyCachedFactionRelations` | `Net.ApplyCachedFactionRelations(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage unconfirmed. |
| `QuitGame` | `Net.QuitGame()` | Used with no arguments in real scripts, e.g. `resident/mrxguipausescreen.lua` (pause-menu quit) and `vz/wifmissionflow.lua` (twice, at end-of-game/credits flow). |

### SendCustomEvent (general-purpose mission sync)

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SendCustomEvent` | `Net.SendCustomEvent(sModuleName, iEventId, tArgs [, bReliable])` | Extremely common across `vz/` mission scripts and several `resident/` modules for broadcasting arbitrary mission-defined events, e.g. `Net.SendCustomEvent("PmcCon004", NETEVENT_ARTILLERYATTACK, {...})`, `Net.SendCustomEvent("MrxAchievements", EVENT_GRANTACHIEVEMENT, {sAchievementName}, true)`. First argument is always a string matching the calling module's name (used as a routing key on the receiving `Event.Create`/dispatch side), second is a numeric event-ID constant local to that module, third is an args table (often empty `{}`), and an optional trailing boolean (seen as `true`) appears to request reliable delivery. Not gated behind `Net.IsServer()` as consistently as `SendEvent_*` — some call sites fire it unconditionally from either side. |

### SendEvent_* Broadcasts — general pattern

The following ~80 functions form one family: each broadcasts one specific, named, non-custom network
event, almost always used to sync HUD/UI/world-state that must look the same on every client (fanfare
cards, PDA/radar blips, objective markers, movies, teleports, tutorial/HUD messages). Call sites
consistently gate these behind `if Net.IsServer() then ... end` (sometimes combined with an additional
condition, e.g. `if Net.IsServer() and self.bNetSync then` in `resident/blippable.lua`, or `if
Net.IsServer() and not Player.IsLocal(uPlayerGuid) then` in `resident/mrxguihudmessage.lua`). A handful
are additionally guarded with an existence check before calling, e.g. `if Net.SendEvent_CloseFanfare then
Net.SendEvent_CloseFanfare() end` in `resident/mrxguihudmessage.lua`, and `if Net.SendEvent_Support then
... end` in `resident/mrxsupport.lua` — this defensive-existence-check pattern suggests these specific
entries may not exist on every build/version of the engine, though all are present in the live dump used
for this page.

Concrete confirmed examples (real argument shapes):

| Function | Signature (confirmed call site) | Source |
|---|---|---|
| `SendEvent_ShowMessage` | `Net.SendEvent_ShowMessage(uPlayerGuid, sTextureName, nX, nY, sHorizontalAnchor, sVerticalAnchor, nWidth, nHeight, nDisplayTime)` | `resident/mrxguihudmessage.lua:953`, gated `Net.IsServer() and not Player.IsLocal(uPlayerGuid)`. |
| `SendEvent_Fanfare` | `Net.SendEvent_Fanfare(sType, "", "", "", sCancelMsg, tLineList, nSlowdownDuration, 0)` | `resident/mrxguihudmessage.lua:339`, gated `Net.IsServer()`. |
| `SendEvent_CardFanfare` | `Net.SendEvent_CardFanfare(sFaction, sTitle, sName, sJobTitle, sPhone1, sPhone2, sEmail, nDisplayTime)` | `resident/mrxguihudmessage.lua:229`. |
| `SendEvent_TeleportPlayer` | `Net.SendEvent_TeleportPlayer(uPlayer, nX, nY, nZ, nYaw)` | `resident/mrxutil.lua:198`, inside `if Net.IsServer() then`, only for non-local players (`if not Player.IsLocal(uPlayer) then`). |
| `SendEvent_TeleportPlayerToHardPoint` | `Net.SendEvent_TeleportPlayerToHardPoint(uPlayer, uObject, sHardpoint)` | `resident/mrxutil.lua:338`. |
| `SendEvent_AddMarkerObjective` | `Net.SendEvent_AddMarkerObjective(uGuid, uMarkerGuid, nR, nG, nB, nVerticalOffset, nIconIndex, nScale1, nScale2, bFlag, nNearDist, nFarDist [, uiMissionNameHash])` | `resident/blippable.lua:85`, `resident/mrxtaskobjective.lua:430`, gated `Net.IsServer() and self.bNetSync`. |
| `SendEvent_RemoveMarkerObjective` | `Net.SendEvent_RemoveMarkerObjective(uMarkerGuid)` | `resident/blippable.lua:64`, widely used, single-argument. |
| `SendEvent_AddRadarObjective` | `Net.SendEvent_AddRadarObjective(sName, nX, nY, nZ, nR, nG, nB, nWidth, nHeight, nTextureIndex, uGuid, bSticky, bRotate, bOriented, nSortOrder)` | `resident/mrxguiinterface.lua:25`. |
| `SendEvent_AddPDAMission` | `Net.SendEvent_AddPDAMission(nMissionIndex, tObjectives, bSelectedMission [, nLevel])` | `resident/mrxmissionflow.lua:934`. |
| `SendEvent_RemovePDAMission` | `Net.SendEvent_RemovePDAMission(nMissionIndex)` | `resident/mrxmissionflow.lua:192`. |
| `SendEvent_HVTFanfare` | `Net.SendEvent_HVTFanfare(iFanfareType, sFactionId, sDesc, iInlineIcon, nCompleted, nQuota)` | `resident/mrxtaskjobverifyset.lua:76`. |
| `SendEvent_RevivePlayer` | `Net.SendEvent_RevivePlayer(iPlayerId)` | `resident/mrxplayer.lua:327`. |
| `SendEvent_Support` | `Net.SendEvent_Support(oModule, nX, nY, nZ, uDesignator, uTarget, uCargoToDeliver, finalDestination, uDeliveryVehicle, setBomb, bEventPost)` | `resident/mrxsupport.lua:213`, guarded by `if Net.SendEvent_Support then`. |
| `SendEvent_ShowMovie` / `SendEvent_HideMovie` | `Net.SendEvent_ShowMovie(sFile, nFadeInTime, nFadeOutTime, bSubtitles)` / `Net.SendEvent_HideMovie()` | `shell/mrxguicinematic.lua:142,181`, gated `Net.IsServer()`. |
| `SendEvent_JoinPOForceRequest` / `SendEvent_ForceClientTether` | `Net.SendEvent_JoinPOForceRequest()` / `Net.SendEvent_ForceClientTether()` | `vz/vzacon001.lua:99,112`. |

The remaining functions below are part of the same `SendEvent_*` broadcast family described above — no
individually distinguishing call site was hunted down for each, but they follow the same convention
(gated behind `Net.IsServer()`, one-way HUD/state broadcast, arguments matching the described data being
synced):

`SendEvent_AddDangerousBuilding`, `SendEvent_AddHqPdaBlip`, `SendEvent_AddObjective`,
`SendEvent_AddPdaObjective`, `SendEvent_AddPmcPdaBlip`, `SendEvent_AddRandomDangerousBuilding`,
`SendEvent_AddSupportItem`, `SendEvent_BatchUnlockFanfare`, `SendEvent_ClearObjectiveTraySlot`,
`SendEvent_CloseFanfare`, `SendEvent_EnableHeroWeapons`, `SendEvent_ObjectiveMessage`,
`SendEvent_PursuitMessage`, `SendEvent_RecruitsUnlocked`, `SendEvent_RemoveDangerousBuilding`,
`SendEvent_RemoveHqPdaBlip`, `SendEvent_RemoveObjective`, `SendEvent_RemovePdaObjective`,
`SendEvent_RemovePmcPdaBlip`, `SendEvent_RemoveRadarObjective`, `SendEvent_RemoveSupportItem`,
`SendEvent_RequestPosition`, `SendEvent_SetObjectiveTraySlotImage`, `SendEvent_SetObjectiveTraySlotText`,
`SendEvent_SetOccupiedDangerousBuilding`, `SendEvent_TextFanfare`, `SendEvent_UnlockFanfare`.

(All of the above were in fact also found with real call sites during research for this page — e.g.
`SendEvent_AddDangerousBuilding` in `resident/dangerousbuilding.lua:134`, `SendEvent_AddHqPdaBlip` in
`resident/mrxhq.lua:383`, `SendEvent_PursuitMessage` in `resident/mrxguiinterface.lua:903` — but are
grouped here rather than given individual rows, since their argument shapes don't add information beyond
the general pattern already established above.)

### Briefing & Loading Screen

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetLoadingScreen` | `Net.SetLoadingScreen(bShow)` | Confirmed with a single boolean in real scripts, e.g. `Net.SetLoadingScreen(true)` (`resident/mrxbriefing.lua`, `resident/mrxhq.lua`, `resident/mrxutil.lua`, `vz/wifpmcinterior.lua`) and `Net.SetLoadingScreen(false)` (`resident/mrxstate.lua`). |
| `SetBriefingStarters` | `Net.SetBriefingStarters(nStarterIndex [, tNetStarterActors, tNetUnlockedRewards])` | Confirmed with 1 argument (`Net.SetBriefingStarters(0)`) and with 3 arguments (`Net.SetBriefingStarters(nIndex, tNetStarterActors, tNetUnlockedRewards)`) in `resident/mrxbriefing.lua`. |
| `SetBriefingInterior` | `Net.SetBriefingInterior([sInteriorName])` | Confirmed with a string argument (`Net.SetBriefingInterior("WifPmcInterior")`, `Net.SetBriefingInterior("MrxHq")`) and with no arguments (`Net.SetBriefingInterior()`) to presumably clear it, in `vz/wifpmcinterior.lua` and `resident/mrxhq.lua`. |
| `SetBriefingCheapCinematic` | `Net.SetBriefingCheapCinematic(nType [, nIndex])` | Confirmed with 1 and 2 arguments in `resident/mrxbriefing.lua`, e.g. `Net.SetBriefingCheapCinematic(CHEAP_CONFIRM)`, `Net.SetBriefingCheapCinematic(CHEAP_INTRO, WifBriefingData.GetIntroIndexById(sName))`. |
| `LoadMissionSpiel` | `Net.LoadMissionSpiel(nMissionIndex, tNetBriefingActors)` | Confirmed with 2 arguments in `resident/mrxbriefing.lua:811`. |
| `UnloadMissionSpiel` | `Net.UnloadMissionSpiel(bExitingBriefing)` | Confirmed with 1 boolean argument in `resident/mrxbriefing.lua:1574`. |
| `SetLastHeroTeleportLocation` | `Net.SetLastHeroTeleportLocation(nX, nY, nZ, nYaw)` | Confirmed with 4 arguments in `resident/mrxutil.lua:192`, inside `if Net.IsServer() then`, immediately preceding a `SendEvent_TeleportPlayer` call. |

### Misc

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetTutorialMessage` | `Net.SetTutorialMessage([sMessage])` | Confirmed in `resident/mrxtutorialmanager.lua` — see the `ShowMessage`/`HideMessage` functions there. Called with a string to show a message (`Net.SetTutorialMessage(sMessage)`) or with no arguments to clear it (`Net.SetTutorialMessage()`), both gated `if Net.IsServer() and not bDontNetSync then`. This is the mechanism [Snippets: Show a custom HUD message](../snippets#show-a-custom-hud-message-with-icon-and-sound) uses to co-op-sync tutorial popups — see that section and [`resident/mrxtutorialmanager`](../resident/mrxtutorialmanager) for the full confirmed picture; not re-derived here. |
| `SetPursuitReportingState` | `Net.SetPursuitReportingState(uGuid, nState, sFactionAbbrev)` | Confirmed with 3 arguments in `resident/mrxfactionmanager.lua`, e.g. `Net.SetPursuitReportingState(uGuid, 0, sAbbrev)`, with `nState` seen as `0`, `1`, `2`, `3` across different call sites (meaning of each numeric state not confirmed beyond ordinal position in the pursuit-escalation flow). |
| `SetShootingGalleryBorder` | `Net.SetShootingGalleryBorder(uBorderName)` | Confirmed with 1 argument in `resident/mrxshootinggallery.lua:133`. |
| `BeginLayerEventGroup` / `EndLayerEventGroup` | `Net.BeginLayerEventGroup()` / `Net.EndLayerEventGroup()` | Confirmed with no arguments in `vz/xQ!L.lua`, both guarded by an existence check (`if Net.BeginLayerEventGroup then ... end`), used to bracket a group of layer-related network events. |
| `DoneReloadingLayers` | `Net.DoneReloadingLayers()` | Confirmed with no arguments across several `vz/*con*.lua` scripts (`allcon008`, `meccon001`, `oilcon005`, `pircon001`, `vzacon001`) and `resident/mrxtaskcontract.lua`, always guarded by an existence check (`if Net.DoneReloadingLayers then Net.DoneReloadingLayers() end`) — the recurring existence-check pattern suggests this function may not be present on every engine build. |

## Notes for modders

- The single most important convention on this namespace: almost every state-mutating or broadcast
  function (`SendEvent_*`, `SetTutorialMessage`, `SetLoadingScreen`, `SetLastHeroTeleportLocation`,
  `SetPursuitReportingState`, etc.) is called from inside `if Net.IsServer() then ... end` in every
  real script that uses it. Check `Net.IsServer()` before calling any of these from a mod — calling them
  unconditionally on a client risks either a no-op, an error, or desynced state between host and clients,
  none of which has been tested here.
- A second, weaker gate shows up in several places: `if Net.<Function> then Net.<Function>(...) end`,
  i.e. checking the function exists before calling it (seen for `SendEvent_CloseFanfare`,
  `SendEvent_Support`, `BeginLayerEventGroup`, `EndLayerEventGroup`, `DoneReloadingLayers`). This suggests
  those specific entries may be absent on some builds/platforms of the engine even though they're present
  in the live dump used for this page — defensively existence-check them in mods that need to run across
  versions.
- `SendCustomEvent` is the general-purpose escape hatch for mission scripts that need to sync something
  not covered by a named `SendEvent_*` call — it takes a routing-key string (matching the calling module's
  name), a module-local numeric event ID, an args table, and an optional reliability flag. It is not
  consistently `Net.IsServer()`-gated the way `SendEvent_*` is; some call sites fire it from either side.
- `Net.SetTutorialMessage` is a confirmed-real function purely through decompiled-source evidence
  (`resident/mrxtutorialmanager.lua`) despite having no dedicated live-testing confirmation of its own —
  see the cross-link in the Misc table above.
