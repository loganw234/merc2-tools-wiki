---
title: Building Your Own Framework
parent: Frameworks
nav_order: 10
---

# Building Your Own Framework

## Overview

A **framework** in this wiki's sense is a reusable global library that lives in `scripts/OnLoad/`,
registers itself once when the game world loads, and stays available to every other script from then on —
distinct from a one-off `OnKey` tool or a single mission's contract script. [Essentials
(Ess)](ess/) is the real, live example every pattern on this page is drawn from; if you want to see these
ideas at full scale rather than in skeleton form, its [Core Primitives](ess/core) page and the deployed
`scripts/OnLoad/1_Ess.lua` are the place to look.

This page exists because Ess's own source has been pointing at it without a destination: `00_core.lua`'s
header comment says to give your framework "a low `lua_loader.ini` number (loads before ModNet/uilib/
ContractFramework if you use those too — see lua-bridge-load-order-convention)" — a page that never got
written until now.

## Where your code runs: the OnLoad folder and load order

Anything dropped in `<game>/scripts/OnLoad/*.lua` runs once, automatically, the first time the loader
detects the game world has actually finished loading (not just the main menu) — see
[`lua-bridge-api/loader.md`](lua-bridge-api/loader) for the broader `Loader` API these scripts run under.
Every `.lua` file in that folder runs, in some order, every time that milestone fires.

**That order is not the file listing you see in Explorer — it's controlled by `scripts/lua_loader.ini`**,
specifically its `[OnLoad]` section, and the mechanism is worth understanding precisely rather than just
copying the convention:

- The loader keeps one entry per script: `SomeFile.lua=<number>`, and **the lowest number loads first** —
  that's not a guess, it's the literal comment the loader itself writes into the top of the ini file.
