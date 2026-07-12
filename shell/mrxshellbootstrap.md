---
title: MrxShellBootstrap
parent: Shell Modules
nav_order: 3
inherits: none
tags: [shell]
verified: false
---

# MrxShellBootstrap

## Overview
A small readiness-gate module that tracks whether the shell's GUI has finished loading and whether the local player has joined, so a caller can be notified once both are true. It's invoked once, by [`Shell.Init()`](shell), at the very top of the front-end build's startup.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxSoundShellBootstrap`, `MrxGuiBootstrap_ShellOnly`

`MrxSoundShellBootstrap` is imported but never referenced anywhere in this file's 38 lines.

## Instance pattern
Singleton-state manager. Module-level globals:
- `_bGuiLoaded` — whether the shell GUI has finished loading.
- `_bLocalPlayerJoined` — whether the local player has joined. Reset to `false` in `Start()`, but nothing in this file ever sets it back to `true`.
- `_sHeroSpawnLocation` (assigned without `local`, so it's a global) — stored but never read anywhere in this file.
- `_fOnDoneCallback` / `_tOnDoneCallbackArgs` — the callback and args passed into `Start()`.

## Functions

### Start(fCallback, tCallbackArgs)
Resets both readiness flags to `false`, clears `_sHeroSpawnLocation`, stores `fCallback`/`tCallbackArgs` into `_fOnDoneCallback`/`_tOnDoneCallbackArgs`, then calls `MrxGuiBootstrap_ShellOnly.SetOnGuiLoadedFunc(_GuiLoaded)` to register `_GuiLoaded` as the GUI-load callback. Called once, by [`Shell.Init()`](shell).

### IsGuiLoaded()
Returns `_bGuiLoaded`.

### _GuiLoaded()
Logs "gui loaded"; if `_bGuiLoaded` isn't already `true`, sets it and calls `_End()`. The `not _bGuiLoaded` guard makes this idempotent against being invoked more than once.

### _End()
Returns early unless both `_bLocalPlayerJoined` and `_bGuiLoaded` are `true`. As decompiled, once both checks pass the function body simply ends — it does not call `_fOnDoneCallback`/`_tOnDoneCallbackArgs`, the values `Start()` stored and that this file otherwise never touches again. See the gotcha below.

### SetHeroSpawnLocation(sHeroSpawnLocation)
Public setter that stores its argument into the global `_sHeroSpawnLocation`. Never read within this file — presumably consumed elsewhere (directly off the `MrxShellBootstrap` global table) once the local player actually spawns into a level from the shell.

## Events
None — no `Event.*` calls. The GUI-loaded notification is a stored function callback (`SetOnGuiLoadedFunc`), not the engine event system.

## Notes for modders
- **The GUI-loaded registration is wired to a no-op in this build.** `Start()` registers `_GuiLoaded` via `MrxGuiBootstrap_ShellOnly.SetOnGuiLoadedFunc(_GuiLoaded)` — but [`MrxGuiBootstrap_ShellOnly.SetOnGuiLoadedFunc`](mrxguibootstrap_shellonly) has an **empty function body** in the shell build (unlike `resident/mrxguibootstrap.lua`'s version, which forwards to `MrxGuiManager.SetLoadingCompleteCallback`). As decompiled, that means `_GuiLoaded` is never actually invoked through this path, so `_bGuiLoaded` has no visible way to become `true` from within this corpus — unless the engine calls it some other way not present in these files.
- **`_bLocalPlayerJoined` has no visible setter at all** in this file — something external would have to poke `MrxShellBootstrap._bLocalPlayerJoined = true` directly (it's a bare global, not locally scoped) for the other half of this gate to ever resolve.
- Taken together, `_End()`'s "both ready" branch looks unreachable from what's visible in `shell/` alone. If you're trying to hook "shell fully ready," this module's stored `_fOnDoneCallback` doesn't look like the live wire — treat it as a documented-but-dormant hook rather than a confirmed extension point.
