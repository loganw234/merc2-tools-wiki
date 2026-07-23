---
title: Sys
parent: Engine Namespaces
nav_order: 9
---

# Sys

## Overview

`Sys` is an **engine namespace**: implemented natively by the game engine, not by any decompiled
`.lua` module. There is no source file behind it, no `import()` needed — it is always globally
available from any script. It is a general system-services grab-bag covering time/clock utilities,
save/autosave control, asset preloading, level and shell state, platform/build/SKU queries, GUID
string conversion, and a scattering of miscellaneous system settings (rumble, subtitles, Y-axis
inversion, HUD/viewport toggles).

## Provenance

The 64 functions listed below are a complete, authoritative enumeration taken from a live
`pairs(Sys)` dump in-game — every name here is confirmed to exist. That dump gives names and raw
function pointers only, nothing about parameters or behavior. Everything beyond that (argument
shapes, likely purpose) is inferred from real call sites in the ~230 decompiled `.lua` files; where
no call site exists anywhere in that corpus, this page says so explicitly rather than guessing.

## Functions

### Time & Clock

| Function | Signature (best-known) | Notes |
|---|---|---|
| `RealTimeStamp` | `uStamp = Sys.RealTimeStamp()` | Used with no arguments in real scripts to capture a timestamp handle, e.g. `uLockTimer = Sys.RealTimeStamp()` (`resident/antiair.lua:279`), later read via `TimeStampGetElapsed`. |
| `MainTimeStamp` | `uStamp = Sys.MainTimeStamp()` | Used the same way as `RealTimeStamp`, e.g. `_uSessionStartTimestamp = Sys.MainTimeStamp()` (`resident/mrxplaystate.lua:111`), `tTimeStamp[uWeapon] = Sys.MainTimeStamp()` (`resident/mrxstatsmanager.lua:501,575`), `self._uTimeStamp = Sys.MainTimeStamp()` (`resident/mrxtaskrace.lua:268`). Distinct from `RealTimeStamp` — presumably tied to the "main" (pausable/scaled) clock rather than a real-world clock, consistent with the separate `MainTime`/`RealTime` accessors below, but the exact difference is not confirmed from source. |
| `TimeStampMark` | `Sys.TimeStampMark(uStamp)` | Used to reset/re-mark an existing timestamp handle in place, e.g. `Sys.TimeStampMark(tTimeStamp[uWeapon])` (`resident/mrxstatsmanager.lua:499`), `Sys.TimeStampMark(self._uTimeStamp)` (`resident/mrxtaskrace.lua:269`) — call sites consistently re-mark a stamp previously produced by `MainTimeStamp`/`RealTimeStamp` rather than creating a new one. |
| `TimeStampGetElapsed` | `n = Sys.TimeStampGetElapsed(uStamp)` | Confirmed pervasively: `nBlink = Sys.TimeStampGetElapsed(tLockOn.uLockTimer) * nRate` (`resident/antiair.lua:350`), `nThisSession = Sys.TimeStampGetElapsed(_uSessionStartTimestamp)` (`resident/mrxplaystate.lua:102`), `resident/mrxstatsmanager.lua:490,564`, `resident/mrxtaskrace.lua:277`. Returns elapsed seconds since the stamp was marked. This — plus `MainTimeStamp`/`TimeStampMark` — is the real building-block pattern used for elapsed-time tracking in this codebase, a lower-level alternative to the callback-based [`Event.TimerRelative`](event#timer--misc-events) pattern for cases that need to poll elapsed time rather than fire once after a delay. |
| `MainTime` | `n = Sys.MainTime()` | Used with no arguments, e.g. `return Sys.MainTime()` (`resident/mrxplaystate.lua:106`) as a fallback session-time source. Presumed to be the game's internal (pausable/scaled) clock in seconds, paired conceptually with `MainTimeStamp` above, but the precise semantics (does it stop on pause? is it time-scaled by `SetTimeScale`?) are not confirmed from source. |
| `RealTime` | `n = Sys.RealTime()` | Live-confirmed via WebSocket lua-bridge probe against a running game (2026-07-22): callable with no arguments, returns a plain number — no longer "no call sites found / unconfirmed." The specific unit/epoch isn't confirmed, but a confirmed numeric return is consistent with the presumed role as the real-world-clock counterpart to `MainTime`, paired with `RealTimeStamp`. |
| `Clock` | `n = Sys.Clock()` | Live-confirmed via WebSocket lua-bridge probe against a running game (2026-07-22): callable with no arguments, returns a plain number — no longer "no call sites found / unconfirmed." Purpose beyond "a number" (raw tick count vs. clock-seconds reading) is still not confirmed. |
| `Time` | `n = Sys.Time()` | Live-confirmed via WebSocket lua-bridge probe against a running game (2026-07-22): callable with no arguments, returns a plain number. Grouped here with `RealTime`/`Clock` above — the live probe found all three returning the same "number" shape. |
| `Date` | `s = Sys.Date()` | Live-confirmed via WebSocket lua-bridge probe against a running game (2026-07-22): callable with no arguments, returns a string in `MM/DD/YY HH:MM:SS` format — no longer "no call sites found / unconfirmed." Unlike its numeric `Time & Clock` siblings here, this one returns a formatted date/time string, not a number. |
| `DiffTime` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed to compute a difference between two time/timestamp values by naming, unconfirmed. |
| `SetTimeScale` | `Sys.SetTimeScale(nScale)` | Confirmed: `Sys.SetTimeScale(Math.min(nNewTimeScale, nMinTimeScale))` (`resident/hero.lua:249`) — used for a slow-motion-style effect, clamped to a minimum scale before being applied. |

### Save System

| Function | Signature (best-known) | Notes |
|---|---|---|
| `RequestAutosave` | `Sys.RequestAutosave(bInMission, bLastMission, fMissionTime, nPercentCompleted)` | Confirmed with 4 arguments: `Sys.RequestAutosave(inMission, lastMission, fMissionTime, MrxStatsManager.GetPercentCompleted())` (`resident/mrxmissionflow.lua:768`). Also guarded defensively elsewhere: `if Sys.RequestAutosave and _bDoMissionAutosave then` (`resident/mrxmissionflow.lua:825`), confirming it's an optional/late-bound engine entry point checked for existence before use, same pattern seen for several other `Sys` functions below. |
| `ForceNextAutosave` | `Sys.ForceNextAutosave()` | Used with no arguments: `Sys.ForceNextAutosave()` (`vz/wifmissionflow.lua:463`). |
| `IsAutosaveEnabled` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed getter counterpart to `SetAutosaveEnabled`, unconfirmed. |
| `SetAutosaveEnabled` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `SetLuaSaveVersion` | `Sys.SetLuaSaveVersion(nVersion)` | Confirmed: `Sys.SetLuaSaveVersion(GetSaveDataVersion())` (`shell/shellbootstrap.lua:68`, `resident/gamebootstrap.lua:41`) — always called with the return value of a local `GetSaveDataVersion()` helper, run once during bootstrap. |
| `RequestGameState` | `Sys.RequestGameState(sState)` | Extremely widely used with a single state-name string, e.g. `"Shell"`, `"ingame"`, `"cinematic"`, `"Pause"`, `"attract"`, `"Exiting"`, `"LTI_precache"`, `"Loading"`, `"unloading"`, `"waitfortether"`, `"WaitForStreaming"`, `"WaitForTether"`, `"PDA"` (dozens of call sites across `shell/mrxguishell.lua`, `resident/mrxstate.lua`, `resident/levelbootstrap.lua`, `vz/wifmissionflow.lua`, and others). This is the core game-state transition request function; state names are free-form strings matched against whatever state machine the engine runs natively — not enumerated anywhere as constants. `resident/mrxutil.lua:113,132` shows it returning a success boolean (`local bSuccess = Sys.RequestGameState("waitfortether")`). |

### Level & Shell State

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetLevelName` | `s = Sys.GetLevelName()` | Very widely used with no arguments, e.g. `resident/gamebootstrap.lua:70`, `resident/levelbootstrap.lua:3`, `resident/mrxbootstrap.lua:60` (`string.lower(Sys.GetLevelName())`), `resident/mrxplayer.lua:408` (compared against `"vz"`). |
| `SetLevelName` | `Sys.SetLevelName(sLevelName)` | Confirmed: `Sys.SetLevelName(LevelName)` (`resident/levelbootstrap.lua:8`), paired with `GetLevelName` reads earlier in the same file. |
| `GetMasterScriptName` | `s = Sys.GetMasterScriptName()` | Confirmed alongside `GetLevelName`, e.g. `shell/mrxguishell.lua:596`, `resident/gamebootstrap.lua:70`, used together to drive `Net.StartServer(...)` and `LevelBootstrap.LoadLevel(...)` calls. |
| `SetMasterScriptName` | `Sys.SetMasterScriptName(sMasterScript)` | Confirmed: `Sys.SetMasterScriptName(MasterScript)` (`resident/levelbootstrap.lua:9`). |
| `GetShellCode` | `s = Sys.GetShellCode()` | Used with no arguments: `local sShellCode = Sys.GetShellCode()` (`shell/mrxguishell.lua:549`). |
| `FinishedShell` | `b = Sys.FinishedShell()` | Guarded/optional-style call: `if Sys.FinishedShell and Sys.FinishedShell() then` (`resident/gamebootstrap.lua:43`). |
| `AutoLoad` | `b = Sys.AutoLoad()` | Used with no arguments as a boolean gate for skipping the shell/menu flow, e.g. `if not Sys.AutoLoad() then` (`shell/mrxguishell.lua:259`), `elseif Sys.AutoLoad() then` (`resident/gamebootstrap.lua:65`, `shell/shellbootstrap.lua:94`). |
| `RequiredAsset` | `Sys.RequiredAsset(sAssetName, sAssetType, nPriority, bFlag)` | Confirmed with 4 arguments: `Sys.RequiredAsset(LevelName .. "_base", "layer", -2, false)` and `Sys.RequiredAsset(MasterScript, "script", -3, false)` (`resident/levelbootstrap.lua:14-15`) — registers an asset (layer or script) as required for the current level, with a numeric priority (negative in both observed cases) and a trailing boolean whose meaning is not confirmed. |
| `GetSkipMission` | `s = Sys.GetSkipMission()` | Used with no arguments: `local sSkipToMissionName = Sys.GetSkipMission()` ([`vz/xQ!L.lua:639`](../vz/xql)). |
| `SetSkipMission` | `Sys.SetSkipMission(sMissionName)` | Confirmed repeatedly with a mission-name string (including an empty-string "clear" call): `Sys.SetSkipMission(sMission)` (`shell/mrxguishell.lua:168`), `Sys.SetSkipMission("")` (`vz/xQ!L.lua:640,689`), `Sys.SetSkipMission(sMissionId)` (`vz/xQ!L.lua:909`). |
| `GetForceNewGame` | `b = Sys.GetForceNewGame()` | Guarded/optional-style call: `if Sys.GetForceNewGame and Sys.GetForceNewGame() then` (`resident/mrxmissionflow.lua:154`). |
| `GetINIBriefing` | `b = Sys.GetINIBriefing()` | Widely used with no arguments as a boolean, e.g. `shell/mrxguishell.lua:148,165`, `vz/xQ!L.lua:643`. |
| `SetINIBriefing` | `Sys.SetINIBriefing(bValue)` | Confirmed: `Sys.SetINIBriefing(not Sys.GetINIBriefing())` (`shell/mrxguishell.lua:165`), `Sys.SetINIBriefing(bBriefing)` ([`vz/xQ!L.lua:910`](../vz/xql)). |
| `GetINILoadLastSave` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |

### Platform & Build Info

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetVersion` | `sCode, sData = Sys.GetVersion()` | Confirmed with two return values: `local sCode, sData = Sys.GetVersion()` (`shell/mrxguishell.lua:527`). |
| `GetPlatform` | `n = Sys.GetPlatform()` | Used with no arguments: `local nPlatform = Sys.GetPlatform()` (`resident/mrxguipda.lua:118`) — treated as a numeric platform ID at the call site, not a string. |
| `GetLanguage` | `s = Sys.GetLanguage()` | Confirmed: `sLanguage = Sys.GetLanguage() or "English"` (`resident/mrxbriefing.lua:1191`) — the `or "English"` fallback suggests it can return `nil`/falsy on some builds. |
| `IsFinalConfig` | `b = Sys.IsFinalConfig()` | Guarded/optional-style call: `if ... Sys.IsFinalConfig and not Sys.IsFinalConfig() then` (`shell/mrxguishell.lua:311`) — gates a debug-only skip button so it's unavailable in final builds. |
| `IsDemoMode` | `b = Sys.IsDemoMode()` | Guarded/optional-style call: `if Sys.IsDemoMode and Sys.IsDemoMode() then` (`shell/mrxgui.lua:421`, `shell/mrxgui_shellonly.lua:291`). |
| `IsGermanSKU` | `b = Sys.IsGermanSKU()` | Confirmed, called unguarded (unlike most other `Is*` queries here): `if not Sys.IsGermanSKU() then` / `if Sys.IsGermanSKU() then` (`resident/mrxtaskobjectiveverify.lua:95,242,404`) — gates region-specific content (presumably gore/violence toggles for the German release). |
| `IsLoadingOrStreaming` | `b = Sys.IsLoadingOrStreaming()` | Guarded/optional-style call: `if Sys.IsLoadingOrStreaming and (not Player.GetLocalCharacter() or Sys.IsLoadingOrStreaming()) then` (`vz/wifvzatmosphere.lua:26`). |
| `LTIGetPrecacheBypass` | `n = Sys.LTIGetPrecacheBypass()` | Confirmed: `if Sys.LTIGetPrecacheBypass() > 0 then` (`shell/shellbootstrap.lua:58`) — returns a number compared against 0, not a plain boolean. |
| `MemUsage` | `n = Sys.MemUsage()` | Live-confirmed via WebSocket lua-bridge probe against a running game (2026-07-22): callable with no arguments, returns a plain number — no longer "no call sites found / unconfirmed," confirming the presumed memory-diagnostics-query role by naming. Units (bytes/KB/MB) not confirmed. |
| `GetCharacterTemplate` | `s = Sys.GetCharacterTemplate()` | Confirmed as a fallback in a chain: `MrxGuiShellBootstrap.GetSelectedCharacter() or Sys.GetCharacterTemplate() or "mattias"` (`resident/mrxplayer.lua:636`) — returns a character-template name string, with `"mattias"` as the ultimate hardcoded fallback. |
| `HaveActiveProfile` | `Sys.HaveActiveProfile()` | Called with no arguments and its result discarded/unused at the one call site found: `Sys.HaveActiveProfile()` (`resident/mrxguipda.lua:1332`) — return value's use elsewhere is not confirmed. |
| `GetForceNewGame` | see Level & Shell State above | Listed once; grouped there since it gates new-game/level-bootstrap flow rather than being a platform query. |

### Asset Preloading

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GetAssetRequestMax` | `n = Sys.GetAssetRequestMax()` | Confirmed: `_knOrigAssetRequestMax = Sys.GetAssetRequestMax()` (`resident/mrxlayermanager.lua:15`), and read again as a comparison bound: `elseif nPendingOps > Sys.GetAssetRequestMax() then` (`resident/mrxlayermanager.lua:200`). |
| `SetAssetRequestMax` | `Sys.SetAssetRequestMax(nMax)` | Confirmed paired with the getter: `Sys.SetAssetRequestMax(_knOrigAssetRequestMax)` to restore the original value, and `Sys.SetAssetRequestMax(nPendingOps)` to raise it temporarily (`resident/mrxlayermanager.lua:197,201`) — the asset-streaming throttle used by the layer manager. |
| `RequiredAsset` | see Level & Shell State above | Listed once; grouped there since its confirmed call sites are both level-bootstrap related. |
| `DisableAssetPreload` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `FlushAssets` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `AddStringDb` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `ClearStringDb` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |

### GUID Conversion

| Function | Signature (best-known) | Notes |
|---|---|---|
| `GuidToString` | `s = Sys.GuidToString(uGuid)` | Very widely used, e.g. `tonumber(Sys.GuidToString(uViewportId))` (`shell/mrxguibase.lua:140`), `Sys.GuidToString(uiStateHashName)` (`resident/fueltank.lua:2`, `resident/islandfortress.lua:52-53`, `resident/oilrig.lua:33`), `Sys.GuidToString(uGateGuid)` (`resident/friendlygate.lua:24,36`), and repeatedly in `resident/mrxtaskcontract.lua`, `resident/mrxtaskobjective.lua`, `resident/mrxparkinglotmanager.lua`. Converts a `uGuid` handle to its string form — often used as a table key (e.g. `tAdjacencyTable[Sys.GuidToString(uNodeNameHash)]` in `resident/islandfortress.lua:76`) or for debug printing. |
| `StringToGuid` | `uGuid = Sys.StringToGuid(sGuidString)` | Confirmed as the namespaced form: `local uVehicle = Sys.StringToGuid(sVehicleGuid)` (`vz/wifpmcgarage.lua:243`), `local uGateGuid = Sys.StringToGuid("0x000f9a64")` (`vz/wiftutorialgatehonk.lua:10`). See **Notes for modders** below — this is very likely the same underlying function as the bare global `StringToGuid` used pervasively elsewhere. |

### Misc Settings

| Function | Signature (best-known) | Notes |
|---|---|---|
| `RumbleEnabled` | `b = Sys.RumbleEnabled()` | Used with no arguments: `bRumble = Sys.RumbleEnabled()` (`resident/mrxguipausescreen.lua:238`), part of the pause-screen options-menu read of current system settings. |
| `SubtitlesEnabled` | `b = Sys.SubtitlesEnabled()` | Used both guarded and unguarded: `if Sys.SubtitlesEnabled and Sys.SubtitlesEnabled() then` (`shell/mrxguicinematic.lua:391`), `bSubtitles = Sys.SubtitlesEnabled()` (`resident/mrxguipausescreen.lua:233`). |
| `YAxisInverted` | `b = Sys.YAxisInverted()` | Used with no arguments: `bInvert = Sys.YAxisInverted()` (`resident/mrxguipausescreen.lua:248`) — read alongside `RumbleEnabled`/`SubtitlesEnabled` in the same pause-screen options read. |
| `IsConfirmOnCircle` | `b = Sys.IsConfirmOnCircle()` | Very widely used, almost always guarded: `if Sys.IsConfirmOnCircle and Sys.IsConfirmOnCircle() then` (`shell/mrxguibase.lua:1910`, `resident/mrxguihudmessage.lua:513,551`, `resident/mrxguisatellite.lua:374`), and unguarded in `resident/mrxbriefing.lua:2996`. Region/platform-specific controller-confirm-button convention (PS-style "circle to cancel" vs "cross to confirm"). |
| `NoHud` | `b = Sys.NoHud()` | Used unguarded: `if Sys.NoHud() then` (`shell/mrxguimanager.lua:66`, `resident/mrxguimanager.lua:66`). |
| `SetNumberOfViewports` | `Sys.SetNumberOfViewports(n)` | Confirmed: `Sys.SetNumberOfViewports(1)` (`shell/mrxguishell.lua:492`). |
| `PlayIntroMovies` | `b = Sys.PlayIntroMovies()` | Confirmed: `if not Sys.PlayIntroMovies() then` (`resident/gamebootstrap.lua:47`, `shell/shellbootstrap.lua:70`). |
| `StartSingleplayer` | `Sys.StartSingleplayer(sLevelName, sMasterScript)` | Confirmed with 2 arguments: `Sys.StartSingleplayer(sLevelName, sMasterScript)` (`shell/mrxguishell.lua:601`). |
| `StartWithResources` | `b = Sys.StartWithResources()` | Guarded/optional-style call: `if Sys.StartWithResources and Sys.StartWithResources() then` (`resident/mrxbootstrap.lua:64`). |
| `TutorialsEnabled` | `b = Sys.TutorialsEnabled()` | See **Notes for modders** below — cross-linked with [`resident/mrxtutorialmanager.md`](../resident/mrxtutorialmanager.md). |
| `SetTutorialsEnabled` | `Sys.SetTutorialsEnabled(bEnable)` | Guarded call: `if Sys.SetTutorialsEnabled then Sys.SetTutorialsEnabled(bEnable) end` (`resident/mrxguitutorial.lua:264-265`). Setter counterpart to `TutorialsEnabled`; see Notes for modders below. |
| `Callback` | — | No call sites found in the decompiled corpus. Exists per live enumeration; unconfirmed. |
| `ToStringL` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed a localized/long string conversion by naming, unconfirmed. |
| `WriteToConsole` | — | No call sites found in the decompiled corpus. Exists per live enumeration; presumed a debug-console print by naming, unconfirmed. |

## Notes for modders

- **`StringToGuid`/`GuidToString` bare-global aliasing.** The same aliasing pattern already documented on
  [`Pg.GetGuidByName`](pg#notes-for-modders) shows up here. Grepping the corpus finds `StringToGuid` called
  in two forms: the namespaced `Sys.StringToGuid(...)` (e.g. `vz/wifpmcgarage.lua:243`,
  `vz/wiftutorialgatehonk.lua:10`) and a bare, unqualified `StringToGuid(...)` used far more often across
  `vz/chicon002.lua`, `vz/meccon001.lua`, `resident/mrxguihudvehicledisguise.lua`, `resident/mrxguiinterface.lua`,
  `resident/mrxsupportdesignatorsmoke.lua`, `resident/oilrig.lua`, and others — always with the identical
  `"0x..."`-style hex-string argument shape. No `GuidToString` call site was found using a bare unqualified
  form (every observed call site uses `Sys.GuidToString(...)`), so the aliasing evidence is one-directional
  here — strong for `StringToGuid`, unconfirmed for `GuidToString`. As with `Pg.GetGuidByName`, this is the
  most plausible reading of consistent call-site behavior (a function aliased onto both `_G` and `Sys`), not
  something confirmed by reading engine source. Prior project notes on a bare-global `StringToGuid` discovery
  line up with this: it is very likely the same function as `Sys.StringToGuid`, just reachable at two scopes.
- **`TutorialsEnabled`/`SetTutorialsEnabled` gate the tutorial-hint HUD message system.** `Sys.TutorialsEnabled()`
  is checked directly in [`resident/mrxtutorialmanager.lua`](../resident/mrxtutorialmanager.md) (lines 98, 125,
  181) before showing or updating a tutorial message, and both functions are read/written defensively (checked
  for existence with `if Sys.TutorialsEnabled then ...`) in `resident/mrxguitutorial.lua` and
  `resident/mrxguipausescreen.lua` (the options-menu toggle for this setting). This is exactly the gate behind
  the custom-HUD-message technique documented in [Snippets: Show a custom HUD message](../snippets#show-a-custom-hud-message-with-icon-and-sound)
  — that snippet reuses the same generic tutorial-popup primitive `MrxTutorialManager` drives, and
  `Sys.TutorialsEnabled()` is the switch that must be true (or bypassed) for it to actually display. Don't
  re-derive the HUD-message mechanics here; see that snippet and the `MrxTutorialManager` page for the full
  picture, this page only documents the two `Sys` entry points that gate it.
- Several functions on this namespace (`FinishedShell`, `AutoLoad`, `GetForceNewGame`, `IsDemoMode`,
  `IsFinalConfig`, `IsLoadingOrStreaming`, `StartWithResources`, `SetTutorialsEnabled`, `TutorialsEnabled`,
  `RequestAutosave`) are consistently called guarded — `if Sys.SomeFunction and Sys.SomeFunction() then` —
  rather than called directly. That pattern across many otherwise-ordinary functions suggests these entry
  points may not exist on every build/platform/version of the engine, so defensive existence-checking before
  calling them is the safer approach for mod code too, even though live enumeration confirms they exist on
  at least this build.
- The time-utility family (`MainTimeStamp`/`RealTimeStamp` + `TimeStampMark` + `TimeStampGetElapsed`) is a
  real, working elapsed-time-polling primitive independent of the callback-based
  [`Event.TimerRelative`](event#timer--misc-events) pattern documented on the `Event` page — use the `Sys`
  family when you need to check "how long has it been" on demand, and `Event.TimerRelative` when you want a
  callback to fire automatically after a delay.
- Functions marked "no call sites found" are real (confirmed via the live `pairs(Sys)` dump) but their
  argument shape is a guess based on naming convention only — don't build mods around them without testing
  in-game first.