- The *first time* the loader ever sees a script it has no ini entry for yet, it doesn't leave the order
  undefined — it sorts every currently-discovered script alphabetically (case-insensitive), and assigns the
  new one a number based on where it landed in that alphabetical pass, then **writes that number into the
  ini permanently** (`lua_bridge_DEV.c` — the discovery pass, auto-assignment, and ini-write live together
  around the loader's `ExecuteLuaFolder` function). From that point on, the ini entry is what's read; the
  filename itself no longer matters for ordering.
- This is why a numeric prefix works, and *why* it's reliable rather than a superstition: ASCII digits sort
  before ASCII letters, so a file named `1_Something.lua` will land at or near the very front of that
  first-ever alphabetical pass almost regardless of what else is in the folder — which means it gets a low
  number auto-written to the ini, which means it loads early from then on.

Here's the actual, current `[OnLoad]` section from a real running install, exactly as it reads on disk:

```ini
[OnLoad]
1_Ess.lua=5
Encounters.lua=20
```

`1_Ess.lua` loads first, at `5`; `Encounters.lua` — a plain, unprefixed mission script with no reason to
race anything — comes in behind it at `20`. Nobody hand-typed those numbers for the second file; the loader
assigned it the first time it saw it.

**Practical takeaways:**
- Ship your framework as `1_YourFramework.lua` (or `2_`, if you know it needs to load after something
  else's `1_`) so that on a **fresh install**, before any ini entries exist, it reliably claims a low
  auto-assigned number ahead of a typical modder's own un-prefixed OnKey/mission-style scripts.
- The prefix only controls the *first-ever* assignment. If you need to guarantee order on an install that
  already has entries — or just want to be exact rather than relying on alphabetical luck — edit
  `scripts/lua_loader.ini` directly. It's a plain, human-editable ini; that's the real source of truth, the
  filename convention is just a good default for it.
- This same ini-driven mechanism (and the same "lowest number first" rule) also governs `[OnBoot]`.
  `[OnKey]` is different — those scripts fire on a keypress, not in a startup batch, so there's no order to
  assign; its ini values are hotkey bindings instead, and that section only ever gets auto-populated
  alphabetically, not renumbered.

## Registering yourself globally

Once your file is loading, it needs to actually make its API reachable from *every other* script that runs
after it — with no `import()`, the way [Engine Namespaces](namespaces/) are always just there. The pattern
Ess itself uses, verbatim from the real deployed source:

```lua
_G.Ess = _G.Ess or {}
local Ess = _G.Ess
Ess.VERSION = "0.3.0"

Ess.Safe = Ess.Safe or {}
Ess.Table = Ess.Table or {}
```

Two things are doing real work here, not just style:

- **`_G.Name = _G.Name or {}` instead of `_G.Name = {}`.** The `or {}` makes this idempotent — safe to run
  twice. That matters because your OnLoad script is not guaranteed to run exactly once per session; see
  **Unsafe patterns** below for why. If your framework got reloaded, this line reuses the existing table
  (and everything already registered on it) instead of silently wiping it out from under any script that
  grabbed a reference earlier.
- **`local Name = _G.Name`** gives you a short, fast local alias to use for the rest of the file, while the
  actual public surface still lives on the real global. Sub-tables (`Ess.Safe`, `Ess.Table`, ...) get built
  the exact same idempotent way, one level down.

**Pick a name nothing else is likely to use.** A generic name like `Utils` or `Data` risks colliding with
another mod; a name that happens to match a real [engine namespace](namespaces/) (`Object`, `Player`,
`Math`, ...) is worse — you'd be shadowing something natively-registered and globally available on every
script, which gets confusing fast for anyone (including future you) trying to tell your table apart from
the engine's. A short, distinctive, framework-specific name — `Ess`, `WaveDefense` — is the safe choice.

**A `VERSION` field is worth including from day one.** It costs nothing to add and other tooling in this
ecosystem actually reads it — `mercs2-lua-web-ide`'s version-drift warning compares a mod's declared
version against what's actually running. If your framework grows enough that other scripts start depending
on specific behavior, a version string is how they (or you, later) can tell drift happened at all.

## Safe patterns

- **`pcall`-wrap every native engine call**, and log through one function rather than scattering raw
  `Loader.Printf` calls everywhere:

  ```lua
  function Ess.Log(msg)
      if Loader and Loader.Printf then
          Loader.Printf("[Ess] " .. tostring(msg))
      end
  end

  function Ess.Safe.call(fn, ...)
      local ok, a, b, c, d = pcall(fn, ...)
      if not ok then
          Ess.Log("Safe.call failed: " .. tostring(a))
          return false
      end
      return true, a, b, c, d
  end
  ```

  One wrapper, reused everywhere, means a bad call fails loud exactly once (in your log) instead of either
  crashing your script or failing silently depending on which of the dozen call sites hit the problem.
- **Guard optional dependencies before touching them** — `if Loader and Loader.Printf then` above means
  `Ess.Log` itself can never throw, even in some future context where `Loader` isn't present. Same idea
  applies to any other framework/global you build on but don't strictly own.
- **Validate *before* calling, not after** — see the next section for why `pcall` alone doesn't cover you
  here.

## Unsafe patterns (and why)

- **Assuming your init code runs exactly once per session.** It doesn't, reliably — `Loader`'s own docs
  note it re-registers its globals "on every queue pump specifically so a `_G` wipe across a game-state
  transition (level load, menu transition) can't strand" them. Your framework can face the same reset. The
  idempotent `_G.Name = _G.Name or {}` pattern above is the direct defense — write your init so running it
  twice is harmless, because it might run twice.
- **Trusting `pcall` to catch a bad call.** It only catches Lua-level errors. Two real, confirmed failure
  modes on this engine don't behave like a Lua error at all:
  - A native call with a missing or wrong argument typically just **returns `nil` silently** — no error,
    because the engine inlines its own argument checks rather than raising one. `pcall` sees success. Only
    a live probe with real arguments tells you whether it actually did anything (see, e.g., any
    [Engine Namespaces](namespaces/) page's "Notes for modders" section).
  - Some calls — most notably spawning or resolving an object by an **unresolved name** — don't error, they
    **crash the game to desktop outright**. `pcall` cannot catch that; it isn't a Lua error, it's a native
    crash. `Pg.Spawn('Austin (CIV)', ...)` doing exactly this, live-confirmed, is documented on
    [`Pg`](namespaces/pg#spawning). The only real defense is validating *before* the call —
    `Pg.GetGuidByName(name) ~= nil` first, every time — not wrapping the call and hoping.
- **Monkey-patching a native engine namespace directly** (reassigning `Object.GetName`, etc.) instead of
  wrapping it. You don't know what else — the engine itself, another mod, a future version of your own
  framework — expects that function to still behave the original way.
- **Picking up an unusual return type on faith.** Some native calls hand back `userdata` where you'd expect
  a `string` or `number` (a guid is `userdata`, not reusable via `tostring`; see [Ess.Guid/Ess.Name on Core
  Primitives](ess/core#essguid--essname) for the real round-trip). Check `type()` before treating a return
  value as the type its name implies.

## A basic skeleton to build from

Everything above, assembled into a minimal, real, working starting point. Save this as
`scripts/OnLoad/1_YourFramework.lua` (renaming `YourFramework` throughout) and it will register itself and
respond to a test call the next time the world finishes loading.

```lua
-- YourFramework.lua -- drop in scripts/OnLoad/ as 1_YourFramework.lua

_G.YourFramework = _G.YourFramework or {}
local YourFramework = _G.YourFramework
YourFramework.VERSION = "0.1.0"

-- One logging chokepoint, guarded against a missing Loader.
function YourFramework.Log(msg)
    if Loader and Loader.Printf then
        Loader.Printf("[YourFramework] " .. tostring(msg))
    end
end

-- One pcall wrapper, reused for every native call this framework makes.
-- Does NOT protect against a native crash-to-desktop (e.g. spawning an
-- unresolved name) -- validate those inputs yourself before calling.
function YourFramework.SafeCall(fn, ...)
    local ok, a, b, c, d = pcall(fn, ...)
    if not ok then
        YourFramework.Log("SafeCall failed: " .. tostring(a))
        return false
    end
    return true, a, b, c, d
end

-- Example: your framework's own sub-table, built the same idempotent way.
YourFramework.Example = YourFramework.Example or {}

function YourFramework.Example.Ping()
    YourFramework.Log("Ping called -- framework is alive.")
    return true
end

YourFramework.Log("YourFramework " .. YourFramework.VERSION .. " loaded.")
```

Drop it in, give it a low-numbered filename, and any script that runs after it — another OnLoad file, an
OnKey script, a mission — can now call `YourFramework.Example.Ping()` with no `import()`, the same way it
would call into `Ess` or a native namespace.

**Where to go from here**, once the skeleton above isn't enough:
- **Multi-file source during development.** Ess's own repo is dozens of `src/*.lua` files
  (`00_core.lua`, `01_math.lua`, ... `97_easy_debug.lua`) merged into the single `1_Ess.lua` you actually
  deploy — a *build-time* numbering convention, separate from the *runtime* `lua_loader.ini` one above, but
  the same underlying idea (deterministic order via a numeric prefix) applied one layer earlier. Worth
  adopting once one file stops being a comfortable place to work.
- **Persistence** — `Loader.SaveVar`/`LoadVar` (see [Loader](lua-bridge-api/loader#persistence)) if your
  framework needs state that survives a restart without touching the real save file.
- **A layered API** (`Raw` → core → `Easy`) for a namespace that grows large enough to want both
  full-control and one-line-call versions of the same operation — see [Ess.Easy](ess/easy) for the fullest
  real example of this shape.
