---
title: "Setting Custom World State from OnLoad — experimental"
parent: Deep Dives
nav_order: 10
---

# Deep Dive: Setting Custom World State from OnLoad

> **Status: experimental, in development.** Two real, confirmed-live bugs are documented (and fixed) in
> the script's own history — a wrongly-unloaded base-geometry layer that left captured-outpost overlays
> floating over nothing, and an `MrxState` refcount left orphaned that hung the post-reload fade-in on a
> black screen — which is real evidence this has actually been run against the game, not just reasoned out
> from source. What hasn't been independently re-confirmed here is the *full* end-to-end flow (autosave
> lock → attitude mutability → captured-layer flip + streaming reload → landing-zone ownership → discovery
> handoff) across a range of starting save states. Treat the *mechanism* — how each piece works and why —
> as demonstrated; treat the specific 14-outpost data table as one mod's own configuration, not a claim
> that it's bug-free for a different layer/outpost set.

This is the general technique behind [`TerritorialWarInit.lua`](#the-current-script), a script built for an
experimental territorial-war RTS gamemode. That mod needed every session to start from a specific baseline
— all outposts already fought over and settled, most under their "native" faction, a few deliberately still
VZ-held — regardless of which save the player loads or where the real campaign's mission flow has actually
gotten to. Doing that for real (not just pretending, in an abstract simulation layer) means rewriting
persistent world state: which buildings exist, who owns them, and what the PDA/radar/fast-travel menu says
about them. None of that is a documented, single-call operation — it's assembled from four separate native
systems, each with its own gotcha found by hitting it.

## The problem: OnLoad can't just flip layers

The game's own capture flow (`resident/mrxtaskcontractoutpost.lua`'s `Complete()`) changes an outpost's
state by calling `MrxLayerManager.MarkForAddition`/`MarkForRemoval` and then letting the *real* mission flow
carry the world through a state transition that actually composites the change. Read `MarkForAddition`/
`MarkForRemoval` themselves (`resident/mrxlayermanager.lua`) and that's the whole story — they just flip
entries in two internal tables (`_tLayersToBeAdded`, `_tLoadedLayers`):

```lua
function MarkForRemoval(vLayers)
  for i, sLayerName in ipairs(tLayers) do
    sLayerName = string.lower(sLayerName)
    if _tLoadedLayers[sLayerName] ~= nil then
      _tLoadedLayers[sLayerName] = true
    end
    _tLayersToBeAdded[sLayerName] = nil
  end
end
```

The actual native load/unload calls (`Pg.LoadLayer`/`Pg.UnloadLayer`, confirmed at
`resident/mrxlayermanager.lua:224` and `:236`) only fire inside `ProcessMarkedLayers`. An `OnLoad` script
*can* call `ProcessMarkedLayers` directly — nothing stops it — but the world still won't visibly change,
because compositing a layer change is normally something the engine does as part of a `WaitForStreaming`
game-state transition, and `OnLoad` scripts run before any of that machinery is in motion. This is the
whole reason `TerritorialWarInit.lua` exists: it has to manually drive the exact state transition the real
mission flow would have driven for it.

## `MrxState`: the choreography that actually composites a world change

`resident/mrxstate.lua` exposes four states (`STATE_CINEMATIC`, `STATE_WAITFORSTREAMING`,
`STATE_WAITFORTETHER`, `STATE_WAITFORGAME`) behind a shared `Enter`/`Exit` API with its own refcounting.
Two matter here.

**`STATE_WAITFORSTREAMING`** is the one that actually forces a composite. Its `Enter` (confirmed,
`resident/mrxstate.lua:26-33`):

```lua
[STATE_WAITFORSTREAMING] = {
  Enter = function()
    Sys.RequestGameState("WaitForStreaming")
    Event.Create(Event.GameStateChange, {"WaitForStreaming", "exit"}, _StateComplete, {STATE_WAITFORSTREAMING})
  end,
  ...
}
```

`Sys.RequestGameState("WaitForStreaming")` is the same native call `resident/mrxtransit.lua`'s
`StartTransit`/fast-travel and the real mission flow's own level transitions use — it's confirmed, reused
plumbing, not a guess. Entering this state is what makes the engine actually load/unload everything just
marked, not just remember that it should.

**`STATE_WAITFORGAME`** doesn't touch streaming at all — its own `Enter` (confirmed,
`resident/mrxstate.lua:60-63`) just calls `_StateComplete` immediately:

```lua
[STATE_WAITFORGAME] = {
  Enter = function()
    _StateComplete(STATE_WAITFORGAME)
  end,
  ...
}
```

