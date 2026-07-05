---
title: Getting Started
nav_order: 2
---

# Getting Started Modding Mercenaries 2

This wiki documents the Lua scripting surface of **Mercenaries 2: World in Flames (PC)** for modders. If
you're new here, start on this page — it covers the *only* supported way to get your own Lua code
running in the live game right now: **lua-bridge**.

## Rapid overview

Already comfortable installing ASI mods and don't need the walkthrough? Here's the whole thing:

1. **Get lua-bridge.** No stable release exists yet — `lua-bridge-DEV` in
   [github.com/loganw234/Merc2-Mods-Exp](https://github.com/loganw234/Merc2-Mods-Exp) is the current
   active build. Either install it manually (drop the built `.asi`/`.ini` into `scripts/`, see [Install](#install)
   below), or install through the community
   [mercs2-modkit](https://github.com/Mercenaries-Fan-Build/mercs2-modkit) mod manager, which can pull it
   for you — see that repo for its own setup instructions.
2. **Launch the game via `pmc_bb.dll`** (the Fan Build ASI loader). lua-bridge doesn't run standalone.
3. **Run code one of two ways:**
   - Interactively: `py tools/lua_console.py`, a small GUI REPL client — write Lua, hit F5, see the
     result. Fastest way to poke at game state.
   - Automatically: drop a `.lua` file into `scripts/OnLoad/` (runs once per level load — use this for
     almost everything) or `scripts/OnKey/` (runs on a hotkey press — declare the key with
     `local KEYVAL = "insert"` in the script's first 10 lines).
4. That's it — no compilation step, no ASI-mod boilerplate. If something's not working, jump to
   [Troubleshooting](#troubleshooting-checklist) at the bottom of this page.

New to this entirely, or want the reasoning behind each step? Keep reading below.

## Why lua-bridge

Mercenaries 2 ships with a statically-linked Lua 5.1.2 runtime driving nearly everything — world
objects, missions, GUI, AI. There's no official modding API. **lua-bridge** hooks into that runtime at
the binary level and exposes it to you two ways:

1. A **live REPL** over a localhost TCP socket — send it a chunk of Lua, get the result back immediately.
2. A **script loader** — drop `.lua` files into watched folders and they run automatically at specific
   points in the game's lifecycle (boot, level load, or a hotkey press).

At this early stage of the modding scene, lua-bridge is the only injection tool available, so this page
is also the closest thing to an "API contract" for how mods are structured — until something else comes
along, build against this.

## Install

1. Build or download `lua_bridge.asi` and its companion `lua_bridge.ini`.
2. Drop both into your game's `scripts/` folder (next to `Mercenaries2.exe`).
3. Launch the game through `pmc_bb.dll` (the Mercenaries Fan Build ASI loader) — lua-bridge is an ASI
   plugin, it doesn't run standalone.
4. On first successful launch, lua-bridge auto-creates `scripts/OnBoot/`, `scripts/OnLoad/`,
   `scripts/OnKey/`, and a `lua_loader.ini` config file next to the exe.

Verified working against **pmc_bb.dll v0.2.0**. If a newer loader breaks compatibility, that'll get
called out here.

## Two ways to run code

### 1. The REPL (fastest for iterating)

lua-bridge listens on `127.0.0.1:27050` by default (configurable in `lua_bridge.ini`). It only accepts
loopback connections — this is a hard security restriction, not just a default, so don't expect to
reach it from another machine.

**Protocol:** open a TCP connection, write your Lua chunk, then write the literal line `<<<RUN>>>` to
mark the end of the chunk. The bridge queues it, runs it on the next engine frame it gets a pump
opportunity on, and writes the result back followed by a literal `<<<END>>>` line.

You don't need to hand-roll this — use `tools/lua_console.py` (interactive) or `tools/lua_repl.py`
(scriptable) from the parent project. But it's worth knowing the wire format if you're writing your own
tooling (e.g. driving the game from a build script or a bot).

**Reading the response:**

| Prefix | Meaning |
|---|---|
| `[ok]` | Your chunk ran and returned normally (`pcall` succeeded). Return values follow, **tab-separated**. |
| `[runtime]` | Your chunk ran but errored at runtime. Return values (usually just the error message) follow, **space-separated**. |
| `[compile]` | Your chunk failed to compile — syntax error. The message follows. |
| `[bridge] ...` | Something went wrong in the bridge itself before your code ran at all (see table below). |

Return values are formatted per-type: `nil`, `true`/`false`, numbers via `%g`, strings in `"quotes"`,
tables as `<table>`, functions as `<function>`. Anything else shows as `<tt=N val=0xADDRESS>` — you're
looking at a raw engine type the formatter doesn't special-case, use `type()` /
`Loader.Printf(tostring(...))` from within your chunk if you need more detail on it.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

That list (`nil`, `true`/`false`, numbers, strings, tables, functions) is the *entire* set of value types
in Lua — there's nothing else. A few that trip people up coming from other languages:

- **`nil` isn't the same as `false`.** `nil` means "nothing here" (an unset variable, a missing table
  field); `false` is a real boolean value. Both make an `if` statement take the "else" branch, which is
  why they're easy to conflate, but `type(nil)` and `type(false)` are different strings.
- **Numbers are just "numbers."** No separate `int` vs `float` types to worry about — see the
  float-vs-double gotcha below for how *this specific game* stores them internally, but at the Lua
  language level, `5` and `5.0` are the same kind of thing.
- **A table can hold anything, including functions.** That's *why* `MrxPmc.AddCashQty(...)` works the way
  it does — `MrxPmc` is a table, `AddCashQty` is a function stored as one of its fields, and `.` reads
  that field before calling it.

If a chunk you write returns a table and you want to see what's actually in it (not just the useless
`<table>` the REPL shows), loop over it yourself: `for k, v in pairs(t) do Loader.Printf(tostring(k) .. " = " .. tostring(v)) end`.

</details>

**One gotcha worth knowing:** this build of the engine's Lua uses **`float`, not `double`**, for
`lua_Number`. Precision-sensitive math (large integers, tight epsilon comparisons) can behave
differently than you'd expect from a stock Lua 5.1 interpreter. If a number "should" be exact but isn't,
this is usually why.

**`[bridge]` errors** mean the bridge couldn't even get your code to Lua:

| Message | What it means |
|---|---|
| `no L` | The bridge hasn't captured a live Lua state yet (too early in boot). Wait and retry. |
| `L failed validation` | The bridge has a Lua state pointer but it doesn't look like a valid one right now — usually a transient timing issue, retry. |
| `empty chunk` | You sent nothing before `<<<RUN>>>`. |
| `chunk too large` | Your chunk is at or past the 1MB buffer limit. Split it up. |
| `executor fn pointers not resolved` | The bridge couldn't resolve the engine's internal Lua exec functions for this game binary — a build-compatibility problem, not something you can fix from Lua. |

### 2. The script loader (for anything that should run automatically)

Drop `.lua` files into one of three folders under `scripts/`:

- **`scripts/OnBoot/`** — runs once, as early as possible, the moment the bridge captures a live Lua
  state. Good for one-time global overrides, injecting your own helper functions into `_G`, etc.
- **`scripts/OnLoad/`** — runs once **per level load**, at the point the game reaches the
  `GlobalExit - Complete` milestone (control has returned to the player). Good for HUD tweaks, spawning
  things, starting per-level logic.
- **`scripts/OnKey/`** — not run automatically; each script is bound to a hotkey and runs (once,
  edge-triggered) every time you press it. Good for debug toggles and manual triggers.

Scripts in `OnBoot`/`OnLoad` run in an order controlled by `lua_loader.ini`, auto-populated (in
increments of 10, alphabetical by default) the first time the loader sees a new script — edit the
numbers in that file to reorder. `scripts/OnKey/*.lua = <keyname>` in the same file binds hotkeys; a
script can also declare its own default by putting `local KEYVAL = "keyname"` somewhere in its
**first 10 lines**, which the loader reads before ever running it.

`OnKey` scripts are re-read from disk on every keypress (via a dedicated background thread polling at
30Hz, so it doesn't stall the game's main thread) — edit-and-repress works without restarting.

As of lua-bridge v0.2.1, rapid double-presses of the same hotkey (within 250ms by default) are
automatically throttled to one run instead of queuing two back-to-back — see
[Loader: OnKey dispatch behavior](lua-bridge-api/loader#onkey-dispatch-behavior) for the full mechanics
and how to disable it.

### `Loader.Printf` — debug output that doesn't get lost

Don't reach for the engine's own `Debug.Printf` to print your own debug messages. It's the game's
original debug-print function, called thousands of times a second from all over the base game's own
scripts — and it's also the exact function lua-bridge itself hooks into as one of its capture points.
Anything you print through it is buried in that noise with no clean way to filter it back out.

Every script instead has access to a global:

```lua
Loader.Printf(message)
```

Same idea as `Debug.Printf`, but it writes only to its own dedicated file — `lua_loader_printf.log`, next
to the game exe — instead of the shared, noisy engine log. Everything in that file is something a script
explicitly asked to log; nothing from the base game leaks in. Use this for anything you actually want to
find again later.

### `Tcp.Send` — fire-and-forget telemetry

Every script (REPL or loader) has access to a global:

```lua
Tcp.Send(host, port, message)
```

Fires a one-way TCP message. **Restricted to `127.0.0.0/8` (localhost) destinations** — this is
intentional, to stop a script from port-scanning your LAN or phoning home over the internet. Useful for
piping game state to a local companion tool (a logger, an overlay, a second bridge instance) without
building that plumbing into the engine hook itself.

## What can I actually call?

Once you can get code running, the next question is *what's there to call*. That's what the rest of
this wiki is for — reference docs for the game's own Lua modules (`resident/`), covering the object
model, lifecycle hooks, and the engine's built-in namespaces (`Object`, `Event`, `Player`, `Marker`,
etc. — always global, no setup needed) as well as the `resident/` modules themselves (`MrxPmc`,
`MrxTransit`, and 226 others — these need an `import("Name")` call before use outside their own file, see
the [Glossary](glossary#importname)). Start with [Resident Modules](resident/) — its landing page
explains the game's module/inheritance pattern before you hit the per-module pages — or jump straight to
a specific module if you already know what you're looking for.

## Troubleshooting checklist

- **Nothing happens when I connect to the REPL** → confirm `lua_bridge.asi` is actually loaded (check
  the pmc_bb.dll loader's own log) and that `lua_bridge.ini`'s `[repl]` section wasn't edited to a
  different port.
- **`[bridge] no L` forever** → the bridge hasn't seen the Lua VM yet. Get further into the game (past
  the main menu) and retry.
- **My `OnLoad` script isn't running** → it only fires once the `GlobalExit - Complete` milestone is
  hit, i.e. after a level has actually finished loading, not on menu load. If you edited
  `lua_loader.ini` by hand, make sure the section header is exactly `[OnLoad]`.
- **My hotkey isn't firing** → check `lua_loader.ini`'s `[OnKey]` section has your exact filename mapped
  to a recognized key name, or that `local KEYVAL = "..."` is within the first 10 lines of the script.
