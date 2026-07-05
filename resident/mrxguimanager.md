---
title: MrxGuiManager
parent: GUI & HUD
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [gui, hud]
verified: true
verified_note: 'deeper pass: re-confirmed all functions, the three real MrxGui.SendEvent EventType payloads, and the singleton instance pattern against source; added the four master GUI layout asset names (MrxGuiHudLayout2/MrxGuiBinocularsLayout/MrxGuiSatelliteLayout/MrxGuiPdaLayout), the ToggleHud context whitelist, and the cached local-HUD widget names; pruned the vacuous CreateGui boilerplate note'
---

# MrxGuiManager

*Module: mrxguimanager.lua*

## Overview
The `MrxGuiManager` module is responsible for managing the creation, duplication, and lifecycle of various GUI layouts in the game. It handles the loading of master copies of HUD, binoculars, satellite, and PDA layouts, then duplicates these layouts per player. The module also manages the visibility state of the HUD through a sleep/visibility stack and routes events related to the satellite overlay.

## Inheritance
- Inherits from: `none` (base/utility module)
- Imports: `MrxGui`, `MrxUtil_Shell`

## Instance pattern
Stateless singleton/utility module — plain module-level globals, no `Create`/`OnActivate`/`Awake`/`tInstance`. All state is declared `false` at load time and populated by `Init()`:
- `_tPlayerGuiList`: keyed by player GUID, each entry a `{oHud, oScope, oSatellite, oPda, nHudState}` table — the actual per-player duplicated layouts. This is the closest thing to "per-instance" state in the file, but it's a plain table keyed by GUID, not a `tInstance`/metatable-based instance.
- `_oMasterHud` / `_oMasterSatellite` / `_oMasterScope` / `_oMasterPda`: the one-time-loaded master layouts (set by `HudLoaded`/`SatelliteLoaded`/`ScopeLoaded`/`PdaLoaded` via `_SetupMasterLayouts`), each duplicated per player in `CreateGui`. Set back to `false` once all four are loaded and consumed.
- `_tPendingList`: player GUIDs whose `CreateGui` call arrived before all four master layouts finished loading.
- `_fLoadingDone` / `_tLoadingDoneData`: a deferred callback + args set by `SetLoadingCompleteCallback` when no GUIs exist yet, fired from `CreateGui`.
- `_tHudStates`: keyed by player GUID, boolean HUD-visible state (mirrors but is distinct from each player's `nHudState` refcount).
- `_tPendingHudWidgets`: keyed by player GUID, widgets queued via `AddWidgetToHud`/`RemoveWidgetFromHud` before that player's GUI exists yet.
- `_bLoadingNow`: guards against re-issuing the four `MrxGui.LoadGuiFile` calls while a load is already in flight.
- `_bFirstGuiInQueue`: `true` initially; the first `CreateGui` call after all masters load consumes the master layouts directly (via `.AddedWidgetList` reassignment) rather than duplicating them, since nothing else needs the masters once the first real player GUI is built.

`Init()` resets `_tPlayerGuiList`, `_tPendingList`, `_tHudStates`, `_tPendingHudWidgets` to fresh empty tables — no call site for `Init()` found in this file itself (presumably invoked once by an external bootstrap).

## Functions
### `Init()`
**Not previously documented** — resets the module's four tracking tables (`_tPlayerGuiList`,
`_tPendingList`, `_tHudStates`, `_tPendingHudWidgets`) to empty. Standard lifecycle reset, not something a
mod would normally call directly.

### `CreateGui(uPlayerGuid)`
Called when a new player's GUI needs to be created. Loads master copies of GUI layouts if they haven't been loaded yet, then duplicates these layouts for the given player. Assigns ownership of these layouts to the player and initializes them. If the local player is creating their GUI, it caches certain widgets like `MessageBox`, `Minimap`, `ObjectiveTray`, `SubtitleBuffer`, and `MapLabel`.

### `ToggleHud(uPlayerGuid, bEnable, sContext)`
Toggles the visibility state of the HUD for a given player. Uses a refcounted sleep/visibility stack (`nHudState`) to manage when widgets should be shown or hidden. Context-specific logic is applied to selectively wake specific widgets based on the context (e.g., "briefing", "hijack").

### `_DetoggleWidget(sName, uOwner)`
Private function that wakes up a single widget by name and owner.

### `_DetoggleWidgetRecursive(sName, uOwner)`
Private function that recursively wakes up a widget and all its children by name and owner.

### `_RecursiveWakeup(oWidget)`
Private recursive function that sets a widget and all its children to be awake (not sleeping).

### `GetHudState(uPlayerGuid)`
Returns the current visibility state of the HUD for a given player.

### `AddWidgetToHud(uPlayerGuid, oWidget, bIncludeChildren)`
Adds a widget to the HUD for a given player. If the widget has children and `bIncludeChildren` is true, it recursively adds all children as well.

### `RemoveWidgetFromHud(uPlayerGuid, oWidget, bRemoveChildren)`
Removes a widget from the HUD for a given player. If the widget has children and `bRemoveChildren` is true, it recursively removes all children as well.

### `ToggleSatellite(uPlayerGuid, bEnable, sType, bSuppressMinigame)`
Toggles the satellite overlay state for a given player. Sets up callbacks for map mode changes and sends events to update the satellite progress and state.

### `ApplySatelliteUpdateEvent(uPlayer, nX, nY, nZ, nPercent)`
Private function that sends an event with updated satellite progress information.

### `DoNothing()`
A no-op function used as a placeholder callback.

