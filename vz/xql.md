---
title: xQ!L
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 17
inherits: none
tags: [world-flow, boot]
verified: false
---

# xQ!L

## Overview
The game's boot-time streaming/save-load conductor — the single module that decides what a new session
actually boots into (a fresh campaign start, a loaded save, a checkpoint retry, or a debug mission-skip),
drives the whole level-streaming handshake from "nothing loaded" to "player has control," and owns the
master save-data table that every other persisted subsystem's own `SaveSingleton`/`LoadSingleton` feeds
into. Nearly every other module in `src/vz/` that persists anything at all is ultimately called *from*
this one file, not the other way around.

**The filename is presumably a decompiler/original-hashed-name artifact** — `xQ!L.lua` doesn't read as a
human-authored name the way every other file in this corpus does, and nothing inside the file itself
suggests what it "should" be called. This page treats `xQ!L` as the module's real, working name rather than
speculating about an intended one, consistent with how it's already cited (by this same name) in
`resident/mrxlayermanager.md`, `deep-dives/world-inspector.md`, `deep-dives/world-state-init.md`, and
several `namespaces/*.md` pages written before this page existed.

## Inheritance
- Inherits from: none — confirmed, no `inherit()` call anywhere in the file
- Imports (34): [`friendlygate`](../resident/friendlygate), [`Munitions`](../resident/munitions),
  [`MrxAchievements`](../resident/mrxachievements), [`MrxBootstrap`](../resident/mrxbootstrap),
  [`MrxCheatBootstrap`](../resident/mrxcheatbootstrap), [`MrxSoundBootstrap`](../resident/mrxsoundbootstrap),
  [`MrxFactionManager`](../resident/mrxfactionmanager), [`MrxLayerManager`](../resident/mrxlayermanager),
  [`MrxStarterManager`](../resident/mrxstartermanager), [`MrxPlayer`](../resident/mrxplayer),
  [`MrxPlayState`](../resident/mrxplaystate), [`MrxPmc`](../resident/mrxpmc),
  [`MrxTransit`](../resident/mrxtransit), [`MrxTutorialManager`](../resident/mrxtutorialmanager),
  [`MrxStatsManager`](../resident/mrxstatsmanager), [`MrxSupportData`](../resident/mrxsupportdata),
  [`MrxRewardData`](../resident/mrxrewarddata), [`MrxState`](../resident/mrxstate),
  [`MrxTask`](../resident/mrxtask), `WifHints`, `WifBios`, `WifMissionFlow`,
  [`WifPmcInterior`](wifpmcinterior), [`WifVzAmbience`](wifvzambience), [`WifVzAtmosphere`](wifvzatmosphere),
  [`WifVzRegionNames`](wifvzregionnames) (imported here as `WifVZRegionNames` — see casing note below),
  [`WifVzBoundary`](wifvzboundary), `StagingAct1`, [`Hero`](../resident/hero), [`MrxGui`](../resident/mrxgui),
  [`MrxUtil`](../resident/mrxutil), [`MrxVoSequence`](../resident/mrxvosequence),
  [`MrxShootingGallery`](../resident/mrxshootinggallery), [`MrxShop`](../resident/mrxshop),
  `WifEquipmentData`

## Instance pattern
**Singleton-state manager** — the same third bucket as [`WifPmcInterior`](wifpmcinterior): module-level
boot-state fields, no `tInstance[]`, no per-`uGuid` object pattern. Key fields, mostly reset together in
`Init()`:
- `_bBootstrapComplete` / `_bStaticLayersLoaded` / `_bDynamicLayersLoaded` / `_bInitialStreamComplete`:
  the four async "are we ready to proceed" flags `_AttemptGameplaySetup` waits on.
- `_bNewSession`, `_bAltSpawnLocation`, `_bLoadIntoWorld`, `_bPmcRequired`, `_bSkipToBriefing`: which of
  several possible boot paths this session is taking.
- `_sSkipToMissionName`: a debug/cheat mission id to jump straight into, if set.
- `_tSaveState`: the deserialized save-data table for this load, consumed piecemeal across several
  functions and cleared once fully applied.
