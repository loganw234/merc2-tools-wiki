---
title: MrxHqManager
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [hq, faction]
verified: true
verified_note: "deeper pass: spot-checked all functions/events/Imports against source — accurate, no changes needed; the two confirmed bugs (UnlockHq logs undeclared sName; _SetupRespawn clobbers the death-event handle with nil) and the -100 HQ-destroyed relation drop remain verified"
---

# MrxHqManager

*Module: mrxhqmanager.lua*

## Overview
The `MrxHqManager` module is responsible for managing Headquarters (HQ) in the game. It handles operations such as unlocking and locking HQs, adding and removing starters, setting respawn behavior, and monitoring their health status. This module also manages events related to HQ deaths and revivals.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`, `MrxHq`, `WifHqData`, `MrxFactionManager`

## Instance pattern
This is a stateless singleton/utility module — plain module-level globals, no `Create`/`OnActivate`/`Awake`/`tInstance`. It tracks the following key fields:
- `_tHqs`: A table that stores HQ instances (created via `MrxHq:Create`) by their HQ name string.
- `_tHqEvents`: A table that stores event handles for HQ-related events, keyed by HQ name (`LockHq`) or by object GUID (`_CreateDeathEvent`, `_SetupRespawn`, `_OnHqDeath`, `_OnHqHibernation`) — the same table is used with both key types.
- `_bInside`: A boolean indicating whether the player is inside an HQ, read/written only via `IsInside`/`SetInside` (not initialized elsewhere in this file; `nil`/falsy until `SetInside` is called).
- `_fUnloadCallback` / `_tUnloadCallbackArgs`: a callback function and its argument table, set via `SetUnloadCallback` and read via `GetUnloadCallback` — not called from anywhere in this file itself, so the actual unload trigger lives elsewhere (not confirmable from this file alone).

## Functions
### `GetHq(sHqName)`
Retrieves an HQ instance by its name. Logs a debug message if the HQ cannot be retrieved and returns `nil`.

### `AddStarter(sHqName, tStarter)`
Adds a starter to an HQ. If the HQ does not exist, it attempts to unlock it first.

### `RemoveStarter(sHqName, tStarter)`
Removes a starter from an HQ.

### `UnlockHq(sHqName)`
Unlocks an HQ by loading its data (via `WifHqData.GetHqConfigFromId`) and setting up its properties on first unlock (creates `MrxHq:Create(tHqData)`, sets its name), then clears its lock flag, refreshes its UI, and enables respawn by default (`SetHqRespawn(sHqName, true)`) if no respawn state is set yet. Logs debug messages for each step.

**Likely bug**: line 37's failure message reads `Debug.Printf("Failed to find data for HQ " .. sName)` — `sName` is not this function's parameter (which is `sHqName`) and is never assigned anywhere in this file, so it's an always-`nil` global. The log line will print `"Failed to find data for HQ nil"` regardless of which HQ actually failed to load.

### `LockHq(sHqName)`
Locks an HQ by setting its lock state to true and refreshing the UI display. Deletes any associated events.

### `LockAllHq()`
Globally locks all HQs that are not already locked.

### `UnlockAllHq()`
Globally unlocks all HQs that were previously globally locked.

### `_CreateDeathEvent(sHqName, uHqGuid)`
Creates a death event for an HQ. Depending on the HQ's configuration, it listens for either object health or object death events.

### `_SetupRespawn(bEnable, sHqName, uHqGuid)`
Sets up respawn behavior for an HQ. If `bEnable` and the HQ object is alive, calls `_CreateDeathEvent`; if `bEnable` and the object is already dead, calls `_OnHqDeath` directly. If not `bEnable` and the object is dead and an event handle exists, deletes it and clears `_tHqEvents[uHqGuid]`.

**Confirmed bug**: line 117 does `_tHqEvents[uHqGuid] = _CreateDeathEvent(sHqName, uHqGuid)`. `_CreateDeathEvent` has no `return` statement in either of its branches — it always implicitly returns `nil`. `_CreateDeathEvent` itself already correctly writes the real `Event.Create(...)` handle into `_tHqEvents[uHqGuid]` internally; `_SetupRespawn` then immediately clobbers that with `nil` by reassigning the call's (nonexistent) return value on top of it. Net effect: after `_SetupRespawn(true, sHqName, uHqGuid)` runs on a live object, `_tHqEvents[uHqGuid]` ends up `nil` even though a live event was registered — meaning `LockHq`'s `if _tHqEvents[sHqName] then Event.Delete(...)` cleanup (and the disable-branch here) can never find that handle to delete it. This looks like a genuine event-handle leak.

### `SetHqRespawn(sHqName, bEnable)`
Enables or disables respawn behavior for an HQ. Updates the HQ's respawn state and sets up or removes the appropriate events based on the new state.

### `_SetHq(sHqName, bEnable)`
Sets the lock state of an HQ and refreshes its UI display.

### `_OnHqDeath(sHqName, uHqGuid, uKilledByTemplate, uCulprit)`
Handles the death event for an HQ. Logs a debug message, clears `_tHqEvents[uHqGuid]`, locks the HQ via `_SetHq(sHqName, false)`. If the culprit isn't `userdata` (i.e. not a raw engine object handle) or is player-controlled, drops relations between the HQ's faction and `"Pmc"` by `-100` via `MrxFactionManager.SetRelation`. Re-fetches the HQ with `GetHq(sHqName)` into a second `local tHq` (shadowing the first, functionally redundant since nothing removed it from `_tHqs` in between) and bails if respawn is disabled; otherwise registers an `Event.ObjectHibernation` listener to revive the HQ later via `_OnHqHibernation`.

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
- **Manage HQs** with `GetHq` / `AddStarter` / `RemoveStarter`, and lock state with `UnlockHq` / `LockHq`
  (or `LockAllHq` / `UnlockAllHq`, which use the per-HQ `bGloballyLocked` flag so a global lock doesn't stomp
  individually-locked HQs). `AddStarter` auto-unlocks the HQ if it doesn't exist yet.
- **Destroying an HQ is a hard `-100` relation hit**: `_OnHqDeath` calls
  `MrxFactionManager.SetRelation(sFaction, "Pmc", -100)` — i.e. it slams that faction to fully hostile — but
  **only if the player caused it** (culprit is player-controlled or not a raw engine handle). That's the
  gameplay lever behind "blow up their HQ, lose all standing."
- **Respawn** is on by default (`UnlockHq` calls `SetHqRespawn(sHqName, true)` when respawn is unset). A
  destroyed HQ with respawn on revives on the next `Event.ObjectHibernation`. Watch out for the
  `_SetupRespawn` handle-clobber bug below if you're debugging why an HQ's death event won't clear.

{: .warning }
> Two confirmed source bugs (see the function notes above): `UnlockHq` logs the undeclared global `sName`
> (always `nil`) on data-load failure, and `_SetupRespawn` overwrites the live death-event handle in
> `_tHqEvents[uHqGuid]` with `nil` (because `_CreateDeathEvent` has no `return`), leaking that handle so
> `LockHq` can't later delete it.