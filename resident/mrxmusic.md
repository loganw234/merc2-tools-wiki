---
title: MrxMusic
parent: Audio & Music
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [music, dynamic]
verified: true
verified_note: "deeper pass: re-confirmed all functions, the two documented bugs (bare sFaction / bare sNewState globals), the full cue table, and the single Event.CreatePersistent call against source; documented the music-cue naming convention + concrete state list, and cross-linked the Sound namespace and MrxSound (the state façade that drives this)"
---

# MrxMusic

*Module: mrxmusic.lua*

## Overview
The `MrxMusic` module manages dynamic music state: faction/freeplay music cue tables, action-level transitions, special music (fanfares, hijack stings, misc cues), and multiplayer sync of music state via custom net events. It drives the engine's [`Sound`](../namespaces/sound) music API (states, transitions, cues, playlists) and keeps clients in sync with the server's current music context. The high-level game-state façade [`MrxSound`](mrxsound) is what calls into this module (`_InitializeMusic`, `_DisableDynamicMusic`, `TransitionMusic`-triggering states, etc.).

### Music-cue naming convention
Every cue in `_tMusicCues` follows a fixed pattern, which is the useful thing to know if you're
retargeting music with `BindMusicCue`:
- **Faction cues:** `mu_fac_<faction>_<role>_NN` — e.g. `mu_fac_an_explore_01`, `mu_fac_gr_threat_01`,
  `mu_fac_pmc_win_01`, `mu_fac_oc_hijack_02`, `mu_fac_ch_kickass_01`. Faction codes seen: `an`, `oc`,
  `gr`, `ch`, `pmc`. Role words seen: `explore`, `threat`, `win`, `fail`, `hijack`, `kickass`.
- **Freeplay cues:** `mu_nomission_<region>_<role>_NN` — e.g. `mu_nomission_city_explore_01`,
  `mu_nomission_jungle_threat_02`, `mu_nomission_water_fail_01`. Regions: `city`, `jungle`, `water`.
- **Shell/UI:** `mu_shell_01` (reused for both the `shell` and `pause` states across every faction).

Note the cue *file* name (`mu_fac_an_threat_01`) differs from the internal *state* name (`action`): the
`threat`/`win`/`fail`/`kickass` audio-file words map to the `action`/`mission_success`/`mission_failure`/
`hijack_success` states, respectively.

## Inheritance
- Inherits from: `none — base/utility module` (no `inherit(...)` call in the file)
- Imports: none — no `import(...)` calls appear anywhere in this file. [`Sound`](../namespaces/sound), [`Net`](../namespaces/net), `Debug`, `String`, and [`Player`](../namespaces/player) are used throughout but are engine-provided global namespaces, not modules this file imports.

## Instance pattern
Stateless singleton/utility module — plain module-level globals, no `Create`/`OnActivate`/`Awake`/`tInstance`. Key fields:
- `NETEVENT_ENTERFREEPLAY` / `NETEVENT_ENTERCONTRACT` / `NETEVENT_PLAYSPECIALMUSIC` / `NETEVENT_STOPSPECIALMUSIC`: integer constants (0-3) identifying custom net-event types sent via `Net.SendCustomEvent("MrxMusic", ...)` and dispatched by `NetEventCallback`. Not `Event.*` system events.
- `_bPrevDynamic`: dynamic-music-enabled flag saved/restored by `_DisableDynamicMusic`/`_RestoreDynamicMusic`.
- `_tMusicCues`: nested table of music cue names, keyed `factions.<an|oc|gr|ch|pmc>.<state>` and `freeplay.<freeplay_city|freeplay_jungle|freeplay_water>.<state>`, each a list of 1-3 cue name strings (e.g. `"mu_fac_an_explore_01"`). States per faction: `explore`, `action`, `mission_success`, `mission_failure`, `hijack`, `hijack_success`, `shell`, `pause`. Freeplay entries additionally have `high_action`.
- `_sRootFactionRegion`: `"freeplay_city"` — passed to `Sound.SetRootFactionRegionMusic` in `_InitializeMusic`.
- `_sSourceMusicState`: `"source"` — passed to `Sound.SetSourceMusic`.
- `_tSourceMusicTransitions`: list of `{entryState, exitState}` pairs (`none`/`none`, `silence`/`silence`, `explore`/`explore`) applied in `_InitializeMusic` via either `Sound.AddSourceMusicEntryState` (lib version >= 11) or `Sound.SetSourceMusicTransition` (older).
- `_sHijackSuccessMusicState` / `_sHijackResumeMusicState`: `"hijack_success"` / `"hijack_success_resume"`, passed to `Sound.SetHijackMusic`.
- `_fNonActionInterval` / `_fActionInterval`: `5` / `15`, tunable via `SetMusicActionInterval` (only `_fActionInterval` is settable; `_fNonActionInterval` has no setter).
- `_tMiscMusicStates`: `{"misc1", "misc2"}` — two slots special/misc music cycles between.
- `_evClientJoined`: handle for the persistent `Event.ScriptEvent` "mpPlayerJoin" listener created in `_InitializeMusic` (server-only, created once).
- `_bPrevFactionLock`: faction-lock state saved before special music plays, restored in `_CleanupSpecialMusic`.
- `_iCurrentMiscMusicIndex`: 0 (idle) or 1/2, current slot in `_tMiscMusicStates` used for special music.
- `_bPlayingSpecialMusic`: whether special music is currently active.
- `_sCurrentContractFaction`, `_sCurrentMusicCue`, `_sStopSpecialMusicCue`: server-side globals set by `EnterContractMusic`/`EnterFreeplayMusic`, `PlaySpecialMusic`, and `StopSpecialMusic` respectively — not initialized at load time, only assigned once those functions run on the server.

