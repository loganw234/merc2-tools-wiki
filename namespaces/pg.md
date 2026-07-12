---
title: Pg
parent: Engine Namespaces
nav_order: 4
---

# Pg

## Overview
`Pg` is an engine namespace: implemented natively by the game engine, not by any decompiled `.lua` module. It lives under no source file in `resident/` — it requires no `import()` and is always available as a global table from any script. It is a broad grab-bag covering object spawning, proximity-based object collection queries (`FastCollect*`), GUID-by-name lookup, the pursuit/wanted-level system, mission contract lifecycle, achievements, static-layer/asset streaming, and miscellaneous world queries (boundary radius, tether points, landing zones, camera-relative points).

## Provenance
The 80 functions listed below are a complete, authoritative enumeration taken from a live `pairs(Pg)` dump in-game — every name here is confirmed to exist. That dump gives names and raw function pointers only, nothing about parameters or behavior. Everything beyond that (argument shapes, likely purpose) is inferred from real call sites in the ~230 decompiled `.lua` files; where no call site exists anywhere in that corpus, this page says so explicitly rather than guessing.

`Pg.Spawn` and `Pg.FastCollectGroundVehicles` are already documented elsewhere in this wiki with real call-site evidence; see the cross-links in the relevant tables below rather than re-deriving them here.

## Functions

### Spawning

| Function | Signature (best-known) | Notes |
|---|---|---|
| `Spawn` | `Spawn(sTemplateName, x, y, z, ...)` | Spawns an object/vehicle/character by template name string at a world position. Extensively documented already in this wiki with real confirmed template-name strings and call sites — see [`resident/bountycopter.md`](../resident/bountycopter.md) (supply drop templates: `"Supply Drop (Blueprints)"`, `"Supply Drop (Treasure)"`, `"Supply Drop (Light MG)"`, called as `Pg.Spawn(sTemplate, x, y + 200, z)`) and [`resident/soldier.md`](../resident/soldier.md). Do not re-derive; cross-link. |
| `SpawnFromCamera` | `SpawnFromCamera(sTemplateName, nDistance, nHeightOrScale, ...)` | Spawns relative to the current camera. Call-site argument counts vary considerably: as few as 3 args (`Pg.SpawnFromCamera("verify flash", 0, 0)` in `mrxtaskobjectiveverify.lua`), up to 7 (`Pg.SpawnFromCamera(uCargoTemplate, nSpawnDistance, 1, true, Player.GetLocalCharacter(), false, true)` in `mrxcopterdrop.lua`). Trailing args appear to include booleans and an owner/player guid; exact meaning of each position beyond the first three is not confirmed by naming alone — treat only the template/distance/height positions as solid. |
| `SpawnRelative` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed to spawn relative to some anchor object by naming symmetry with `SpawnFromCamera`, but that is inference, not evidence. |
| `SpawnPlayer` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `SpawnPlayerAdvanced` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |

### Proximity Collection (FastCollect*)

