---
title: Your First Menu
parent: Recipes
nav_order: 3
---

# Your First Menu

[Your First Mod](first-mod) got you to a single script that does one thing on one keypress. This page is
the next step up: a script that opens a **menu** — several options, each one calling its own function —
and **remembers state** between presses, so a toggle you turned on stays on the next time you open the
menu. The example is deliberately small (two toggles, nothing else) so the pattern stays visible; the
[All-In-One Cheat Menu](cheat-menu) is what this same pattern looks like once it's grown into something
real.

## What's a `uGuid`, and how do you get your own?

Almost every call you'll make needs to know *which* object to act on — a specific vehicle, a specific
character, your own character. The engine identifies each one with a **`uGuid`** — a runtime handle, not
a name or a save-file ID, just an opaque value that means "this specific thing, right now." (Full
definition in the [Glossary](glossary#uguid) if you want it.) You'll pass a `uGuid` as the first argument
to most `Object.*` calls, and you get your own character's `uGuid` with:

```lua
local uChar = Player.GetLocalCharacter()
```

That's it — no arguments, just hand back whatever `uChar` gives you to the next call that needs to know
who "you" are. (There are `GetPrimaryCharacter`/`GetSecondaryCharacter` variants too, for telling co-op
players apart — see [Engine Namespaces: Player](namespaces/player) if you get that far. For now, one
player, one character, `GetLocalCharacter` is all you need.)

## Three pieces, combined

A menu that remembers its own state is really three separate, simple ideas stacked on top of each other.
Worth seeing each one on its own before combining them:

**1. State that survives between presses.** An `OnKey` script re-runs its *entire file* from scratch every
time you press the key — any plain `local` variable is gone the instant the script finishes. `_G` (the one
truly global table, shared across every script) is what actually persists across separate runs:

```lua
_G.MyMenuState = _G.MyMenuState or {
  bInfiniteAmmo = false,
  bInvincible = false,
}
local State = _G.MyMenuState
```

The `or` matters: **`_G.MyMenuState or {...}`** means "reuse the table that's already there from last
time, if one exists — otherwise start fresh." Without it, every keypress would silently reset both toggles
back to `false`, no matter what you'd actually turned on.

**2. Calling the game safely.** Wrap the actual game call in `pcall` so a bad `uGuid` (a character who's
since respawned, a despawned vehicle) can't kill the rest of your script — see
[Snippets: Protect a risky call with pcall](snippets#protect-a-risky-call-with-pcall) for the full
mechanics if you haven't read it yet. The short version: `pcall(f, ...)` calls `f` for you and hands back
`true` (plus whatever `f` returned) if it worked, or `false` (plus an error message) if it didn't — either
way, your script keeps running.

**3. A menu, built from `MrxMultiPageMenu`.** Three calls: `Reset()` clears any previous menu,
`AddOption(sLabel, fCallback, tArgs)` adds one row (label text, the function to call if it's picked, and
that function's arguments as a table), and `Display(sTitle)` actually shows it:

```lua
import("MrxMultiPageMenu")

MrxMultiPageMenu.Reset()
MrxMultiPageMenu.AddOption("Say hello", function() Loader.Printf("hi!") end)
MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)
MrxMultiPageMenu.Display("Test Menu:")
```

That last option is the standard "close/cancel" row used throughout this wiki's sample scripts — the
trailing `true, true` binds it to the menu's own cancel button, and a `nil` callback there is a
special-cased no-op (not something you'd want to do for a *real* option — see
[`MrxMultipageMenu`'s notes for modders](resident/mrxmultipagemenu#notes-for-modders) on exactly this if
you're curious why).

## Putting it together

Two toggles — Infinite Ammo and Invincibility, the same simple pair used to introduce this same pattern
on the [All-In-One Cheat Menu](cheat-menu) page — each its own function, each remembering its own on/off
state, each menu label updating to show which state you're currently in:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

import("MrxMultiPageMenu")

_G.MyMenuState = _G.MyMenuState or {
  bInfiniteAmmo = false,
  bInvincible = false,
}
local State = _G.MyMenuState

local function ToggleInfiniteAmmo()
  State.bInfiniteAmmo = not State.bInfiniteAmmo
  pcall(Object.SetInfiniteAmmo, Player.GetLocalCharacter(), State.bInfiniteAmmo)
end

local function ToggleInvincible()
  State.bInvincible = not State.bInvincible
  pcall(Object.SetInvincible, Player.GetLocalCharacter(), State.bInvincible, "MyFirstMenu")
end

MrxMultiPageMenu.Reset()
MrxMultiPageMenu.AddOption("Infinite Ammo: " .. (State.bInfiniteAmmo and "ON" or "OFF"), ToggleInfiniteAmmo)
MrxMultiPageMenu.AddOption("Invincibility: " .. (State.bInvincible and "ON" or "OFF"), ToggleInvincible)
MrxMultiPageMenu.AddOption("Close this menu", nil, nil, true, true)
MrxMultiPageMenu.Display("My First Menu:")
```

Drop that in as `scripts/OnKey/first_menu.lua` and press Insert. Picking "Infinite Ammo: OFF" flips the
flag, calls `Object.SetInfiniteAmmo`, and — because the whole script re-runs from the top on every
press — immediately rebuilds the menu with the label now reading "Infinite Ammo: ON". Press Insert again
without picking anything and the state is still exactly where you left it, because `_G.MyMenuState`
never got thrown away.

(Wondering why the label uses `condition and "ON" or "OFF"` instead of an if/else? That's Lua's
ternary-operator stand-in — see the [lua101 aside on the cheat-menu page](cheat-menu#player) for the
mechanics and its one real gotcha.)

## Where to go next

- [All-In-One Cheat Menu](cheat-menu) — this exact pattern (state + `pcall` + `MrxMultiPageMenu`), grown
  into submenus, a dozen more toggles, and a few genuinely silly extras.
- [Sample Scripts: OnKey](sample-scripts-onkey) — more complete, ready-to-drop-in scripts using the same
  building blocks, including ones with actual persistent per-object state (not just two booleans).
- [Snippets](snippets) — smaller, single-purpose building blocks if you want more pieces before combining
  your own.