## Functions
### `_DisableDynamicMusic()`
Saves `Sound.IsDynamicMusic()` into `_bPrevDynamic`, then disables dynamic music.

### `_RestoreDynamicMusic()`
Restores dynamic music to whatever `_bPrevDynamic` holds.

### `SetMusicActionInterval(fActionInterval)`
Sets `_fActionInterval` if `fActionInterval >= 0`; otherwise logs a `Debug.Printf` warning and leaves the existing value unchanged.

### `BindMusicCue(sFaction, sState, iCueIndex, sCue)`
Requires `0 < iCueIndex < 4`. Searches all of `_tMusicCues` (both `factions` and `freeplay` categories) for a matching faction/state pair and overwrites `cueTable[iCueIndex] = sCue`. Logs a warning via `Debug.Printf` if the faction/state isn't found, or if `iCueIndex` is out of range.

### `_InitializeMusic()`
Top-level setup, expected to run once. For every faction in `_tMusicCues.factions`, calls `_InitializeFaction` then `_BindMusicStateCues`. Same for every freeplay region in `_tMusicCues.freeplay` via `_InitializeFreeplay`. Sets root faction region and source music (`Sound.SetRootFactionRegionMusic`, `Sound.SetSourceMusic`), then configures source-music transitions using the version-appropriate `Sound` API (`Sound._GetLibVersion() >= 11` branches to `AddSourceMusicEntryState`, else `SetSourceMusicTransition`). Calls `Sound.SetHijackMusic(_sHijackSuccessMusicState, _sHijackResumeMusicState)`. If running as server and `_evClientJoined` isn't already set, creates a persistent `Event.ScriptEvent` listener for `"mpPlayerJoin"` (guarded so it only fires for non-local players when this instance is the server) that calls `SendPlayerJoinEvents` when a player joins.

### `SendPlayerJoinEvents()`
Sends catch-up net events to a newly joined player: `NETEVENT_ENTERCONTRACT` with `{sFaction}` if the bare global `sFaction` is truthy, else `NETEVENT_ENTERFREEPLAY`. Then `NETEVENT_PLAYSPECIALMUSIC` with `{_sCurrentMusicCue}` if `_sCurrentMusicCue` is set, else `NETEVENT_STOPSPECIALMUSIC` with `{_sStopSpecialMusicCue or "silence", 0}`.

**Likely bug**: the `sFaction` checked at the top of this function (no leading underscore) is never assigned anywhere in this file — `_sCurrentContractFaction` is the variable actually set by `EnterContractMusic`/`EnterFreeplayMusic`. As written, `sFaction` reads as an always-`nil` global, so the `NETEVENT_ENTERCONTRACT` branch is dead code and this function always tells a joining player they're in freeplay, even mid-contract. No other assignment to a bare `sFaction` global exists in this file.

### `_InitializeFaction(sFaction)`
Registers a full faction music state machine via `Sound.AddFactionMusic`/`AddMusicState`/`SetActionThresholdsMusic`/`AddMusicTransition` calls: states `none, explore, action, mission_success, mission_failure, hijack, hijack_success, hijack_success_resume, source, shell, misc1, misc2, pause, silence`, plus transitions between them (none↔explore, explore→action, hijack_success→explore/hijack_success_resume, etc.).

