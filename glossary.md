---
title: Glossary
nav_order: 5
---

# Glossary

Terms used throughout this wiki that either aren't standard Lua vocabulary or mean something specific
in this game's engine.

**`uGuid`**
: A unique handle identifying one live world-object instance at runtime (a spawned crate, vehicle,
character, etc.). Most engine calls that operate on "an object" take a `uGuid` as their first argument.
Not stable across game sessions — it's a runtime handle, not a permanent ID.

**module**
: A single `.lua` file, addressed by its filename without the extension. `crate.lua` defines the module
`Crate`. There's no `require` — every module is just a global table the engine loads and wires up via
`inherit`/`import`.

**engine namespace**
: A built-in table like `Object`, `Event`, `Player`, `MrxPmc` — these are provided by the engine itself,
not defined by any `.lua` module in this corpus. You call into them (`Object.GetPosition(...)`) but
won't find their implementation in `resident/`.

**`inherit("Name")`**
: Declared at the top of a module, makes it prototype-inherit from another module's table. See the
[Resident Modules](resident/) landing page for the full explanation with examples.

**`import("Name")`**
: Pulls another module in as a callable namespace, without inheriting from it.

**`getfenv()`**
: Stock Lua 5.1 built-in returning the calling function's environment table — in this codebase, that's
almost always used as a way for a module to refer to *itself* (its own global table, i.e. "the class")
from inside one of its own functions. See the `Awake`/`Create` idiom on the
[Resident Modules](resident/) page.

**instance / per-instance table**
: The table created by `Create(oPrototype, uGuid, ...)` for one specific `uGuid`, with the module's own
table set as its metatable `__index`. Fields you set on the instance override the module's shared
defaults for that one object only.

**`OnActivate` / `OnDeactivate` / `OnDeath`**
: Lifecycle functions the engine calls directly when a world-object instance is spawned, torn down, or
its underlying object dies. Not arbitrary names — see the lifecycle table on
[Resident Modules](resident/).

**`Event.Create` / `Event.CreatePersistent` / `Event.Delete`**
: Subscribe to (or unsubscribe from) an engine event — a timer firing, an object leaving hibernation, a
winch state changing, etc. `Event.Create` returns a handle you pass to `Event.Delete` later.

**`KEYVAL`**
: A convention (not a language feature) for `scripts/OnKey/` scripts: put `local KEYVAL = "insert"` (or
any key name) somewhere in the script's first 10 lines, and the script loader reads it as that script's
default hotkey, no config file edit required. See [Your First Mod](first-mod).

**`[ok]` / `[runtime]` / `[compile]` / `[bridge]`**
: Prefixes on lua-bridge REPL responses. `[ok]` = ran successfully, `[runtime]` = ran but errored,
`[compile]` = syntax error, `[bridge]` = the bridge itself couldn't run your code at all (see the error
table in [Getting Started](getting-started)).

**`float`, not `double`**
: This build's Lua uses 4-byte floats for `lua_Number`, not the 8-byte doubles a stock Lua 5.1 build
would use. Numbers can lose precision you wouldn't expect from "normal" Lua — see
[Getting Started](getting-started) for details.

**`MrxPmc`**
: The engine namespace for player-economy state — cash, fuel, fuel capacity.

**`Pg`**
: Broad world/level-state queries — landing zones, spawn points, contract state, achievements, "collect
all objects of type X in the world" helpers. Likely short for "Playground" (the exact expansion isn't
confirmed), but functionally: world-wide queries, as opposed to per-player state (`Player`) or
per-object state (`Object`).
