---
title: ShellBootstrap
parent: Shell Modules
nav_order: 2
inherits: none
tags: [shell]
verified: false
---

# ShellBootstrap

## Overview
`ShellBootstrap` is the front-end build's top-level startup orchestrator — it plays the EA/Pandemic splash movies, waits on an asset-precache gate, then routes into auto-connect, auto-lobby, auto-server, autoload, or the main menu proper. It also owns the reverse path: tearing the shell down (fading audio, resetting/exiting the shell GUI) when leaving. It's the shell build's direct counterpart to [`GameBootstrap`](../resident/gamebootstrap), and while the two are clearly cut from the same source, they genuinely diverge in several places — see Notes below.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxSoundShellBootstrap`, `MrxGuiShellBootstrap`, `MrxGuiBase`, `MrxSound`

## Instance pattern
Stateless manager module. Module-level globals:
- `tMovies` — the splash-movie playlist, a list of `{sMovieName, nLoopTime}` pairs.
- `_oIntroMovieWidget` — the active `MrxGuiBase.MovieWidget` instance, or `nil` when none is playing.
- `_nMovie` (assigned without `local` inside `_PlayMovie`, so it's a global) — index of the current movie in `tMovies`.
- `IsFinishedPrecache` — a `0`/`1` flag (not a boolean) for whether asset precache has completed.

`EXITSHELL_FADELENGTH`, used in `ResetSingleton` below, is *not* defined in this file — it lives on [`MrxSoundShellBootstrap`](mrxsoundshellbootstrap).

## Functions

### _PlayMovie()
Advances `_nMovie` and plays the next entry in `tMovies`. When the list is exhausted (or `_oIntroMovieWidget` is `nil`), it logs "All movies complete", removes/deletes the movie widget, clears `_oIntroMovieWidget`, and calls **`StartPrecache()`** — notably *not* `Start()` directly (see the divergence note below). Otherwise it sets the widget's movie, registers a local `_EndMovie` closure as the end callback via `:SetEndCallback`, and calls `:Play()`; `_EndMovie` stops the widget and recurses into `_PlayMovie()` to advance to the next entry.

### IsFinishedPrecache / FinishedPrecache()
`IsFinishedPrecache` starts at `0`; `FinishedPrecache()` sets it to `1`. Nothing in this file calls `FinishedPrecache()` — it's presumably invoked externally once whatever the engine is precaching for the shell finishes loading.

### _WaitPrecache()
Polls `IsFinishedPrecache`: if it's greater than `0`, calls `Start()`. Otherwise logs and reschedules itself via `Event.Create(Event.TimerRelative, {2}, _WaitPrecache)` — checking again every 2 seconds.

### StartPrecache()
If `Sys.LTIGetPrecacheBypass()` returns greater than `0`, skips straight to `Start()`. Otherwise calls `_WaitPrecache()` (arming the poll loop) and then `MrxGuiShellBootstrap.EnterPrecache()`, in that order.

### Init()
The engine-called entry point. Logs "Top of ShellBootstrap::Init()", sets `Sys.SetLuaSaveVersion(GetSaveDataVersion())` and `Graphics.SetGamma(0, 0.8, 1)`. If `Sys.PlayIntroMovies()` is false, calls `Start()` directly (skipping precache too — see below) and returns. Otherwise creates `_oIntroMovieWidget`, sets it fullscreen-letterboxed and pause-ignoring, adds it via `MrxGuiBase.AddWidget`, guardedly calls `Sound.OverrideUserMusic()` if that function exists, and kicks off `_PlayMovie()`.

### Start()
Guardedly calls `Sound.RestoreUserMusic()` if it exists, then branches in priority order, same shape as `GameBootstrap.Start()`: `Net.AutoClient()` → load shell, connect to server; `Net.AutoLobby()` → load shell, enter lobby; `Sys.AutoLoad()` with `Net.AutoServer()` → load shell, start server; `Sys.AutoLoad()` alone → `MrxGuiShellBootstrap.LoadShell()`; else → `MrxGuiShellBootstrap.EnterShell()` (the main menu).

### GetSaveDataVersion()
Returns `3` — same hardcoded value as `GameBootstrap`.

### ResetSingleton()
Shell-only teardown entry point (no resident equivalent). Calls `MrxSoundShellBootstrap.PreExitShell()` to start fading audio, then schedules `ShellExitComplete` via `Event.Create(Event.TimerRelative, {MrxSoundShellBootstrap.EXITSHELL_FADELENGTH + 0.05, true}, ShellExitComplete)`.

### ShellExitComplete()
Shell-only teardown finisher. Calls `MrxSoundShellBootstrap.ExitShell()`, `MrxGuiShellBootstrap.Reset()`, `MrxGuiShellBootstrap.ExitShell()`, then `Pg.ResetSingletonDone()`.

## Events
- `Event.Create(Event.TimerRelative, {2}, _WaitPrecache)` — repeating poll while waiting for precache to finish.
- `Event.Create(Event.TimerRelative, {MrxSoundShellBootstrap.EXITSHELL_FADELENGTH + 0.05, true}, ShellExitComplete)` — one-shot delayed teardown completion, timed to outlast the audio fade.
- Movie sequencing itself is a widget-level callback (`MovieWidget:SetEndCallback`), not the `Event` system — same as `GameBootstrap`.

## Notes for modders
**This is the shell build's counterpart to [`GameBootstrap`](../resident/gamebootstrap), and the two genuinely diverge** — this isn't just a renamed copy:
- **Splash order is reversed.** Shell plays `{"EA",-1},{"Pandemic",-1}`; resident plays `{"Pandemic",-1},{"EA",-1}`.
- **Resident has a bail-out this file lacks.** `GameBootstrap.Init()` opens with `if Sys.FinishedShell and Sys.FinishedShell() then return end` right after setting gamma — `ShellBootstrap.Init()` has no equivalent check and always proceeds.
- **No direct level-load path.** In the plain-`Sys.AutoLoad()` branch, resident calls `LevelBootstrap.LoadLevel(Sys.GetLevelName(), Sys.GetMasterScriptName())` directly. Shell calls `MrxGuiShellBootstrap.LoadShell()` instead — there's no `LevelBootstrap.lua` anywhere in `shell/`, so the front end never loads a level directly; it always routes through the shell GUI.
- **Shell interposes a precache gate resident doesn't have.** When the intro movies finish playing, this file's `_PlayMovie()` calls `StartPrecache()` (which waits on `IsFinishedPrecache` via a 2-second poll before calling `Start()`); `GameBootstrap._PlayMovie()` calls `Start()` straight away with no equivalent wait. But when movies are *skipped* (`Sys.PlayIntroMovies()` false), this file's own `Init()` also jumps straight to `Start()`, bypassing precache entirely — so the precache wait only happens on the normal splash-movie path, not the skip-movies path.
- **Shell mutes/restores user music around the splash movies.** `Init()` guardedly calls `Sound.OverrideUserMusic()` before playing movies, and `Start()` guardedly calls `Sound.RestoreUserMusic()` — resident's `GameBootstrap` does neither.
- **Shell owns its own teardown** (`ResetSingleton`/`ShellExitComplete`) — resident's `GameBootstrap` has no equivalent pair; leaving/resetting the shell is naturally a shell-only concern.
- Skip or reorder the splash logos the same way as resident: edit `tMovies`. Note the reversed default order above before assuming it's a typo elsewhere in the wiki.
