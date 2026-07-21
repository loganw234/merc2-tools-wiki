---
title: "3. Reading Before Writing"
parent: Tutorials
nav_order: 3
---

# Tutorial 3: Reading Before Writing

> Built from `Player.GetCash()`/`Player.GetLocalCharacter()`/`Object.GetPosition`, calls already used and
> confirmed elsewhere on this wiki (see [Your First Menu](../first-menu#whats-a-uguid-and-how-do-you-get-your-own))
> — combined here with Tutorials 1 and 2's `Loader.Printf`/`ShowMessage` as the vehicle for showing what
> comes back.

Every tutorial so far has told the game to *do* something — print a line, show a popup. This one asks the
game a **question** and shows you the answer. Reading state and changing state are different halves of
almost everything you'll ever script: read first, decide, *then* act.

## The code

Create `scripts/OnKey/reading_state.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines

local nCash = Player.GetCash()
Loader.Printf("[reading_state] current cash: " .. nCash)
```

Load into a level, press **Insert**, and check `lua_loader_printf.log` (from [Tutorial 1](hello-log)) for
a line like:

```
[reading_state] current cash: 15000
```

Whatever number shows up is your actual, real, current in-game cash — not a made-up example value.

## Reading something with more than one part

Cash is a single number. Your position in the world is three numbers at once — `x`, `y`, and `z`. Extend
the same script:

```lua
local KEYVAL = "insert"

local nCash = Player.GetCash()
Loader.Printf("[reading_state] current cash: " .. nCash)

local uChar = Player.GetLocalCharacter()
local x, y, z = Object.GetPosition(uChar)
Loader.Printf("[reading_state] position: " .. x .. ", " .. y .. ", " .. z)
```

Press **Insert** again and check the log:

> **[Image placeholder — `../img/readingstatelog.png`]** Screenshot of `lua_loader_printf.log` showing
> both the "current cash: ..." line and the "position: ..., ..., ..." line together, from the same
> keypress.

## What's actually happening

`Player.GetCash()` takes no arguments and just hands back a number — the simplest possible read.
`Player.GetLocalCharacter()` is a little different: it hands back a **`uGuid`** (see the
[Glossary](../glossary#uguid) if you want the full definition) — a runtime handle that means "your
character, specifically" — which you then pass to `Object.GetPosition(uChar)` to ask a *second* question
about that *specific* thing. This two-step "get a handle, then ask the handle something" pattern shows up
constantly: almost nothing meaningful can be asked about "a vehicle" or "a character" in the abstract, only
about one specific `uGuid` at a time.

`Object.GetPosition` hands back **three** values at once — `x, y, z` — not a table, not one value. Lua
functions can return more than one thing; whoever calls them decides how many of those returned values to
actually keep by how many names they put on the left of the `=`.

## Try it yourself

- Add `Player.GetFuel()` (no arguments, same shape as `GetCash`) and log it the same way.
- Walk somewhere else in the game world, then press Insert again — confirm the position numbers actually
  changed.
- Try logging *only* `x` and `z`, throwing away `y`: `local x, _, z = Object.GetPosition(uChar)`. The `_`
  is just a variable name — Lua has no special "discard" syntax, but naming something you don't care about
  `_` is a common convention for "I need the third value but not this one."

## Where this comes from

- [Your First Menu: What's a `uGuid`](../first-menu#whats-a-uguid-and-how-do-you-get-your-own) —
  `Player.GetLocalCharacter()` introduced and explained.
- [Glossary: `uGuid`](../glossary#uguid)

**Next:** [Tutorial 4: Two Clocks, Side by Side](two-clocks) — so far every script has been an `OnKey`
script. Time to meet its counterpart.
