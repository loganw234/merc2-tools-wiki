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
and Notes for modders — and links back to the exact source file so you can verify anything that looks
off.

## How these modules actually work

There's no `require` in this engine. Every `.lua` file in `resident/` is a global module, addressed by
its filename — `crate.lua` defines module `Crate`. Two built-ins glue modules together:

- **`inherit("Name")`** at the top of a file makes it prototype-inherit from another module's table.
  E.g. `airplane.lua` starts with `inherit("VehicleBlippable")`, so `Airplane` reuses (and can override)
  everything `VehicleBlippable` defines. Chains can run several modules deep.
- **`import("Name")`** pulls another module in as a callable namespace without inheriting from it.

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
