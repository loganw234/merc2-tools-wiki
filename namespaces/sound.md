---
title: Sound
parent: Engine Namespaces
nav_order: 8
---

# Sound

## Overview

`Sound` is an **engine namespace**, not a `resident/` module — there's no `.lua` source file behind it,
no `import()` call needed, and it's always globally available to every script. Its functions cover the
game's dynamic music system (action-level and faction-based music state, transitions, source-music
playlists, fade/pitch categories), direct sound and ambience cueing/playback, sound and wave bank
loading, and audio mixing/reverb configuration.

## Provenance

This page's function list comes from a live `pairs(Sound)` enumeration in-game (via lua-bridge), not from
reading engine source — the engine implementation isn't available to us. That means the list of 88 function
names below is complete and authoritative: every one of them really exists on the namespace. It does **not**
mean every entry is documented with confirmed arguments. Where a function is actually called somewhere in
the ~230 decompiled `.lua` scripts, we can show a real argument pattern. Where it isn't called anywhere in
that corpus, we only know the name — arguments, return values, and behavior for those are unconfirmed.

Two modules dominate the call-site evidence on this page: `mrxmusic.lua` (the dynamic music state/transition
system) and `mrxsound.lua` / `mrxsoundcategories.lua` / `mrxsoundbanks.lua` (cueing, categories, bank
loading). Each of these exists twice in the decompiled corpus, once under `shell/` and once under
`resident/`, with identical line numbers and content in every call site checked — the two copies appear to
be the same module shipped/decompiled into both locations rather than two different implementations.

## Functions

### Direct Sound & Ambience Cueing

