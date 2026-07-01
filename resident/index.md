---
title: Resident Modules
nav_order: 6
has_children: true
has_toc: false
---

# Resident Modules

Reference pages for the modules in `src/resident/` — the game's core reusable engine/library modules
and world-entity scripts (as opposed to `src/vz/`, which is mostly per-mission/level content, and
`src/shell/`, the front-end menu system).

There are 228 of these, so they're split into categories (in the sidebar) rather than one flat list:

- **[Cheats & Dev Tools](cat-cheats-dev)** — start here for working, copy-pasteable examples
- **[Vehicles](cat-vehicles)**
- **[Support & Airstrikes](cat-support-airstrikes)** — the supply-drop/airstrike system, the largest category
- **[Missions & Tasks](cat-missions-tasks)** — contracts, jobs, objectives, briefing flow
- **[GUI & HUD](cat-gui-hud)** — widgets, menus, HUD elements
- **[World Objects & Props](cat-world-objects)** — everything interactive/environmental that doesn't fit elsewhere
- **[Audio & Music](cat-audio-music)**
- **[Core Engine & Utilities](cat-core-utilities)** — bootstraps, base classes, cross-cutting managers

Each category page has its own short intro explaining what's in it and where to start. Use the search
bar (top of the page) to jump straight to a module by name if you already know what you're looking for.

Every module page follows the same layout: Overview, Inheritance, Instance pattern, Functions, Events,
and Notes for modders. Each page names its source `.lua` file so you know what you're reading about, but
doesn't link to or reproduce the file itself — the decompiled source isn't republished here, only
descriptions of what it does.

## How these modules actually work

There's no `require` in this engine. Every `.lua` file in `resident/` is a global module, addressed by
its filename — `crate.lua` defines module `Crate`. Two built-ins glue modules together:

- **`inherit("Name")`** at the top of a file makes it prototype-inherit from another module's table.
  E.g. `airplane.lua` starts with `inherit("VehicleBlippable")`, so `Airplane` reuses (and can override)
  everything `VehicleBlippable` defines. Chains can run several modules deep.
- **`import("Name")`** pulls another module in as a callable namespace without inheriting from it.

<details class="lua101" markdown="1">
<summary>New to Lua? Click to expand</summary>

Everything below assumes you already know what a function, a table, and a variable are. If you've never
programmed before, or never used Lua specifically, here's the minimum vocabulary to get through this
page — skip this box entirely if any of it is already familiar.

- **A function is a named, reusable chunk of code.** `function Foo(x) ... end` defines one called `Foo`
  that takes one input (`x`). You run it later by writing `Foo(5)`. Nothing inside a function happens
  until something actually calls it by name.
- **A table is Lua's one and only data structure.** Other languages have separate "array" and "object"/
  "dictionary" types; Lua has just tables, and they do both jobs. `{1, 2, 3}` is a table used as a list.
  `{x = 1, y = 2}` is the same kind of table used as a set of named fields, accessed as `t.x` / `t.y`.
  Every "object" you'll see in this wiki (a player, a support item, a menu option) is really just a
  table with some fields and functions attached to it.
- **`local` limits where a name is visible.** `local nCash = 100` creates a variable that only exists
  inside the current function/file. Leave off `local` and the name becomes *global* — visible from any
  script, which is how e.g. `_G.Cheat` in [`MrxCheatBootstrap`](mrxcheatbootstrap) ends up callable from
  anywhere.
- **`self` and the colon (`:`) are a shortcut for "the table this function was called on."** Writing
  `oInstance:Create(uGuid)` is Lua sugar for `Inheritable.Create(oInstance, uGuid)` — the thing before
  the colon gets silently passed as the function's first argument, conventionally named `self` inside
  the function body. You'll see this constantly: `:GetParent()`, `:IsActive()`, `:Complete()` are all
  "call this function, passing the table on my left as the first argument."
  - Naming note: Lua itself doesn't require the parameter to be called `self` — it's purely a
    convention. `oPrototype:Create(uGuid, iArg)` below expands to a function whose *first* parameter
    receives `oPrototype`, and that file happens to name it `oPrototype` instead of `self`. Same
    mechanism, different chosen name.
- **A metatable is a fallback lookup.** `setmetatable(oInstance, {__index = oPrototype})` means: "if
  something asks `oInstance` for a field it doesn't have, go check `oPrototype` instead." That single
  line is the entire mechanism behind "inheritance" in this codebase — an instance only stores what
  makes it unique, and silently falls back to its class/prototype table for everything else.

With that vocabulary, the code below reads as: "make a new empty table, tell it to fall back to
`oPrototype` for anything it doesn't have itself, tag it with which world object it belongs to, remember
it in a lookup table by that tag, and hand it back."

</details>

The root of most inheritance chains is [`Inheritable`](inheritable), which defines the actual
per-instance pattern:

```lua
function Create(oPrototype, uGuid, iArg)
  local oInstance = {}
  setmetatable(oInstance, {__index = oPrototype})  -- instance falls back to the class table
  oInstance.uGuid = uGuid
  tInstance[uGuid] = oInstance                      -- per-instance state keyed by world object GUID
  return oInstance
end
```

And the standard activation idiom at the top of nearly every world-object script:

```lua
function OnActivate(uGuid, uRuntimeOwner, iArg)
  Event.Create(Event.ObjectHibernation, {uGuid, "awake"}, Awake, {uGuid, iArg})
end

function Awake(uGuid, iArg)
  local oPrototype = getfenv()                      -- this file's own global table = "the class"
  local oInstance = oPrototype:Create(uGuid, iArg)   -- resolves to Inheritable.Create via inheritance
end
```

`OnActivate` fires when the engine spawns/activates a world-object instance; it defers real setup to
`Awake` (waiting for the object to leave hibernation). `Awake` creates a per-instance table keyed by
`uGuid` (a unique runtime object handle), with the module's own table as its metatable `__index` — so
`self` in instance methods falls back to shared class behavior for anything not set on the instance
itself. That's the prototypal-OOP pattern every "Instance pattern" section on these pages is describing.

Not every module follows this — plenty are stateless utility/manager modules (just functions and
module-level globals, no `Create`/`uGuid` pattern). Each page's Instance pattern section says which kind
it is.