What it *does* get is the shared `_GlobalEnter`/`_GlobalExit` machinery every state goes through once,
globally, on the very first `Enter` call while nothing is already locked (confirmed,
`resident/mrxstate.lua:81-114`): a full-screen fade, `Player.SetInputEnabled(uPlayer, false)`, and
`Object.SetInvincible(uChar, true, "MrxState")` for every player, undone symmetrically by `_GlobalExit`
once every active state has fully exited. Wrapping the reload in `STATE_WAITFORGAME` is what gets the
player faded out, input-locked, and invincible for the duration — so they can't fall through geometry that
hasn't streamed in yet, or take damage mid-reload — using the exact mechanism the real game already uses
for every other hard cut, rather than rolling a custom fade by hand.

### The refcount gotcha that caused a black-screen hang

`Enter` increments a per-state `nRefCount`; only an explicit `Exit` call decrements it (confirmed,
`resident/mrxstate.lua:222` and `:277`). `_AttemptGlobalExit` (confirmed, `:287-306`) walks every state and
bails out — leaving the player faded to black, input-locked, invincible — if **any** state still has
`nRefCount > 0` or is still `bLocked`:

```lua
function _AttemptGlobalExit()
  if not _bGloballyLocked then return end
  local bAllStatesExited = true
  for nState, tStateData in ipairs(_States) do
    if tStateData.nRefCount > 0 or tStateData.bLocked then
      bAllStatesExited = false
      break
    end
  end
  if bAllStatesExited then
    _GlobalExit()
    _bGloballyLocked = nil
  end
end
```

Critically, `STATE_WAITFORSTREAMING`'s completion path (`_StateComplete`, confirmed `:179-190`) clears
`bLocked` once the engine's own `"WaitForStreaming"`/`"exit"` `GameStateChange` event fires, and fires
whatever `fReadyToExitCallback` was registered on `Enter` — but it does **not** decrement `nRefCount`
itself (that adjustment is special-cased for `STATE_WAITFORTETHER` only, `:183-185`). If nothing in that
`readyToExitCallback` calls `Exit(STATE_WAITFORSTREAMING)`, the refcount stays elevated forever,
`_AttemptGlobalExit` bails out on every subsequent attempt, and `_GlobalExit` — the fade back in — never
runs. This was a real, live-hit bug: the first version of this script entered `WaitForStreaming` with no
`readyToExitCallback` and never called `Exit`, which orphaned the refcount and hung the screen on black
after every world flip. The fix is to pair them explicitly, the same way `resident/mrxtransit.lua`'s
`StartTransit`/`FinishTransit` already do it internally:

```lua
MrxState.Enter(MrxState.STATE_WAITFORSTREAMING, nil, nil, function()
  MrxState.Exit(MrxState.STATE_WAITFORSTREAMING)
end)
MrxState.Exit(MrxState.STATE_WAITFORGAME) -- release the fade-holder; WAITFORSTREAMING clears itself above
```

**General rule, confirmed against source rather than assumed:** every `MrxState.Enter` needs a
correspondingly-reachable `Exit` for that same state, or the global fade-lock never releases. For
`STATE_WAITFORSTREAMING` specifically, that pairing has to happen inside the `readyToExitCallback` (4th
argument to `Enter`), since that's the only callback the native `"exit"` game-state event actually drives.

## Layer semantics: `pristine` is base geometry, not a flag

