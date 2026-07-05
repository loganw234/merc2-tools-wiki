---
title: MrxBootstrap
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [bootstrap, initialization]
verified: true
verified_note: "deeper pass: expanded _End (both-flags gate, full StartWithResources payload incl. support-stock fill + SetIgnoreRequirements) and SetDefaultAtmosphere's concrete graphics constants, cross-linked imports, pruned vacuous notes; zero-Event.* finding re-confirmed"
---

# MrxBootstrap

*Module: mrxbootstrap.lua*

## Overview
The `MrxBootstrap` module is responsible for initializing the game world by handling GUI loading and local player joining events. It sets up the initial atmosphere settings, manages faction setup, and optionally grants starting resources to the player if a cheat is enabled.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: [`MrxSoundBootstrap`](mrxsoundbootstrap), [`MrxFactionManager`](mrxfactionmanager),
  [`MrxGuiBootstrap`](mrxguibootstrap), [`MrxLayerManager`](mrxlayermanager),
  [`MrxSupportData`](mrxsupportdata), [`MrxPlayer`](mrxplayer), [`MrxPmc`](mrxpmc), [`MrxState`](mrxstate),
  [`MrxUtil`](mrxutil)

## Instance pattern
This is a stateless manager/utility module. It does not track per-instance state but manages global initialization tasks.

## Functions
### `Start(fCallback, tArgs)`
Wires GUI-loaded and local-player-joined callbacks, calls `MrxPlayer.Start()`. Sets up the initial state for bootstrapping the game world.

### `IsGuiLoaded()`
Returns whether the GUI has been loaded.

### `_GuiLoaded()`
Called when the first GUI load event is received. Logs a debug message and sets `_bGuiLoaded` to true. If `_bHandleStateTransitions` is enabled, it enters the `STATE_WAITFORGAME` state and calls `_End`.

### `_LocalPlayerJoined()`
Called when the local player joins the game session. Logs a debug message and sets `_bLocalPlayerJoined` to true. Calls `_End` to complete initialization.

### `_End()`
The real completion step, but it early-returns unless **both** `_bLocalPlayerJoined` and `_bGuiLoaded` are
true — so whichever of `_GuiLoaded`/`_LocalPlayerJoined` fires second is the one that actually runs the
body. It exits `STATE_WAITFORGAME` (only if `_bHandleStateTransitions`), calls
`MrxFactionManager.Setup()`, and applies `SetDefaultAtmosphere()` for non-VZ levels (skipped when the
lowercased level name is `"vz"`). If `Sys.StartWithResources()` is true it maxes the player out:
`MrxPmc.AddCashQty(10000000)` (10M cash), fuel capacity/qty `9999`, fills every support type in
`MrxSupportData.tSupportData` to its `nMaxStock`, and calls `MrxSupportData.SetIgnoreRequirements(true)`.
Finally it fires the stored done-callback via `MrxUtil.CallWithOptionalArgs`.

### `SetDefaultAtmosphere()`
Sets the default atmosphere/bloom/monochrome/contrast settings for non-VZ levels. This function configures various graphics parameters to create a consistent visual environment.

### `SetHeroSpawnLocation(sHeroSpawnLocation)`
Sets the hero spawn location, which is not used in this module but can be referenced elsewhere.

### `SetHandleStateTransitions(bEnable)`
Enables or disables state transition handling during bootstrapping. This allows for more control over the initialization process.

## Events
This file has **zero `Event.*` references** — no `Event.Create`, no engine event constants. Both
"triggers" below are plain stored-callback wiring through other modules' setter functions, invoked by
direct function call when those modules decide the condition is met:
- `Start` calls `MrxGuiBootstrap.SetOnGuiLoadedFunc(_GuiLoaded)`, registering `_GuiLoaded` as the
  callback `MrxGuiBootstrap` invokes once the GUI finishes loading.
- `Start` calls `MrxPlayer.SetLocalPlayerJoinedCallback(_LocalPlayerJoined)`, registering
  `_LocalPlayerJoined` as the callback `MrxPlayer` invokes once the local player joins.

## Notes for modders
- **`SetDefaultAtmosphere()` is a big block of concrete graphics tunables** for the non-VZ look — sky
  `"afternoon"`, time-of-day `0.3` with speed `0` (frozen), bloom (`SetBlurRadius 0.5`, `SetThreshold
  0.775`, `SetMultiplier 0`), contrast (`SetLimit 0.1`, `SetMultiplier 1.5`), plus full ambient-cube and
  monochrome-gradient calls, all wrapped in `Graphics.Atmosphere.Begin()`/`.End(8)`. Edit these numbers to
  reskin the default world lighting. VZ levels skip this entirely.
- **`StartWithResources` is the "start rich" cheat**: 10M cash, `9999` fuel (capacity + qty), every support
  type filled to `nMaxStock`, and support requirements ignored. Gated on `Sys.StartWithResources()`.
- `SetHeroSpawnLocation` only stashes the value in `_sHeroSpawnLocation`; nothing in this file reads it
  back, so setting it here alone does nothing unless another module consumes it.
- `_End` runs its body only once both the GUI-loaded and local-player-joined flags are set — don't expect
  faction/atmosphere setup to happen off just one of them.