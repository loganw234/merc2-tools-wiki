---
title: WifMissionFlow
parent: World & Mission Flow
grand_parent: VZ Modules
nav_order: 2
inherits: MrxMissionFlow
tags: [world-flow]
verified: false
---

# WifMissionFlow

## Overview
`WifMissionFlow` is the single-player campaign's critical-path controller — a save-driven "key" graph
where completing one contract awards a key, which satisfies another entry's prerequisite, which runs
that entry's consequence (unlock the next contract(s), play a cutscene, swap world-state layers, grant an
achievement, adjust Fiona's hint pool, and so on). Nearly the entire file is one function,
`GetOriginalFlowData()`, that builds and returns this graph; a handful of smaller helpers and a
networked end-game-credits handshake round out the rest.

## Inheritance
- Inherits from: [`MrxMissionFlow`](../resident/mrxmissionflow) — a real `resident/` module (see that
  page for the base class's own behavior), the same way several vz/ contract files inherit from
  documented native task-framework classes like `MrxTaskJobDestroyType`. **This is the one file in this
  "World & Mission Flow" batch that actually uses `inherit()`** — contrast with its `wif*`/`xQ!L`
  siblings, which are plain data/utility modules with no `inherit()` at all.
- Imports: `MrxCinematic`, `MrxFactionManager`, `MrxGui`, `MrxGuiBase`, `MrxLayerManager`, `MrxPlayState`,
  `MrxStarterManager`, `MrxState`, `MrxSupportData`, `MrxUtil`, `MrxTransit`, `MrxVoSequence`,
  `Munitions`, `WifVzBoundary`, [`WifPmcInterior`](wifpmcinterior) (imported twice — both line-16 and
  line-22 say `import("WifPmcInterior")`; a harmless duplicate visible in the decompiled source),
  `MrxAchievements`, `MrxVerifyManager`, [`WifHints`](wifhints), `MrxSoundBootstrap`, [`WifBios`](wifbios),
  `MrxSoundCategories`, `MrxMusic`, `friendlygate`. `MrxHqManager` is also called directly (inside the
  `OilCon002` flow entry) without ever being `import()`-ed in this file — everything here resolves
  through shared globals once loaded, so `import()` reads more like a load-order declaration than a
  strict access requirement, but its absence for `MrxHqManager` specifically stands out next to this
  file's otherwise-thorough import list.

## Instance pattern
Singleton — one mission flow per game session, no `uGuid`. Its persistent "key" state (`HasKey`/
`AwardKey`/`GetKeyValue`) lives in the native `MrxMissionFlow` base, not in this file. A long list of
methods are called throughout this file's own code without ever being *defined* here — `HasKey`,
`AwardKey`, `GetKeyValue`, `UnlockMission`, `DestroyMission`, `SetFlowData`, `GetMissionStartLocations`,
`EnableResourceCounters`/`AreResourceCountersEnabled`, `SetGrappleEnabled`/`IsGrappleEnabled`,
`SetVehicleDisguiseEnabled`/`IsVehicleDisguiseEnabled`, `GetMissionStates`, `SaveSingleton`/
`LoadSingleton`, `_BeginBlockingSequence`/`_EndBlockingSequence` — all of these resolve through the
`inherit("MrxMissionFlow")` fallback to the native base class: called bare inside this file, and reached
via ordinary dot-access (`WifMissionFlow.SaveSingleton()`) from outside it.

## Functions

### `GetOriginalFlowData()`
Builds and returns the entire flow graph fresh: a table keyed by mission id or milestone-combo id (e.g.
`"PmcCon002_JetIntro"`), each entry `{ fPrereq = function() ... end, fConseq = function() ... end }`
(`fConseq` is optional — a few entries, like `PmcJob001`, have only `fPrereq`). Representative entries,
verbatim:

```lua
Start = {
  fPrereq = function()
    return true
  end,
  fConseq = function()
    -- plays the opening movie, sets up the three heroes' starting dossiers/state, unlocks VzaCon001
  end
},
```

```lua
GurCon001 = {
  fPrereq = function()
    return HasKey("GurCon001")
  end,
  fConseq = function()
    WifHints.RemoveActiveHint("FionaHint11")
    WifHints.RemoveActiveHint("FionaHint13")
    MrxSoundBootstrap.SetPmcRadio("ReporterNeutral.MissionVO.Gur01")
    MrxLayerManager.MarkForRemoval({"vz_state_gurcon001_fortress", "vz_state_gurcon001_staging", "Vz_State_GurCon001"})
    MrxLayerManager.MarkForAddition("vz_state_gurcon001_fortress_destroyed")
  end
},
```

```lua
PmcCon031_x3 = {
  fPrereq = function()
    return GetKeyValue("PmcCon031") >= 3
  end,
  fConseq = _AddHeroCostume
},
```

Most `fPrereq` functions are just `HasKey("SomeMissionId")`; a few combine conditions
(`HasKey(...) and HasKey(...) and not HasKey(...)`) to gate multi-step unlocks, and the `_x3` entries use
`GetKeyValue(id) >= 3` to detect a repeatable contract's 3rd completion. `fConseq` bodies commonly: play
an FMV through `_PlayMovie`, wrap the whole thing in `_BeginBlockingSequence`/`_EndBlockingSequence`
around `MrxState.Enter`/`Exit(MrxState.STATE_WAITFORGAME, ...)`, unlock the next mission(s) via
`UnlockMission`, swap world layers via `MrxLayerManager.MarkForRemoval`/`MarkForAddition`, and update
Fiona's hint pool via [`WifHints`](wifhints).

Almost every `fConseq` checks `MrxCheatBootstrap.IsSkipModeEnabled()` first and skips the cutscene/
state-transition machinery entirely when true, running its callback immediately instead — that's the
mission-skip debug cheat (see `resident/mrxcheatbootstrap` and [`WifCheatStockpile`](wifcheatstockpile))
short-circuiting the normal story presentation.

### `Reset(bResetMore)`
Calls `MrxMissionFlow.Reset(bResetMore)` — an **explicit, qualified** call to the base implementation,
needed because this file's own `Reset` overrides it and a bare `Reset(bResetMore)` here would recurse
into itself — then `SetFlowData(GetOriginalFlowData())` (bare; not overridden in this file, so the
inherited setter is reached directly) to reload the flow graph from scratch.

### `_AddIntro(sStarterName, sIntroName)` / `_RemoveIntro(sStarterName, sIntroName)`
Look up a starter object via `MrxStarterManager.GetStarter` and add/remove a named "intro" flag on it.
`_AddIntro` also immediately marks the intro as already-viewed when skip mode is active, so cheat-skipping
past a mission doesn't leave a stale unviewed-intro popup behind.

### `_PlayMovie(tArgs)`
Plays an FMV via `Hud.Cinematic:Show(...)` — unless skip mode is enabled, in which case it calls
`tArgs.fCallback` directly (via `MrxUtil.CallWithOptionalArgs`) and skips the movie entirely.

### `_ChangeOutpostStaging(fCallback, tCallbackArgs)`
Normally just forwards straight to `fCallback`. Only diverges under skip mode, where it instead runs
`MrxLayerManager.ProcessMarkedLayers(...)` first — under normal play the layer-processing that accompanies
an outpost capture is presumably already driven elsewhere, and this function only needs to force it
through when skip mode has bypassed that other path.

### `_AddHeroCostume()`
Bumps [`WifPmcInterior`](wifpmcinterior)'s available-costume count by one (`GetAvailableCostumes`/
`SetAvailableCostumes`) and fires an unlock-fanfare toast (`MrxUnlockFanfare.AddUnlockedItem`) for each
costume that comes back unlocked. Used as the `fConseq` for the `PmcCon03x_x3` milestone entries.

