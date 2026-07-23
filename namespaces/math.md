---
title: Math
parent: Engine Namespaces
nav_order: 20
---

# Math

## Overview

`Math` is an **engine namespace**: implemented natively by the game engine, not by any decompiled `.lua`
module. There is no source file behind it, no `import()` needed — it is always globally available from
any script. It's a small numeric-utility table sitting alongside the general-purpose helpers on `Sys` and
`Junk`: vector cross products, rounding, angle conversion, exponentiation.

**Disambiguation:** this is a different table from `Ess.Math`, the mod-authored [Essentials
framework](../ess/core#essmath)'s own math-helper module (`clamp`, `lerp`, `dist2D`, `angleTo`, and so
on). The two share a name and nothing else — `Ess.Math` is pure Lua written for this wiki's own mod
framework, while the `Math` documented on this page is a native engine binding that exists independently
of `Ess` on every script. Watch which one a piece of code is actually calling; `Math.round` and
`Ess.Math.round` are not the same function.

## Provenance

This page does not come from a live `pairs(Math)` dump the way most pages in this section do — that's a
**different discovery method** from the one behind [`Sys`](sys), [`Camera`](camera), [`Junk`](junk), and
the other pairs()-enumerated namespaces. It comes from a newer research pass: a static dump of all 973
`luaL_Reg` engine bindings compiled into the game executable, diffed against the 370-file decompiled Lua
corpus to find bindings that are registered but never called anywhere in that corpus. That diff left
several `luaL_Reg` binding tables unlabeled — a raw code address with no name attached. The table at
`0x00799BE8` was one of them; it was resolved to the runtime global `Math` by cross-referencing which
corpus call-prefixes (`Math.CrossProduct(...)`, etc.) matched its member functions, then confirmed live
with a `type(Math) == "table"` check over lua-bridge's WebSocket transport against a running game.

That means the function list below is a **first, partial batch** — only the members that happened to turn
up as `Math.*` call-prefixes during that cross-reference — not a complete `pairs()`-style enumeration the
way, e.g., [`Sys`](sys)'s 64 functions are. There is very likely more on this table than the six members
named so far.

**Independent corroboration.** This table's identity isn't resting on the live probe alone. An earlier,
purely static-analysis pass (`lua_engine_bindings_audit_deep_dive.md`, 2026-05-19 — predates the live probe
by two months and used no runtime testing at all) had already found the same `0x00799BE8`–`0x00799C70`
table by locating the literal string `"Math"` in the executable's `.rdata` section (address `0x007DD858`)
and following the dword cross-reference back to the registration row — the tool's own documented
highest-confidence ("CERTAIN") resolution method, since it reads the name Pandemic's own compiler embedded
rather than inferring it from behavior. That pass also counted the table at exactly 17 entries, consistent
with "more members than the six named here."

**This is not lua-bridge's `math.*` polyfill** ([Stdlib Additions](../lua-bridge-api/stdlib)) — a fair
thing to double-check, since that page also patches numeric functions into a global table. Three
independent reasons it isn't: lua-bridge's polyfill only ever touches the pre-existing **lowercase**
`math` table (confirmed directly from its source, `lua_bridge_DEV.c` — every `RegisterMathLib` call passes
the literal libname `"math"`, never `"Math"`); its added function set (`sin`, `cos`, `tan`, `asin`, `acos`,
`atan`, `atan2`, `sinh`, `cosh`, `tanh`, `sqrt`, `log`, `log10`, `fmod`, `ldexp`, `modf`, `frexp`, `random`,
`randomseed`, plus the `pi`/`huge`/`assert` polyfill chunk) shares zero names with `CrossProduct`/`round`/
`deg`/`exp`/`abs`/`PolarToRect`; and the static audit places the Lua 5.1 stdlib's own range (which is where
native lowercase `math.floor`/`math.abs`/etc. actually live) at a completely different address,
`0x007923A8`–`0x00792580`, far from this table's `0x00799BE8`. Lua is case-sensitive — `Math` and `math`
are two unrelated globals here, and lua-bridge, which didn't exist when the original binary was compiled,
has no code path that creates or touches the capitalized one.

## Functions

| Function | Signature (best-known) | Notes |
|---|---|---|
| `CrossProduct` | `cx, cy, cz = Math.CrossProduct(ax, ay, az, bx, by, bz)` | Live-probed directly against a running game over lua-bridge: called with two 3D vectors (`ax,ay,az` and `bx,by,bz`) and returns their 3-component cross product. The only member of this table with a fully live-confirmed argument and return shape. |
| `round` | `n = Math.round(n)` | Live-probed against a running game; takes and returns a number. Rounding behavior (round-half-up vs. round-half-to-even, whether a second decimal-places argument is accepted) was not tested beyond the plain single-argument call. |
| `deg` | `n = Math.deg(nRadians)` | Live-probed against a running game; takes and returns a number. Read as "radians to degrees" from the name and from returning plausible degree-range values in the probe, but the exact conversion was not independently verified against known reference values. |
| `exp` | `n = Math.exp(n)` | Live-probed against a running game; takes and returns a number. Presumed the standard exponential function (eˣ) by name; not independently verified against known values. |
| `abs` | — | Named as an existing member of this table by the corpus call-prefix cross-reference described above, but not itself live-probed for this page. Presumed absolute-value by name; signature unconfirmed. |
| `PolarToRect` | — | Named alongside `abs` by the same cross-reference, not live-probed. Presumed a polar-to-rectangular coordinate conversion by name (plausibly something like `x, y = Math.PolarToRect(nAngle, nRadius)`), but that argument shape is a guess, not a confirmed signature. |

## Notes for modders

- The cross-reference that resolved this table's identity described its known members with the shorthand
  "`abs…PolarToRect`, `CrossProduct`, `round`, `deg`, `exp`" — the `…` between `abs` and `PolarToRect`
  means more members turned up alphabetically between those two without being individually named in that
  pass. Don't treat the six functions above as the complete list; they're only the ones with confirmed
  names so far. A live `pairs(Math)` dump (see [Snippets: Dump every engine namespace at
  once](../snippets#dump-every-engine-namespace-at-once)) would settle full membership the same way it
  already has for the other namespaces in this section.
- Missing or wrong arguments return `nil` silently on this engine — there is no `bad argument #N` error,
  because the engine inlines its own argument checks. That makes a read-only function like `round`/`deg`/
  `exp` safe to probe blind (a bad call just returns `nil` rather than crashing), but it also means arity
  can't be discovered from an error message, only from a live probe with valid arguments. Given how little
  of this table is confirmed, treat everything above as a starting point for further live probing, not a
  finished picture.
