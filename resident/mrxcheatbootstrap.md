---
title: MrxCheatBootstrap
parent: Cheats & Dev Tools
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [cheats, menu, beginner-friendly]
verified: true
verified_note: "deeper pass: re-confirmed the _G.Cheat = {DisplayOptions=...} and _G.DebugTeleport surface, all 16 imports, the cash/fuel preset lists, and the exact 'The Works!' body against source; all prior live-test results left intact; cross-linked the cheat-menu top-level page and the imported resident modules that have wiki pages"
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
For the full walkthrough of the on-screen menu (screenshots, every option), see the
[Cheat Menu](../cheat-menu) top-level page.

## Even quicker: skip the menu, call the actions directly

Every menu option ultimately just calls a handful of underlying functions. If you want the effect
without the UI (e.g. from an `OnKey` script), these are exactly what the menu itself calls — copy-paste
ready.

**One catch, confirmed by live testing:** every row below except the last is a `resident/` module
namespace (`MrxPmc`, `MrxTransit`, `MrxRewardData`, `MrxFactionManager`), not a built-in engine
namespace — it isn't visible outside this file until you `import()` it yourself. Skip that and you'll
get `attempt to index global 'MrxPmc' (a nil value)` (or whichever name). `_G.Cheat.DisplayOptions()`
(above) and `_G.DebugTeleport(...)` (last row) are the exceptions: they're published directly to `_G` by
this file, so they work from anywhere with no import needed. See the [Glossary](../glossary#importname)
for why.

| Want to... | Call this |
|---|---|
| Add cash | `import("MrxPmc"); MrxPmc.AddCashQty(100000)` — the menu offers 1000 / 10000 / 100000 / 1000000 / 10000000 / 100000000 as preset buttons, but any number works. **Confirmed working, HUD updates.** |
| Add fuel | `import("MrxPmc"); MrxPmc.AddFuelQty(1000)` — if the amount would exceed the current capacity, raise it first: `MrxPmc.SetFuelCapacity(9999, true)`. **Confirmed working, HUD updates.** |
| Unlock every landing zone | `import("MrxTransit"); MrxTransit.UnlockAllLandingZones()` — **confirmed working**, but runs silently: no on-screen confirmation, check the map/travel menu to see the effect |
| Dispense every reward | `import("MrxRewardData"); MrxRewardData.DispenseAllRewards()` — **confirmed working**: grants a large amount of cash, fuel, faction reputation, and shop-item unlocks all at once |
| Give one support item | `import("MrxPmc"); MrxPmc.AddSupportQty(sSupportKey, 1)` — keys come from `MrxSupportData.tSupportData`. **Confirmed working.** |
| Change a faction relationship | `import("MrxFactionManager"); MrxFactionManager.SetRelation(sSubjectAbbrev, sObjectAbbrev, nRelation)` — **read the caveat below before using this one** |
| Teleport all players | `_G.DebugTeleport(x, y, z)` — no import needed, see below (and read the warning first) |

Confirmed by live testing: the lower-level `Player.SetCash(...)`/`Player.AddCash(...)` (true engine
namespace, always global, no import needed) *do* change your actual cash/fuel — but they skip the HUD
refresh `MrxPmc.AddCashQty`/`AddFuelQty` trigger, so the on-screen number won't visibly update even
though the value changed. Use the `MrxPmc.*` calls above, not the raw `Player.*` setters, if you want
what's displayed to actually update.

### `SetRelation` caveat: it silently no-ops for non-mutable factions

Confirmed by live testing: `MrxFactionManager.SetRelation("All", "Pmc", 100)` had no discernible effect.
Reading the source explains why —

```lua
function SetRelation(sSubjectAbbrev, sObjectAbbrev, nRelation, bInitialize)
  if sObjectAbbrev == "Pmc" and not IsAttitudeMutable(sSubjectAbbrev) then
    Debug.Printf("CAN'T SET RELATION ... ATTITUDE IS NOT MUTABLE")
    return
  end
  -- ...
end
```

Each faction has a runtime `bAttitudeMutable` flag, normally flipped on by the mission flow once that
faction becomes "contestable" in the story — not something that's necessarily true from the start.
`SetRelation` toward `"Pmc"` silently returns if that flag isn't set yet, and the only trace of it
happening is a message on the engine's own noisy `Debug.Printf` channel (the exact channel `Loader.Printf`
exists to avoid — see [Getting Started](../getting-started)), so from the console it just looks like
nothing happened.

