---
title: Collectable
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [collectible, toolbox]
---

# Collectable

*Module: collectable.lua*

## Overview
The `Collectable` module represents collectible objects in the game world. These objects can be interacted with using the toolbox context action and are automatically killed if they have the "CollectableInvalidated" label or when collected.

## Inheritance
- Inherits from: `Inheritable`
- Imports: `MrxGui`, `MrxPmc`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `uEvent`: Handle for the persistent event listener.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It checks if the object is alive and creates a new per-instance table for the object using the module's prototype.

### `Create(oPrototype, uGuid, uRuntimeOwner)`
Creates a new per-instance table for the object using the `Inheritable` prototype. If the object is not alive or has the "CollectableInvalidated" label, it sets a very small hibernation distance and kills the object. Otherwise, it adds a context action for the toolbox and registers an event listener for the `ContextAction` event.

### `Delete(oSelf)`
Tears down the per-instance table by deleting the persistent event listener and removing the context action. It then calls the base class's `Delete`.

### `OnContextAction(oSelf, uCharacter)`
Called when the toolbox context action is triggered on the collectible object. It kills the object.

## Events
- Listens for `Event.ContextAction` to call `OnContextAction` when the toolbox context action is triggered.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of collectible objects.
- The "CollectableInvalidated" label automatically kills the object, so be cautious when applying this label.
- Use the toolbox context action to interact with collectible objects.
- Be aware that network synchronization may affect multiplayer behavior.