### `_InitializeFreeplay(sFreeplay)`
Same as `_InitializeFaction` but also registers a `high_action` state and its transitions (none/explore/source/action ↔ high_action) — the escalation level that factions don't have.

### `_BindMusicStateCues(sFaction, tCues)`
Calls `Sound.SetFactionMusic(sFaction)`, then for every state/cue-list pair in `tCues`, calls `Sound.BindMusicCue(cue, state)` for each cue in the list.

### `Reset()`
Re-enables dynamic music (`Sound.SetDynamicMusic(true)`, resets `_bPrevDynamic` to `true`), calls `_CleanupSpecialMusic()`, clears faction lock (`_bPrevFactionLock = false`, `Sound.LockFactionMusic(false)`), and resets action-level music (`Sound.SetActionLevelsMusic(0,0,0,0)`, `Sound.LockActionLevelMusic(false)`).

### `EnterFreeplayMusic()`
Logs via `Debug.Printf`, calls `Reset()`, activates faction-region music, transitions to `"explore"`. If server: clears `_sCurrentContractFaction` and sends `NETEVENT_ENTERFREEPLAY`.

### `EnterContractMusic(sFaction)`
Logs via `Debug.Printf`, sets/locks faction music to `sFaction`, transitions to `"explore"`. If server: sets `_sCurrentContractFaction = sFaction` and sends `NETEVENT_ENTERCONTRACT` with `{sFaction}`.

### `PlayFanfare(bMissionSuccess)`
Calls `_CleanupSpecialMusic()`, then transitions (with the `true` "force" flag) to `"mission_success"` or `"mission_failure"` depending on `bMissionSuccess`.

### `PlaySpecialMusic(sMusicCue)`
Logs via `Debug.Printf`. If not already in the middle of special music (`_iCurrentMiscMusicIndex == 0`), saves the current faction-lock state into `_bPrevFactionLock`. Locks faction music, advances the misc-music slot via `_SetMiscMusicIndex()`, clears and rebinds that slot's cue to `sMusicCue`, transitions to it. If server: sets `_sCurrentMusicCue = sMusicCue` and sends `NETEVENT_PLAYSPECIALMUSIC`. Sets `_bPlayingSpecialMusic = true`.

### `_SetMiscMusicIndex()`
Toggles `_iCurrentMiscMusicIndex` between the two `_tMiscMusicStates` slots: if currently `> 1` (i.e. `2`), decrements to `1`; otherwise increments (covers both the initial `0` and the `1` case, both becoming/staying `1` then `2` on alternating calls — net effect is it alternates `1, 2, 1, 2, ...` once started from `0`).

### `_ResumeSpecialMusic()`
If `_bPlayingSpecialMusic`, re-transitions to the current misc music slot (`_tMiscMusicStates[_iCurrentMiscMusicIndex]`).

### `_IsPlayingSpecialMusic()`
Returns `_bPlayingSpecialMusic`.

### `StopSpecialMusic(sNewState)`
If `_bPlayingSpecialMusic`: logs via `Debug.Printf`, calls `_CleanupSpecialMusic()`, transitions to `sNewState` if given, else `"none"`. If server: clears `_sCurrentMusicCue`, sets `_sStopSpecialMusicCue = sNewState`, sends `NETEVENT_STOPSPECIALMUSIC` with `{sNewState or "none", 0}`.

### `_CleanupSpecialMusic()`
If `_bPlayingSpecialMusic`: restores faction lock to `_bPrevFactionLock`, resets `_iCurrentMiscMusicIndex` to `0`, sets `_bPlayingSpecialMusic = false`. If server: clears `_sCurrentMusicCue`, sends `NETEVENT_STOPSPECIALMUSIC` with `{sNewState or "none", 1}`.

