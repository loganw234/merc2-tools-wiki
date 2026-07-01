---
title: Your First Mod
nav_order: 3
layout: verified_page
verified: false
---

# Your First Mod

This walks you from "lua-bridge is installed" to a working hotkey mod, in three steps. If you haven't
installed lua-bridge yet, do that first — see [Getting Started](getting-started).

## Step 1: Say hello (via the console, not raw sockets)

You *can* talk to the REPL with a raw TCP client, and [Getting Started](getting-started) documents that
wire protocol for people building their own tooling. But for actually writing mods, use
**`lua_console.py`** instead — it's a small stdlib-only Python GUI built specifically for this, and it's
a much nicer way to work than a bare socket:

- Tabbed editor with Lua syntax highlighting and line numbers
- Execute the current tab with the toolbar button, **Ctrl+Enter**, or **F5**
- A status dot in the corner that's green when the bridge is reachable, red when it isn't
- Save/open `.lua` files, a recent-files list — it's a lightweight IDE, not just a text box

Run it with `py tools/lua_console.py`. It opens with a starter script already in the editor:

```lua
-- Merc2 Lua console
-- Ctrl+Enter / F5 to execute. Ctrl+T new tab. Ctrl+S save.
return "Hello from Mercenaries 2 (cash = " .. Player.GetCash() .. ")"
```

With the game running and the bridge loaded (status dot green), press **F5**. The output panel below
should show your returned string, cash value included. If you see a red `[bridge] ...` message instead,
check the troubleshooting list at the bottom of [Getting Started](getting-started) — most commonly it
means the bridge hasn't captured a live Lua state yet.

This console is where you'll iterate on almost everything — write a chunk, run it, see the result,
adjust. Once something works here, *then* decide whether it belongs in a loader script (below).

## Step 2: Make it automatic with OnLoad

A one-off chunk in the console is great for testing, but it only runs once, by hand. For a mod that
should run every time you play, use the script loader.

**Use `scripts/OnLoad/` for almost everything.** Most of the game's actual state — the player, world
objects, the mission/task system — isn't meaningfully available until a level has finished loading. The
engine itself gates a lot of its own startup logic behind a specific milestone (internally logged as
`GlobalExit - Complete`), and `OnLoad` scripts are timed to run right after that point, once control has
returned to the player. If you're not sure whether your mod belongs in `OnBoot` or `OnLoad`, it almost
certainly belongs in `OnLoad`.

Create `scripts/OnLoad/hello_load.lua`:

```lua
Debug.Printf("[hello_load] level ready, cash = " .. Player.GetCash())
```

Load into a level. You should see the message in the game's log. Because this runs on *every* level
load, it's the right place for anything that needs to happen "at the start of a mission" — HUD tweaks,
spawning something, kicking off a per-level timer, etc.

**When would you use `OnBoot` instead?** `OnBoot` runs earlier — as soon as the bridge captures a Lua
state at all, before any level has loaded. The main use case is patching something in the game's
front-end/menu system itself (the main menu, attract mode, the shell UI), since that code runs and can
already be interacted with before you've ever loaded into a level. If your mod only cares about
gameplay, you want `OnLoad`; if it needs to touch the main menu, `OnBoot` is what actually fires early
enough to matter.

## Step 3: Trigger it on demand with OnKey

This is the one you'll probably use the most. `OnLoad` runs automatically; `OnKey` scripts run *only*
when you press a bound hotkey — perfect for debug toggles, "give me X" cheats, or anything you want to
fire on demand instead of every single load.

Create `scripts/OnKey/give_cash.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines -- this is how the script declares its own default key

Player.SetCash(Player.GetCash() + 10000)
Debug.Printf("[give_cash] +10000 cash")
```

That `local KEYVAL = "insert"` line is doing real work: the loader reads the first 10 lines of every
`OnKey` script looking for it, and uses it as that script's default hotkey binding — you don't have to
touch any config file for the common case. Load into a level and press **Insert**; you should see cash
increase and the debug message appear.

A few things worth knowing about how `OnKey` actually behaves, since it's easy to assume it works like a
normal event handler and get confused when it doesn't:

- **It's edge-triggered, not held.** The script fires once per press, not repeatedly while the key is
  down (there's `was_down` tracking under the hood specifically to prevent that).
- **The script is re-read from disk on every press.** This means you can edit `give_cash.lua`, save it,
  and press Insert again in-game to test the new version — no restart, no reload. This is the fastest
  iteration loop available for anything gameplay-facing, faster than editing an `OnLoad` script (which
  needs a fresh level load to re-run).
- **Multiple scripts can share a key.** If two `OnKey` scripts both declare (or are configured with) the
  same hotkey, both run on that press.
- **If `KEYVAL` isn't picked up**, or you'd rather not hardcode it in the script, set it explicitly in
  `lua_loader.ini` instead:
  ```ini
  [OnKey]
  give_cash.lua = insert
  ```
  A key name here always reflects what's actually bound — check this file if a hotkey doesn't seem to
  be firing and the in-script `KEYVAL` isn't obviously wrong.

## Where to go next

You now have all three ways of running code: interactive (console), automatic (`OnLoad`/`OnBoot`), and
on-demand (`OnKey`). From here:

- [Recipes](recipes) has more copy-pasteable snippets once you know where they'd go.
- [Resident Modules](resident/) is the reference for what else you can call — start there once "give
  cash" isn't enough anymore.