- `_tTeleportLocations`: hero spawn points to teleport to once the world is ready (as opposed to
  `MrxPlayer.SetSpawnLocations`, used when heroes don't exist as objects yet).
- `_tPreContractSaveData`: a snapshot of `GenerateSaveData()` taken immediately before a contract starts
  (see `SetPreContractSaveData`).
- `_oMasterStub`: the native mission-tree root object (`MrxTask:Create()`), re-created on every gameplay
  setup and handed to `WifMissionFlow`/`MrxCheatBootstrap`.
- `_fUnloadLayersCallback` / `_tUnloadLayersCallbackData`: a deferred `LoadSingleton` call, parked here if
  it arrives while a `ResetSingleton` teardown is still unloading static layers.
- `nInGameCash`: a scratch value used only by the client-side pre-save cash display trick.
- `_nOldCash` / `_nOldFuel`: read and cleared by `SaveComplete()`, but **never assigned anywhere in this
  file, or anywhere else in this corpus** (confirmed by corpus-wide search) — either some native,
  non-Lua part of the save flow sets them before calling `SaveComplete`, or this cleanup path is currently
  unreachable from any Lua call site.

Also holds the two literal boot-time layer manifests as module-level data:
`_tStaticLayers` (170 entries) and `_tDefaultDynamicLayers` (246 entries) — see
[`MrxLayerManager`'s boot-time layer manifest section](../resident/mrxlayermanager#boot-time-layer-manifest-vz-xq-l-lua)
for the full lists and what they mean; this page focuses on how and when they get loaded.

## Functions

### Boot and save-data assembly

**`Init()`** is the true entry point, presumably called once when a session first spins up. Resets every
boot-state flag, resets [`MrxLayerManager`](../resident/mrxlayermanager) and
[`MrxVoSequence`](../resident/mrxvosequence), tells [`MrxBootstrap`](../resident/mrxbootstrap) not to
auto-handle state transitions and to call `_AttemptGameplaySetup({"boot"})` once its own native bootstrap
work finishes, resets [`MrxPlayer`](../resident/mrxplayer) (server/non-MP only), disables state-fade, and
attempts `Pg.LoadGame("InitialSaveData")`. If no save is found, it calls `LoadSingleton(nil)` itself
(fresh-game path) — if a save *is* found, this file's own `LoadSingleton` is presumably invoked by the save
system through the same naming convention every other subsystem here uses, though the exact native hook
isn't visible from this file alone.

**`SaveSingleton()`** is the actual top-level function the save system calls to serialize the entire game.
It stashes [`WifPmcInterior`](wifpmcinterior)'s available-costume count onto the player profile, then
returns `GenerateSaveData()`.

**`GenerateSaveData()`** assembles the master save table by calling `SaveSingleton()` on roughly 20
subsystems in sequence: [`MrxPmc`](../resident/mrxpmc), [`WifPmcInterior`](wifpmcinterior),
[`MrxTransit`](../resident/mrxtransit), [`MrxSupportData`](../resident/mrxsupportdata),
[`MrxRewardData`](../resident/mrxrewarddata), [`MrxFactionManager`](../resident/mrxfactionmanager),
[`MrxLayerManager`](../resident/mrxlayermanager), [`MrxStarterManager`](../resident/mrxstartermanager),
`WifMissionFlow`, [`MrxPlayer`](../resident/mrxplayer), [`WifVzBoundary`](wifvzboundary), `WifHints`,
`WifBios`, [`Munitions`](../resident/munitions), [`MrxTutorialManager`](../resident/mrxtutorialmanager),
[`MrxStatsManager`](../resident/mrxstatsmanager), [`MrxShop`](../resident/mrxshop), `WifEquipmentData`,
[`MrxAchievements`](../resident/mrxachievements), and [`friendlygate`](../resident/friendlygate) — plus a
handful of directly-computed scalar fields (last completed mission name, elapsed play time, grapple/
vehicle-disguise/resource-counter toggle states, available costume count) and the player's currently
equipped support item (`Pda.Support:ReadEquippedSupport`). Retry locations
(`WifMissionFlow.GetRetryLocations()`) are folded in afterward, only if present. This is the single
authoritative list of what a Mercenaries 2 save file actually contains from the Lua side.

**`SetPreContractSaveData()`** snapshots a fresh `GenerateSaveData()` call (deep-copied via
`MrxUtil.CopyTable`) into `_tPreContractSaveData`. Registered with
`WifMissionFlow.SetPreContractSaveFunction(SetPreContractSaveData)` inside
`_GameplaySetup_LoadWorldState` (below) — i.e. `WifMissionFlow` calls this itself right
before a contract begins, presumably to have a known-good rollback point available.

**`ClientReimburseForSave()`** / **`ClientRestorePreSaveCash()`** are a client-only display trick: before a
save, the client temporarily shows its cash combined with `MrxPmc.GetClientReimburseAmount()`, then restores
the real value once the pause menu closes (`Event.GameStateChange`, `{"Pause", "exit"}`).

**`SaveComplete()`** restores `_nOldCash`/`_nOldFuel` if they were set (see the caveat under Instance
pattern above).

**`RequestAutosave()`** is a one-line wrapper over `Pg.SaveGame("autosave")`.

**`ResetSingleton(fCallback, tCallbackArgs)`** is the full world-teardown routine — used both for returning
to the main menu and for transitioning into a freshly-skipped mission. It resets
[`MrxFactionManager`](../resident/mrxfactionmanager), suppresses the Pda, force-ejects every player from any
vehicle seat, reimburses client cash if applicable, resets
[`MrxState`](../resident/mrxstate)/[`MrxPlayState`](../resident/mrxplaystate)/
[`MrxVoSequence`](../resident/mrxvosequence)/`WifMissionFlow`/[`MrxShootingGallery`](../resident/mrxshootinggallery),
exits [`MrxSoundBootstrap`](../resident/mrxsoundbootstrap), then calls
`MrxLayerManager.RemoveAllLayers` on a copy of `_tStaticLayers` plus `"vz_base"`, with a completion callback
(`_PostDeleteLayers`) that resets `WifMissionFlow` again, resets camera/shadow `Graphics.*` overrides, cleans
up [`MrxGui`](../resident/mrxgui) fade/flash state, resets and deinits
[`MrxPlayer`](../resident/mrxplayer), calls `Pg.ResetSingletonDone()`, fires the caller's own `fCallback`,
and finally — if a `LoadSingleton` call arrived mid-teardown and got deferred into
`_fUnloadLayersCallback` — invokes that deferred load now that static layers have finished unloading.

### Loading a game and the streaming handshake

**`LoadSingleton(tSaveData)`** is the master load entry point, and the one place all the different "how did
we get here" boot paths converge. If a `ResetSingleton` teardown is still unloading static layers
(`Pg.GetUnloadingStaticLayers()`), it defers itself into `_fUnloadLayersCallback` and returns — it'll be
re-invoked from `_PostDeleteLayers` once that finishes. Otherwise, for server/non-MP sessions: resets and
frees [`MrxPlayState`](../resident/mrxplaystate), stores `tSaveData` into `_tSaveState`, and — only for a
genuinely fresh boot with no save and no pending skip — checks `Sys.GetSkipMission()` for a debug/cheat
mission-skip request (arming `MrxCheatBootstrap.EnableSkipMode` if present) or otherwise notices if the
configured player-start isn't the default `"PlayerLocation_Start"` (setting `_bAltSpawnLocation`, an
alt-boot path used for non-standard entry points). It then resolves where the heroes should end up, in
priority order: a checkpoint retry's own retry locations
(`Pg.LoadIsRetry()` + `WifMissionFlow.GetRetryLocations()`) &gt; retry locations embedded in the save
itself &gt; the PMC entry points (ordinary save load, setting `_bPmcRequired`) &gt; — for a brand-new game
only — the skip-to mission's own start/briefing locations, or else `VzaCon001`'s (the game's actual opening
mission) start locations, or else a final hardcoded PMC-starter fallback. Depending on session freshness,
those locations either go straight to `MrxPlayer.SetSpawnLocations` or get stashed in
`_tTeleportLocations` for later. Finally, either enters `MrxState.STATE_WAITFORSTREAMING` and calls
`_LoadLayers` (checkpoint-retry path) or calls `_LoadLayers()` immediately.

**`_LoadLayers()`** kicks off both the static and dynamic layer loads. Static layers
(`MrxLayerManager.Add(_tStaticLayers, _AttemptGameplaySetup, {"static"}, true, true)`) load once per
session, guarded by `_bStaticLayersLoaded`. Dynamic layers (server/non-MP only) load either from the save's
own layer snapshot (`MrxLayerManager.LoadSingleton(_tSaveState.tLayerData, ...)`) or, for a fresh game, the
hardcoded `_tDefaultDynamicLayers` list — wrapped in `Net.BeginLayerEventGroup()` where that API exists, to
batch the resulting replication events.

**`_AttemptGameplaySetup(sSignal)`** is the convergence point for three (or four) independent async
signals: `"boot"` (native bootstrap done), `"static"` (static layers loaded — also kicks
`MrxPlayer.Start()` immediately), `"dynamic"` (dynamic layers loaded, server/non-MP only), and — only for a
checkpoint-retry session — `"stream"` (initial streaming complete). Only once every signal applicable to
this session type has arrived does it proceed: server/non-MP enters `MrxState.STATE_WAITFORGAME` (queuing
`_CompleteGameplaySetup`) and, for a retry session, exits `STATE_WAITFORSTREAMING`; clients instead call
`_GameplaySetup_LoadWorldState()` directly, since clients don't run subsystem restoration themselves.

**`_CompleteGameplaySetup()`** just calls `_GameplaySetup_RestoreSubsystems()` then
`_GameplaySetup_LoadWorldState()`.

**`_GameplaySetup_RestoreSubsystems()`** ends survival/downed mode and reloads ammo/idle state for every
player's character, clears the currently-equipped Pda support item, stops music, and — if loading a save —
restores per-player state via `MrxPlayer.LoadSingleton(_tSaveState.tPlayerData)`.

**`_GameplaySetup_LoadWorldState()`** is the largest function in the file. It unconditionally starts the
three VZ region-flavor modules — `WifVzAmbience.Start()`, `WifVzAtmosphere.Start()`,
`WifVZRegionNames.Start()` — then, for clients, re-syncs faction relations/position and briefly toggles
resource counters to refresh the cash/fuel HUD display. For server/non-MP: starts `StagingAct1`, decides
whether to (re-)establish the world boundary (`bSetupBoundary`, false for an alt-spawn or skip-to-mission
boot), then either — loading a save — restores roughly 18 more subsystems in sequence
([`WifVzBoundary`](wifvzboundary), [`MrxPmc`](../resident/mrxpmc),
[`MrxSupportData`](../resident/mrxsupportdata), [`MrxRewardData`](../resident/mrxrewarddata),
[`MrxFactionManager`](../resident/mrxfactionmanager), [`MrxTransit`](../resident/mrxtransit),
[`WifPmcInterior`](wifpmcinterior), `WifHints`, `WifBios`, [`Munitions`](../resident/munitions), grapple/
vehicle-disguise flags, [`MrxTutorialManager`](../resident/mrxtutorialmanager),
[`MrxShop`](../resident/mrxshop), `WifEquipmentData`, [`MrxAchievements`](../resident/mrxachievements),
last-completed-mission name, [`friendlygate`](../resident/friendlygate), available costumes, and
optionally the equipped support item) — or, for a fresh game, just calls
`WifVzBoundary.SetupBoundaryIntro()` (if applicable), resets [`MrxTransit`](../resident/mrxtransit), and
disables munitions tagging. Either way, it then (re-)creates the native mission-tree root
(`_oMasterStub = MrxTask:Create()`, configured `{sName = "Missions"}` and activated), rewires
`WifMissionFlow` to it (`SetMissionParent`, plus registering
`SetPreContractSaveData` as the pre-contract save hook), and tells
[`MrxCheatBootstrap`](../resident/mrxcheatbootstrap) about the new root and `SkipToMission` as its
mission-skip-dialog callback. If teleport locations are pending, it teleports the heroes there (completion
callback `_SecondaryStreamComplete`) and returns early — posting a `"parkingLotStart"` event first if this
was a checkpoint retry. Otherwise it falls through to
`MrxState.Enter(MrxState.STATE_WAITFORSTREAMING, nil, nil, _SecondaryStreamComplete)`, waiting for
background streaming to finish.

**`_SecondaryStreamComplete()`** exits `STATE_WAITFORSTREAMING` and calls `_StartPlayerVisibleGameplay()`.

**`_StartPlayerVisibleGameplay()`** is the final step before the player actually gets control. Stops music
again; if loading a save, restores `WifMissionFlow`/[`MrxStarterManager`](../resident/mrxstartermanager)/
elapsed-session-time/[`MrxStatsManager`](../resident/mrxstatsmanager) and clears `_tSaveState` (so this only
ever runs once per load); otherwise seeds elapsed time at zero. Starts the session timer if not already
running, and (server/non-MP) resets the weapon-usage stat timer. Unless this was an alt-spawn boot, calls
`WifMissionFlow.Refresh(...)` to exit `STATE_WAITFORGAME` once mission state is current; closes the net
layer-event group opened earlier. If a PMC entry was required (`_bPmcRequired` — an ordinary save load
with no retry checkpoint), enters [`WifPmcInterior`](wifpmcinterior) (exiting first if somehow already
inside), with a load callback that finally exits `STATE_WAITFORGAME`. Finishes with
`MrxTutorialManager.Setup()` and clearing every transient boot-state flag.

### Mission skip (debug/cheat)

**`SkipToMission(sMissionId, bBriefing)`** is the debug "jump straight to mission X" entry point, wired as
`MrxCheatBootstrap`'s mission-skip-dialog callback above. Sets the engine-level skip-mission/skip-briefing
flags (`Sys.SetSkipMission`, `Sys.SetINIBriefing`) and requests a full state transition to `"unloading"` —
triggering a level reload that, on the way back in through `Init()`/`LoadSingleton()`, will notice
`Sys.GetSkipMission()` is set and boot directly into that mission instead of the normal flow.

## Events
Unlike its `WifVz*` sibling modules (which are built almost entirely around `Event.Boundary` crossings),
`xQ!L` barely uses `Event.*` at all — its own internal synchronization is done through
`MrxState.Enter`/`Exit` state-gating and direct callback chaining instead. Confirmed only 2 direct uses:
- `Event.GameStateChange` — `{"Pause", "exit"}` in `ClientReimburseForSave`, restoring the client's real
  cash display once the pause menu closes.
- `Event.Post("parkingLotStart", {false})` — in `_GameplaySetup_LoadWorldState`, for a checkpoint-retry
  load with pending teleport locations. Note this is the same `"parkingLotStart"` event name
  [`WifPmcInterior`](wifpmcinterior)`._DoParkingLot` posts — a shared event-name convention between the two
  files, not a coincidence.

## Notes for modders
- **This is the conductor everything else in `vz/`'s own save/load ultimately routes through.** If you're
  trying to understand *when* something loads relative to something else — e.g. "does my mod's state exist
  yet when `WifMissionFlow` starts up" — `_GameplaySetup_LoadWorldState`'s call order above is the
  authoritative sequence, not any individual subsystem's own page.
- The boot sequence, summarized: native bootstrap + static layers + dynamic layers all converge in
  `_AttemptGameplaySetup` -> subsystems restore (`_GameplaySetup_RestoreSubsystems`) -> world state loads
  and ~20 subsystems' `LoadSingleton`s run (`_GameplaySetup_LoadWorldState`) -> background streaming
  finishes (`_SecondaryStreamComplete`) -> the player actually gets control
  (`_StartPlayerVisibleGameplay`). All of it is gated on `MrxState.STATE_WAITFORSTREAMING` /
  `STATE_WAITFORGAME`, the same state-machine primitive used throughout this corpus for "block until X."
- `_tStaticLayers`/`_tDefaultDynamicLayers` are the real, complete, boot-time bulk-population lists for the
  open world — see [`MrxLayerManager`'s own page](../resident/mrxlayermanager) for the full 170/246-entry
  lists and why they matter for anything trying to enumerate "every layer that exists."
- **Confirmed casing inconsistency:** this file imports the region-names module as `WifVZRegionNames`
  (capital `VZ`) and calls `WifVZRegionNames.Start()`, while `resident/mrxguipda.lua` imports the same
  module as `WifVzRegionNames` (lowercase `z`) to read `tBoundaryList`. Both presumably resolve to the same
  `wifvzregionnames.lua` file — this corpus's module loader appears tolerant of the mismatch, consistent
  with inconsistent casing showing up elsewhere too (e.g. layer names) — but it's a real, confirmed textual
  difference between the two call sites, not a typo introduced by decompilation.
- `SkipToMission(sMissionId, bBriefing)` is the actual mechanism behind any in-game mission-skip/debug menu
  — useful to know if you're building a modded mission-select tool, since it works by requesting a full
  level reload rather than hot-swapping mission state in place.
- Treat `GenerateSaveData()`'s field list as the closest thing to a save-file schema reference available
  from source — if you're building an external save editor or a mod that needs to read/patch save data,
  every top-level key it writes is named there.
