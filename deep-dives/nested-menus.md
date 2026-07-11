---
title: "Building Nested Menus with MrxMultiPageMenu"
parent: Deep Dives
nav_order: 12
---

# Deep Dive: Building Nested Menus with MrxMultiPageMenu

> **Status: confirmed working live.** Every piece of this — the pattern itself, the bare-global gotcha,
> and the shared-state approach — is extracted directly from `MasterCheatMenu.lua`
> ([All-In-One Cheat Menu](../cheat-menu)), a script whose full menu tree ("Player," "Support & Rewards,"
> "Spawner," "Fun," each with a working "Back") is itself confirmed working by live testing.

[`MrxMultiPageMenu`](../resident/mrxmultipagemenu) is the native menu system every custom menu on this wiki
"hijacks" — it's built into the game, already wired to the controller/dialog-box UI, and auto-paginates
past 8 options for free. What it *doesn't* have is any concept of a submenu. There's no `PushMenu`, no
`GoBack`, no menu stack at all. Building a multi-level menu tree out of it is entirely on you, using
nothing but the same three calls a single flat menu uses. This page is that technique, worked through with
the real, confirmed code it comes from.

## Why there's no built-in nesting

Read the module's own state (see [MrxMultipageMenu](../resident/mrxmultipagemenu)'s Instance pattern) and
the reason becomes obvious: it's a **stateless, module-global manager** — one shared set of tables
(`_tOptions`, `_tOptionsToCallbacks`, ...), not one instance per menu. "Only one multi-page menu can be in
progress at a time module-wide; a second `Reset()`/`AddOption()`/`Display()` sequence overwrites the
first." There's nowhere for a "parent menu" to wait while a submenu is open — showing a submenu doesn't
*suspend* the root menu's state, it **destroys** it. Going "back" isn't resuming anything; it's throwing
away the submenu's state and rebuilding the parent from scratch, same as opening it the first time.

Once that clicks, the whole technique is just: **every menu, at every level, is its own complete
`Reset → AddOption(...) → Display` sequence, wrapped in its own function.** A submenu option's callback is
just a function that happens to build a different menu. A "Back" option's callback is just a function that
happens to rebuild the parent.

## The confirmed pattern

Straight from `MasterCheatMenu.lua`, lightly trimmed — the root menu and one of its four submenus:

```lua
DisplayPlayerMenu = function()
  MrxMultiPageMenu.Reset()
  MrxMultiPageMenu.AddOption("Add $1,000,000", MrxPmc.AddCashQty, {1000000})
  MrxMultiPageMenu.AddOption("Fill Fuel", FillFuel)
  MrxMultiPageMenu.AddOption("Infinite Ammo: " .. (State.bInfiniteAmmo and "ON" or "OFF"), ToggleInfiniteAmmo)
  MrxMultiPageMenu.AddOption("Invincibility: " .. (State.bInvincible and "ON" or "OFF"), ToggleInvincible)
  MrxMultiPageMenu.AddOption("Unlock Costumes", UnlockAllCostumes)
  MrxMultiPageMenu.AddOption("Back", DisplayRootMenu)
  MrxMultiPageMenu.Display("Player Cheats:")
end

-- ============================================================
-- Root menu
-- ============================================================
DisplayRootMenu = function()
  MrxMultiPageMenu.Reset()
  MrxMultiPageMenu.AddOption("Player", DisplayPlayerMenu)
  MrxMultiPageMenu.AddOption("Support & Rewards", DisplaySupportMenu)
  MrxMultiPageMenu.AddOption("Spawner", DisplaySpawnerMenu)
  MrxMultiPageMenu.AddOption("Fun", DisplayFunMenu)
  MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)
  MrxMultiPageMenu.Display("Cheat Menu:")
end

DisplayRootMenu()
```

That's the entire technique. `"Player"` in the root menu points at `DisplayPlayerMenu` the same way any
other option points at any other callback — `AddOption` has no idea it's building a "submenu" versus a
one-shot action, because there's no such distinction in the module itself. `"Back"` inside
`DisplayPlayerMenu` is exactly as ordinary an option as `"Fill Fuel"` — it just happens to call a function
that rebuilds the menu one level up.

