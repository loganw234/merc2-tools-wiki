---
title: MrxCheatBootstrap
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [cheats, menu, beginner-friendly]
---

# MrxCheatBootstrap

*Module: mrxcheatbootstrap.lua*

## Overview

`MrxCheatBootstrap` is the game's own developer cheat menu — an in-game, multi-page dialog for adding
cash/fuel/support, skipping to any mission, modifying faction attitudes, unlocking landing zones, and
dispensing rewards. It's a stateless manager module: no per-instance state, just a set of functions that
build and display `MrxMultiPageMenu` dialogs.

**This module is one of the best starting points in the whole corpus for a new modder.** Everything it
does is already a real, working, non-destructive example of calling into the game's economy, faction,
and mission systems — and several of its actions are useful called *directly*, one-off, from the
`lua_console.py` REPL, without ever opening the interactive menu at all.

## Quick start: open the menu

```lua
_G.Cheat.DisplayOptions()
```

That's the entire public entry point — the module registers itself as `_G.Cheat` at the bottom of the
file (`_G.Cheat = {DisplayOptions = DisplayOptions}`). Run that one line from the console while in a
level and the game's own cheat menu should open on-screen, exactly as it would for a developer build.

## Even quicker: skip the menu, call the actions directly

Every menu option ultimately just calls a handful of underlying functions. If you want the effect
without the UI (e.g. from an `OnKey` script), these are exactly what the menu itself calls — copy-paste
ready:

| Want to... | Call this |
|---|---|
| Add cash | `MrxPmc.AddCashQty(100000)` — the menu offers 1000 / 10000 / 100000 / 1000000 / 10000000 / 100000000 as preset buttons, but any number works |
| Add fuel | `MrxPmc.AddFuelQty(1000)` — if the amount would exceed the current capacity, raise it first: `MrxPmc.SetFuelCapacity(9999, true)` |
| Unlock every landing zone | `MrxTransit.UnlockAllLandingZones()` |
| Dispense every reward | `MrxRewardData.DispenseAllRewards()` |
| Teleport all players | `_G.DebugTeleport(x, y, z)` — also defined in this file, see below |
| Give one support item | `MrxPmc.AddSupportQty(sSupportKey, 1)` — keys come from `MrxSupportData.tSupportData` |
| Change a faction relationship | `MrxFactionManager.SetRelation(sSubjectAbbrev, sObjectAbbrev, nRelation)` |

### "The Works!" — give (almost) everything at once

The support-menu's `"The Works! + $ + F"` option is the single most generous action in the file. As a
standalone snippet:

```lua
local tSupportData = MrxSupportData.tSupportData
for sKey, tData in pairs(tSupportData) do
  MrxPmc.AddSupportQty(sKey, tData.nMaxStock - (MrxPmc.GetSupportQty(sKey) or 0))  -- max out every support item
end
MrxPmc.AddCashQty(10000000)
MrxPmc.SetFuelCapacity(9999, true)
MrxPmc.AddFuelQty(9999)
MrxSupportData.SetIgnoreRequirements(true)  -- bypasses whatever prerequisites normally gate support items
```

Note the last line: `MrxSupportData.SetIgnoreRequirements(true)` is a global switch, not scoped to this
menu session — once set, support-item prerequisite checks stay bypassed.

## `_G.DebugTeleport(x, y, z)`

```lua
function _G.DebugTeleport(x, y, z)
  local tPlayers = Player.GetAllPlayers()
  local tLocs = {}
  for k, v in pairs(tPlayers) do
    table.insert(tLocs, {x, y, z})
  end
  MrxUtil.TeleportHeroesToLocations(tLocs)
end
```

