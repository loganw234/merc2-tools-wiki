---
title: WifPmcInterior
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 10
inherits: none
tags: [world-flow, pmc]
verified: false
---

# WifPmcInterior

## Overview
The PMC HQ job-board/menu system — the indoor space the player teleports into to see the four PMC-faction
starters, pick a contract, change outfits, and check owned support-item stock. Its four starters are
Fiona (`PmcBoss`, the main mission-giver, plus the hint and bribe systems), Ewan (`HelPmcBoss`, the transit
system), Eva (`MecPmcBoss`, the garage and custom-vehicle shop), and Misha (`JetPmcBoss`) — confirmed
directly from the VO cue name prefixes and `WifStarterData`'s own boolean feature flags for each. This
module owns the entire enter/exit transition (layer swap, hero teleport, loading screen, camera near/far
override), the four starters' presence/markers/idle chatter, the exterior-to-interior (and interior-room-
to-interior-room) portal network, the custom-outfit wardrobe, the ammo/support "stockpile" crate visuals,
and the PMC PDA map blip listing available jobs. At 2,115 lines and 89 top-level functions, this is one of
the largest single files in `src/vz/`.

This is also the one file in this batch that talks to [`wifmissiondata`](wifmissiondata) directly —
confirmed 9 call sites (`GetMissionStarter`, `GetMissionTitle`, `GetMissionFaction`, `GetMissionRepeatable`,
`GetMissionLevels`, `GetMissionIdFromIndex`, `IsMissionOnCriticalPath` ×2, `GetMissionIndexFromId`), all in
service of rendering the PDA job-list blip and the wager-mission follow-up flow.

## Inheritance
- Inherits from: none — confirmed, no `inherit()` call anywhere in the file
- Imports: [`MrxGui`](../resident/mrxgui), [`MrxCheatBootstrap`](../resident/mrxcheatbootstrap),
  [`MrxFactionManager`](../resident/mrxfactionmanager), [`MrxGuiBootstrap`](../resident/mrxguibootstrap),
  [`MrxLayerManager`](../resident/mrxlayermanager), [`MrxMultiPageMenu`](../resident/mrxmultipagemenu),
  [`MrxPlayer`](../resident/mrxplayer), [`MrxPlayState`](../resident/mrxplaystate),
  [`MrxPmc`](../resident/mrxpmc), [`MrxSound`](../resident/mrxsound),
  [`MrxStarterManager`](../resident/mrxstartermanager), [`MrxState`](../resident/mrxstate),
  [`MrxUtil`](../resident/mrxutil), `WifFreePlay`, [`wifmissiondata`](wifmissiondata), `WifMissionFlow`,
  `WifPmcGarage`, `WifVzBoundary`, [`MrxHq`](../resident/mrxhq), `WifBriefingData`,
  [`MrxTransit`](../resident/mrxtransit), [`MrxVoSequence`](../resident/mrxvosequence),
  [`MrxRewardData`](../resident/mrxrewarddata), [`MrxGuiInterface`](../resident/mrxguiinterface)

`WifVzBoundary` is imported but **never actually called anywhere in this file** (confirmed by direct
search) — a dead import; boundary/interior-mode transitions around PMC HQ are handled by
[`MrxHq`](../resident/mrxhq) instead.

## Instance pattern
**Singleton-state manager** — module-level state, no `tInstance[]` table, no `OnActivate`/`Create` per-
`uGuid` idiom. This is a third instance-pattern bucket distinct from both `resident/`'s "per-`uGuid` world
object" pattern and a fully stateless utility module: `Enter`/`Exit`/`IsUnlocked`/`SetEntranceLock`-style
functions all operate on one shared set of module-level fields for the entire game session. Key state:

- `_bUnlocked`, `_bInside`, `_bEntering`, `_bExiting` — the HQ's overall lock and enter/exit-in-progress
  flags.
