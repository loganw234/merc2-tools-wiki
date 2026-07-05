---
title: Collectable
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [collectible, toolbox]
verified: true
verified_note: confirmed real per-uGuid pattern via Inheritable.Create/tInstance; noted OnDeactivate is inherited (not defined in this file) and resolves to this file's Delete; flagged MrxGui/MrxPmc imports as unused in this file; corrected OnActivate (guards on Object.IsAlive before creating instance, returns early otherwise).
---

# Collectable

*Module: collectable.lua*

## Overview
The `Collectable` module represents collectible objects in the game world. These objects can be interacted with using the toolbox context action and are automatically killed if they have the "CollectableInvalidated" label or when collected.

## Inheritance
- Inherits from: `Inheritable`
- Imports: `MrxGui`, `MrxPmc` — neither is actually referenced anywhere else in this file; likely dead imports.

## Instance pattern
Real per-`uGuid` instance pattern. `Create(oPrototype, uGuid, uRuntimeOwner)` calls `Inheritable.Create` directly
(builds the instance table, `setmetatable`s it, registers it in `Inheritable`'s `tInstance`). Tracks one
instance field:
- `uEvent`: Handle for the persistent `Event.ContextAction` listener (only set if the object survives the
  alive/invalidated checks in `Create`).

`OnDeactivate` is not defined in `collectable.lua` itself — it's inherited from `Inheritable.OnDeactivate`,
which looks up the instance in `tInstance` and calls `oInstance:Delete()`, resolving (via metatable fallback)
to this file's own `Delete` below.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Returns immediately if `Object.IsAlive(uGuid)` is false. Otherwise creates the per-instance table via
`oPrototype:Create(uGuid, uRuntimeOwner)`. Unlike most world-object scripts, this does not defer to an
`Event.ObjectHibernation` "awake" event first — `Create` runs synchronously from `OnActivate`.

### `Create(oPrototype, uGuid, uRuntimeOwner)`
Calls `Inheritable.Create(oPrototype, uGuid, uRuntimeOwner)` to build the instance. If the object is not alive,
returns the instance as-is (no context action, no event). If it has the `"CollectableInvalidated"` label, sets
`Object.SetHibernationDistance(uGuid, 1.0E-6)` and calls `Object.Kill(uGuid)`, then returns. Otherwise adds a
toolbox context action (`Pg.AddContextAction(uGuid, "[ContextAction.Toolbox]", 2, 0, 0, 0, 0)`) and registers
`oInstance.uEvent` as a persistent `Event.ContextAction` listener (fires for `Player.GetAnyCharacter()` on this
`uGuid`), calling `oInstance.OnContextAction`.

### `Delete(oSelf)`
Tears down the per-instance table: deletes `oSelf.uEvent`, removes the toolbox context action via
`Pg.RemoveContextAction(oSelf.uGuid)`, then calls `Inheritable.Delete(oSelf)`.

### `OnContextAction(oSelf, uCharacter)`
Called when the toolbox context action is triggered on the collectible object. It kills the object
(`Object.Kill(oSelf.uGuid)`) — `uCharacter` is accepted but unused.

## Events
- Listens for `Event.ContextAction` (via `Event.CreatePersistent`) to call `OnContextAction` when the toolbox context action is triggered.

## Notes for modders
- `OnDeactivate` is never called explicitly in this file — it comes from `Inheritable` and triggers `Delete` automatically. No need to wire it up yourself.
- The "CollectableInvalidated" label short-circuits `Create` and kills the object immediately, before any context action or event is registered.
- Use the toolbox context action to interact with collectible objects.
- `MrxGui` and `MrxPmc` are imported but unused in the current source — likely leftover from a previous version.