### `SetSatelliteSuccessCallback(uPlayer, fCallback, tData)`
Sets the success callback for the satellite minigame. This callback is triggered when the satellite designation is successful.

### `SetSatelliteMinigameData(uPlayer, tData)`
Sets the data for the satellite minigame sectors.

### `SetSatelliteCost(uPlayer, nCost)`
Sets the cost of the satellite minigame.

### `DeleteGui(uPlayerGuid)`
Deletes the GUI for a given player by removing and deleting all widgets associated with that player's layouts.

### `DeleteAllGuis()`
Deletes the GUI for all players by calling `DeleteGui` for each player in the list.

### `SetLoadingCompleteCallback(fFunc, tData)`
Sets a callback function to be called when all GUIs have been loaded. If there are already loaded GUIs, it calls the function immediately; otherwise, it stores the callback and data for later use.

### `HudLoaded(oHudModule)`
Called when the HUD layout is loaded. Sets up the master HUD layout.

### `ScopeLoaded(oScopeModule)`
Called when the binoculars (scope) layout is loaded. Sets up the master scope layout.

### `SatelliteLoaded(oSatelliteModule)`
Called when the satellite layout is loaded. Sets up the master satellite layout.

### `PdaLoaded(oPdaModule)`
Called when the PDA layout is loaded. Sets up the master PDA layout.

### `_SetupMasterLayouts(oHud, oSatellite, oScope, oPda)`
Private function that sets up the master copies of GUI layouts once they are all loaded.

### `_AllRequiredModulesLoaded()`
Private function that checks if all required GUI modules have been loaded.

### `_RemoveAndDeleteWidgets(tLayout)`
Private function that removes and deletes all widgets in a given layout.

## Events
No `Event.*` calls appear anywhere in this file — there is no `OnActivate`/`Awake`/`Event.ObjectHibernation`, and no `HideMarker` event of any kind. All "events" this module deals with are plain Lua tables with an `EventType` string field, dispatched via `MrxGui.SendEvent(tEvent)` — the GUI system's own notification mechanism, unrelated to the engine `Event.*` API. Three real payload shapes appear:
- `EventType = "E3HudMode"` with `bOn` (boolean) — sent from `CreateGui` when `MrxGui.IsE3HudModeActive()` is true.
- `EventType = "SatelliteStateChange"` with `uPlayerGuid`, `bActivate`, `bAdvanced`, `bMinigame` — sent from `ToggleSatellite`.
- `EventType = "SatelliteProgressUpdate"` with `uPlayerGuid`, `nX`, `nY`, `nZ`, `nPercent` — sent from both `ToggleSatellite` (reset to 0%) and `ApplySatelliteUpdateEvent` (the callback registered via `Player.SetPDAMapModeCallback` in `ToggleSatellite`).

## Module constants & tunables
- **The four master layout asset names** loaded once by `CreateGui` (via `MrxGui.LoadGuiFile`):
  `"MrxGuiHudLayout2"` (HUD), `"MrxGuiBinocularsLayout"` (scope), `"MrxGuiSatelliteLayout"` (satellite overlay),
  `"MrxGuiPdaLayout"` (PDA). These are the layout definitions every player's GUI is duplicated from.
- **`ToggleHud` context whitelist** — the `sContext` strings that selectively keep some widgets awake while the
  rest of the HUD sleeps: `"briefing"`, `"hijack"`, `"satellite"`, `"scope"`. Any other string hides everything.
  Each context wakes a specific hard-coded widget set (e.g. `"briefing"` keeps `"MessageBox"`,
  `"Subtitle Buffer"`, `"Context Action Text"`, `"Faction Display"`, `"Resource Counters"` visible).
- **Cached local-HUD widget names** (`CreateGui`, local player only): `"MessageBox"`, `"Minimap"`,
  `"Objective Tray"`, `"Subtitle Buffer"`, `"Map Label"` — exposed as the globals
  `_G.MessageBox`/`_G.Minimap`/`_G.ObjectiveTray`/`_G.SubtitleBuffer`/`_G.MapLabel`.
- **Satellite overlay widget name: `"Satellite overlay"`** — the target of `SetSatelliteSuccessCallback`,
  `SetSatelliteMinigameData`, and `SetSatelliteCost` (all via `MrxGui.GetWidgetByNameAndOwner`).

## Notes for modders
- Use `ToggleHud` to control the visibility of the HUD for players — it's refcounted via `nHudState`, so mismatched enable/disable calls will leave the HUD in an unexpected state.
- Customize widget behavior by adding or removing widgets using `AddWidgetToHud` and `RemoveWidgetFromHud` — both work correctly even before the target player's GUI exists yet, queuing into `_tPendingHudWidgets` and flushing once `CreateGui` runs for that player.
- Manage satellite overlay state with `ToggleSatellite`, which also drives `Player.SetPDAMapModeCallback` — disabling swaps the callback to the no-op `DoNothing`, it does not clear the callback.
- The very first player's GUI after all four master layouts finish loading takes over the master layouts' `AddedWidgetList` directly (`_bFirstGuiInQueue`); every subsequent player gets a fresh `MrxGui.DuplicateLayout` copy. This asymmetry is only relevant if you're hooking `CreateGui` itself.
- `CreateGui` caches several global widget references (`_G.MessageBox`, `_G.Minimap`, `_G.ObjectiveTray`, `_G.SubtitleBuffer`, `_G.MapLabel`) — but only when `uPlayerGuid == Player.GetLocalPlayer()`, so these globals reflect the local player's HUD only.