- `_tStarters`: the four PMC starters' runtime binding data (`oStarter` object reference, `uStarter` guid,
  markers, chatter state, `bIntroduced`), keyed by starter id (`PmcBoss`/`HelPmcBoss`/`MecPmcBoss`/
  `JetPmcBoss`) — built from [`WifStarterData`](wifstarterdata)'s catalog but populated with live state
  here.
- `_tPortals`: a `uGuid`-keyed internal registry of active world<->interior portal markers/events.
  **Despite the `uGuid` keying, this is not the `Inheritable` per-object pattern** — it's an ordinary
  bookkeeping table inside this one singleton, with no metatable/prototype linkage and no `Create`/`Delete`
  idiom.
- `_tPortalData` / `_tInteriorPortalData`: static portal topology. `_tPortalData` has 4 entrance pairs
  (A-D), all routing to the same `sInteriorRoom = "MainHall"`. **`_tInteriorPortalData` is declared `{}`
  and never populated anywhere in this corpus** (confirmed by direct search) — the interior-room-to-room
  portal system (`_EnableInteriorPortals`/`_OnInteriorPortalEnter`) is fully wired but inert, consistent
  with all 4 exterior entrances leading to the same single interior room.
- `_tOutfits`, `_tStockpile`/`_tStockpileQty`: static per-hero outfit catalog and support-item display
  thresholds/current-known-quantities.
- `_tBuildings`/`_tBuildingStates`/`_tBuildingEvents`: tracks whether each of the 3 physical HQ buildings
  is currently alive or destroyed.
- `_sCurrentRoom`, `_nPortal`, `_bTeleport`, `_sCurrentStarterId`, `_sCurrentStarterChatter`,
  `_WardrobeOpen`, `_CostumeDialogBox`, and the `NETEVENT_*` constants used for custom net-event dispatch.

## Functions

Grouped by feature area (89 top-level functions total).

### Unlock state and wager tracking
`Unlock()` marks the HQ unlocked, refreshes the UI, unlocks `WifPmcGarage`, and revives
every HQ building. `IsUnlocked()` / `IsGarageAlive()` (checks building index 2's state) are simple
accessors. `SetEntranceLock(bSet)` toggles `_bEntranceLock`, which `RefreshUiDisplay` checks to hide the
PDA blip/portals entirely regardless of other state. `SetWagerStatus(sMissionId, bWin)` / `GetWagerStatus()`
record the outcome of a high-stakes "wager" mission: applies the wager amount
([`MrxRewardData`](../resident/mrxrewarddata)`.GetRewards(sMissionId).nWagered`) as a direct cash gain or
loss via [`MrxPmc`](../resident/mrxpmc)`.AddCashQty`, and flags `_bWagerMissionComplete` so the next
`_Kickoff` immediately re-opens that starter's briefing instead of leaving the player idle in the HQ.

### Entering the interior
`Enter(bTeleport, nPortal)` is the public entry point (server/host-only; a no-op on clients) — shows a
loading screen and calls `_OnEnter`, unless a debug skip-mode session is active, in which case it just
fires the teleport/unload callbacks immediately without an actual transition.
`_OnEnter(nPortal)` guards against double-entry, disables faction-reporting chatter, and (server only) sets
up the multiplayer-join watch before entering `MrxState.STATE_WAITFORGAME` to run `_CompleteOnEnter`.
`_CompleteOnEnter` resets a batch of load-tracking flags, calls `_SetupStarters` (binds each `_tStarters`
entry to its live [`MrxStarterManager`](../resident/mrxstartermanager) object), repositions the transit
suppression, revives the player, stops the freeplay nag and all sound, then kicks off `_LoadInterior` (adds
the interior layers, computed by `_GetStarterLayers` — the base `Vz_State_PmcInterior` layer plus each
active/absent starter's own layer) in parallel with a `dynamic_import("MrxBriefing", ...)`.
`_OnInteriorLoad` (the interior-layers callback) sets the interior atmosphere region, teleports the heroes
to the chosen portal's interior spawn points (or skips straight to `_LoadStarters` if this is a same-session
re-entry with `bTeleport = false`), enables the interior room's portals, and starts up the custom-outfit
wardrobe marker. `_LoadStarters` enables each starter, checks for the special `OilCon020`/`PmcCon031`
pre-recorded-greeting case, then loads every active starter's assets, converging on `_Kickoff(1)` once
they've all reported in (or immediately if none are active). `_BriefingModuleLoaded` (the
`dynamic_import` callback) associates every starter with the now-loaded briefing module and kicks off its
asset table preload, converging on `_Kickoff(2)`. `_Kickoff(nSignal)` is the rendezvous point for both
async paths (hero teleport = signal 1, briefing assets = signal 2) — once both have reported, it enables
portals, updates the stockpile, fires the registered load callback, and either exits
`STATE_WAITFORGAME` normally or, if a wager mission just completed, jumps straight into that starter's
briefing via `_StartStarter`. `_SetFakePDA(bSet)` fakes every player's PDA map position to sit at the real
(non-fake) PMC HQ's world coordinates while physically standing in the separate "HqInterior" cell, so the
map doesn't show the player somewhere nonsensical. `NetSafeGetSpecialCaseGreeting()` is a trivial
client-safe wrapper returning the hardcoded `"Fiona-Briefing-Contract-Oil020-13"` string.

