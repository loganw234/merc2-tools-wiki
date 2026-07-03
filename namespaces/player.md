---
title: Player
parent: Engine Namespaces
nav_order: 5
---

# Player

## Overview

`Player` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it,
no `import()` call needed, and it's always globally available to every script. Its functions cover
player/character identity (which `uGuid` is "the player," in both single-player and co-op), co-op player
join/leave management, the cash and fuel economy (partly re-exposed at a higher level by the `resident/`
module `MrxPmc` — see cross-links below), camera and viewport control, mission boundaries, costumes and
vehicle disguise, the satellite-scan minigame, PDA map mode, and low-level input/control locking.

This is also the namespace behind the discovery that motivated this whole "Engine Namespaces" section —
see [Notes for modders](#notes-for-modders) and the [section index](index) for the full story.

## Provenance

This page's function list comes from a live `pairs(Player)` enumeration in-game, not from reading engine
source — the engine implementation isn't available to us. That means the list of 107 function names below
is complete and authoritative: every one of them really exists on the namespace. It does **not** mean
every entry is documented with confirmed arguments. Where a function is actually called somewhere in the
~230 decompiled `.lua` scripts, we can show a real argument pattern. Where it isn't called anywhere in that
corpus, we only know the name — arguments, return values, and behavior for those are unconfirmed and not
guessed beyond patterns established by confirmed sibling functions on this namespace.

## Functions

### Player & Character Identity

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetLocalPlayer` | `uPlayerGuid = Player.GetLocalPlayer()` | Extremely common in real scripts, no arguments, returns the local player-slot guid (distinct from the character guid). |
| `GetLocalCharacter` | `uGuid = Player.GetLocalCharacter()` | **Confirmed working by live testing** — see [Snippets](../snippets#get-your-current-position). Widely used in real scripts with no arguments. |
| `GetPrimaryPlayer` | `uPlayerGuid = Player.GetPrimaryPlayer()` | Very common in real scripts, no arguments, e.g. `Player.SetAimMode(Player.GetPrimaryPlayer(), true)`. |
| `GetSecondaryPlayer` | `uPlayerGuid = Player.GetSecondaryPlayer()` | Common in co-op-aware scripts, no arguments; call sites routinely guard it with `if Player.GetSecondaryPlayer() then` since it can be absent outside co-op. |
| `GetPrimaryCharacter` | `uGuid = Player.GetPrimaryCharacter()` | Already documented and used throughout this wiki — see [Snippets: Toggle infinite ammo](../snippets#toggle-infinite-ammo), [Sample Scripts: OnKey](../sample-scripts-onkey), and the [function-override deep dive](../deep-dives/function-override). No arguments. |
| `GetSecondaryCharacter` | `uGuid = Player.GetSecondaryCharacter()` | Already documented — see [Snippets: Toggle infinite ammo](../snippets#toggle-infinite-ammo) ("if you're in co-op and want to affect the second player too"). No arguments. |
| `GetAnyCharacter` | `uGuid = Player.GetAnyCharacter()` | Extremely common in mission/objective scripts as a target-filter value (e.g. passed as `vTgtInclude`), always called with no arguments. |
| `GetCharacter` | `uGuid = Player.GetCharacter(uPlayerGuid)` | Used with a player-slot guid in real scripts, e.g. `Player.GetCharacter(tData.uPlayerGuid)` — the character-guid counterpart to a raw player guid. |
| `GetPlayer` | `uPlayerGuid = Player.GetPlayer(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetPlayerId` | `Player.GetPlayerId(uPlayerGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetLocalId` | `Player.GetLocalId()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetLocalPlayerId` | `Player.GetLocalPlayerId()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetName` | `s = Player.GetName(uPlayerGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetAllPlayers` | `t = Player.GetAllPlayers()` | Used with no arguments in real scripts, e.g. `tPlayers = Player.GetAllPlayers()`; returns a table. |
| `GetAllCharacters` | `t = Player.GetAllCharacters()` | Used with no arguments in real scripts as a target-filter value, e.g. `Player.GetAllCharacters()` passed directly into a proximity/collect call. |
| `GetCurrentPlayers` | `n = Player.GetCurrentPlayers()` | Used with no arguments in real scripts, treated as a count/truthy multiplayer flag, e.g. `local isMultiplayer = Player.GetCurrentPlayers()`. |
| `GetCurrentLocalPlayers` | `Player.GetCurrentLocalPlayers()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed local-only counterpart to `GetCurrentPlayers`. |
| `GetMaximumPlayers` | `Player.GetMaximumPlayers()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetMaximumLocalPlayers` | `Player.GetMaximumLocalPlayers()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `IsJoined` | `b = Player.IsJoined(uPlayerGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `IsLocal` | `b = Player.IsLocal(uPlayerGuid)` | Used with a player guid in real scripts, e.g. `Net.IsServer() and not Player.IsLocal(tData[1])`. |
| `IsRemote` | `b = Player.IsRemote(uPlayerGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed inverse of `IsLocal`. |
| `IsCoopMultiplayer` | `b = Player.IsCoopMultiplayer()` | Used with no arguments in real scripts, e.g. `if Player.IsCoopMultiplayer() then`. |
| `CreatePlayer` | `Player.CreatePlayer(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `DestroyPlayer` | `Player.DestroyPlayer(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `AttachToCharacter` | `Player.AttachToCharacter(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `DetachFromCharacter` | `Player.DetachFromCharacter(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `BindToLocal` | `Player.BindToLocal(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `BindToRemote` | `Player.BindToRemote(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `Unbind` | `Player.Unbind(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetPlayerJoinedCallback` | `Player.SetPlayerJoinedCallback(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumably follows the same callback-registration shape as `Event.Create`, but that is inference, not evidence. |
| `SetPlayerLeftCallback` | `Player.SetPlayerLeftCallback(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `RemovePlayerJoinedCallback` | `Player.RemovePlayerJoinedCallback(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `RemovePlayerLeftCallback` | `Player.RemovePlayerLeftCallback(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetWaitForInGame` | `Player.SetWaitForInGame(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Cash & Fuel

These are largely covered elsewhere in this wiki already — see the cross-links instead of re-deriving.

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetCash` | `n = Player.GetCash()` | **Confirmed working by live testing** — see [Your First Mod](../first-mod) and [Snippets: Print debug info](../snippets#print-debug-info), both of which call it directly with no arguments. |
| `SetCash` | `Player.SetCash(nAmount)` | **Confirmed working by live testing**, but with a documented nuance — see [Snippets: Read / give cash](../snippets#read--give-cash): it genuinely changes the balance but skips the HUD refresh that `MrxPmc.AddCashQty` triggers, so the on-screen number won't visibly update. Prefer `MrxPmc.AddCashQty`/`GetCashQty` (a `resident/` wrapper — see [`MrxPmc`](../resident/mrxpmc) and [`MrxCheatBootstrap`](../resident/mrxcheatbootstrap)) unless you specifically want the silent low-level write. |
| `AddCash` | `Player.AddCash(nAmount)` | Same nuance as `SetCash` above — see [Snippets: Read / give cash](../snippets#read--give-cash). |
| `GetFuel` | `n = Player.GetFuel()` | Wrapped by `MrxPmc.GetFuelQty()` — see [`MrxPmc`](../resident/mrxpmc) ("a thin wrapper over `Player.GetFuel()`," confirmed working by live testing) and [Snippets: Read / give fuel](../snippets#read--give-fuel). |
| `SetFuel` | `Player.SetFuel(nAmount)` | Not directly exercised in the wiki's live tests, but is the presumed low-level setter behind `MrxPmc.AddFuelQty`/`SetFuelCapacity` — see [Snippets: Read / give fuel](../snippets#read--give-fuel) for the capacity-before-quantity ordering that matters when raising fuel. |
| `AddFuel` | `Player.AddFuel(nAmount)` | No direct call sites found in the decompiled corpus; presumed counterpart to `AddCash` by naming symmetry. Prefer `MrxPmc.AddFuelQty` (see [Snippets](../snippets#read--give-fuel)) for the same HUD-refresh reason noted under `SetCash` above — unconfirmed whether the same nuance applies here, but treat it as likely. |
| `GetFuelCapacity` | `n = Player.GetFuelCapacity()` | No direct call sites found in the decompiled corpus; presumed backing store for `MrxPmc.GetFuelCapacity()` — see [Snippets: Read / give fuel](../snippets#read--give-fuel). |
| `SetFuelCapacity` | `Player.SetFuelCapacity(nCapacity [, bFlag])` | No direct call sites found in the decompiled corpus; presumed backing store for `MrxPmc.SetFuelCapacity(nCapacity, bFlag)`, which real snippets call as `MrxPmc.SetFuelCapacity(9999, true)` — see [Snippets: Read / give fuel](../snippets#read--give-fuel). Argument shape here is inferred from that wrapper, not independently confirmed. |

### Camera & Viewport

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetCamera` | `uCameraGuid = Player.GetCamera(uPlayerGuid)` | Very common in real scripts, always a player guid, e.g. `Player.GetCamera(uPlayer)`; the returned guid is then passed into `Camera.*` calls (e.g. `Camera.GetYaw(Player.GetCamera(self:GetOwner()))`). |
| `GetCameraXZHeading` | `n = Player.GetCameraXZHeading(uPlayerGuid)` | Used with a player guid in real scripts, e.g. `Player.GetCameraXZHeading(oWidget:GetOwner())`, returns a heading/rotation value used to rotate HUD compass elements. |
| `TeleportCamera` | `Player.TeleportCamera(uPlayerGuid)` | Used with a plain player guid in real scripts, e.g. `Player.TeleportCamera(uSecondaryPlayer)`, snapping the camera to the player's current position (used around co-op transitions in `mrxutil.lua`). |
| `GetViewport` | `Player.GetViewport(uPlayerGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetViewportId` | `uViewportId = Player.GetViewportId(uPlayerGuid)` | Used with a player guid in real scripts, e.g. `Player.GetViewportId(uPlayerGuid)`, used to bind GUI widgets to the correct split-screen viewport. |

### Boundaries

A mission/region boundary system: a player can have one or more boundary zones registered, with a
callback fired on crossing and an optional "death outside boundary" mode.

| Function | Signature (best-known) | Notes |
|---|---|---|
| `AddBoundary` | `Player.AddBoundary(uPlayerGuid, uBoundaryGuid)` | Confirmed with a player guid and a boundary-object guid in real scripts, e.g. `Player.AddBoundary(uPlayerGuid, uBoundary)` (`wifvzboundary.lua`). |
| `RemoveBoundary` | `Player.RemoveBoundary(uPlayerGuid, uBoundaryGuid)` | Confirmed with the same two-guid shape as `AddBoundary`, e.g. `Player.RemoveBoundary(uPlayerGuid, uBoundary)`. |
| `RemoveAllBoundary` | `Player.RemoveAllBoundary(uPlayerGuid)` | Confirmed with a plain player guid in real scripts, e.g. `Player.RemoveAllBoundary(uPlayerGuid)`. |
| `GetAllBoundaryGuid` | `t = Player.GetAllBoundaryGuid(uPlayerGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetBoundaryCallback` | `Player.SetBoundaryCallback(uPlayerGuid, fCallback)` | Confirmed in real scripts, e.g. `Player.SetBoundaryCallback(uPlayerGuid, BoundaryCallback)`. |
| `SetOutBoundary` | `Player.SetOutBoundary(uPlayerGuid, bState)` | Confirmed with a player guid and boolean in real scripts, e.g. `Player.SetOutBoundary(secondaryPlayer, true)` / `Player.SetOutBoundary(uPlayerGuid, false)`. |
| `GetOutBoundary` | `Player.GetOutBoundary(uPlayerGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed getter counterpart to `SetOutBoundary`. |
| `IsPositionOutBoundary` | `b = Player.IsPositionOutBoundary(uPlayerGuid, nX, nY, nZ)` | Confirmed with a player guid and three coordinates in real scripts, e.g. `Player.IsPositionOutBoundary(Player.GetLocalPlayer(), nX * 0.5 - nXOffset, 0, nY * 0.5 - nZOffset)` (PDA map code). |
| `IsBoundaryDeath` | `b = Player.IsBoundaryDeath(uCharacterGuid)` | Confirmed with a character guid in real scripts, e.g. `Player.IsBoundaryDeath(uChar)`, used to decide whether being outside a boundary should be lethal. |

### Costumes & Disguise

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetAvailableCostumes` | `n = Player.GetAvailableCostumes()` | Confirmed with no arguments in real scripts, e.g. `nAvailableOutfits = Player.GetAvailableCostumes()` (`wifpmcinterior.lua`). Distinct from the similarly-named `WifPmcInterior.GetAvailableCostumes()` covered in the [function-override deep dive](../deep-dives/function-override) — that one is a `resident/`-module function with its own small `_nAvailableCostumes or 1` fallback logic; this is the underlying engine-level count it likely reads from or writes through, but the exact relationship between the two is not confirmed. |
| `SetAvailableCostumes` | `Player.SetAvailableCostumes(n)` | Confirmed in real scripts, e.g. `Player.SetAvailableCostumes(WifPmcInterior.GetAvailableCostumes())` — note this call site reads from the `resident/`-module getter and writes into this engine setter, suggesting they're kept in sync rather than being the same storage. |
| `GetProfileCostume` | `n = Player.GetProfileCostume()` | Confirmed with no arguments in real scripts, e.g. `local nCurrentOutfit = Player.GetProfileCostume()` and `tCharacterConfig.iCostume = Player.GetProfileCostume()`. |
| `SetProfileCostume` | `Player.SetProfileCostume(iIndex)` | Confirmed in real scripts, e.g. `Player.SetProfileCostume(iIndex - 1)` (note the zero-based adjustment at the call site). |
| `SetOutfit` | `Player.SetOutfit(uGuid, sModelName)` | Confirmed with a character guid and a model-name string in real scripts, e.g. `Player.SetOutfit(uGuid, sModelName)` (`wifpmcinterior.lua`, wardrobe code — same area covered by the [function-override deep dive](../deep-dives/function-override)). |
| `GetProfileCharacter` | `Player.GetProfileCharacter()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetProfileCharacter` | `Player.SetProfileCharacter(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetProfileUpgrade` | `Player.GetProfileUpgrade(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetProfileUpgrade` | `Player.SetProfileUpgrade(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetVehicleDisguise` | `b = Player.GetVehicleDisguise()` | Confirmed with no arguments in real scripts, e.g. `if not Player.GetVehicleDisguise() then` and repeated `tData.oIcon:SetVisible(Player.GetVehicleDisguise())` HUD calls — treated as a boolean state flag. |
| `SetVehicleDisguise` | `Player.SetVehicleDisguise(bEnable)` | Confirmed with a single boolean in real scripts, e.g. `Player.SetVehicleDisguise(bEnable)` (`mrxmissionflow.lua`). |
| `GetVehicleDisguiseState` | `b = Player.GetVehicleDisguiseState({Player = uGuid})` | Confirmed in real scripts called with a **table argument** containing a `Player` field, e.g. `Player.GetVehicleDisguiseState({Player = uRider})` and `Player.GetVehicleDisguiseState({...})` in `wiftutorialgatehonk.lua` — unusual among `Player.*` functions for taking a table instead of positional args; this shape is real, not inferred. |
| `VehicleDisguise` | `Player.VehicleDisguise({Player = uGuid, Callback = fCallback})` or `Player.VehicleDisguise({Player = uGuid, Remove = true})` | Confirmed in real scripts with the same table-argument convention as `GetVehicleDisguiseState`, e.g. `Player.VehicleDisguise({Player = uRider, Callback = DisguiseChangedCallback})` to start a disguise change and `Player.VehicleDisguise({Player = uRider, Remove = true})` to remove it. |

### Satellite Scan

A radar/scan minigame feature family, driven from `mrxsupportdesignatorsatellite.lua`,
`mrxguisatellite.lua`, and `mrxutil.lua`. See also the PDA Map Mode table below — the two systems are used
together (satellite scanning happens while the PDA is in map mode).

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetSatelliteScanMode` | `Player.SetSatelliteScanMode(uPlayerGuid, bEnable, nX, nY, nZ)` | Confirmed in real scripts with exactly this shape, e.g. `Player.SetSatelliteScanMode(uPlayer, false, 0, 0, 0)` (`mrxutil.lua`) — only the disable form (`bEnable = false`, zeroed coordinates) is attested; the enable form's coordinate meaning is not confirmed. |
| `SetupSatelliteScan` | `Player.SetupSatelliteScan(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `AddSatelliteScanTarget` | `Player.AddSatelliteScanTarget(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetSatelliteScanCallbacks` | `Player.SetSatelliteScanCallbacks(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetSatelliteScanPaused` | `Player.SetSatelliteScanPaused(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### PDA Map Mode

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetPDAMapMode` | `Player.SetPDAMapMode(uPlayerGuid, bEnable, nX, nY, nZ, nRadius, nMinZoomDelta, nMaxZoomDelta, bUseMinigame)` | Confirmed with a long argument list in real scripts, e.g. `Player.SetPDAMapMode(self.uOwner, true, nX, nY + self.nStartZoom, nZ, self.nRadius, self.nStartZoom - self.nMinZoom, self.nMaxZoom - self.nStartZoom, MrxGuiSatellite.UseMinigame())`; also called with just `(uGuid, false)` to disable. |
| `SetPDAMapModeCallback` | `Player.SetPDAMapModeCallback(uPlayerGuid, bFlag, fCallback [, tArgs])` | Confirmed in real scripts, e.g. `Player.SetPDAMapModeCallback(self.uOwner, true, SatelliteTargettingEnd, {self})` and `Player.SetPDAMapModeCallback(uPlayerGuid, false, ApplySatelliteUpdateEvent)`. |
| `SetPDAMapModeCancelCallback` | `Player.SetPDAMapModeCancelCallback(uPlayerGuid, fCallback)` | Confirmed in real scripts, e.g. `Player.SetPDAMapModeCancelCallback(self.uOwner, SatelliteTargettingCancel, {self})`. |
| `RequestPDAMapModeCancel` | `Player.RequestPDAMapModeCancel(uPlayerGuid)` | Confirmed with a plain player guid in real scripts, e.g. `Player.RequestPDAMapModeCancel(uPlayer)`. |
| `RequestPDAMapModeExit` | `Player.RequestPDAMapModeExit(uPlayerGuid, fCallback [, tArgs])` | Confirmed in real scripts, e.g. `Player.RequestPDAMapModeExit(oMinigame:GetOwner(), _RemoveSatelliteTargettingMode, {oMinigame})`. |

### Input & Control

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetInputEnabled` | `Player.SetInputEnabled(uPlayerGuid, bEnable [, bFlag])` | Confirmed in real scripts both with a plain 2-argument form (`Player.SetInputEnabled(uPlayer, false)`) and a 3-argument form with a trailing boolean (`Player.SetInputEnabled(Object.IsPlayerControlled(uActioner), false, true)`) — the meaning of the 3rd argument is unconfirmed. |
| `SetAimMode` | `Player.SetAimMode(uPlayerGuid, bEnable)` | Confirmed with a player guid and boolean in real scripts, very common, e.g. `Player.SetAimMode(Player.GetPrimaryPlayer(), true)`. |
| `SetGrappleEnabled` | `Player.SetGrappleEnabled(uGuid, bEnable)` | Confirmed in real scripts, e.g. `Player.SetGrappleEnabled(uGuid, bEnable)` (`mrxmissionflow.lua`). |
| `SetScopeEnabled` | `Player.SetScopeEnabled(uPlayerGuid, bEnable)` | Confirmed in real scripts, e.g. `Player.SetScopeEnabled(Player.GetLocalPlayer(), false)`. |
| `SetHealthClamp` | `Player.SetHealthClamp(uPlayerGuid, bEnable)` | Confirmed in real scripts, e.g. `Player.SetHealthClamp(uPlayer, true)` (paired with `SetSurvivalMode` in `hero.lua`). |
| `SetVehicleControlsLock` | `Player.SetVehicleControlsLock(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetSeatMovementLocks` | `Player.SetSeatMovementLocks(uPlayerGuid, bEnable)` | Confirmed with a player guid and boolean in real scripts, e.g. `Player.SetSeatMovementLocks(uPlayerGuid, true)` / `(uPlayerGuid, false)`. |
| `GetControlBindingType` | `s = Player.GetControlBindingType(uPlayerGuid)` | Confirmed with a player guid in real scripts, e.g. `local sControlType = Player.GetControlBindingType(uPlayerGuid)` (pause-screen control-scheme display). |
| `SetInPmc` | `Player.SetInPmc(uPlayerGuid, bEnable)` | Confirmed with a player guid and boolean in real scripts, e.g. `Player.SetInPmc(uPlayer, true)` / `(uPlayer, false)` (`wifpmcinterior.lua` — entering/leaving the PMC hub). |
| `SetSurvivalMode` | `Player.SetSurvivalMode(uPlayerGuid, bEnable)` | Confirmed with a player guid and boolean in real scripts, e.g. `Player.SetSurvivalMode(uPlayer, true)` (paired with `SetHealthClamp` in `hero.lua`). |
| `SetSurvivalModeCallback` | `Player.SetSurvivalModeCallback(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetSwimmingSearchRadius` | `Player.SetSwimmingSearchRadius(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `InCinematicMode` | `b = Player.InCinematicMode(uPlayerGuid)` | Confirmed with a player guid in real scripts, e.g. `if not Object.IsAlive(uChar) or Player.InCinematicMode(uPlayerGuid) then`. |
| `SetCinematicMode` | `Player.SetCinematicMode(uPlayerGuid, bEnable [, ...extra args])` | Confirmed in real scripts with a 2-argument form (`Player.SetCinematicMode(uPlayer, false)`) and richer forms, e.g. `Player.SetCinematicMode(uPlayer, true, true)` and `Player.SetCinematicMode(uPlayer, not bOn, "Bone_Attach_Root", 0, true)` — the extra trailing arguments vary by call site and their exact meaning is unconfirmed beyond "camera/cinematic attach parameters." |

### Vehicle Seat & Control

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetControlledObject` | `uGuid = Player.GetControlledObject(uPlayerGuid)` | Extremely common in real scripts, always a player guid, e.g. `Player.GetControlledObject(uPlayer)`; returns the character or vehicle the player currently controls. |
| `GetSeat` | `Player.GetSeat(uPlayerGuid)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Compare with `Vehicle.GetSeatFromRider`/`Vehicle.GetFromRider` on the [Vehicle](vehicle) page, which cover similar ground from the vehicle side with real call sites. |
| `ClaimSeat` | `Player.ClaimSeat(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `UnClaimSeat` | `Player.UnClaimSeat(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |

### Misc

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetTargetUnderReticle` | `nX, nY, nZ, uGuid = Player.GetTargetUnderReticle(uPlayerGuid)` | See [Notes for modders](#notes-for-modders) below — this is the flagship reason this whole "Engine Namespaces" section exists. Confirmed with real call sites (contrary to the section index's original framing that it had zero callers — see below): used in `mrxguisatellite.lua` and `mrxguisniperscope.lua` as `local nX, nY, nZ, uGuid = Player.GetTargetUnderReticle(oWidget:GetOwner())`, returning world coordinates of whatever's under the reticle plus (as a 4th return value) the target's `uGuid`, which can be `nil` if nothing is targeted. |
| `GetPlayerStart` | `v = Player.GetPlayerStart()` | Confirmed with no arguments in real scripts, e.g. `local vSpawnLocation = Player.GetPlayerStart()`, and compared directly to a string constant in `xQ!L.lua` (`Player.GetPlayerStart() ~= "PlayerLocation_Start"`) — suggesting the return value can be a named-location string as well as a position, unconfirmed which form is canonical. |
| `SetPlayerStart` | `Player.SetPlayerStart(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed setter counterpart to `GetPlayerStart`. |
| `GetRetryPosition` | `Player.GetRetryPosition(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `CheckSpawnPos` | `Player.CheckSpawnPos(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `ClearPlayerDB` | `Player.ClearPlayerDB()` | Confirmed with no arguments in real scripts, e.g. `Player.ClearPlayerDB()` (`mrxplayer.lua`). |
| `ClearGPS` | `Player.ClearGPS(uPlayerGuid)` | Confirmed with a player guid in real scripts, e.g. `Player.ClearGPS(Player.GetLocalPlayer())`. |
| `GetAllTargetMarkerPos` | `t = Player.GetAllTargetMarkerPos()` | Confirmed with no arguments in real scripts, e.g. `local tAllMarkerList = Player.GetAllTargetMarkerPos()` (`mrxguipda.lua`), returns a table. |

## Notes for modders

- **`GetTargetUnderReticle` is why this "Engine Namespaces" section exists at all** — see the
  [section index](index) for the origin story: a static grep for "what is the player aiming at" across
  every plausible function name in the entire ~230-file decompiled corpus came back completely empty, and
  live `pairs(Player)` enumeration turned this function up on the first try. While writing this page,
  further grepping actually *did* turn up real call sites for it (in `mrxguisatellite.lua` and
  `mrxguisniperscope.lua`, both under `oWidget:GetOwner()` / `oMinigame:GetOwner()` argument forms) — so
  the original "zero call sites anywhere" claim doesn't hold in its strongest form, but the broader point
  stands: nobody found it by guessing plausible names, only by enumerating the namespace live. The
  confirmed shape is `nX, nY, nZ, uGuid = Player.GetTargetUnderReticle(uPlayerGuid)`.
- **Proposed live test**, following the pattern of other simple no-arg-style `Player.*` getters
  (`GetPrimaryCharacter()`, `GetLocalCharacter()`): first try
  `Loader.Printf(tostring(Player.GetTargetUnderReticle()))` from the console with no arguments at all. Real
  call sites always pass a player-guid-like first argument (an `oWidget:GetOwner()` result), so if the
  no-arg form errors, fall back to
  `Loader.Printf(tostring(Player.GetTargetUnderReticle(Player.GetLocalPlayer())))`. Aim the reticle at
  something identifiable first (a vehicle, an NPC) and confirm the 4th return value is a real `uGuid` you
  can feed into `Object.GetHealth`/`Object.GetLocalizedName` to verify it's actually the thing you were
  looking at.
- Cash and fuel: use `MrxPmc.AddCashQty`/`MrxPmc.AddFuelQty` (see [Snippets](../snippets#read--give-cash),
  [`MrxPmc`](../resident/mrxpmc), [`MrxCheatBootstrap`](../resident/mrxcheatbootstrap)) rather than the raw
  `Player.SetCash`/`Player.AddCash`/`Player.SetFuel`/`Player.AddFuel` setters documented above, unless you
  specifically want a change that skips the HUD refresh — that HUD-skip nuance is already confirmed by live
  testing and documented on the Snippets page; this page doesn't re-derive it.
- `GetVehicleDisguiseState` and `VehicleDisguise` are the only two functions on this namespace confirmed to
  take a **table argument** (`{Player = uGuid, ...}`) instead of positional arguments — don't assume every
  `Player.*` function follows the plain-positional convention seen everywhere else on this page.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Player)` dump) but their
  argument shape is a guess based on naming convention and sibling functions only — don't build mods around
  them without testing in-game first, especially `GetSeat`/`ClaimSeat`/`UnClaimSeat`, which have zero
  attested usage anywhere in the corpus despite sounding straightforward.