## The gotcha: why these are bare globals, not `local function`

Look closely at the declarations above: `DisplayPlayerMenu = function() ... end`, not
`local function DisplayPlayerMenu() ... end`. This is deliberate, and it's the one genuinely non-obvious
part of the whole technique.

`DisplayPlayerMenu` references `DisplayRootMenu` (in its `"Back"` option), and `DisplayRootMenu` references
`DisplayPlayerMenu` (in its `"Player"` option) — each one needs the other to already exist. Lua resolves a
bare name at the moment it's *used*, not when the enclosing function is *defined* (the same late-binding
fact [Overriding a Function](function-override#why-it-works) leans on) — so as long as **neither function
is actually called until every one of them has been assigned**, the mutual reference is completely safe
regardless of which one is written first in the file. `DisplayRootMenu()`, the one call that actually
kicks things off, sits at the very bottom of the script, after every `Display*Menu` assignment has already
run — so by the time anything is *called*, everything it might reference already exists.

Given that, plain `local function` declarations would actually work here too, with one sharp edge: it
would only keep working *because* nothing gets called early. Reorder the file, or add some helper that
calls one of these menu functions before the last declaration has run, and a `local` version can silently
capture a still-`nil` sibling — while `AddOption` doesn't error on that (a `nil` callback just closes the
menu quietly, per [MrxMultipageMenu](../resident/mrxmultipagemenu#notes-for-modders)), so the bug is a menu
option that mysteriously does nothing, not a crash pointing at the cause. Bare globals sidestep the
ordering question entirely — every `Display*Menu` name exists and is reachable the instant its assignment
line runs, so it no longer matters what order the functions appear in, or whether some future edit calls
one of them earlier than today's code does. The tradeoff is real: `DisplayPlayerMenu` is now a genuine
`_G` global, reachable (and collidable with an identically-named function) from anywhere else in the
session — a small price, worth paying deliberately rather than fighting declaration order for no reason.

## Sharing state across levels

Every submenu in `MasterCheatMenu.lua` reads and writes the *same* state table — not four separate ones —
because it's the exact `_G`-guarded pattern [Your First Menu](../first-menu#three-pieces-combined) already
establishes for a single flat menu, just referenced from more than one `Display*Menu` function instead of
one:

```lua
_G.MasterCheatMenuState = _G.MasterCheatMenuState or {
  bInfiniteAmmo = false,
  bInvincible = false,
  -- ...
}
local State = _G.MasterCheatMenuState
```

`State` here is a `local`, but it's a local alias for a table that lives in `_G` — every `Display*Menu`
function created later in the same file-execution closes over that same `local State`, so
`DisplayPlayerMenu` toggling `State.bInfiniteAmmo` and some other submenu reading it back both see the one
shared table. Nothing about navigating between menu levels needs its own plumbing; it's the same
"one shared table, guarded so a re-run doesn't reset it" idea, just read from more than one place.

## Putting it together: a minimal 2-level example

A smaller, from-scratch version of the same pattern — a spawn menu with two categories, each with its own
`"Back"`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

import("MrxMultiPageMenu")

local function SpawnHere(sTemplate)
  local uChar = Player.GetLocalCharacter()
  local x, y, z = Object.GetPosition(uChar)
  pcall(Pg.Spawn, sTemplate, x, y + 2, z)
end

-- ---- Leaf menus (deepest first -- pure style choice, order doesn't matter; see the gotcha above) ----
DisplayCarsMenu = function()
  MrxMultiPageMenu.Reset()
  MrxMultiPageMenu.AddOption("Veyron", SpawnHere, {"Veyron"})
  MrxMultiPageMenu.AddOption("ZTZ98 (Tank)", SpawnHere, {"ZTZ98"})
  MrxMultiPageMenu.AddOption("Back", DisplayRootMenu)
  MrxMultiPageMenu.Display("Spawn: Cars")
end

DisplayAircraftMenu = function()
  MrxMultiPageMenu.Reset()
  MrxMultiPageMenu.AddOption("UH1 Transport", SpawnHere, {"UH1 Transport (PMC)"})
  MrxMultiPageMenu.AddOption("Back", DisplayRootMenu)
  MrxMultiPageMenu.Display("Spawn: Aircraft")
end

-- ---- Root menu ----
DisplayRootMenu = function()
  MrxMultiPageMenu.Reset()
  MrxMultiPageMenu.AddOption("Cars", DisplayCarsMenu)
  MrxMultiPageMenu.AddOption("Aircraft", DisplayAircraftMenu)
  MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)
  MrxMultiPageMenu.Display("Spawn Menu:")
end

DisplayRootMenu()
```

Drop that in as `scripts/OnKey/NestedSpawnMenu.lua` and press Insert. Picking "Cars" replaces the menu
entirely with the Cars submenu; picking "Back" there rebuilds the root menu from scratch — there's no
third state hiding anywhere, just two more functions following the exact same shape as the root.

**Going a level deeper** (Root → Category → Sub-category) is the identical pattern recursed one more time:
a third tier of `Display*Menu` functions whose own `"Back"` points at their *immediate* parent, not the
root — nesting doesn't change the technique at all, it's the same three-call shape at every depth.

## Known limitations

- **Only one menu tree can be live at a time, wiki-wide.** The module's module-global state means your
  nested menu and, say, `CommonSpawnMenu.lua`'s picker can't both be "open" simultaneously — opening one
  while the other is up silently overwrites it. Not usually a practical problem (a player can only look at
  one menu anyway), but worth knowing if you're combining several menu-driven scripts.
- **The 8-option page cap applies at every level independently.** A submenu with a dozen entries
  auto-paginates exactly like a flat menu would — nesting organizes options into groups, it doesn't raise
  the per-page limit.
- **No breadcrumb, no "back to root" shortcut.** Each `"Back"` option is hand-wired to one specific
  function. Three levels deep, the bottom level's `"Back"` goes to the middle level — getting all the way
  back to the root still takes two presses, since nothing tracks "how did I get here" for you.
- **Bare-global menu functions can collide.** `DisplayRootMenu`/`DisplayPlayerMenu`-style names are real,
  reachable `_G` globals for the rest of the session — fine for a single dedicated menu script, worth a
  more specific prefix if you're combining several menu-driven tools in one file the way
  `MasterCheatMenu.lua` does.

## See also

- [MrxMultipageMenu](../resident/mrxmultipagemenu) — the module reference this whole page builds on:
  `AddOption`'s exact parameter order, the `_knMaxOptionsPerPage = 8` pagination cap, and why a `nil`
  callback is only safe on the cancel-bound option.
- [All-In-One Cheat Menu](../cheat-menu) — the full, real, confirmed-working script this page's pattern is
  extracted from, four submenus deep.
- [Your First Menu](../first-menu) — the single-level version of the `_G`-guarded state pattern this page
  extends to multiple menu functions.
- [Building ForgeMenu — a Reusable Nested-Menu Library](forge-menu) — the easier alternative: a library
  that reuses the `forge.gfx` Scaleform movie instead of the native dialog box, turning everything on this
  page (the manual `Reset`/`AddOption`/`Display` per level, the bare-global gotcha, hand-wiring "Back")
  into declaring a plain tree of categories and entries. Worth reading this page first anyway — the
  reasoning here (why nesting isn't built in, how state threads across levels) still applies, ForgeMenu
  just handles the bookkeeping for you.
- **[UI Kit: UI.Menu](../uilib/menu)** — the same declarative `:entry`/`:category` API as ForgeMenu, plus
  eight sibling widgets (toasts, modal dialogs, a two-pane board) sharing one focus/heartbeat engine, so a
  menu action can pop a confirm dialog or a typed prompt without leaving the menu's own input handling.