The outpost capture layers in this game (per `vz/*con05x.lua`'s `GetOutpostConfig()` blocks) come in four
kinds per outpost: a `_Pristine` layer, a `_Staging` layer, a `_Defenses` layer, and a `_Captured` layer.
The real capture flow (`resident/mrxtaskcontractoutpost.lua`'s `Complete()`) removes staging and defenses,
adds captured, and **leaves pristine alone**. An earlier version of this script got that wrong by also
removing pristine, on the assumption it was some kind of "uncaptured" flag layer — it isn't. `xQ!L.lua`'s
`_tDefaultDynamicLayers` (confirmed, line 184+) lists pristine layers among the level's own default dynamic
content: it's the outpost's actual base geometry, loaded by default on a fresh save. Unloading it left the
captured overlay (flags, new faction units) rendering over an empty hole in the map — the "destroyed and
empty" bases symptom this bug produced live. The fix adds pristine back explicitly (not just "leaves it
alone") specifically so a session that already ran the broken version — which had genuinely unloaded it —
gets it restored without needing a full level reload; `MarkForAddition` is a no-op for anything already
loaded, so this is safe to do unconditionally.

The general lesson: a layer name that reads like a status flag ("pristine" as in "not yet captured") can
just as easily be load-bearing geometry. Confirm what a layer actually contains — check where else it's
referenced, and what a level's own default-dynamic-layer manifest says — before assuming a name's plain
-English meaning is the whole story.

## Faction attitudes: `bDynamic` gates which factions can even go hostile/friendly at runtime

`MrxFactionManager.SetAttitudeMutable(sAbbrev)` is what the story's own mission intros call to let a
faction's relationship with the player actually change during play; before that, an attitude is fixed.
It's gated by `CanAttitudeBeMutable`, which just checks a static per-faction flag (confirmed,
`resident/mrxfactionmanager.lua:66-297` and `:512-514`):

```lua
function CanAttitudeBeMutable(sAbbrev)
  return _tFactions[sAbbrev].bDynamic == true
end
```

Reading `_tFactions`' own definitions confirms exactly which factions this applies to: `All`, `Chi`, `Gur`,
`Oil`, and `Pir` are all `bDynamic = true`; `Civ`, `Pmc`, and `Vza` are all `bDynamic = false`. A world-flip
script that wants a faction to actually behave as a live combatant — not just display a different color —
needs `SetAttitudeMutable` called for it first; calling it for a `bDynamic = false` faction is a silent
no-op (`CanAttitudeBeMutable` gates the whole function body), not an error, so nothing will look wrong
until you notice that faction never reacts to anything.

## Landing-zone ownership: `MrxTransit` is what the PDA/radar/fast-travel menu actually reads

Flipping layers changes what's physically in the world, but the fast-travel menu, PDA markers, and radar
colors read a separate system: `MrxTransit`. `SetLocationEnabled(nLocation, sFactionAbbrev, bSuppressFanfare)`
(confirmed, `resident/mrxtransit.lua:175+`) stamps one landing-zone index with an owning faction abbreviation
and enables it for fast travel; `SetSystemEnabled(true, false)` (confirmed, `:247+`) turns the whole transit
system on if it isn't already. Skipping this step means the world *looks* captured up close but the
map/PDA still shows the old ownership — a believable-sounding bug that's easy to not notice until someone
opens the map.

`_tLandingZones` (confirmed, populated in `Reset` at `resident/mrxtransit.lua:317-339` from
`Pg.GetAllLandingZones`) turned out to matter for a second reason, independent of ownership display: each
landing zone's own location object (`uLocation1`) is a stable position anchor that comes from the transit
system itself, not from any `vz_state_*` layer — so unlike a named building, it survives a captured-layer
flip that removes or renames the building object a `Pg.GetGuidByName(sOutpostName)` lookup depends on. The
outpost-tracking side of this project uses the landing-zone anchor as a fallback when the named-building
lookup fails post-flip, and it separately rescued at least one outpost name that had never resolved by
name at all in earlier testing.

## Autosave: the first thing any world-mutating OnLoad script should kill

Before touching anything else, `TerritorialWarInit.lua` overrides the two Lua-reachable autosave
choke points to no-ops:

```lua
local function DisableSaves()
  if not Sys._twRealRequestAutosave and Sys.RequestAutosave then
    Sys._twRealRequestAutosave = Sys.RequestAutosave
  end
  if not Sys._twRealForceNextAutosave and Sys.ForceNextAutosave then
    Sys._twRealForceNextAutosave = Sys.ForceNextAutosave
  end
  Sys.RequestAutosave = function() end
  Sys.ForceNextAutosave = function() end
end
```

`Sys.RequestAutosave`/`Sys.ForceNextAutosave` are confirmed called from `resident/mrxmissionflow.lua:768`,
`resident/mrxtaskcontract.lua:825`, and `resident/wifmissionflow.lua:462` — real, load-bearing story-flow
call sites, not theoretical. The order matters: this runs *first*, before any layer/attitude/transit
change, specifically so an experimental script that's still finding bugs (see the two above) can't have one
of those bugs get written into the player's real save file. The originals are stashed on `Sys` rather than
discarded, so a deliberate re-enable stays possible later — this script just never calls it, by design.

## The HQ-interior gate: some regions aren't streamed yet at `OnLoad` time

A session that starts (or resumes) inside the PMC HQ interior hasn't streamed in the open-world outpost
regions at all — a `Pg.GetGuidByName` for an outpost building genuinely has nothing to find yet, and a
`WaitForStreaming` transition has nothing meaningful to composite. `TerritorialWarInit.lua` checks for this
(`WifPmcInterior.IsInside()`) and for any other `MrxState` transition already in flight
(`MrxState.IsLocked()`) before attempting the flip, deferring on a short poll until both are clear:

```lua
local function ApplyFlipWhenReady()
  if not IsInHqInterior() and not IsStateLocked() then
    ApplyLayersWithReload(Handoff)
    return
  end
  F.Schedule("TerritorialWarInit.WaitForOutside", 5, function()
    if IsInHqInterior() or IsStateLocked() then return end
    F.Unschedule("TerritorialWarInit.WaitForOutside")
    ApplyLayersWithReload(Handoff)
  end)
end
```

Skipping the `IsStateLocked()` half of this check specifically risks stacking this script's own fade on
top of whatever fade the HQ-exit transition is already mid-flight — since `MrxState`'s global fade/lock is
shared across every caller (see the choreography section above), two callers entering it back-to-back
without waiting for the first to fully resolve is exactly the kind of thing that mechanism is meant to
serialize safely, but it's still simpler to just wait for a clean, unlocked starting point.

## The current script

`TerritorialWarInit.lua` (load order: after `Framework.lua`/the war sim/outpost bridge — see its own header
for the `lua_loader.ini` entry):

```lua
-- TERRITORIAL WAR -- INIT (approach B). Puts the world into an "all 14 outposts
-- liberated by their home faction" baseline from ANY campaign state, WITHOUT
-- running the real mission flow (no cinematics, no teleports, no key-awarding, no
-- ordering assumptions). Four steps, then it hands off to the war sim's discovery:
--
--   1. Hard-disable Lua-driven autosave FIRST, so nothing below can bleed into the
--      player's real save. (Sys.RequestAutosave / Sys.ForceNextAutosave are the two
--      Lua-reachable choke points -- confirmed callers: mrxmissionflow.lua:768,
--      mrxtaskcontract.lua:825, wifmissionflow.lua:462.)
--   2. Make the 5 combat factions' attitudes mutable (live war participants) -- the
--      same MrxFactionManager.SetAttitudeMutable the story intros call. All/Chi/Gur/
--      Oil/Pir are bDynamic=true; Pmc/Vza are not and are left alone.
--   3. Swap each outpost to its source-verified CAPTURED layer set (add captured +
--      captured-Tg, remove pristine/staging/staging-Tg/defense), then force a
--      streaming reload so the engine actually COMPOSITES the change. This is the
--      crux: MrxLayerManager.MarkFor*/ProcessMarkedLayers only issues Pg.LoadLayer/
--      UnloadLayer; the world isn't re-composited until a "WaitForStreaming" game-
--      state transition runs -- which is exactly what an OnLoad script lacks, and why
--      layer edits from OnLoad are silently rejected. MrxState.STATE_WAITFORSTREAMING
--      (mrxstate.lua:26 -> Sys.RequestGameState("WaitForStreaming")) IS the world
--      reload the contracts/fast-travel ride on; we wrap it in STATE_WAITFORGAME for
--      the same fade + input-lock + invincibility so the player can't fall through
--      un-streamed geometry or take damage mid-reload.
--   4. Set each outpost's landing-zone faction ownership (MrxTransit.SetLocationEnabled)
--      so the PDA/radar reads the right colours and fast-travel works.
--
-- Then calls TerritorialWarOutposts.DiscoverOutposts() so the sim binds to the now-
-- flipped world.
--
-- ALL LAYER NAMES / CAPTURE POINTS / LZ INDICES BELOW ARE SOURCE-VERIFIED from the 14
-- vz/*con05x.lua GetOutpostConfig() blocks and vz/wifhqdata.lua _tHqConfigs -- not
-- invented. (allcon052's staging layer really is "...Staging2", kept exact.)
--
-- LOAD ORDER: after Framework/War/Outposts. Add to lua_loader.ini [OnLoad]:
--     TerritorialWarInit.lua=80
-- The save-block re-asserts every level load (cheap, idempotent); the heavy attitude/
-- layer/reload pass runs ONCE per session (guarded), re-triggerable via I.ForceReinit().

if not _G.Framework then
  error("[TerritorialWarInit] Framework.lua must load first")
end
local F = _G.Framework
local I = F.GetState("TerritorialWarInit")

-- abbrev is BOTH the MrxFactionManager attitude key AND the MrxTransit faction id.
local tCombatFactions = {"All", "Chi", "Gur", "Oil", "Pir"}

-- Per outpost: bldg, faction abbrev (fac), landing-zone index (lz), and the layer names.
-- Set keepVz=true on any entry to LEAVE it VZ-occupied: its pristine+staging+defense stay
-- loaded (a populated VZ base the player must still capture), it's excluded from the flip,
-- and its LZ is flagged Vza (enemy) instead of unlocked. When you do that, ALSO set that
-- outpost's sFaction="VZ" in TerritorialWarOutposts.lua's tOutpostSeed so the sim tracks it
-- as VZ-owned. (capTg/stgTg remain for reference; BuildLayerLists ignores them now.)
local tOutposts = {
  {bldg="AllJob001_01_Outpost", fac="All", lz=20, cap="Vz_State_AllJob001_01_Captured", capTg="Vz_State_AllCon050c_Tg", pri="Vz_State_AllJob001_01_Pristine", stg="Vz_State_AllJob001_01_Staging",  stgTg="Vz_State_AllCon050_Tg", def="Vz_State_AllJob001_01_Defenses"},
  {bldg="AllJob001_03_Outpost", fac="All", lz=22, cap="Vz_State_AllJob001_03_Captured", capTg="Vz_State_AllCon052c_Tg", pri="Vz_State_AllJob001_03_Pristine", stg="Vz_State_AllJob001_03_Staging2", stgTg="Vz_State_AllCon052_Tg", def="Vz_State_AllJob001_03_Defenses"},
  {bldg="AllJob001_04_Outpost", keepVz=true, fac="All", lz=21, cap="Vz_State_AllJob001_04_Captured", capTg="Vz_State_AllCon053c_Tg", pri="Vz_State_AllJob001_04_Pristine", stg="Vz_State_AllJob001_04_Staging",  stgTg="Vz_State_AllCon053_Tg", def="Vz_State_AllJob001_04_Defenses"},
  {bldg="ChiJob001_01_Outpost", fac="Chi", lz=23, cap="Vz_State_ChiJob001_01_Captured", capTg="Vz_State_ChiCon050c_Tg", pri="Vz_State_ChiJob001_01_Pristine", stg="Vz_State_ChiJob001_01_Staging",  stgTg="Vz_State_ChiCon050_Tg", def="Vz_State_ChiJob001_01_Defenses"},
  {bldg="ChiJob001_02_Outpost", fac="Chi", lz=24, cap="Vz_State_ChiJob001_02_Captured", capTg="Vz_State_ChiCon051c_Tg", pri="Vz_State_ChiJob001_02_Pristine", stg="Vz_State_ChiJob001_02_Staging",  stgTg="Vz_State_ChiCon051_Tg", def="Vz_State_ChiJob001_02_Defenses"},
  {bldg="ChiJob001_04_Outpost", keepVz=true, fac="Chi", lz=25, cap="Vz_State_ChiJob001_04_Captured", capTg="Vz_State_ChiCon053c_Tg", pri="Vz_State_ChiJob001_04_Pristine", stg="Vz_State_ChiJob001_04_Staging",  stgTg="Vz_State_ChiCon053_Tg", def="Vz_State_ChiJob001_04_Defenses"},
  {bldg="GurJob003_Outpost",    fac="Gur", lz=4,  cap="Vz_State_GurJob003_Captured",    capTg="Vz_State_GurCon050c_Tg", pri="Vz_State_GurJob003_Pristine",    stg="Vz_State_GurJob003_Staging",     stgTg="Vz_State_GurCon050_Tg", def="Vz_State_GurJob003_Defenses"},
  {bldg="GurJob008_01_Outpost", fac="Gur", lz=18, cap="Vz_State_GurJob008_01_Captured", capTg="Vz_State_GurCon052c_Tg", pri="Vz_State_GurJob008_01_Pristine", stg="Vz_State_GurJob008_01_Staging",  stgTg="Vz_State_GurCon052_Tg", def="Vz_State_GurJob008_01_Defenses"},
  {bldg="GurJob008_02_Outpost", keepVz=true, fac="Gur", lz=17, cap="Vz_State_GurJob008_02_Captured", capTg="Vz_State_GurCon053c_Tg", pri="Vz_State_GurJob008_02_Pristine", stg="Vz_State_GurJob008_02_Staging",  stgTg="Vz_State_GurCon053_Tg", def="Vz_State_GurJob008_02_Defenses"},
  {bldg="OilJob001_Outpost",    fac="Oil", lz=15, cap="Vz_State_OilJob001_Captured",    capTg="Vz_State_OilCon050c_Tg", pri="Vz_State_OilJob001_Pristine",    stg="Vz_State_OilJob001_Staging",     stgTg="Vz_State_OilCon050_Tg", def="Vz_State_OilJob001_Defenses"},
  {bldg="OilJob002_Outpost",    fac="Oil", lz=3,  cap="Vz_State_OilJob002_Captured",    capTg="Vz_State_OilCon051c_Tg", pri="Vz_State_OilJob002_Pristine",    stg="Vz_State_OilJob002_Staging",     stgTg="Vz_State_OilCon051_Tg", def="Vz_State_OilJob002_Defenses"},
  {bldg="OilJob005_Outpost",    keepVz=true, fac="Oil", lz=16, cap="Vz_State_OilJob005_Captured",    capTg="Vz_State_OilCon052c_Tg", pri="Vz_State_OilJob005_Pristine",    stg="Vz_State_OilJob005_Staging",     stgTg="Vz_State_OilCon052_Tg", def="Vz_State_OilJob005_Defenses"},
  {bldg="PirJob002_02_Outpost", fac="Pir", lz=27, cap="Vz_State_PirJob002_02_Captured", capTg="Vz_State_PirCon051c_Tg", pri="Vz_State_PirJob002_02_Pristine", stg="Vz_State_PirJob002_02_Staging",  stgTg="Vz_State_PirCon051_Tg", def="Vz_State_PirJob002_02_Defenses"},
  {bldg="PirJob002_03_Outpost", fac="Pir", lz=28, cap="Vz_State_PirJob002_03_Captured", capTg="Vz_State_PirCon052c_Tg", pri="Vz_State_PirJob002_03_Pristine", stg="Vz_State_PirJob002_03_Staging",  stgTg="Vz_State_PirCon052_Tg", def="Vz_State_PirJob002_03_Defenses"},
}

-- ===== Step 1: kill Lua-driven saving (re-asserted every load) ==================
-- Overrides the two engine choke points to no-ops. Stashes the originals on Sys so a
-- deliberate re-enable is still possible; nothing here re-enables, by design. Only the
-- authoritative side needs to (and does) touch this -- a client never drives autosave.
local function DisableSaves()
  if not Sys._twRealRequestAutosave and Sys.RequestAutosave then
    Sys._twRealRequestAutosave = Sys.RequestAutosave
  end
  if not Sys._twRealForceNextAutosave and Sys.ForceNextAutosave then
    Sys._twRealForceNextAutosave = Sys.ForceNextAutosave
  end
  Sys.RequestAutosave = function() end
  Sys.ForceNextAutosave = function() end
  I.bSavesDisabled = true
end

-- ===== Step 2: attitudes ========================================================
local function SetAttitudes()
  F.SafeCall("Init.Attitudes", function()
    import("MrxFactionManager")
    for _, sAbbrev in ipairs(tCombatFactions) do
      if not MrxFactionManager.IsAttitudeMutable(sAbbrev) then
        MrxFactionManager.SetAttitudeMutable(sAbbrev)
        F.Log("TerritorialWarInit", "attitude made mutable: " .. sAbbrev)
      end
    end
  end)
end

-- ===== Step 4: landing-zone ownership ===========================================
-- (numbered after step 3 in the header but has no ordering dependency on it; runs in
-- the same faded window.) Enables the transit system and stamps each outpost LZ with
-- its owning faction. Best-effort per LZ so one bad index can't abort the rest.
local function SetLandingZones()
  F.SafeCall("Init.LZ", function()
    import("MrxTransit")
    MrxTransit.Reset()               -- no-op if already initialized in-game
    MrxTransit.SetSystemEnabled(true, false)
    for _, o in ipairs(tOutposts) do
      -- keepVz outposts flagged Vza (enemy/suppressed -- must be captured to unlock);
      -- the rest unlocked under their owning faction. 3rd arg = bSuppressFanfare.
      pcall(MrxTransit.SetLocationEnabled, o.lz, o.keepVz and "Vza" or o.fac, true)
    end
  end)
end

-- ===== Step 3: captured layers + the streaming reload ===========================
-- Mirrors the REAL capture, mrxtaskcontractoutpost.lua Complete(): remove staging +
-- defense, add captured, KEEP pristine. The first cut wrongly removed pristine (and
-- added the _Tg layers). pristine is the outpost's BASE GEOMETRY -- a default dynamic
-- layer loaded on a fresh save (xQ!L.lua _tDefaultDynamicLayers, line 184+), NOT static
-- -- so MarkForRemoval genuinely unloaded it, leaving the captured overlay (flags/units)
-- floating over nothing = the "destroyed and empty" bases you saw. pristine is ADDED
-- here (not merely left alone) so a session that already ran the old version -- which
-- unloaded it -- gets it back without a full level reload; MarkForAddition is a no-op if
-- it's already loaded. The _Tg layers are the contract's objective graphics; Complete()
-- never touches them, so neither do we (capTg/stgTg stay in the table above, just unused).
-- One aggregated add/remove list so the whole world still flips in a single reload cycle.
local function BuildLayerLists()
  local tAdd, tRemove = {}, {}
  for _, o in ipairs(tOutposts) do
    if not o.keepVz then         -- keepVz: skip the flip, leave pristine+staging+defense (populated VZ base)
      table.insert(tAdd, o.pri)    -- base geometry: restore/keep it
      table.insert(tAdd, o.cap)    -- faction overlay: the units the AI-faction switch comes from
      table.insert(tRemove, o.stg) -- VZ staging forces
      table.insert(tRemove, o.def) -- VZ defensive emplacements
    end
  end
  return tAdd, tRemove
end

-- Contract-faithful reload. NOTE: this MrxState choreography mirrors StartTransit and
-- the wifmissionflow beats (fade via WAITFORGAME -> process layers -> WAITFORSTREAMING
-- forces Sys.RequestGameState("WaitForStreaming") -> both states clear -> fade back in).
-- It's the one sequence to eyeball live first; everything else here is plain state-set.
-- fDone runs once the layer requests have been ISSUED and the reload kicked off (the
-- discovery handoff doesn't need to wait for the fade-in), and still runs if the reload
-- path errors, so discovery is never stranded.
local function ApplyLayersWithReload(fDone)
  local tAdd, tRemove = BuildLayerLists()
  local bDoneFired = false
  local function FireDone()
    if bDoneFired then return end
    bDoneFired = true
    F.Unschedule("TerritorialWarInit.HandoffGuard")
    if fDone then F.SafeCall("Init.Handoff", fDone) end
  end
  local bOk = F.SafeCall("Init.Layers", function()
    import("MrxLayerManager")
    import("MrxState")
    MrxState.Enter(MrxState.STATE_WAITFORGAME, function()
      if #tRemove > 0 then MrxLayerManager.MarkForRemoval(tRemove) end
      if #tAdd > 0 then MrxLayerManager.MarkForAddition(tAdd) end
      MrxLayerManager.ProcessMarkedLayers(function()
        F.Log("TerritorialWarInit", "layers processed: +" .. #tAdd .. " / -" .. #tRemove .. ", committing via WaitForStreaming")
        -- Pair the streaming state PROPERLY. Enter increments a refcount that only
        -- Exit decrements; the WaitForStreaming game-state-change fires the readyToExit
        -- callback (4th arg) but does NOT itself decrement -- so the readyToExit MUST
        -- call Exit, exactly how MrxTransit.StartTransit pairs it with FinishTransit
        -- (mrxtransit.lua:422). Entering with no readyToExit + never calling Exit orphans
        -- the refcount and the global fade-in never runs -- the original black-screen hang.
        MrxState.Enter(MrxState.STATE_WAITFORSTREAMING, nil, nil, function()
          MrxState.Exit(MrxState.STATE_WAITFORSTREAMING)
        end)
        MrxState.Exit(MrxState.STATE_WAITFORGAME) -- release the fade-holder; WAITFORSTREAMING clears itself above
        FireDone()
      end)
    end)
  end)
  if not bOk then FireDone() end
  -- Safety net: if ProcessMarkedLayers never calls back (e.g. every layer culled), the
  -- discovery handoff still runs so it isn't stranded. Framework tick, not a raw timer,
  -- to stay on the confirmed clock; FireDone is guarded so this is a no-op on the happy path.
  F.Schedule("TerritorialWarInit.HandoffGuard", 30, FireDone)
end

-- ===== Orchestration ============================================================
local function Handoff()
  local Outposts = F.GetState("TerritorialWarOutposts")
  if Outposts and Outposts.DiscoverOutposts then
    Outposts.DiscoverOutposts()
    F.Log("TerritorialWarInit", "handoff -> DiscoverOutposts()")
  else
    F.Log("TerritorialWarInit", "WARNING: TerritorialWarOutposts.DiscoverOutposts not found (load order?)")
  end
end

-- True while the player is inside the PMC HQ interior (the usual campaign start).
-- In there, the 14 outpost regions aren't streamed -- Pg.GetGuidByName misses them and
-- a WaitForStreaming has nothing to composite (this is the "4/19, all real outposts not
-- found" symptom). So the flip is deferred until the player is in the open world.
local function IsInHqInterior()
  local bInside = false
  pcall(function()
    import("WifPmcInterior")
    bInside = WifPmcInterior.IsInside()
  end)
  return bInside
end

local function IsStateLocked()
  local bLocked = false
  pcall(function()
    import("MrxState")
    bLocked = MrxState.IsLocked()
  end)
  return bLocked
end

-- The captured-layer flip + streaming reload, gated so it commits with the outpost
-- world actually streamed and no other MrxState transition in flight (so it can't stack
-- its fade on top of the HQ exit's own fade).
local function ApplyFlipWhenReady()
  if not IsInHqInterior() and not IsStateLocked() then
    ApplyLayersWithReload(Handoff)
    return
  end
  F.Log("TerritorialWarInit", "waiting for open world before flipping (in HQ / transition in flight)")
  F.Schedule("TerritorialWarInit.WaitForOutside", 5, function()
    if IsInHqInterior() or IsStateLocked() then return end
    F.Unschedule("TerritorialWarInit.WaitForOutside")
    F.Log("TerritorialWarInit", "open world reached -- applying world flip")
    ApplyLayersWithReload(Handoff)
  end)
end

-- Only the authoritative side re-writes world state; a client's world is driven by its
-- own local streaming + the sim's Net mirror, same gating as the rest of the mod.
local function RunHeavy()
  if not F.Net.IsAuthoritative() then
    F.Log("TerritorialWarInit", "non-authoritative side -- skipping world flip, mirror only")
    return
  end
  SetAttitudes()      -- safe from any context (no streaming needed)
  SetLandingZones()   -- ditto
  ApplyFlipWhenReady()
end

function I.ForceReinit()
  I.bDone = nil
  DisableSaves()
  I.bDone = true
  RunHeavy()
end

-- Bypass the open-world gate and flip NOW -- for triggering by hand from the control
-- script once you're already outside (or to retry after roaming so more regions have
-- streamed in). Safe to call repeatedly.
function I.ForceApplyNow()
  F.Unschedule("TerritorialWarInit.WaitForOutside")
  ApplyLayersWithReload(Handoff)
end

-- Save-block every load (idempotent). Heavy world flip once per session.
DisableSaves()
if not I.bDone then
  I.bDone = true
  RunHeavy()
  F.Log("TerritorialWarInit", "init complete (saves disabled, world flipped, discovery started)")
else
  F.Log("TerritorialWarInit", "already initialized this session -- saves re-blocked, world flip skipped")
end
```

## General lessons

1. **`MrxLayerManager.MarkForAddition`/`MarkForRemoval` are inert without a `WaitForStreaming`
   transition.** They only edit bookkeeping tables; nothing actually loads or unloads until
   `ProcessMarkedLayers` runs, and even that doesn't *composite* into the visible world without
   `MrxState.Enter(MrxState.STATE_WAITFORSTREAMING, ...)` (or the equivalent already-running mission-flow
   transition) somewhere in the sequence. An `OnLoad` script gets none of that machinery running for free.
2. **Every `MrxState.Enter` needs a reachable `Exit` for that exact state, confirmed via the refcount
   mechanics in `resident/mrxstate.lua`.** For `STATE_WAITFORSTREAMING` specifically, that pairing has to
   happen inside the `readyToExitCallback` (`Enter`'s 4th argument) — the native `"exit"` game-state event
   drives that callback, not a plain completion callback, and doesn't decrement the refcount on its own.
   Getting this wrong doesn't error; it silently hangs the fade-in forever.
3. **A layer's name is not a reliable guide to what it contains.** "Pristine" read as "not yet
   captured, therefore safe to remove" — it's actually the outpost's own base geometry, confirmed against
   the level's own default-dynamic-layer manifest. Removing it produced a real, confirmed-live bug
   (overlay floating over nothing) that a name-only reading wouldn't have predicted.
4. **`bDynamic` gates faction attitude mutability, and it's a static, source-readable table** —
   `resident/mrxfactionmanager.lua`'s `_tFactions`. No trial and error needed to find out which factions
   `SetAttitudeMutable` will actually affect.
5. **A landing zone's own location object survives layer changes that a named building doesn't.**
   `MrxTransit`'s `_tLandingZones` comes from `Pg.GetAllLandingZones`, entirely separate from any
   `vz_state_*` layer — useful as a position anchor specifically *because* it doesn't depend on whatever
   layer state a building's own name-lookup does.
6. **Disable autosave before any other world mutation, in a script that's still finding bugs.** Both
   confirmed bugs above happened live, during development — exactly the scenario autosave-blocking exists
   to contain the blast radius of.

## Open questions

- **Full end-to-end confirmation across a range of starting states.** The two bugs documented above are
  real, confirmed-live findings, which is good evidence this has actually been exercised in-game — but a
  clean run from a genuinely fresh campaign start, through every step in order, with no prior partial
  state left over from an earlier version of the script, hasn't been separately walked through here.
- **Co-op behavior is untested.** `RunHeavy` gates the whole world-mutating half of this on
  `F.Net.IsAuthoritative()`, matching the pattern already used elsewhere on this wiki for host-authoritative
  state — but whether a joining client's own local streaming actually converges to the same result the host
  just forced, without its own layer/state hiccups, is unconfirmed.
- **`I.ForceReinit()`/`I.ForceApplyNow()` repeat-triggering.** Both are written to be safe to call more
  than once (idempotent `MarkForAddition`, a fresh `ApplyLayersWithReload` each time), but repeated live
  triggering — especially `ForceReinit` after the world has already been roamed and possibly re-saved —
  hasn't been separately exercised.
- **Whether this generalizes past this specific 14-outpost table.** The layer names, LZ indices, and
  `keepVz` set here are one mod's specific configuration, sourced from `vz/*con05x.lua` and
  `vz/wifhqdata.lua` for this exact set of outposts. The *mechanism* (autosave lock, attitude mutability,
  layer-list-plus-reload, transit ownership, HQ-interior gate) should generalize to a different set of
  layers/locations; the data table itself won't.

## See also

- [`resident/mrxstate`](../resident/mrxstate) — the `Enter`/`Exit`/refcount API this script drives directly.
- [`resident/mrxfactionmanager`](../resident/mrxfactionmanager) — `SetAttitudeMutable`/`IsAttitudeMutable`
  and the full `_tFactions` table.
- [`resident/mrxtaskcontractoutpost`](../resident/mrxtaskcontractoutpost) — the real capture flow this
  script's layer choice mirrors.
- [`resident/mrxlayermanager`](../resident/mrxlayermanager) — `MarkForAddition`/`MarkForRemoval`/
  `ProcessMarkedLayers`, the layer-edit API this script's world flip is built on.
- [`resident/mrxtransit`](../resident/mrxtransit) — `SetLocationEnabled`/`_tLandingZones`, the landing-zone
  ownership and position-anchor system this script's discovery handoff relies on.
- [`resident/mrxoutpostmanager`](../resident/mrxoutpostmanager) — the native outpost-tracking counterpart
  this project's own war-sim discovery layer sits alongside.
