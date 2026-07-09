---
title: Stdlib Additions
parent: lua-bridge API
nav_order: 2
---

# Stdlib Additions

## Overview

Like [Loader](loader), this page documents globals **lua-bridge itself adds** — not part of the game,
not enumerable via `pairs()` on any engine namespace, and documented directly from the implementation by
the person who wrote it. Where `Loader` adds things the engine never had at all (keyboard input, a clean
log), this page covers a different kind of gap: standard Lua 5.1 base/`math` library functions that exist
in a normal Lua build but were stripped out of this game's statically-linked runtime. As of **lua-bridge
v0.2.0**, the most commonly-needed ones are patched back in, so AI-assisted or copy-pasted script authors
can reach for `math.sqrt`, `assert(x, msg)`, `math.random`, etc. and have them just work, instead of
hitting a silent `attempt to call a nil value` the first time a script tries to use one.

**Version floor: v0.2.0** for everything on this page except `math.sin`/`math.cos`, which shipped one
release earlier in **v0.1.6**. If you're relying on anything else here, confirm your lua-bridge build is
at least v0.2.0 — see the [lua-bridge API](./) landing page.

## What's added

A stdlib-completeness probe run against the live game identified 19 missing `math` functions and one
missing base function. All are now registered via the same custom-ABI `luaL_register` path used
throughout lua-bridge, additive to the engine's own pre-existing `math.floor`/`math.abs`/`math.max`/
`math.min`/etc. — nothing here replaces or shadows a function the engine already had.

| Function | Notes |
|---|---|
| `math.sin`, `math.cos` | Shipped in **v0.1.6**, one release before the rest of this page. If you've seen a Taylor-series `CustomSin`/`CustomCos` fallback anywhere on this wiki (the [Freecam deep dive](../deep-dives/freecam), [DestroyerTool.lua](../sample-scripts-onkey), [MasterCheatMenu.lua](../cheat-menu), etc.), that workaround predates this — it's no longer necessary on v0.1.6+, kept in older snippets only because they haven't been revisited since. |
| `math.tan` | New in v0.2.0. |
| `math.asin`, `math.acos`, `math.atan`, `math.atan2` | Inverse trig. |
| `math.sinh`, `math.cosh`, `math.tanh` | Hyperbolic. |
| `math.sqrt`, `math.log`, `math.log10` | The three AI-generated scripts reach for constantly. |
| `math.fmod`, `math.ldexp`, `math.modf`, `math.frexp` | Low-level number-manipulation set. |
| `math.random(...)`, `math.randomseed(x)` | Matches stock Lua 5.1 semantics: `random()` returns a float in `[0,1)`, `random(n)` an integer in `[1,n]`, `random(m,n)` an integer in `[m,n]`. **This is a different function from the engine's own `math.randf()`** (used throughout the decompiled game source, e.g. `resident/mrxartilleryattack.lua`) — `randf`/`random` are two independent RNGs living side by side; neither replaces the other. |
| `math.pi`, `math.huge` | Constants, injected via a Lua polyfill chunk since `luaL_register` only takes functions, not values. |
| `assert(v, msg)` | Polyfilled in Lua on top of the engine's existing `error`. Idempotent (`if not _G.assert then ...`) and re-applied on every pump batch, so a `_G` wipe across a level transition can't strand it. |

All of the above are backed by the C stdlib's single-precision routines, with the same `SafeProbe` +
type-tag safety wrapping used throughout the rest of lua-bridge.

**As of v0.3.0**, every function on this page got the same fast-path treatment as
[`Loader`'s input functions](loader#notes-for-modders): the per-call defensive validation was measured as
unnecessary overhead on this call path and removed, dropping each call to roughly sub-microsecond cost.
Calling `math.sin`/`math.sqrt`/etc. in a per-frame loop is measured-safe on v0.3.0+, the same way the
`Loader` input functions are.

## v0.2.1 fixes (still worth knowing about)

Two small polyfill nits, both caught in the v0.2.0 code review and fixed one release later:

- **`assert`'s error location was wrong.** The polyfill's `error(msg or 'assertion failed!')` used the
  default error level (`1`), which pointed the message at the polyfill chunk itself
  (`[string "if math then..."]:1: bad msg`) instead of at whatever line actually called `assert(...)`.
  Now uses `error(..., 2)` to skip the `assert` function's own stack frame, matching stock Lua semantics
  — **critical if you're relying on `assert` failure messages to debug a script**, since before this fix
  they pointed at the wrong file entirely.
- **The polyfill's own success log was lying.** Earlier builds logged `[*] polyfill applied ...`
  unconditionally, even if the underlying `LuaDoString` call actually returned a `[compile]` or `[bridge]`
  error. Fixed to check the result buffer for those prefixes and log `[!] polyfill FAILED to apply: ...`
  instead when that happens — so a broken polyfill can't hide behind a misleading success line in the log.

## Notes for modders

- **Don't assume any of this is present without checking your lua-bridge version.** Everything here is
  additive and silent when missing — a script calling `math.sqrt` on a pre-v0.2.0 build fails exactly the
  same way it always did (`attempt to call a nil value`), with nothing about the failure pointing at "your
  lua-bridge is out of date" as the cause.
- **`math.randf()` (engine-native) and `math.random()` (lua-bridge polyfill, v0.2.0+) coexist** — pick
  whichever matches the convention of the code you're extending. New scripts with no existing convention
  to match can reach for the stock-Lua-semantics `math.random`/`math.randomseed` pair now, rather than
  needing to reverse-engineer `randf`'s exact range/behavior from call sites the way earlier scripts on
  this wiki had to.
- If you maintain an older script that carries its own `CustomSin`/`CustomCos`/Taylor-series workaround
  (see the cross-links in the table above), it's safe to delete and replace with real `math.sin`/`math.cos`
  once you've confirmed lua-bridge v0.1.6+ — nothing about keeping the workaround is harmful, it's just
  unnecessary now.
