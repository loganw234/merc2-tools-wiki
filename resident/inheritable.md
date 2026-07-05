---
title: Inheritable
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [base, object, beginner-friendly]
verified: true
verified_note: "deeper pass: re-verified all 7 functions line-for-line against the 39-line source (Create/Delete/GetFromGuid signatures and the OnActivate->Event.ObjectHibernation->Awake->Create idiom all exact); no changes needed — this remains the canonical instance-pattern reference the rest of the wiki points at"
---

# Inheritable

*Module: inheritable.lua*

## Overview

`Inheritable` is the root of the per-instance object pattern used by nearly every world-object script in
`resident/` — see the [Resident Modules landing page](index#how-these-modules-actually-work) for the
general explanation of `inherit()`/`import()` and the `OnActivate`→`Awake`→`Create` idiom this module
defines. The entire file is short enough to quote in full:

```lua
tInstance = {}

function OnActivate(uGuid, uRuntimeOwner, iArg)
  Event.Create(Event.ObjectHibernation, {uGuid, "awake"}, Awake, {uGuid, iArg})
end

function Awake(uGuid, iArg)
  local oPrototype = getfenv()               -- this file's own global table = "the class"
  local oInstance = oPrototype:Create(uGuid, iArg)
end

function OnDeactivate(uGuid)
  local oInstance = tInstance[uGuid]
  if oInstance then
    oInstance:Delete()
  end
end

function OnDeath(uGuid)
  OnDeactivate(uGuid)
end

function Create(oPrototype, uGuid, iArg)
  local oInstance = {}
  setmetatable(oInstance, {__index = oPrototype})  -- instance falls back to the class table
  oInstance.uGuid = uGuid
  oInstance.sName = tostring(uGuid)
  tInstance[uGuid] = oInstance                     -- per-instance state keyed by world object GUID
  return oInstance
end

function Delete(oSelf)
  tInstance[oSelf.uGuid] = nil
end

function GetFromGuid(uGuid)
  return tInstance[uGuid]
end
```

If a module built on `Inheritable` (directly or several `inherit()` links deep) never defines its own
`Create`, calling `oPrototype:Create(uGuid, iArg)` in `Awake` resolves all the way up the chain to this
file's `Create` — one instance table per world-object `uGuid`, falling back to its module's own table
(via `__index`) for anything not set on the instance itself. This is the mechanism the
[Lua-101 box on the landing page](index#how-these-modules-actually-work) walks through in plain terms if
any of this is new.

## Inheritance
- Inherits from: none — this is the base
- Imports: none

## Instance pattern
`Inheritable` itself holds no per-object state — `tInstance` (module-level, keyed by `uGuid`) is the
shared registry every subclass's instances get added to and removed from, via `Create`/`Delete`.

## Functions

### `OnActivate(uGuid, uRuntimeOwner, iArg)`
The engine calls this by naming convention when a world-object instance activates. Defers real setup to
`Awake`, waiting for the object to leave hibernation first (`Event.ObjectHibernation`).

### `Awake(uGuid, iArg)`
Calls `Create` on the calling module's own prototype table (via `getfenv()`), producing the actual
per-instance object.

### `Create(oPrototype, uGuid, iArg)`
Builds a new table, sets `oPrototype` as its metatable `__index`, tags it with `uGuid` and a default
`sName`, and registers it in `tInstance`. **A subclass that overrides `Create` and wants `OnDeactivate`/
`GetFromGuid` to keep working needs to still register the instance in `tInstance` itself** — nothing
enforces that automatically once you stop calling this version.

### `OnDeactivate(uGuid)`
Looks up the instance in `tInstance` and calls `oInstance:Delete()` if it exists.

### `OnDeath(uGuid)`
Just calls `OnDeactivate(uGuid)`. **Not wired through an explicit `Event.ObjectDeath` listener anywhere in
this file** — like `OnActivate`/`OnUse` elsewhere in this codebase, `OnDeath` is a name the engine calls
directly by convention, not something this module registers for itself.

### `Delete(oSelf)`
Removes the instance from `tInstance`, keyed by `oSelf.uGuid`. Called as `oInstance:Delete()` — relies on
`Create` having set `uGuid` on the instance.

### `GetFromGuid(uGuid)`
Looks up a live instance by its world-object GUID. The general-purpose way to go from "I have a `uGuid`"
to "I have the actual per-instance object with all its methods/state" for anything built on this base.

## Events
- Listens for `Event.ObjectHibernation` inside `OnActivate` — the actual per-instance creation is deferred
  until the object wakes up, not done immediately on activation.
- `OnDeath` (and `OnActivate`/`OnUse` on other modules) are engine-called by name, not subscribed to via
  an explicit `Event.Create` in this file — don't go looking for the registration, there isn't one.

## Notes for modders
- **This is the base class almost everything in `resident/` ultimately inherits from** — read this page
  once, and the "Instance pattern" section on every other world-object page on this wiki will make sense
  in terms of it.
- **`GetFromGuid(uGuid)`** is the general tool for "I have a GUID from somewhere else (an event, a query),
  give me the actual object" — works for any module built on this base, not just ones you wrote yourself.
- If you override `Create` in your own module, remember to still populate `tInstance` (or call
  `Inheritable.Create` and layer your own fields on top of what it returns) — `OnDeactivate`/`GetFromGuid`
  both depend on that registry being populated correctly.
