---
title: "Meta: Override"
parent: Essentials (Ess)
nav_order: 13
---

# Meta: Override

## Overview

`Ess.Override` (`90_override.lua`) is a direct productization of
[Deep Dive: Safely Overriding a Function](../deep-dives/function-override) — the two confirmed-safe ways to
change a piece of the game's own logic, packaged as reusable one-liners instead of a pattern you have to
remember and hand-apply every time. It doesn't re-derive the *why*; read the deep dive for the full story
(the wardrobe-unlock case, the three wrong turns, the confirmed screenshot). This page documents the two
functions it packages.

## The confirmed crash, recapped

`SomeModule.SomeFunction = function(...) return fOriginal(...) end` compiles as a Lua **tail call** — the
current stack frame is replaced rather than a new one pushed. This engine's own module system uses
`getfenv(n)` in places (walking `n` stack levels to find a module's environment), and a collapsed frame
throws that level-counting off, surfacing as `:1: no function environment for tail call at level 2` — thrown
from deep inside the **engine's own code**, not the mod that caused it. This is the exact crash
[custom-contract.md](../deep-dives/custom-contract) hit on an already-shipped mission before it was
understood. The confirmed fix, applied consistently everywhere on this wiki: capture the original in a
local, call it as a plain statement, return its result on a separate line — never `return fOriginal(...)`
directly.

## `Ess.Override.wrap(target, name, newFn) -> ok`

The deep dive's fix, packaged as a one-liner. Rather than trust every caller to remember the two-statement
rule by hand, `wrap` makes the crashing shape **structurally impossible to write**: `newFn` never touches the
real original function at all. It's called as `newFn(callOriginal, ...)`, where `callOriginal` is a small
closure `wrap` builds once, and that closure is the *only* thing allowed to invoke the real original — always
via the confirmed-safe two-statement shape:

```lua
local function callOriginal(...)
    local a, b, c, d = orig(...)
    return a, b, c, d
end
```

The outer replacement itself also avoids tail-calling `newFn`, for the same reason — belt and suspenders,
since `newFn` is arbitrary caller code that may eventually reach back into engine environment-sensitive calls
via `callOriginal`, and keeping every frame in the chain a real (non-collapsed) frame removes any doubt about
`getfenv(n)`'s level-counting landing wrong.

```lua
Ess.Override.wrap(target, name, newFn) -> ok
```

- `target` — the module table holding the function (must already be `import()`'d by the caller).
- `name` — the field name to replace.
- `newFn(callOriginal, ...)` — your replacement; call `callOriginal(...)` to invoke the real original.

```lua
Ess.Override.wrap(demo, "greet", function(callOriginal, name)
    local base = callOriginal(name)   -- the real original, invoked the crash-proof way
    return base .. "!"                -- ...then augment it
end)
```

Guards:

- **Refuses a non-table `target`** or a `target[name]` that isn't a function — logs and returns `false`.
- **Refuses to double-wrap.** `target._essWrapped[name]` is set the first time `wrap` succeeds on that key; a
  second `wrap` call on an already-wrapped `target`/`name` logs and returns `false` rather than silently
  stacking an invisible extra layer.

This is what [`Ess.Net.hijackCallback`](net) is built on, generalizing `wrap` into a mark-check-claim-or-
passthrough callback hijack for the co-op networking layer.

## `Ess.Override.mergeIntoLiveTable(t, key, data) -> ok`

```lua
Ess.Override.mergeIntoLiveTable(t, key, data) -> ok
```

Appends each entry in `data` (a list) onto the existing table at `t[key]`, creating it fresh only if it
doesn't already exist — **never** replacing `t[key]` with a new table object if one is already there.

This is the deep dive's *other* confirmed pattern — the wardrobe-unlock case's actual mechanism: prefer
merging new data into a table the game's own logic already reads from over replacing the function that reads
it. The wardrobe menu's costume-select code re-reads `WifPmcInterior._tOutfits[sHero]` **fresh by index every
single time it runs**, never a cached copy — so appending new rows into that same live table object makes
them appear in the existing, unmodified menu-building/costume-change code with zero risk of losing whatever
responsibilities (co-op branching, tutorial-dialog special cases, pagination, network sync) a full function
replacement would silently drop. "Tables are references, not copies" is what makes this work: every reader
holding onto `t[key]` sees the same object, appended-to in place, immediately — no new lookup or refresh
needed on the reader's side.

```lua
local menu = { items = { "stock_A", "stock_B" } }
local liveRef = menu.items
Ess.Override.mergeIntoLiveTable(menu, "items", { "modded_C", "modded_D" })
-- #menu.items == 4, and menu.items == liveRef (same object, grown in place)
```

Guard: refuses a non-table `t` — logs and returns `false`.

## Which one to reach for

Per the deep dive's own general pattern: **prefer `mergeIntoLiveTable` over `wrap` wherever the thing you
want to change is data a live table already holds**, not logic. Full-function replacement (`wrap`) should be
the fallback once you've confirmed there's no live table to merge into — every function downstream of a
merged table keeps working unmodified, because it was never touched; every function you *do* replace with
`wrap`, you inherit all of its untouched responsibilities along with the one behavior you meant to change.

## See also

- [Deep Dive: Safely Overriding a Function](../deep-dives/function-override) — the full investigation this
  namespace packages: three wrong turns, the confirmed working fix, live-test screenshot, and known
  limitations (doesn't survive a full game restart, untested on a non-host co-op client, etc. — all specific
  to the wardrobe case, not to `Ess.Override` itself).
- [Networking](net) — `Ess.Net.hijackCallback`, built directly on `Ess.Override.wrap`.
- [Essentials (Ess)](index) — the framework index.
