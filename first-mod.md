---
title: Your First Mod
nav_order: 3
layout: verified_page
verified: true
verified_note: native path -- all 3 steps live-tested (console hello-world, OnLoad, OnKey + MrxPmc.AddCashQty
  fix). Ess path uses calls already confirmed elsewhere in Ess's own test history (see the Ess repo's
  CAPABILITIES.md / CHANGELOG.md) -- not independently re-tested on this exact page.
---

# Your First Mod

This walks you from "lua-bridge is installed" to a working hotkey mod, in three steps. If you haven't
installed lua-bridge yet, do that first — see [Getting Started](getting-started).

> **This page predates [Ess](ess/)** — the Lua framework most of this ecosystem now targets — and used to
> be pure native-engine code end to end. It now shows both: **Using Ess** (recommended — it's what
> [mercs2.tools' own Start Here walkthrough](https://mercs2.tools/#s-start) leads into once lua-bridge is
> installed) for anyone who installed it, and the original **Native** version for anyone who'd rather not
> take on the dependency. Both produce the same result on screen; pick whichever fits your mod.

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

This step is the same whether or not Ess is loaded yet — it's just proving the console itself works.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

Three things in that four-line starter script, if none of this is familiar yet:

- **Lines starting with `--` are comments.** Lua ignores everything from `--` to the end of that line —
  they're notes for a human reader, not instructions. The first two lines of the starter script are
  entirely comments; the actual code is just the one `return` line.
- **`return` sends a value back to whoever ran the chunk.** Here, that's the console — whatever follows
  `return` is what shows up in the output panel. A script doesn't have to `return` anything at all; plenty
  of scripts later in this guide just *do* something (add cash, print a message) with nothing to return.
- **`..` joins strings together.** `"Hello, " .. "world"` produces `"Hello, world"`. `Player.GetCash()`
  returns a number, not a string, so it gets silently converted to text for the join — Lua does that
  automatically for `..`, but not for most other operations.

</details>

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

**Using Ess** — create `scripts/OnLoad/hello_load.lua` (a low `lua_loader.ini` number, after `1_Ess.lua`):

```lua
if not _G.Ess then Loader.Printf("hello_load: load Ess first (1_Ess.lua in scripts/OnLoad, before this file)") return end
Ess.Log("[hello_load] level ready, cash = " .. Player.GetCash())
```

`Ess.Log` is a thin, always-safe wrapper over `Loader.Printf` (it no-ops instead of erroring if `Loader`
is somehow missing) — that's the only difference from the native version below; the log line itself reads
the same either way (Ess prefixes its own `[Ess]` tag in front of whatever you pass it, which is normal —
every Ess recipe's log line looks like `[Ess] [recipe] ...` the same way).

**Native** — create `scripts/OnLoad/hello_load.lua`:

```lua
Loader.Printf("[hello_load] level ready, cash = " .. Player.GetCash())
```

Load into a level. You should see the message in the game's log either way. Because this runs on *every*
level load, it's the right place for anything that needs to happen "at the start of a mission" — HUD
tweaks, spawning something, kicking off a per-level timer, etc.

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

**Using Ess (recommended)** — create `scripts/OnKey/give_cash.lua`:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines -- this is how the script declares its own default key

if not _G.Ess then Loader.Printf("give_cash: load Ess first (1_Ess.lua in scripts/OnLoad)") return end
Ess.Player.giveCash(10000)
Ess.Log("[give_cash] +10000 cash")
```

One call. `Ess.Player.giveCash` already routes through the same HUD-updating native path the manual
version below has to spell out — you don't need to know `import()`, resident modules, or which of three
possible cash-setting calls is the *correct* one exist at all. This exact call is in Ess's own confirmed
test history (see [Ess: Core Primitives](ess/core) / the framework's `CAPABILITIES.md`).

**Native (no Ess dependency)** — same file:

```lua
local KEYVAL = "insert"  -- must be in the first 10 lines -- this is how the script declares its own default key

import("MrxPmc")         -- MrxPmc is a resident module, not an engine namespace -- needs its own import
MrxPmc.AddCashQty(10000)
Loader.Printf("[give_cash] +10000 cash")
```

That `local KEYVAL = "insert"` line is doing real work: the loader reads the first 10 lines of every
`OnKey` script looking for it, and uses it as that script's default hotkey binding — you don't have to
touch any config file for the common case (true for both versions above).

Two things worth knowing here, both confirmed by live testing: `MrxPmc.AddCashQty` is used (instead of
the lower-level `Player.SetCash`/`Player.AddCash`) specifically because it also refreshes the HUD —
calling `Player.SetCash` directly *does* change your actual cash, but the on-screen number won't update
to show it. And `MrxPmc` needs that `import("MrxPmc")` line because it's a `resident/` module, not a
built-in engine namespace like `Player` — see the [Glossary](glossary#importname) if you want the full
explanation of why. **This is exactly the kind of trap Ess exists to paper over** — the Ess version above
never has to know any of this.

Load into a level and press **Insert**; you should see cash increase on-screen and the debug message
appear, either version.

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

**If you're using Ess:**

- [Ess Framework](ess/) — this wiki's own namespace-by-namespace reference, and the install/tiering
  walkthrough if you skipped straight here.
- [Ess: samples/recipes](https://github.com/loganw234/mercs2-lua-essentials/tree/master/samples/recipes) —
  a couple dozen more "how do I *X*?" scripts in the exact same shape as this page's steps, one task each.

**Either way:**

- [Your First Menu](first-menu) is the very next step — a menu with a couple of toggle options that
  remembers its own state between presses, the smallest complete example of state + `pcall` + a real
  menu combined.
- [Recipes](recipes) has more copy-pasteable snippets once you know where they'd go.
- [Deep Dive: Overriding a Function](deep-dives/function-override) goes one level deeper — replacing a
  piece of the game's own logic instead of just reading/writing a value, worked through end to end.
- [Resident Modules](resident/) is the reference for what else you can call — start there once "give
  cash" isn't enough anymore.
- [lua-bridge API](lua-bridge-api/) documents globals lua-bridge itself adds on top of the game — not
  part of Mercenaries 2, only present if your lua-bridge build includes them, but worth knowing about
  since they cover things (like real keyboard input) the game's own Lua surface never exposes.