If you want to force it: every faction also has a static `bDynamic` flag (set once, at table-definition
time, not mission-dependent) gating whether its mutability *can* be turned on at all via
`SetAttitudeMutable`:

```lua
import("MrxFactionManager")
MrxFactionManager.SetAttitudeMutable("All")           -- flips bAttitudeMutable on, if bDynamic allows it
MrxFactionManager.SetRelation("All", "Pmc", 100)       -- now has a chance of actually taking effect
```

**Confirmed working by live testing** — the faction meter in the game's own UI visibly shifts. Tested
against the `"All"` faction specifically (the only one visible that early in a fresh game); other
factions should behave the same way once they've appeared, but that hasn't been individually confirmed
for each one.

### "The Works!" — give (almost) everything at once

The support-menu's `"The Works! + $ + F"` option is the single most generous action in the file. As a
standalone snippet:

```lua
import("MrxPmc")
import("MrxSupportData")
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

**Confirmed working by live testing** — ran the full snippet as-is, no errors. Correctly triggered the
same UI feedback as the individual cash/support calls, and maxed out at 99 of every support item plus
the cash/fuel amounts specified.

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
[`Object.GetPosition(...)`](../snippets#get-your-current-position) to first read a known-good location
before jumping somewhere new.

**Confirmed by live testing — crashes to desktop if used while inside an interior cell** (e.g. the PMC
HQ interior). Works fine outdoors/in the open world. Exit to an outdoor area before calling this, or
avoid it entirely while indoors. Root cause not confirmed (plausibly the target coordinates being
outside the interior's own coordinate space, or the interior's rendering/physics state not expecting a
sudden teleport) — treat "safe outdoors, unsafe indoors" as the operating rule regardless of cause.

## Inheritance
- Inherits from: none — base/utility module
- Imports (16): [`MrxFactionManager`](mrxfactionmanager), [`MrxLayerManager`](mrxlayermanager),
  [`MrxMultiPageMenu`](mrxmultipagemenu), [`MrxPlayState`](mrxplaystate), [`MrxRewardData`](mrxrewarddata),
  [`MrxTaskState`](mrxtaskstate), [`MrxTransit`](mrxtransit), [`MrxUtil`](mrxutil), `WifMissionData`,
  `WifMissionFlow`, `WifVzBoundary`, `WifCheatStockpile`, [`MrxPmc`](mrxpmc),
  [`MrxSupportData`](mrxsupportdata), `WifPmcInterior`, [`Munitions`](munitions). (The `Wif*` modules
  are level/campaign data with no wiki pages of their own.)

## Instance pattern

Stateless manager module — no `Create`/`uGuid` pattern. A handful of module-level globals track menu
navigation state between dialog callbacks: `_oCurrTask` (current node in the mission-tree traversal
dialog), `_sSubjectAbbrev`/`_sObjectAbbrev` (faction-attitude dialog's current selection),
`_sSkipToMissionId`/`_bSkipToBriefing` (pending mission-skip target), `_sLastCompletedContractName`.

## Functions

### `DisplayOptions()`
The public entry point (exposed as `_G.Cheat.DisplayOptions`). Calls `_DisplayRootDialog()`.

### `SetTaskTreeRoot(oCurrTask)`
**Not previously documented** — the setter for `_oCurrTask` (see Instance pattern above), i.e. what
`_DisplayTraverseDialog` actually starts walking from. Not called anywhere else in this file; something
external (the mission/task system itself, when a mission activates) is expected to call this to point the
traversal dialog at the right root.

### `_AddRootOption()` / `_AddCloseOption()`
**Not previously documented** — two tiny shared helpers used throughout this file's dialog builders:
`_AddRootOption` adds a `"Return to root menu"` option that calls `_DisplayRootDialog`, `_AddCloseOption`
adds a plain `"Close this menu"` option. Both just wrap a one-line `MrxMultiPageMenu.AddOption` call so every
submenu gets the same two navigation options without repeating the exact wording/flags each time.

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