| Function | Signature (best-known) | Notes |
|---|---|---|
| `FastCollectHumans` | `FastCollectHumans(x, y, z, fRadius, sFilter?)` | Widely used, e.g. `Pg.FastCollectHumans(x, y, z, 15, "Hero")`, `Pg.FastCollectHumans(x, y, z, 25, sFaction)` (`resident/friendlygate.lua`), `Pg.FastCollectHumans(x, y, z, 60, "Prisoner")`. Filter argument is a string, sometimes with `&&`/`\|\|` compound expressions (e.g. `"Allied && Human"`, `"OC && Human"`). Every call site found for this specific function includes the filter argument; the optional-filter pattern is confirmed for the family as a whole via `FastCollectGroundVehicles` and `FastCollectBuildings` below, not directly for this one. |
| `FastCollectGroundVehicles` | `FastCollectGroundVehicles(x, y, z, fRadius, sFilter?)` | Already noted elsewhere in this project as callable with or without a trailing filter argument; confirmed here with fresh call-site evidence: `Pg.FastCollectGroundVehicles(nSpawnX, nSpawnY, nSpawnZ, 200)` with no filter (`resident/autogunship.lua`), `Pg.FastCollectGroundVehicles(2113, -7, -1547, 250, "amx30")` with a string filter (`vz/gurcon002.lua`), and `Pg.FastCollectGroundVehicles(nSpawnX, nSpawnY, nSpawnZ, 200, oFilter)` with what appears to be a non-string filter object (`resident/mrxharmstrike.lua`). The filter argument's type is therefore not strictly a string in all cases — confirmed variable/optional. |
| `FastCollectBuildings` | `FastCollectBuildings(x, y, z, fRadius, sFilter?)` | Used as `Pg.FastCollectBuildings(x, y, z, 100, "Occupied")` (`resident/alarm.lua`, 3 call sites) and `Pg.FastCollectBuildings(nBombX, nBombY, nBombZ, nRadius)` with no filter (`resident/mrxbunkerbuster.lua`). Confirms the same optional-filter pattern. |
| `FastCollectFlying` | `FastCollectFlying(x, y, z, fRadius)` | Used as `Pg.FastCollectFlying(nSpawnX, nSpawnY, nSpawnZ, 200)` (`resident/mrxcombatairpatrol.lua`). No filter argument observed in the one call site found. |
| `FastCollectTanks` | `FastCollectTanks(x, y, z, fRadius)` | Used as `Pg.FastCollectTanks(nSpawnX, nSpawnY, nSpawnZ, 200)` (`resident/mrxtankbuster.lua`). No filter argument observed in the one call site found. |
| `FastCollectHelicopters` | `FastCollectHelicopters(x, y, z, fRadius)` | Used as `Pg.FastCollectHelicopters(x, y, z, 12)` (`resident/mrxutil.lua`). No filter argument observed. |
| `FastCollectBoats` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed same `(x, y, z, fRadius, sFilter?)` shape as the rest of the family by strong pattern consistency, but unconfirmed for this specific member. |
| `FastCollectCars` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `FastCollectJets` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `FastCollectProps` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `FastCollectUsables` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `FastCollectGroundVehiclesExceptTanks` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |

### Object Lookup by Name

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetGuidByName` | `GetGuidByName(sName)` | Extremely widely used (dozens of call sites across `vz/*.lua`), e.g. `Pg.GetGuidByName("China")`, `Pg.GetGuidByName("Civ_VIP_1")`, `Pg.GetGuidByName(sVeh)`. Resolves a level-designer-assigned name string to a GUID. See "Notes for modders" below for the bare-global-vs-namespaced finding. |
| `GetAllGuidsByName` | — | No call sites found under either `Pg.GetAllGuidsByName` or a bare `GetAllGuidsByName` anywhere in the decompiled corpus, despite being confirmed on both `Pg` and bare `_G` in live dumps (per prior live-testing notes referenced for this task). Presumed to return a table of every GUID sharing a given name (useful when multiple objects share one designer-assigned name), but that is inference from the name only — not evidence. |

### Pursuit/Wanted System

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetPursuitState` | `GetPursuitState()` | Used with no arguments: `local tCurrentPursuit = Pg.GetPursuitState()` (`resident/mrxfactionmanager.lua`). Returns some pursuit-state value/table. |
| `SetPursuit` | `SetPursuit(uFaction, nLevel, bFlag)` | Used as `Pg.SetPursuit(uFaction, nLevel, true)` (`resident/mrxfactionmanager.lua`). |
| `SetPursuitSeconds` | `SetPursuitSeconds(uFaction, nSeconds, bFlag)` | Used as `Pg.SetPursuitSeconds(uFaction, 5, true)` (`resident/mrxfactionmanager.lua`). |
| `SetPursuitLevelTimes` | `SetPursuitLevelTimes(nTime1, nTime2)` | Used as `Pg.SetPursuitLevelTimes(120, 300)` (`resident/mrxfactionmanager.lua`). |
| `LockPursuit` | `LockPursuit(uGuid, nLevel)` | Used as `Pg.LockPursuit(uGuid, nLevel)` (`resident/mrxfactionmanager.lua`). |
| `ClearPursuitLock` | `ClearPursuitLock(bFlag)` | Used as `Pg.ClearPursuitLock(true)` (`resident/mrxfactionmanager.lua`), and passed as a bare function reference with a table arg in `vz/pircon004.lua` (`{...}, Pg.ClearPursuitLock, {true}`), consistent with a single boolean argument. |
| `SetCustomPursuit` | `SetCustomPursuit(uFaction, nDuration, tSettings)` | Used as `Pg.SetCustomPursuit(uFaction, nDuration, tSettings)` (`resident/mrxfactionmanager.lua`); third argument is a table. |
| `ClearCustomPursuit` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed inverse of `SetCustomPursuit` by naming, unconfirmed. |
| `AdjustPursuitLevel` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `AdjustPursuitTimer` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `SetMaxPursuitLevel` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `SetMaxPursuitTime` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `RestrictAllPursuit` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `RestrictPursuitFaction` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `RestrictPursuitType` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `ClearPursuitRestrictions` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `TweakPursuitParam` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |

### Contracts & Achievements

| Function | Signature (best-known) | Notes |
|---|---|---|
| `ContractActivated` | `ContractActivated(sMissionName)` | Used as `Pg.ContractActivated(sMissionName)` (`resident/mrxtaskcontract.lua`). |
| `ContractCompleted` | `ContractCompleted()` | Used with no arguments: `Pg.ContractCompleted()` (`resident/mrxtaskcontract.lua`). |
| `ContractCancelled` | `ContractCancelled()` | Used with no arguments: `Pg.ContractCancelled()` (`resident/mrxtaskcontract.lua`). |
| `AchievementAddCount` | `AchievementAddCount(sAchievementName, nIndex, nDelta, nRequiredCount)` | Used as `Pg.AchievementAddCount(sAchievementName, i - 1, 1, tAchievement.nRequiredCount)` and with a variable delta (`resident/mrxachievements.lua`). |
| `AchievementIsGranted` | `AchievementIsGranted(sAchievementName, nIndex, nRequiredCount)` | Used as `bGranted = Pg.AchievementIsGranted(sAchievementName, i - 1, tAchievement.nRequiredCount)` (`resident/mrxachievements.lua`). |

### Asset & Layer Streaming

| Function | Signature (best-known) | Notes |
|---|---|---|
| `LoadAsset` | `LoadAsset(sAssetName, sAssetType, ...)` | Widely used, e.g. `Pg.LoadAsset("player_mattias_bare_technoviking", "animation")`, `Pg.LoadAsset("Mercs2Globals", "sounddb", MrxSoundCategories._DuckGlobalTable)` (`shell/mrxsoundbanks.lua`) — third argument sometimes present, sometimes omitted. |
| `UnloadAsset` | `UnloadAsset(sAssetName, sAssetType)` | Mirrors `LoadAsset`; e.g. `Pg.UnloadAsset("Mercs2Globals", "sounddb")` (`shell/mrxsoundbanks.lua`). |
| `ReloadAsset` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed to combine unload+load by naming, unconfirmed. |
| `AssetExists` | `AssetExists(sLayerName, sType)` | Used as `Pg.AssetExists(sLayerName, "layer")` (`resident/mrxlayermanager.lua`). |
| `LoadLayer` | `LoadLayer(sLayerName, bNotStatic, fCallback, tCallbackData, bClientNeedsLoadingScreen)` | Used as `Pg.LoadLayer(sLayerName, not bStatic, _LayerStatusChange, tLoadCallbackData, bClientNeedsLoadingScreen)` (`resident/mrxlayermanager.lua`); returns a success boolean. |
| `UnloadLayer` | `UnloadLayer(sLayerName, fCallback, tCallbackData, bClientNeedsLoadingScreen)` | Used as `Pg.UnloadLayer(sLayerName, _LayerStatusChange, tUnloadCallbackData, bClientNeedsLoadingScreen)` (`resident/mrxlayermanager.lua`). |
| `ReloadLayer` | `ReloadLayer(sLayerName, fCallback, tCallbackData, bClientNeedsLoadingScreen)` | Used as `Pg.ReloadLayer(sLayerName, _LayerStatusChange, tReloadCallbackData, bClientNeedsLoadingScreen)` (`resident/mrxlayermanager.lua`). |
| `IsStaticLayer` | `IsStaticLayer(sLayerName)` | Used as `Pg.IsStaticLayer(sLayerName)` (`resident/mrxlayermanager.lua`), guarding both add and remove requests. |
| `LoadingStaticLayers` | `LoadingStaticLayers(bFlag)` | Used as `Pg.LoadingStaticLayers(false)` / `Pg.LoadingStaticLayers(bOldStaticLayers)` (`resident/mrxtask.lua`) — appears to be a setter, distinct from `GetLoadingStaticLayers` below despite the similar name. |
| `GetLoadingStaticLayers` | `GetLoadingStaticLayers()` | Used with no arguments: `local bOldStaticLayers = Pg.GetLoadingStaticLayers()` (`resident/mrxtask.lua`) — the getter counterpart of `LoadingStaticLayers`. |
| `UnloadingStaticLayers` | `UnloadingStaticLayers(bFlag)` | Used as `Pg.UnloadingStaticLayers(false)` / `Pg.UnloadingStaticLayers(true)` ([`vz/xQ!L.lua`](../vz/xql)) — setter, mirrors `LoadingStaticLayers`. |
| `GetUnloadingStaticLayers` | `GetUnloadingStaticLayers()` | Used with no arguments: `if Pg.GetUnloadingStaticLayers() then ...` (`vz/xQ!L.lua`, `resident/mrxlayermanager.lua`) — getter counterpart. |
| `ResetSingletonDone` | `ResetSingletonDone()` | Used with no arguments: `Pg.ResetSingletonDone()` (`shell/shellbootstrap.lua`, `vz/xQ!L.lua`). |
| `SaveGame` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `LoadGame` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `LoadIsRetry` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `AddSkirmishTemplate` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `SetSkirmishTable` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `SetGlobalSkirmishState` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |

### World Queries & Misc

| Function | Signature (best-known) | Notes |
|---|---|---|
| `FindPointFromCamera` | `FindPointFromCamera(nForwardOffset, nHeightOrAltitude, nUnknown, uOwner?, nAngle?)` | Very widely used (dozens of call sites), consistently returning 3 values (`x, y, z`). Common shapes: `Pg.FindPointFromCamera(300, 100, -1, self.uOwner)` (`resident/mrxcombatairpatrol.lua`), with an optional trailing angle argument: `Pg.FindPointFromCamera(300, 200, -1, self.uOwner, nAngle)` (`resident/mrxclusterbomb.lua`). The third positional argument is consistently `-1` or a small number across observed sites; its meaning is not confirmed beyond "usually -1". |
| `GetObjectsInArea` | `GetObjectsInArea(x, y, z, fRadius, sFilterName)` | Used repeatedly with a string filter naming a specific object/template type, e.g. `Pg.GetObjectsInArea(x, y, z, 10, "Listening Post")` (`resident/oilcon002.lua`), `Pg.GetObjectsInArea(x, y, z, 1, "RumJug")` (`vz/pircon002.lua`), `Pg.GetObjectsInArea(x, y, z, 150, "Vehicle")` (`vz/wifpmcgarage.lua`). Filter argument appears mandatory in every observed call site (unlike the optional filter on `FastCollect*`). |
| `IsPointInBoundary` | `IsPointInBoundary(x, y, z, uBoundaryGuid)` | Used as `Pg.IsPointInBoundary(nX, nY, nZ, Pg.GetGuidByName("LR_TowerBase"))` (`vz/gurcon001.lua`). |
| `GetBoundaryRadius` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed getter counterpart of `SetBoundaryRadius`, unconfirmed. |
| `SetBoundaryRadius` | `SetBoundaryRadius(fRadius)` | Used as `Pg.SetBoundaryRadius(38.5)` (`resident/mrxcoop.lua`). |
| `GetWarningRadius` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `SetWarningRadius` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `GetTetherDiameterStart` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `GetTetherDiameterEnd` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `GetAllLandingZones` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `GetAwakeObjects` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `GetDistantSpawnPointOnPath` | `GetDistantSpawnPointOnPath(uPath, uBackupPointOrPrimaryPt, nSecondaryPt, fDist)` | Used as `res, x, y, z, yaw = Pg.GetDistantSpawnPointOnPath(uPath, uBackupPoint, 0, fDist)` (`vz/oilcon001.lua`) and `return Pg.GetDistantSpawnPointOnPath(iPathGuid, iPrimaryPt, iSecondaryPt, fRadius)` (`resident/mrxutil.lua`); returns a result flag plus `x, y, z, yaw`. |
| `GetLineRegionPoints` | `GetLineRegionPoints(uRegionGuid, bInvert?)` | Used as `local tX, tY = Pg.GetLineRegionPoints(tData.uGuid, tData.bInvert)` (`resident/mrxguihudradar.lua`) and `Pg.GetLineRegionPoints(uRegion, bInvert)` (`resident/mrxguipda.lua`); returns two tables (point arrays). |
| `AddContextAction` | `AddContextAction(uGuid, sLabelOrKey, nPriority?, ...more numeric/bool args)` | Very widely used with a highly variable tail: as few as 2 args (`Pg.AddContextAction(uGuid, "Dance", false)`, `resident/danceradio.lua`) up to 8 (`Pg.AddContextAction(uGuid, sActionLabel, 2, 0, 200, 0, 2, uCharacterGuid)`, `resident/mrxfollow.lua`). First two args (guid, label/localization-key string) are solid; everything after that varies by call site and is not confirmed as a fixed schema — likely priority/range/color/flags, but that is inference. Returns a success boolean in several call sites. |
| `RemoveContextAction` | `RemoveContextAction(uGuid)` | Very widely used, consistently with a single guid argument, mirroring `AddContextAction`. |
| `EnableRoad` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `EnableIntersection` | `EnableIntersection(bEnable, uGuid)` | Used as `Pg.EnableIntersection(false, StringToGuid("_maracaibo_bridge_segmentb 0x0008ab9c"))` (`vz/chicon002.lua`). |
| `Rumble` | `Rumble(uCharacterGuid, fLength)` | Used as `Pg.Rumble(self._hijacker, fRumbleLength)` and `Pg.Rumble(eCharGuid, 0.15555)` (`resident/mrxactionhijack.lua`). |
| `StartHeliWaveSpawner` | `StartHeliWaveSpawner(tParams)` | Used as `Pg.StartHeliWaveSpawner({...})` (`vz/pmccon003.lua`) — takes a single table of parameters, contents not enumerated here. |
| `StopHeliWaveSpawner` | `StopHeliWaveSpawner(oSelf)` | Used as `Pg.StopHeliWaveSpawner(self)` (`vz/pmccon003.lua`), and passed as a bare function reference elsewhere in the same file. |

## Notes for modders

The `FastCollect*` family (`FastCollectHumans`, `FastCollectGroundVehicles`, `FastCollectBuildings`, `FastCollectFlying`, `FastCollectTanks`, `FastCollectHelicopters`, plus the unconfirmed `Boats`/`Cars`/`Jets`/`Props`/`Usables`/`GroundVehiclesExceptTanks` variants) is the main building block used throughout the decompiled mission scripts for "find nearby objects of type X" logic — e.g. finding all soldiers of a faction near a point, all occupied buildings near a target, or all ground vehicles near a spawn point before filtering targets. The shared shape is `(x, y, z, fRadius, sFilter?)`, with the filter argument confirmed optional (multiple functions in the family have call sites both with and without it) and confirmed to sometimes be a non-string object rather than a plain string (see `FastCollectGroundVehicles` in `resident/mrxharmstrike.lua`, which passes `oFilter`). Anything building a "nearby objects" helper should model itself on this pattern; see also `resident/alarm.lua`, `resident/outpost.lua`, and `resident/mrxutil.lua` for real usage in context.

`GetGuidByName` — flagging the aliasing question directly: a live `pairs(_G)` scan (per prior work in this project) found `GetGuidByName` and `GetAllGuidsByName` present as bare loose globals on `_G`, in addition to being members of `Pg`. Grepping the decompiled corpus confirms both call forms exist for `GetGuidByName`: the namespaced `Pg.GetGuidByName(...)` is used in the large majority of call sites, but a substantial number of scripts (`vz/allcon001.lua`, `vz/chicon002.lua`, `vz/gurcon001.lua`, `vz/gurcon002.lua`, `vz/oilcon002.lua`, `vz/oilcon021.lua`, `vz/pmccon003.lua`, and others) call the bare, unqualified `GetGuidByName(...)` directly. The strongest evidence is in `vz/allcon001.lua` lines 77-81, where the same lookup (`GetGuidByName("China")`) and `Pg.GetGuidByName(...)` calls appear interleaved in adjacent statements within the same function, operating on equivalent name strings — strongly suggesting these are the same underlying function reachable at two scopes (i.e. `GetGuidByName` is aliased onto `_G` in addition to living on `Pg`), rather than two distinct implementations. This is inference from consistent call-site behavior, not confirmed by reading engine source (which isn't available) — but it is the most plausible reading of the evidence. `GetAllGuidsByName` by contrast has zero call sites under either form anywhere in the decompiled corpus, so nothing about its behavior can be confirmed beyond its existence in both live dumps.