Registered globally (not just inside this module), so it's callable any time this module has loaded:
`_G.DebugTeleport(100, 0, 250)`. Moves *every* player to the same coordinates — there's no per-player
targeting here, it builds one location per player but always the same `x, y, z`. Pair this with
[`Object.GetPosition(...)`](../recipes#get-your-current-position) to first read a known-good location
before jumping somewhere new.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `MrxFactionManager`, `MrxLayerManager`, `MrxMultiPageMenu`, `MrxPlayState`, `MrxRewardData`,
  `MrxTaskState`, `MrxTransit`, `MrxUtil`, `WifMissionData`, `WifMissionFlow`, `WifVzBoundary`,
  `WifCheatStockpile`, `MrxPmc`, `MrxSupportData`, `WifPmcInterior`, `Munitions`

## Instance pattern

Stateless manager module — no `Create`/`uGuid` pattern. A handful of module-level globals track menu
navigation state between dialog callbacks: `_oCurrTask` (current node in the mission-tree traversal
dialog), `_sSubjectAbbrev`/`_sObjectAbbrev` (faction-attitude dialog's current selection),
`_sSkipToMissionId`/`_bSkipToBriefing` (pending mission-skip target), `_sLastCompletedContractName`.

## Functions

### `DisplayOptions()`
The public entry point (exposed as `_G.Cheat.DisplayOptions`). Calls `_DisplayRootDialog()`.

### `_DisplayRootDialog()`
Builds and shows the root menu. Skip-to-mission, skip-to-briefing, "complete current contract", and
"traverse mission hierarchy" are all hidden while `WifPmcInterior.IsInside()` is true (i.e. while inside
a PMC interior/HQ) — those five options only appear during actual mission gameplay.

### `_DisplaySkipDialog(bDoBriefing)`
Lists every mission name from `WifMissionData.tMissionData`, alphabetically. Selecting one calls
whatever callback was registered via `SetMissionSkipDialogCallback`, passing `(sMissionName, bDoBriefing)`.

### `_DisplayTraverseDialog()`
Walks the live mission/task tree starting from `_oCurrTask`. Lists active children
(`oChild:IsActive()`), and offers Complete / Cancel / "Up a level" depending on the current task's state
and `MrxPlayState.Get()`. Auto-climbs past already-completed parent tasks before rendering. This is a
working example of the task-tree object API (`:GetParent()`, `:GetChildren()`, `:IsActive()`,
`:Complete()`, `:Cancel()`, `:GetLineage()`) if you need to inspect or manipulate mission state
programmatically instead of through the menu.

### `_CompleteCurrentContract()`
`MrxPlayState.GetCurrentMission():Complete()` on whatever contract is currently active.

### `_DisplayAddCashDialog()` / `_DisplayAddFuelDialog()` / `_DisplayAddSupportDialog()`
Preset-amount dialogs — see the table above for the exact values and equivalent direct calls.

### `_DisplayModAttitudeDialog(sSubjectAbbrev, sObjectAbbrev, nRelation)` / `_DisplayFactionDialog(bSubject)` / `_DisplayAttitudeDialog()`
Three linked dialogs for reading/writing faction relationships. Defaults to subject `"All"`, object
`"Pmc"` if unset. Reading: `MrxFactionManager.GetRelation(subject, object)`. Writing:
`MrxFactionManager.SetRelation(subject, object, relation)`. Faction abbreviations come from
`MrxFactionManager.GetFactionAbbrevs()`; named attitude levels (rather than raw relation numbers) come
from `MrxFactionManager.GetAttitudes()`.

### `_G.DebugTeleport(x, y, z)`
See above.

### `EnableSkipMode(bEnable, sMissionId, bBriefing)`
Arms or disarms "skip to mission" mode. On disable, if a target mission was set, restores resources to
whatever `WifCheatStockpile[sMissionId]` specifies for that mission (support items, equipment, cash,
fuel) — a mission-appropriate loadout rather than leaving whatever the player had.

### `IsSkipModeEnabled()` / `GetMissionSkipData()`
Simple accessors for the skip-mode state set by `EnableSkipMode`.

### `SetMissionSkipDialogCallback(fMissionSkipDialogCallback)`
Registers the callback `_DisplaySkipDialog` invokes when a mission is selected — this is how the actual
skip behavior gets wired up from outside this module.

## Events

Doesn't subscribe to engine events directly — all navigation happens through `MrxMultiPageMenu`
option/callback wiring instead.

## Notes for modders

- `_G.Cheat.DisplayOptions()` and `_G.DebugTeleport(...)` are the two functions explicitly exposed on
  `_G`, meaning they're always reachable by name regardless of what else you're doing — good first
  things to try from the console.
- Every dialog function here follows the same shape: `MrxMultiPageMenu.Reset()`, add options, add a
  "return to root" and/or "close" option, `MrxMultiPageMenu.Display(...)`. That's a reusable template if
  you want to build your own multi-page in-game menu for a mod.
- `MrxSupportData.SetIgnoreRequirements(true)` is a global, sticky toggle — worth knowing if a mod
  behaves differently after someone has opened this menu and used "The Works!".