### Exiting the interior
`Exit(nPortal, bForReload)` disables the interior portals and (server only) shows a loading screen and tears
down the multiplayer-join/quit/remote-player-awake event handles before entering
`STATE_WAITFORGAME` to run `_OnExit`. `_OnExit` disables portals/starters, restores normal transit,
removes the interior layers (`MrxLayerManager.Remove`), and — unless this is a save/level reload
(`bForReload`) — teleports the heroes either back to the chosen exterior portal, or (if any starter has a
pending contract) to that mission's own start locations via `WifMissionFlow.GetMissionStartLocations` plus
`_DoParkingLot`. It also tears down the outfit-change wardrobe and unloads the briefing module's assets.
`_ExitEnd(nSignal, bForReload)` is a three-way rendezvous (layers removed = signal 1, hero teleport complete
= signal 2, assets unloaded = signal 3) — it waits for signals 1 and 3 always, and additionally for signal
2 unless this is a reload. Once satisfied, it queues a 2-second delayed block that refreshes the UI, restarts
the freeplay nag, accepts any missions the starters queued up while the player was inside
(`WifMissionFlow.AcceptMissions`), and finally exits `STATE_WAITFORGAME` and fires the unload callback.
`_ExitComplete()` just re-animates the radar blip size for any HQ whose intro was viewed this session.

### PDA/HUD job-list blip
`RefreshUiDisplay()` is the real "recompute what to show" entry point: decides whether the PMC blip should
display at all (`_bEntranceLock` forces it off) and whether it should be "sticky" (any starter has a
critical-path briefing or unviewed intro, gated on freeplay), builds the full list of offered mission
indices across all starters, calls `AddPmcPdaBlip` plus a `Net.SendEvent_AddPmcPdaBlip` to replicate to
clients, and separately (de-duped against the last-known display/sticky state) adds or removes the actual
radar HUD objective. `GetMissionDesc(tMissions)` formats each mission's title, faction icon, and
(if repeatable) current level into the blip description text. `AddPmcPdaBlip(bSticky, tMissions)` builds
the full PDA blip, including a header line for whether the shop/transit systems are unlocked, and
critical-path missions sorted ahead of non-critical ones. `RemovePmcPdaBlip()` / `NetSafeRemovePmcPdaBlip()`
and `NetSafeAddPmcPdaBlip(bSticky, tMissions)` are the removal/net-safe-callable counterparts.