**Likely bug**: `_CleanupSpecialMusic` takes no parameters and has no local `sNewState`. It references a bare global `sNewState` that is never assigned anywhere in this file — `StopSpecialMusic`'s parameter of the same name is a *different*, function-local variable and isn't visible here (this codebase's Lua has no closures capturing sibling-call locals that way). So the `sNewState or "none"` in this function always evaluates to `"none"`, regardless of what state `StopSpecialMusic` was asked to transition to. The net event this sends therefore always reports `"none"` even when `StopSpecialMusic` was called with a real target state — clients that use `GetStateByStringHash` on this payload would resolve back to `"silence"` (its no-match fallback) rather than the actual intended state, unless "none" itself hashes to a state.

### `AddMusicPlaylist(sPlaylist, fGap)`
Wraps `Sound.AddMusicSourcePlaylist(sPlaylist, fGap)`.

### `BindPlaylistCue(sPlaylist, sCue)`
Wraps `Sound.AddCueToMusicSourcePlaylist(sPlaylist, sCue)`.

### `ClearMusicPlaylist(sPlaylist)`
Wraps `Sound.ClearMusicSourcePlaylist(sPlaylist)`.

### `GetFactionByStringHash(uFactionStringHash)`
Searches every category/faction key in `_tMusicCues` for one whose `String.GetHash(faction)` matches. Returns the faction name string, or `nil` if none match.

### `GetStateByStringHash(uStateStringHash)`
Searches every category/faction/state key in `_tMusicCues` for one whose `String.GetHash(state)` matches. Returns the state name string, or `"silence"` if none match (unlike `GetFactionByStringHash`, which returns `nil` on no match — different fallback conventions between the two).

### `NetEventCallback(nEventType, tArgs)`
Dispatches on `nEventType` (one of the four `NETEVENT_*` constants): calls `EnterFreeplayMusic()`; or resolves `tArgs[1]` via `GetFactionByStringHash` and calls `EnterContractMusic(sFaction)` (asserting via `ASSERT(0, ...)` if the hash doesn't resolve); or calls `PlaySpecialMusic(tArgs[1])`; or resolves `tArgs[1]` via `GetStateByStringHash` and calls either `_CleanupSpecialMusic()` (if `tArgs[2] == 1`) or `StopSpecialMusic(sNewState)`.

## Events
Only one real `Event.*` call exists in this file: `Event.CreatePersistent(Event.ScriptEvent, {"mpPlayerJoin", <guard fn>}, SendPlayerJoinEvents)` inside `_InitializeMusic`, registered once, server-side only. The guard function restricts it to firing for non-local players when `Net.IsServer()`.

The four `NETEVENT_*` constants are **not** `Event.*` system events — they're integer codes for this module's own custom-event channel, sent with `Net.SendCustomEvent("MrxMusic", <code>, <args>, true)` and received via `NetEventCallback(nEventType, tArgs)` (presumably wired up as the handler for net events on the `"MrxMusic"` channel by engine/bootstrap code not visible in this file — no explicit registration of `NetEventCallback` as a net-event handler appears here). The four codes:
- `NETEVENT_ENTERFREEPLAY` (0) — sent by `EnterFreeplayMusic`, `SendPlayerJoinEvents`; handled by dispatching to `EnterFreeplayMusic()`.
- `NETEVENT_ENTERCONTRACT` (1) — sent by `EnterContractMusic`, `SendPlayerJoinEvents`; handled by resolving the faction and calling `EnterContractMusic(sFaction)`.
- `NETEVENT_PLAYSPECIALMUSIC` (2) — sent by `PlaySpecialMusic`, `SendPlayerJoinEvents`; handled by calling `PlaySpecialMusic(tArgs[1])`.
- `NETEVENT_STOPSPECIALMUSIC` (3) — sent by `StopSpecialMusic`, `_CleanupSpecialMusic`, `SendPlayerJoinEvents`; handled by calling `_CleanupSpecialMusic()` or `StopSpecialMusic(...)` depending on a second flag argument.

## Notes for modders
- Call-order: `_InitializeMusic()` must run once before other functions are meaningful — it's what registers all the `Sound.AddMusicState`/`AddMusicTransition`/`BindMusicCue` data with the engine's audio system.
- `BindMusicCue` lets you retarget which sound file plays for a given faction/state/index at runtime without re-running `_InitializeMusic`.
- `SetMusicActionInterval` is the only tunable with a public setter; `_fNonActionInterval` and the two threshold/transition tables have no setters and would need direct global reassignment before `_InitializeMusic()` runs to take effect.
- Two likely bugs found by reading the source (see Functions section for detail): `SendPlayerJoinEvents` checks an unassigned global `sFaction` instead of `_sCurrentContractFaction`, so it never sends the contract-catch-up event to newly joined players; and `_CleanupSpecialMusic` references an unassigned global `sNewState` instead of taking it as a parameter, so its `NETEVENT_STOPSPECIALMUSIC` payload always reports `"none"`.
- `GetFactionByStringHash` and `GetStateByStringHash` have different no-match fallbacks (`nil` vs `"silence"`) — don't assume symmetry if you're calling both.
