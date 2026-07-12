---
title: MrxGuiBootstrap_ShellOnly
parent: Shell Modules
nav_order: 5
inherits: none
tags: [shell]
verified: false
---

# MrxGuiBootstrap_ShellOnly

## Overview
The shell build's counterpart to [`MrxGuiBootstrap`](../resident/mrxguibootstrap): same function names (`ToggleHud`, `CreatePlayerHud`, `DeleteHud`, `DeleteAllHuds`, `SetSatelliteOverlay`, `SetOnGuiLoadedFunc`), but every one of them is an empty stub here. There's no per-player gameplay HUD to create, delete, or toggle from the main menu, so the shell build ships the same call surface with the bodies gutted rather than removing the functions outright.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxGuiBase`, `MrxGui`, `MrxGuiShellBootstrap`

Compare `resident/mrxguibootstrap.lua`, which imports those same three **plus** `MrxGuiManager`, `MrxUtil`, and `MrxGuiInterface` — the extra imports it needs to actually delegate to `MrxGuiManager`.

## Instance pattern
Stateless utility module. One incidental module-level global: `oPauseModule` (assigned without `local` inside `_PauseScreenLoaded`, the same leak-to-global pattern flagged on the resident version).

## Functions

### Init()
Identical to `resident/mrxguibootstrap.lua`'s `Init()`: loads `"MrxGuiPauseLayout"` via `MrxGuiBase.LoadGUIFile`, and registers `ExitMultiplayer` with `MrxGuiShellBootstrap.SetExitMultiplayerCallback(ExitMultiplayer, {})`.

### Deinit()
Empty. Not implemented in either build.

### _PauseScreenLoaded(PauseScreenModule)
Identical to resident: closes the pause screen immediately via `PauseScreenModule.MrxGuiPauseScreen.ClosePauseScreen(...)`, then stashes `PauseScreenModule` into the global `oPauseModule`.

### ToggleHud(uGuid, bVisible, sContext)
Empty stub. Resident's version forwards to `MrxGuiManager.ToggleHud(uGuid, bVisible, sContext)`.

### CreatePlayerHud(uPlayerGuid)
Empty stub. Resident's version forwards to `MrxGuiManager.CreateGui(uPlayerGuid)`.

### DeleteHud(uPlayerGuid)
Empty stub. Resident's version forwards to `MrxGuiManager.DeleteGui(uPlayerGuid)`.

### DeleteAllHuds()
Empty stub. Resident's version calls `MrxGuiManager.DeleteAddGuis()` — which, per [the resident page](../resident/mrxguibootstrap), doesn't actually exist (the real function is `DeleteAllGuis`), making resident's version a guaranteed error if it's ever called. The shell build sidesteps that broken call entirely by not implementing anything here.

### GetNumberOfPlayersFromShellSelection()
**Not stubbed** — identical in both builds: `return MrxGuiShellBootstrap.nPlayersSelected`. The one function here that still does real work.

### SetSatelliteOverlay(uPlayer, bOn, sFaction)
Empty stub. Resident's version forwards to `MrxGuiManager.ToggleSatellite(uPlayer, bOn, sFaction)`.

### SetOnGuiLoadedFunc(fFunc, tArgs)
Empty stub. Resident's version forwards to `MrxGuiManager.SetLoadingCompleteCallback(fFunc, tArgs)`. This is the function [`MrxShellBootstrap.Start()`](mrxshellbootstrap) registers `_GuiLoaded` against — because this body is empty, that registration is a no-op in the shell build (see the notes on that page).

## Events
No `Event.*` calls in either build — `Init()`'s callback wiring (`LoadGUIFile`'s load-completion callback, `SetExitMultiplayerCallback`) is plain stored-function wiring, same as resident.

## Notes for modders
**Concrete divergence from [`MrxGuiBootstrap`](../resident/mrxguibootstrap):** the function signatures are identical, but six of the ten functions here (`ToggleHud`, `CreatePlayerHud`, `DeleteHud`, `DeleteAllHuds`, `SetSatelliteOverlay`, `SetOnGuiLoadedFunc`) have empty bodies instead of forwarding to `MrxGuiManager`. `Init()`, `Deinit()`, `_PauseScreenLoaded()`, and `GetNumberOfPlayersFromShellSelection()` are the same in both. This makes sense in context — there's no per-player gameplay HUD to manage from the main menu — but it also means:
- **Calling `SetOnGuiLoadedFunc` from the shell doesn't register anything.** See [`MrxShellBootstrap`](mrxshellbootstrap): its `Start()` calls this function expecting it to wire up a GUI-loaded callback, and as decompiled nothing happens.
- If you're extending shell code and expect HUD-management calls to do *something*, they won't here — that's not a bug so much as an accurate reflection of "there is no HUD in the main menu."