### Portal network
`_SetPortalMarker(uGuid, bEnable)` adds/removes a world-space blip + disc marker for one portal object
(texture differs for entrance vs. exit). `_AddPortal(uGuid, bExit, fCallback, tCallbackArgs)` registers a
context action ("Enter"/"Exit") and its marker once the object is awake (deferring via
`Event.ObjectHibernation` if it isn't yet); `_RemovePortal(uGuid)` tears the same down.
`_AddPortalAtHardpoint`/`_RemovePortalAtHardpoint` spawn or remove a portal actor at a named hardpoint
first. `_EnablePortals(bEnable, bExits)` walks all 4 `_tPortalData` entries, wiring either the exterior
entrances (-> `_OnEnter`) or interior exits (-> `Exit`). `_EnableInteriorPortals(bEnable)` /
`_OnInteriorPortalEnter(nPortal)` are the interior-room-to-room equivalent over `_tInteriorPortalData` —
currently inert since that table is always empty (see Instance pattern above).

### Starter presence, markers, and chatter
`_SetupStarters()` binds each `_tStarters` entry to its live `MrxStarterManager` object.
`_EnableStarters(bEnable)` calls `_EnableStarter`/`_DisableStarter` for all four. `_EnableStarter(sStarterId)`
finds the starter's current seat rider, sets it as the `oStarter`'s active actor, wires its "Talk" context
action (-> `MrxState.Enter(STATE_WAITFORGAME, _StartStarter, ...)`), and enables its marker and idle
chatter; `_DisableStarter` reverses all of it. `_SetStarterContextAction`/`_SetStarterMarker` are the
per-starter context-action and world-marker primitives (marker color/fade depends on whether the starter
currently has a critical-path briefing or unviewed intro). `_SetStarterChatter(sStarterId, bEnable)` arms
or disarms a proximity trigger (within 7m) that calls `_StarterChatter`, which plays a VO line via
[`MrxVoSequence`](../resident/mrxvosequence) and re-arms itself with a 20-second cooldown afterward.
`_StartStarter(sStarterId)` exits the starter from its seat, hides all markers/chatter, and calls the
starter object's own `:Start()`. `BriefingComplete(bDontResetStarters)` reverses that once a briefing ends,
re-seating the starter and re-enabling markers/chatter (or the "come back" nag specifically, if this is
the pre-`OilCon020` period). `IsInside()` / `IsEntering()` are simple flag accessors.
**`IsContractPending()` is dead code — see Notes below.** `GetStarterBriefingLocs(sStarterId)` returns a
starter's briefing camera locations. `_SetAllMarkers(bEnable)` / `_SetAllStarterChatter(bEnable)` are
all-starters-plus-all-portals / all-starters convenience wrappers. `_GetStarterChatterVo(sStarterId)` is
the large VO-selection table (custom-outfit lines, first-time "introducing a new starter" lines for Fiona,
and rotating greeting pools with extra conditional lines based on cash/mission-flag state).

### Load/unload/teleport callback registration
`SetLoadCallback(fCallback, tCallbackArgs)` / `SetUnloadCallback(...)` / `SetTeleportCallback(...)` are
one-shot callback slots — [`xQ!L`](xql) and other callers register a callback here before calling
`Enter`/`Exit`, and the module clears the slot (`SetLoadCallback(nil, nil)` etc.) immediately after firing
it. **Not a queue** — registering a second callback before the first fires overwrites it.

### Custom outfit system
`_SetCustomOutfitMarker(bEnable)` adds/removes the wardrobe object's context action and marker.
`_InitOutfitChange()`/`_DeinitOutfitChange()` set that up (and, server-side, watch for a remote player
leaving to re-init) whenever the "Custom Outfit Location" object exists in the level; `_ReinitOutfitChange`
re-does both if the wardrobe menu isn't currently open. `_SelectOutfit(uGuid)` opens the outfit-picker
[`MrxMultiPageMenu`](../resident/mrxmultipagemenu) (or, if the player has no unlocked alternate costumes
yet, a one-button tutorial dialog instead) for whichever hero interacted with the wardrobe.
`_CloseCostumeDialog()` tears that dialog down. `_ChangeOutfit`/`_CompleteChangeOutfit` apply the chosen
outfit's model, replicate it over the net, and play a "preening" VO line once the new model finishes
loading. `ChangeOutfit(uGuid, sOutfitName, ...)` is the public by-name entry point.
`GetAvailableCostumes()`/`SetAvailableCostumes(n)` track how many alternate costumes are unlocked so far.
`_GetPreeningVo(sCharacter, sOutfit)` is the per-hero, per-outfit VO line table.

### Stockpile (support-item crate) display
`_UpdateStockpile(bClientJoined)` reads current cash/support-item quantities from
[`MrxPmc`](../resident/mrxpmc), only ever increasing the displayed `_tStockpileQty` cache (never lowering
it visually), and batches the deltas out to clients 4-at-a-time via a custom net event.
`_SetStockpileCategoryQty(sCategoryName, nQty)` hides/disables physics on whichever physical crate props
in the HQ exceed the current quantity tier, once each prop wakes up. `_SendStockpileToClient(uGuid)` /
`_ClientUpdateStockpile(uGuid)` are the client-side join/sync counterparts.

### Save / load
`SaveSingleton()` persists `_bUnlocked`, `_tStockpileQty`, and which non-`PmcBoss` starters have already
been introduced (`tIntroduced`). `LoadSingleton(tSaveData)` re-unlocks the HQ if needed (also re-checking
`WifPmcGarage`'s Fiona-car state), restores stockpile quantities, and re-applies the
introduced-starter flags.

### Multiplayer client join / net events
`_OnPlayerJoined()` refreshes the stockpile for the new client, re-inits the outfit wardrobe, and disables
hero weapons momentarily. `NetSafeBriefingModuleLoaded`/`NetSafeLoadAssets1`/`NetSafeLoadAssets`/
`NetSafeUnloadAssets` are the client-side mirrors of the briefing-module load/unload path, callable safely
from net-replicated context. `NetEventCallback(nEventType, tArgs)` is the dispatcher for this module's 3
custom net events (`NETEVENT_UPDATESTOCKPILE`, `NETEVENT_CHANGEOUTFIT`, `NETEVENT_NOTIFYOUTFITCHANGE`),
sent via `Net.SendCustomEvent("WifPmcInterior", ...)`. `_ClientOnEnter()`/`_ClientExit()` are the
client-side visual-only equivalents of `_CompleteOnEnter`/parts of `_OnExit` (camera, fake-PDA, HQ
enter/exit — no layer loading, since layers replicate automatically).

### Fiona's "come back to PMC" nag
`_SetupPreOilCon020Nag(nDelay)` arms a one-shot timer (default 5s, re-armed at 30s afterward) that plays
one of Fiona's "at PMC" VO lines while the pre-`OilCon020` state is active; `_StopPreOilCon020Nag()`
cancels the timer and any in-progress VO; `_PreOilCon020Nag()` is the timer callback itself.

### HQ building destruction and resurrection
`_OnPmcDeath(nBuilding)` reacts to one of the 3 tracked HQ buildings dying: marks it dead, disables the
relevant system (portals for building 1, transit for building 2), and watches for it to go back to sleep
(`Event.ObjectHibernation`, `"s"`) before calling `_OnPmcHibernation`. `_OnPmcHibernation(nBuilding,
bInitialize)` marks it alive again, revives the object and re-enables the relevant system (unless this is
the initial boot call), and re-arms the death watch (`Event.ObjectDeath`) — a resurrect-when-hibernated
loop for HQ buildings that get blown up during play.

### Transit and wager parking lot
`_SetPmcTransitLocation(bEnable)` suppresses/restores transit location 1 via
[`MrxTransit`](../resident/mrxtransit)`.SuppressLocation` while the player is inside the HQ.
`_DoParkingLot(sMissionName)` fires the `"parkingLotStart"` event with either just `{false}` (if the
mission about to start is a wager, per [`MrxRewardData`](../resident/mrxrewarddata)`.GetWagerData`) or the
exterior entrance/parking-lot/heli-point guids otherwise — the camera sequence that plays as the player
walks out to their vehicle before a mission.

## Events
Confirmed by direct search of this file (15 registration call sites):
- `Event.ScriptEvent` — `"mpPlayerJoin"` (persistent, server-only, in `_OnEnter`) and `"mpPlayerLeft"`
  (persistent, server-only, in `_InitOutfitChange`).
- `Event.ContextAction` — 3 distinct registration sites: portal enter/exit prompts (`_AddPortal`'s
  internal `_Go`), the "Talk" prompt on each starter (`_EnableStarter`), and the wardrobe "change outfit"
  prompt (`_SetCustomOutfitMarker`).
- `Event.ObjectHibernation` — waiting for a portal object to wake (`_AddPortal`) and waiting for a
  destroyed HQ building to finish hibernating before resurrecting it (`_OnPmcDeath`).
- `Event.ObjectDeath` — re-arming the death watch on a resurrected HQ building (`_OnPmcHibernation`).
- `Event.ObjectProximity` — the 7m starter-idle-chatter trigger (`_SetStarterChatter`).
- `Event.ObjectIsReady` — waiting for a new outfit model to finish loading before playing the "preening" VO
  (`_CompleteChangeOutfit`).
- `Event.TimerRelative` — 4 distinct uses: the 2-second delayed post-exit cleanup (`_ExitEnd`), the
  20-second starter-chatter cooldown (`_StarterChatter`'s nested `_ChatterComplete`), the 2-second
  re-arm-chatter-after-briefing delay (`BriefingComplete`), and the configurable pre-`OilCon020` nag delay
  (`_SetupPreOilCon020Nag`).

Custom net events (`Net.SendCustomEvent("WifPmcInterior", ...)`, dispatched through `NetEventCallback`):
`NETEVENT_UPDATESTOCKPILE`, `NETEVENT_CHANGEOUTFIT`, `NETEVENT_NOTIFYOUTFITCHANGE`.

## Notes for modders
- **`IsContractPending()` is confirmed dead code with a real external caller.** Its body computes
  `bContractPending` across every starter but never `return`s it — the function always returns `nil`.
  `resident/mrxbriefing.lua:767` calls it as half of a boolean check:
  `_oStarter:IsPmcStarter() and WifPmcInterior.IsContractPending() or _oStarter:IsContractPending()` — since
  the first branch can never be true, that line always falls through to the per-starter
  `_oStarter:IsContractPending()` instead, for every starter including PMC ones. If you need this
  information from a mod, call the per-starter method directly rather than this module-level one.
- `SetLoadCallback`/`SetUnloadCallback`/`SetTeleportCallback` are single-slot, not a queue — if you hook one
  of these and something else (including this module's own internal flows) registers after you, your
  callback is silently overwritten before it fires.
- `WifVzBoundary` is imported here but never called — don't expect entering/exiting the PMC interior to
  touch world boundary state directly; that's handled by [`MrxHq`](../resident/mrxhq)'s own
  `SetInteriorMode` calls instead.
- The interior-room-to-room portal system (`_tInteriorPortalData`) is fully implemented but shipped with
  zero entries — every exterior entrance leads to the same `"MainHall"` interior room, so it's never been
  needed.
- Decompiler/source artifact: `_OnEnter` contains a literally duplicated condition,
  `if Net.IsServer() then if Net.IsServer() then Net.SetLoadingScreen(true) end end` — harmless, just
  redundant.
- 9 confirmed call sites here go straight to [`wifmissiondata`](wifmissiondata) for title/faction/level/
  critical-path lookups when building the PDA job list — if you're adding a custom mission that should show
  up on the PMC board, make sure it's registered wherever that module expects.
