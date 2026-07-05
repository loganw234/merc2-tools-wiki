---
title: lua-bridge API
nav_order: 6
has_children: true
has_toc: false
---

# lua-bridge API

Every other reference section on this wiki — [Resident Modules](../resident/), [Engine Namespaces](../namespaces/) —
documents things that are part of Mercenaries 2 itself: real game code, reachable because lua-bridge gives
a live Lua console into the running engine. This section is different. It documents globals that
**lua-bridge itself adds** to that environment — functions with no `.lua` file behind them and no engine
namespace to enumerate via `pairs()`, because the game never shipped them. They exist purely because
modding needed something the engine's own Lua surface didn't expose.

That distinction matters for one practical reason: everything in [Engine Namespaces](../namespaces/) is
guaranteed present in any copy of the game lua-bridge can attach to, regardless of which lua-bridge build
you're running. Everything here ships in the stock lua-bridge install — but which specific pieces you can
rely on depends on which build you're running, since this section has grown across several releases:

| Added in | What |
|---|---|
| v0.1.6 | `Loader`'s keyboard input API; `math.sin`/`math.cos` |
| v0.2.0 | The rest of `math.*` (trig, hyperbolic, `sqrt`/`log`/`log10`, low-level number manipulation, `random`/`randomseed`, `pi`/`huge`) and `assert(v, msg)` |
| v0.2.1 | Per-script OnKey reentrancy cooldown; missing-file guard for OnKey scripts; fixes to `assert`'s error location and the stdlib polyfill's own success/failure logging |

If you're relying on anything past the keyboard API and basic trig, confirm you're on **v0.2.0 or later**.

## Available namespaces

- **[Loader](loader)** — logging, the game's first real general-purpose keyboard input API (full
  keyboard-state snapshots, a single-key predicate, an edge-triggered keystroke queue, foreground-focus
  detection), and the OnKey dispatch safety behavior added in v0.2.0/v0.2.1 (reentrancy cooldown,
  missing-file guard). The keyboard API was added specifically to unblock the
  [co-op text chat](../deep-dives/coop-chat) idea, whose "Input" problem had no answer anywhere in the
  game's own Lua surface.
- **[Stdlib Additions](stdlib)** — standard Lua 5.1 `math`/base-library functions (full trig, `sqrt`,
  `random`, `assert`, and more) that exist in a normal Lua build but were stripped from this game's
  runtime, patched back in as of v0.2.0.

`Tcp.Send(host, port, msg)` (see the [lua-bridge README](https://github.com/loganw234/Mercenaries2)) is
also a lua-bridge-provided global, registered the same way — not yet written up as its own page here.