| Function | Signature (best-known) | Notes |
|---|---|---|
| `CueSound` | `Sound.CueSound(uGuid, sCueName)` | Extremely common in real scripts. Used both with a real object `uGuid` (e.g. `Sound.CueSound(uGuid, "fol_bldg_alarm_activate")` in `resident/alarm.lua`) and with a literal `0` for UI/HUD-attached one-shots (e.g. `Sound.CueSound(0, _ksAcceptSound)` throughout `shell/mrxguidialogbox.lua`, `shell/mrxguinumericbox.lua`). Also used as a bare event callback: `Event.Create(Event.TimerRelative, {1}, Sound.CueSound, {uGuid, sCue})` in `resident/beacon.lua` and `resident/Init.lua`. |
| `StopSound` | `Sound.StopSound(uGuid, sCueName)` | Common in real scripts, always paired with a prior `CueSound` on the same `(uGuid, sCueName)` pair, e.g. `resident/alarm.lua`, `resident/mine.lua`, `resident/jammer.lua`. Also used with `0` for UI sounds (e.g. `resident/mrxguihudreticle.lua`, `resident/mrxguisatellite.lua`). |
| `PauseSound` | `Sound.PauseSound(uGuid, sCueName)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to `CueSound`/`StopSound`. |
| `TestCueSound` | `Sound.TestCueSound(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. The `Test` prefix suggests a debug/dev-console variant of `CueSound`. |
| `TestPauseSound` | `Sound.TestPauseSound(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed debug/dev-console variant of `PauseSound`, by naming only. |
| `TestStopSound` | `Sound.TestStopSound(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed debug/dev-console variant of `StopSound`, by naming only. |
| `CueAmbience` | `Sound.CueAmbience(sAmbienceStreamName)` | Confirmed in real scripts with a single string argument, e.g. `Sound.CueAmbience(ksMissionAmbience)` (`vz/oilcon001.lua`), `Sound.CueAmbience(sAmbienceStream)` (`vz/wifvzambience.lua`). |
| `StopAmbience` | `Sound.StopAmbience(sAmbienceStreamName)` | Confirmed in real scripts, always paired with a prior `CueAmbience` on the same name, e.g. `Sound.StopAmbience(ksMissionAmbience)` (`vz/oilcon001.lua`), `Sound.StopAmbience(sAmbienceStream)` (`vz/wifvzambience.lua`). |
| `SilenceAmbience` | `Sound.SilenceAmbience(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed a mute/duck variant distinct from `StopAmbience`, by naming only. |
| `StopAndFlushAllSounds` | `Sound.StopAndFlushAllSounds()` | Confirmed in real scripts with no arguments, always guarded by an existence check: `if Sound.StopAndFlushAllSounds then Sound.StopAndFlushAllSounds() end` (`resident/mrxhq.lua`, `vz/wifpmcinterior.lua`) — the guard pattern implies this function was added in a later game build than some of the calling code. |
| `RequestAmbienceBank` | `Sound.RequestAmbienceBank(sBankName)` | Confirmed with a single localized bank-name string in real scripts: `Sound.RequestAmbienceBank(_GetLocalizedName(sBank))` (`shell/mrxsoundbanks.lua`). |
| `SetVehicleEngineBoost` | `Sound.SetVehicleEngineBoost(uGuid, nBoostLevel)` | Confirmed with a vehicle `uGuid` and a numeric level (observed as `0` and `1`) in `resident/spyhunter.lua`, always guarded: `if Sound.SetVehicleEngineBoost then Sound.SetVehicleEngineBoost(uGuid, 0) end` — same late-addition guard pattern as `StopAndFlushAllSounds`. |

### Dynamic Music System

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetDynamicMusic` | `Sound.SetDynamicMusic(bEnabled)` | Very common in real scripts, a single boolean, e.g. `Sound.SetDynamicMusic(false)` / `Sound.SetDynamicMusic(true)` in `resident/mrxsound.lua`, `resident/mrxmusic.lua`, and multiple `vz/*.lua` mission scripts. |
| `IsDynamicMusic` | `b = Sound.IsDynamicMusic()` | Confirmed with no arguments, used to snapshot prior state before a temporary override: `_bPrevDynamic = Sound.IsDynamicMusic()` (`resident/mrxmusic.lua`). |
| `SetActionLevelsMusic` | `Sound.SetActionLevelsMusic(nLevel, n2, n3, n4)` | Confirmed with 4 numeric arguments in real scripts, e.g. `Sound.SetActionLevelsMusic(3, 0, 0, 0)` (`vz/allcon001.lua`), `Sound.SetActionLevelsMusic(15, 0, 0, 0)` (`vz/chicon002.lua`), `Sound.SetActionLevelsMusic(10, 0, 0, 0)` (`vz/jetcon001.lua`). The first argument varies by call site (observed 0, 3, 10, 15) and appears to force/raise the current action level; the meaning of the trailing three (always `0` at every call site seen) is not confirmed. |
| `LockActionLevelMusic` | `Sound.LockActionLevelMusic(bLocked)` | Very common in real scripts, a single boolean, consistently paired with `SetActionLevelsMusic` to hold a forced action level for a duration, e.g. `resident/mrxsound.lua` (hijack music), `vz/allcon001.lua`, `vz/jetcon001.lua`, `vz/oilcon003.lua`. One call site passes it directly as an event callback: `Event.Create(Event.TimerRelative, {nEndTime}, Sound.LockActionLevelMusic, {false})`. |
| `IsActionLevelLockedMusic` | `b = Sound.IsActionLevelLockedMusic()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed getter counterpart to `LockActionLevelMusic`, by naming only. |
| `SetActionThresholdsMusic` | `Sound.SetActionThresholdsMusic(sState, n2, n3)` | Confirmed with a state-name string and 2 numeric arguments in real scripts, always as `Sound.SetActionThresholdsMusic("none", 2, 0)` and `Sound.SetActionThresholdsMusic("explore", 2, 0)` (`shell/mrxmusic.lua`) — only these two exact state names appear at any call site. |
| `AddMusicState` | `Sound.AddMusicState(sState, n1, n2, n3, n4, n5)` | Confirmed with a state-name string and 5 numeric arguments in real scripts, called for a fixed set of states during music-system init (`"none"`, `"explore"`, `"action"`, `"high_action"`, `"mission_success"`, `"mission_failure"`, `"hijack"`, `"hijack_success"`, `"hijack_success_resume"`, `"source"`, `"shell"`, `"pause"`, `"silence"`, plus two runtime-selected "misc" states) in `shell/mrxmusic.lua`. The exact meaning of each numeric slot (duration/priority/fade-in/interval/fade-out are plausible guesses given typical music-state systems) is not confirmed by call-site evidence alone. |
| `AddMusicTransition` | `Sound.AddMusicTransition(sFromState, sToState, n1, n2, n3)` | Confirmed with two state-name strings and 3 numeric arguments in real scripts, defining the legal state graph (e.g. `Sound.AddMusicTransition("none", "explore", 1, 1, 0)`, `Sound.AddMusicTransition("hijack_success", "hijack_success_resume", 1, 1, 0)`) in `shell/mrxmusic.lua`. Numeric argument meanings not confirmed. |
| `TransitionMusic` | `Sound.TransitionMusic(sState [, bFlag])` | Very common in real scripts — the actual trigger that moves the music state machine, e.g. `Sound.TransitionMusic("hijack")` guarding vehicle-hijack music in `resident/mrxsound.lua:BeginActionHijack`, `Sound.TransitionMusic("hijack_success")` / `Sound.TransitionMusic("action")` in the matching `EndActionHijack`, and `Sound.TransitionMusic("mission_success", true)` / `Sound.TransitionMusic("mission_failure", true)` (`shell/mrxmusic.lua`, `vz/mecjob.lua`) with a trailing boolean whose meaning is unconfirmed. State names passed are always ones previously registered via `AddMusicState`. |
| `ForceActionTransition` | `Sound.ForceActionTransition(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed a forced variant of `TransitionMusic` restricted to action-level states, by naming only. |
| `BindMusicCue` | `Sound.BindMusicCue(sCue, sState)` | Confirmed with a cue string and a state string in real scripts, e.g. `Sound.BindMusicCue(cue, state)` (loop over a cue table) and `Sound.BindMusicCue(sMusicCue, _tMiscMusicStates[_iCurrentMiscMusicIndex])`, both in `shell/mrxmusic.lua`. |
| `ClearMusicCues` | `Sound.ClearMusicCues(sState)` | Confirmed with a single state-name string in real scripts: `Sound.ClearMusicCues(_tMiscMusicStates[_iCurrentMiscMusicIndex])` (`shell/mrxmusic.lua`), immediately followed by a `BindMusicCue` re-bind. |
| `AddFactionMusic` | `Sound.AddFactionMusic(sFaction)` | Confirmed with a single faction/freeplay-name string in real scripts, e.g. `Sound.AddFactionMusic(sFaction)`, `Sound.AddFactionMusic(sFreeplay)` (`shell/mrxmusic.lua`, during music-system init). |
| `SetFactionMusic` | `Sound.SetFactionMusic(sFaction)` | Confirmed with a single faction-name string in real scripts, e.g. `Sound.SetFactionMusic(sFaction)` (`shell/mrxmusic.lua`). |
| `LockFactionMusic` | `Sound.LockFactionMusic(bLocked)` | Confirmed with a single boolean in real scripts, used to hold a forced faction-music selection, e.g. `Sound.LockFactionMusic(true)` / `Sound.LockFactionMusic(false)` (`shell/mrxmusic.lua`). |
| `IsFactionLockedMusic` | `b = Sound.IsFactionLockedMusic()` | Confirmed with no arguments in real scripts, used to snapshot prior lock state before a temporary override: `_bPrevFactionLock = Sound.IsFactionLockedMusic()` (`shell/mrxmusic.lua`). |
| `ActivateFactionRegionMusic` | `Sound.ActivateFactionRegionMusic()` | Confirmed with no arguments in real scripts, called immediately after `SetFactionMusic`/`LockFactionMusic(false)` to commit the region's faction music (`shell/mrxmusic.lua`). |
| `SetRootFactionRegionMusic` | `Sound.SetRootFactionRegionMusic(sRootFaction)` | Confirmed with a single faction-name string in real scripts, called once during music-system init: `Sound.SetRootFactionRegionMusic(_sRootFactionRegion)` (`shell/mrxmusic.lua`). |
| `SetHostilityDecayRateMusic` | `Sound.SetHostilityDecayRateMusic(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetHijackMusic` | `Sound.SetHijackMusic(sSuccessMusicState, sResumeMusicState)` | Confirmed with two state-name strings in real scripts: `Sound.SetHijackMusic(_sHijackSuccessMusicState, _sHijackResumeMusicState)`, called once during music-system init in `shell/mrxmusic.lua`/`resident/mrxmusic.lua`. This registers which music states back the hijack-success/resume music; it is **not** called from the same module as `Vehicle.HijackStart` (that lives in `resident/mrxactionhijack.lua`) — the two aren't in the same call chain in this corpus. The actual hijack-time transition is driven separately by `Sound.TransitionMusic("hijack")` in `resident/mrxsound.lua:BeginActionHijack`/`EndActionHijack` (see [Vehicle](vehicle) for the `HijackStart`/`HijackAbort`/`HijackComplete` state machine those functions bracket). |
| `SetTimerUpdateMusic` | `Sound.SetTimerUpdateMusic(bEnabled)` | Confirmed with a single boolean in real scripts, e.g. `Sound.SetTimerUpdateMusic(false)` / `Sound.SetTimerUpdateMusic(true)` (`resident/mrxsound.lua`), toggled around timer-critical gameplay (mission countdown contexts). |
| `SetSurvivalMode` | `Sound.SetSurvivalMode(bEnabled)` | Confirmed with a single boolean in real scripts, e.g. `Sound.SetSurvivalMode(true)` / `Sound.SetSurvivalMode(false)` (`resident/mrxsound.lua`, `shell/mrxsound.lua`), paired with `Sound.CueSound(0, "sfx_survival_lp")` / `Sound.StopSound(0, "sfx_survival_lp")` in the same functions. |
| `OverrideUserMusic` | `Sound.OverrideUserMusic()` | Confirmed with no arguments in real scripts, always guarded: `if Sound.OverrideUserMusic then Sound.OverrideUserMusic() end` (`shell/shellbootstrap.lua`) — same late-addition guard pattern seen elsewhere on this namespace. |
| `RestoreUserMusic` | `Sound.RestoreUserMusic()` | Confirmed with no arguments in real scripts, always guarded the same way as `OverrideUserMusic` and called as its counterpart: `if Sound.RestoreUserMusic then Sound.RestoreUserMusic() end` (`shell/shellbootstrap.lua`). |
| `SetSourceMusic` | `Sound.SetSourceMusic(sState)` | Confirmed with a single state-name string in real scripts: `Sound.SetSourceMusic(_sSourceMusicState)` (`shell/mrxmusic.lua`, music-system init). |
| `SetSourceEnterMusic` | `Sound.SetSourceEnterMusic(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed related to `SetSourceMusic`/`SetSourceExitMusic` by naming only. |
| `SetSourceExitMusic` | `Sound.SetSourceExitMusic(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetSourceMusicTransition` | `Sound.SetSourceMusicTransition(sEntryState, sExitState)` | Confirmed with two state-name strings in real scripts, in a fallback branch used when `Sound._GetLibVersion() < 11`: `Sound.SetSourceMusicTransition(transition.entryState, transition.exitState)` (`shell/mrxmusic.lua`). |
| `ClearSourceMusicTransitions` | `Sound.ClearSourceMusicTransitions()` | Confirmed with no arguments in real scripts, in the same `_GetLibVersion() < 11` fallback branch as `SetSourceMusicTransition`, called immediately before it (`shell/mrxmusic.lua`). |
| `AddSourceMusicEntryState` | `Sound.AddSourceMusicEntryState(sEntryState)` | Confirmed with a single state-name string in real scripts, in the `Sound._GetLibVersion() >= 11` branch (the newer API replacing `SetSourceMusicTransition`): `Sound.AddSourceMusicEntryState(transition.entryState)` (`shell/mrxmusic.lua`). |
| `ClearSourceMusicEntryStates` | `Sound.ClearSourceMusicEntryStates()` | Confirmed with no arguments in real scripts, in the same `>= 11` branch, called immediately before `AddSourceMusicEntryState` (`shell/mrxmusic.lua`). |
| `AddMusicSourcePlaylist` | `Sound.AddMusicSourcePlaylist(sPlaylist, nGap)` | Confirmed with a playlist-name string and a numeric gap value in real scripts: `Sound.AddMusicSourcePlaylist(sPlaylist, fGap)` (`shell/mrxmusic.lua`). |
| `AddCueToMusicSourcePlaylist` | `Sound.AddCueToMusicSourcePlaylist(sPlaylist, sCue)` | Confirmed with a playlist-name string and a cue-name string in real scripts: `Sound.AddCueToMusicSourcePlaylist(sPlaylist, sCue)` (`shell/mrxmusic.lua`). |
| `ClearMusicSourcePlaylist` | `Sound.ClearMusicSourcePlaylist(sPlaylist)` | Confirmed with a single playlist-name string in real scripts: `Sound.ClearMusicSourcePlaylist(sPlaylist)` (`shell/mrxmusic.lua`). |
| `RemoveMusicSourcePlaylist` | `Sound.RemoveMusicSourcePlaylist(sPlaylist)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed counterpart to `AddMusicSourcePlaylist`, by naming only. |
| `AddSourceMusicEntryState` | *(see above)* | Listed once; do not confuse with `SetSourceEnterMusic`, a distinct unconfirmed function. |
| `SetCinematicMode` | `Sound.SetCinematicMode(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetSystemPause` | `Sound.SetSystemPause(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetPauseFilter` | `Sound.SetPauseFilter(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetMessageFiltering` | `Sound.SetMessageFiltering(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `LockListenerPosition` | `Sound.LockListenerPosition(bLocked)` | Confirmed with a single boolean in real scripts, e.g. `Sound.LockListenerPosition(true)` / `Sound.LockListenerPosition(false)` (`resident/mrxsound.lua`, `shell/mrxsound.lua`) — used in pairs bracketing a scripted camera/audio moment. |

### Bank Loading

| Function | Signature (best-known) | Notes |
|---|---|---|
| `LoadBank` | `Sound.LoadBank(sBankName, sType)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `LoadBankWithCallback`/`LoadTempBank` below. |
| `UnloadBank` | `Sound.UnloadBank(sBankName, sType)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed synchronous counterpart to `LoadBank`, by naming only. |
| `LoadBankWithCallback` | `Sound.LoadBankWithCallback(sBankName, sType, funcCallback)` | Confirmed in real scripts: `Sound.LoadBankWithCallback(_GetLocalizedName(sBank), sType, _FlagAssetOpComplete)` (`shell/mrxsoundbanks.lua`), asynchronous asset-load with a completion callback. |
| `UnloadBankWithCallback` | `Sound.UnloadBankWithCallback(sBankName, sType, funcCallback)` | Confirmed with the same shape as `LoadBankWithCallback`: `Sound.UnloadBankWithCallback(_GetLocalizedName(sBank), sType, _FlagAssetOpComplete)` (`shell/mrxsoundbanks.lua`). |
| `LoadTempBank` | `Sound.LoadTempBank(sBankName, sType, funcCallback, tCallbackData)` | Confirmed in real scripts: `Sound.LoadTempBank(_GetLocalizedName(sBank), sType, funcCallback, tCallbackData)` (`shell/mrxsoundbanks.lua`) — a 4-argument variant with a callback-data table in addition to the callback function itself. |
| `UnloadTempBank` | `Sound.UnloadTempBank(sBankName, sType, funcCallback, tCallbackData)` | Confirmed with the same shape as `LoadTempBank`: `Sound.UnloadTempBank(_GetLocalizedName(sBank), sType, funcCallback, tCallbackData)` (`shell/mrxsoundbanks.lua`). |
| `LoadSoundBank` | `Sound.LoadSoundBank(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. `LoadBankWithCallback`/`LoadTempBank` are the confirmed loading entry points actually used; this may be a lower-level or type-specific variant, but that is inference, not evidence. |
| `UnloadSoundBank` | `Sound.UnloadSoundBank(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `LoadWaveBank` | `Sound.LoadWaveBank(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `UnloadWaveBank` | `Sound.UnloadWaveBank(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `RequestAmbienceBank` | *(see Direct Sound & Ambience Cueing above)* | Listed there since its one confirmed call site is ambience-specific, not general bank loading. |
| `GetAudioDir` | `s = Sound.GetAudioDir()` | Confirmed with no arguments in real scripts: `local sAudioDir = Sound.GetAudioDir()` (`shell/mrxsoundbanks.lua`), used to build a bank file path. |
| `OpenStreamFile` | `Sound.OpenStreamFile(sStreamName, sFileName)` | Confirmed with two string arguments in real scripts: `Sound.OpenStreamFile(sStreamFile, sFileName)` (`shell/mrxsoundbanks.lua`). |
| `CloseStreamFile` | `Sound.CloseStreamFile(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Presumed counterpart to the confirmed `OpenStreamFile`, by naming only. |
| `SetStreamBlockDumping` | `Sound.SetStreamBlockDumping(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `RegisterReadyCallback` | `Sound.RegisterReadyCallback(funcCallback)` | Confirmed with a single function argument in real scripts: `Sound.RegisterReadyCallback(_FlagSystemReady)` (`shell/mrxsound.lua`) — invoked once the audio system finishes initializing. |

### Mixing & Reverb

| Function | Signature (best-known) | Notes |
|---|---|---|
| `SetMasterVolume` | `Sound.SetMasterVolume(nVolume, nFadeTime)` | Confirmed with 2 numeric arguments in real scripts, e.g. `Sound.SetMasterVolume(1, 0)`, `Sound.SetMasterVolume(0, 0.5)` (`shell/mrxsound.lua`, `shell/mrxsoundcategories.lua`) — volume level (observed `0`/`1`) plus a fade duration in seconds. |
| `SetCategoryVolume` | `Sound.SetCategoryVolume(sCategory, nVolume)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `FadeCategoryUp`/`FadeCategoryDown`. |
| `GetCategoryVolume` | `Sound.GetCategoryVolume(sCategory)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetCategoryPitch` | `Sound.SetCategoryPitch(sCategory, nPitch)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `PitchCategoryActivate`. |
| `GetCategoryPitch` | `Sound.GetCategoryPitch(sCategory)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `AddFadeCategory` | `Sound.AddFadeCategory(sCategory)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `FadeCategoryUp`/`FadeCategoryDown`. |
| `ClearFadeCategories` | `Sound.ClearFadeCategories()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `FadeCategoryDown` | `Sound.FadeCategoryDown(sCategory, nLevel, nDuration)` | Confirmed with a category string and 2 numeric arguments in real scripts: `Sound.FadeCategoryDown(category, fLevel, fEnterLength)` (`shell/mrxsoundcategories.lua`). |
| `FadeCategoryUp` | `Sound.FadeCategoryUp(sCategory, nDuration)` | Confirmed with a category string and 1 numeric argument in real scripts: `Sound.FadeCategoryUp(category, fExitLength)` (`shell/mrxsoundcategories.lua`), the counterpart restore call to `FadeCategoryDown`. |
| `AddPitchCategory` | `Sound.AddPitchCategory(sCategory)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature inferred only by analogy to the confirmed `PitchCategoryActivate`/`PitchCategoryDeactivate`. |
| `ClearPitchCategories` | `Sound.ClearPitchCategories()` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `PitchCategoryActivate` | `Sound.PitchCategoryActivate(sCategory, nLevel, nDuration)` | Confirmed with a category string and 2 numeric arguments in real scripts: `Sound.PitchCategoryActivate(category, fLevel, fEnterLength)` (`shell/mrxsoundcategories.lua`). |
| `PitchCategoryDeactivate` | `Sound.PitchCategoryDeactivate(sCategory, nDuration)` | Confirmed with a category string and 1 numeric argument in real scripts: `Sound.PitchCategoryDeactivate(category, fExitLength)` (`shell/mrxsoundcategories.lua`), the counterpart restore call to `PitchCategoryActivate`. |
| `DefineReverbPreset` | `Sound.DefineReverbPreset(nId, sName, ...)` | Confirmed with an integer ID, a preset-name string, and a long run of further numeric parameters in real scripts: `Sound.DefineReverbPreset(1, "CITY_KG_LIGHT_REFLECTIONS", -1000, -1000, 0, 0.09, 0.23, -602, 0.02, -698, 0.03, 100, 100, 5000, 0, 5000, -5000)` (`resident/mrxsoundbootstrap.lua`). The individual meaning of each of the 14 trailing numeric parameters (standard reverb-DSP parameters such as room size, decay time, reflections level/delay, diffusion, etc. are plausible by convention) is not confirmed by this single call site. |
| `SetReverbPreset` | `Sound.SetReverbPreset(vPresetIdOrName)` | Confirmed in real scripts accepting either the preset name string or its integer ID interchangeably: `Sound.SetReverbPreset("CITY_KG_LIGHT_REFLECTIONS")` and `Sound.SetReverbPreset(1)` (`resident/mrxsoundbootstrap.lua`), gated by a version/feature check between the two forms. |
| `SetReverb` | `Sound.SetReverb(nId)` | Confirmed with a single integer argument in real scripts: `Sound.SetReverb(1)` (`resident/mrxsoundbootstrap.lua`), called as a fallback alongside `SetReverbPreset`. |
| `SetLowPassFilter` | `Sound.SetLowPassFilter(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `SetLowPassFilterSettings` | `Sound.SetLowPassFilterSettings(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. |
| `GetMaxDuration` | `n = Sound.GetMaxDuration(sCueName)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Signature guessed only from the name (a cue-length query), not from any observed call. |

### Misc / Internal

| Function | Signature (best-known) | Notes |
|---|---|---|
| `_GetLibVersion` | `n = Sound._GetLibVersion()` | Leading-underscore name, consistent with this codebase's convention (seen throughout `resident/`) for marking private/internal members — likely an internal/debug-facing accessor rather than part of the intended public surface, though it is genuinely called in real code. Confirmed with no arguments and a numeric return, used repeatedly as a feature-gate: `if Sound._GetLibVersion() >= 11 then` (`shell/mrxmusic.lua`, choosing between `SetSourceMusicTransition` and the newer `AddSourceMusicEntryState` API), and `if Sound._GetLibVersion() >= 12 then` (`shell/mrxsoundbanks.lua`), `if Sound._GetLibVersion() >= 10 then` (`resident/mrxsoundbootstrap.lua`, choosing between `SetReverbPreset` and `SetReverb`). This is effectively an audio-engine build/version number the scripts branch on. |
| `_SummonEd` | `Sound._SummonEd(...)` | No call sites found in the decompiled corpus — exists (confirmed via live `pairs()` enumeration) but usage/arguments unconfirmed. Leading-underscore name matches the private/internal convention noted above; "Ed" plausibly names a specific internal/debug tool (an editor or debug-visualization hook), but that is speculation, not evidence — the name itself is the only clue available. |

## Notes for modders

- The dynamic music system is a small state machine layered on top of named "music states" (`"none"`,
  `"explore"`, `"action"`, `"high_action"`, `"hijack"`, `"hijack_success"`, `"mission_success"`,
  `"mission_failure"`, `"silence"`, `"pause"`, `"shell"`, `"source"`, plus mission-specific ones). States
  are registered with `AddMusicState`, legal transitions between them with `AddMusicTransition`, and the
  actual runtime move between states is `TransitionMusic(sState)`. If you want to trigger custom music
  behavior, `TransitionMusic` with an already-registered state name is the safest lever — inventing a new
  state name would additionally require call sites this corpus doesn't show for `AddMusicState`/
  `AddMusicTransition` registration timing (they only run once, during shell/mission init).
- `Sound.SetHijackMusic` only registers which states back hijack success/resume music during init — it is
  not the function that starts hijack music during actual gameplay. The real hijack-time trigger is
  `Sound.TransitionMusic("hijack")` / `Sound.TransitionMusic("hijack_success")` in
  `resident/mrxsound.lua`'s `BeginActionHijack`/`EndActionHijack`, called alongside `LockActionLevelMusic`.
  See [Vehicle](vehicle) for the `HijackStart`/`HijackAbort`/`HijackComplete` state machine those wrap
  around — the two systems cooperate (audio reacting to hijack state) but are driven by separate call
  chains in this corpus, not a single combined call site.
- Several functions (`StopAndFlushAllSounds`, `SetVehicleEngineBoost`, `OverrideUserMusic`,
  `RestoreUserMusic`) are only ever called behind an `if Sound.XxxFunction then` existence guard in the
  decompiled scripts. That pattern elsewhere in this codebase means the function was added in a later
  engine/game build than some of the code calling it — treat these as real but possibly build-dependent.
- `_GetLibVersion` and `_SummonEd` are flagged by this page's naming convention (leading underscore) as
  likely internal/debug functions, matching how private members are marked elsewhere in the `resident/`
  corpus. `_GetLibVersion` is nonetheless genuinely exercised by shipped code as a feature-gate check;
  `_SummonEd` has zero call sites and its purpose is not inferable beyond the name itself — don't guess
  further than "probably a debug/dev tool."
- A large fraction of the mixing/reverb/category getters (`GetCategoryVolume`, `GetCategoryPitch`,
  `SetCategoryVolume`, `SetCategoryPitch`, `AddFadeCategory`, `AddPitchCategory`, `ClearFadeCategories`,
  `ClearPitchCategories`, `SetLowPassFilter`, `SetLowPassFilterSettings`) have zero call sites in this
  corpus even though their "activate/deactivate" and "up/down" counterparts are confirmed. These look like
  a complete, symmetric API where only half of each pair happened to be exercised by the ~230 scripts
  available — a reasonable target for live testing if you want mixing control beyond what's confirmed here.