### `NetEventCallback(nEventType)` / `_ClientStartCredits()` / `_ClientEndCredits(oCredits)` / `_ClientQuitToShell(oCredits)`
Multiplayer credits handshake: the host plays the ending credits locally (inside `PmcCon004`'s
`fConseq`) and sends a custom net event (`NETEVENT_CLIENTCREDITS`) so clients independently show the same
credits sequence and quit to shell afterward, instead of just being dropped when the host's session ends.

## Events
`Event.GameStateChange` (the `NETEVENT_CLIENTCREDITS` handler waits for the `"cinematic"`/`"exit"` state
change before starting client credits) is the only direct `Event.*` call in this file; everything else
that looks event-like (`MrxState.Enter`/`Exit`, blocking sequences) is delegated to imported/inherited
systems instead.

## Notes for modders
- The hero-letter substitution (`sHeroLetter`, from `MrxUtil.GetCharacterIdentity(Player.GetPrimaryCharacter())`,
  first letter, defaulting to `"M"` unless it's `"M"`/`"J"`/`"C"`) is how movie filenames like
  `"01_AOA_" .. sHeroLetter` pick the right voice-actor cut for whichever hero the player is playing.
- Cross-references heavily with [`WifHints`](wifhints) (hint-pool swaps at nearly every story beat),
  [`WifBios`](wifbios) (dossier unlocks), and `MrxSoundBootstrap.SetPmcRadio` (over a dozen calls swapping
  the PMC radio playlist to a mission-specific VO cue).
- This file is the mission-*unlock* side of the mission-skip cheat: `MrxCheatBootstrap` reads
  [`WifCheatStockpile`](wifcheatstockpile) to reset the player's cash/support/equipment when
  skip-jumping, while this file's `IsSkipModeEnabled()` checks throughout `GetOriginalFlowData()` are
  what let that same jump skip every cutscene/state-transition along the way instead of just the resource
  grant.
- If you need this file's own inherited helpers (`HasKey`, `UnlockMission`, etc.) from outside it, call
  them the normal way — `WifMissionFlow.HasKey(...)` — the metatable fallback that makes bare calls work
  inside this file works for external dot-access too.
