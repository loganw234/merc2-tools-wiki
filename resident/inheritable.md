---
title: Inheritable
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [base, object]
---

# Inheritable

*Module: inheritable.lua*

## Overview
The `Inheritable` module serves as the base class for all world objects in the game. It provides a framework for creating and managing per-instance tables with prototype inheritance, allowing derived modules to override or extend functionality.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module that does not track any specific instance state itself. It provides the foundational `Create` and `Delete` methods for managing per-instance tables, which are used by derived modules.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when an object instance is activated. It sets up an event to call `Awake` once the object leaves hibernation.

### `Awake(uGuid, iArg)`
Creates a new per-instance table for the object using the module's prototype.

### `OnDeactivate(uGuid)`
Tears down the per-instance table by calling the instance's `Delete` method if it exists.

### `OnDeath(uGuid)`
Called when an object instance dies. It simply calls `OnDeactivate`.

### `Create(oPrototype, uGuid, iArg)`
Constructs a new per-instance table with the given prototype as its metatable (`__index`). The instance is registered in the global `tInstance` table keyed by `uGuid`.

### `Delete(oSelf)`
Removes the instance from the global `tInstance` table.

### `GetFromGuid(uGuid)`
Retrieves an instance from the global `tInstance` table using its `uGuid`.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for `Event.ObjectDeath` to call `OnDeactivate` when the object dies.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage instance lifecycle.
- Use `Create` to instantiate new objects and `Delete` to clean up instances.
- The global `tInstance` registry can be used to access instances by their `uGuid`.
- Be aware of the prototype inheritance chain when extending this module.