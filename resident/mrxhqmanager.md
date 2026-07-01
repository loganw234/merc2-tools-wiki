---
title: MrxHqManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [hq, faction]
---

# MrxHqManager

*Module: mrxhqmanager.lua*

## Overview
The `MrxHqManager` module is responsible for managing Headquarters (HQ) in the game. It handles operations such as unlocking and locking HQs, adding and removing starters, setting respawn behavior, and monitoring their health status. This module also manages events related to HQ deaths and revivals.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`, `MrxHq`, `WifHqData`, `MrxFactionManager`

## Instance pattern
This is a stateless manager/utility module. It tracks the following key fields:
- `_tHqs`: A table that stores HQ instances by their names.
- `_tHqEvents`: A table that stores event handles for HQ-related events.
- `_bInside`: A boolean indicating whether the player is inside an HQ.

## Functions
### `GetHq(sHqName)`
Retrieves an HQ instance by its name. Logs a debug message if the HQ cannot be retrieved and returns `nil`.

### `AddStarter(sHqName, tStarter)`
Adds a starter to an HQ. If the HQ does not exist, it attempts to unlock it first.

### `RemoveStarter(sHqName, tStarter)`
Removes a starter from an HQ.

### `UnlockHq(sHqName)`
Unlocks an HQ by loading its data and setting up its properties. Logs debug messages for each step of the process.

### `LockHq(sHqName)`
Locks an HQ by setting its lock state to true and refreshing the UI display. Deletes any associated events.

### `LockAllHq()`
Globally locks all HQs that are not already locked.

### `UnlockAllHq()`
Globally unlocks all HQs that were previously globally locked.

### `_CreateDeathEvent(sHqName, uHqGuid)`
Creates a death event for an HQ. Depending on the HQ's configuration, it listens for either object health or object death events.

### `_SetupRespawn(bEnable, sHqName, uHqGuid)`
Sets up respawn behavior for an HQ. If enabled and the HQ is alive, it creates a death event. If disabled and the HQ is not alive, it deletes any associated events.

### `SetHqRespawn(sHqName, bEnable)`
Enables or disables respawn behavior for an HQ. Updates the HQ's respawn state and sets up or removes the appropriate events based on the new state.

### `_SetHq(sHqName, bEnable)`
Sets the lock state of an HQ and refreshes its UI display.

### `_OnHqDeath(sHqName, uHqGuid, uKilledByTemplate, uCulprit)`
Handles the death event for an HQ. Logs a debug message, updates the HQ's lock state, adjusts faction relations if necessary, and sets up revival events if respawn is enabled.

### `_OnHqHibernation(sHqName, uHqGuid)`
Handles the hibernation event for an HQ by reviving it, updating its lock state, and setting up death events again.

### `IsInside()`
Returns whether the player is inside an HQ.

### `SetInside(bInside)`
Sets whether the player is inside an HQ.

### `SetUnloadCallback(fCallback, tCallbackArgs)`
Sets a callback function and arguments to be called when the module unloads.

### `GetUnloadCallback()`
Retrieves the unload callback function and its arguments.

## Events
- Listens for `Event.ObjectHealth` or `Event.ObjectDeath` to handle HQ death events.
- Listens for `Event.ObjectHibernation` to handle HQ hibernation events.

## Notes for modders
- Use `GetHq`, `AddStarter`, and `RemoveStarter` to manage HQ starters.
- Use `UnlockHq` and `LockHq` to control the lock state of HQs.
- Use `SetHqRespawn` to enable or disable respawn behavior for HQs.
- Be aware that faction relations may change when an HQ is destroyed.
- The module uses internal functions prefixed with `_` for internal operations.