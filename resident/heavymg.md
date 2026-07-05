---
title: Heavymg
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [weapon, event]
verified: true
verified_note: all functions and the single Event.WeaponEvent call confirmed against 17-line source; tEvents table added to Instance pattern description; page was already largely accurate
---

# Heavymg

*Module: heavymg.lua*

## Overview
The `Heavymg` module is responsible for handling the removal of heavy machine gun (HMG) objects when they are dropped by a human player. It listens for specific weapon events and triggers the appropriate actions to despawn the HMG.

## Inheritance
- Inherits from: `none — base/utility module`
- Imports: `MrxUtil`

## Instance pattern
Not a per-`uGuid` object pattern — no `OnActivate`/`Awake`/`Create`/`setmetatable`/`tInstance` registry.
It's a stateless-object utility module with one shared table, `tEvents` (`tEvents = tEvents or {}`, guarding
against re-initialization), keyed by `uGuid` to hold each HMG's single event handle. `import("MrxUtil")` is
present but unused by any function in this file.

## Functions
### `OnActivate(uGuid, iArg)`
Called when the HMG object instance is activated (engine world-object lifecycle hook, not a per-instance
`Create`). Registers `tEvents[uGuid]` as an `Event.Create(Event.WeaponEvent, {"Human", "Drop", uGuid}, ...)`
listener, with `Object.Remove` as the callback and `{uGuid}` as its argument — so dropping the weapon as a
human directly removes the object.

### `OnDeactivate(uGuid)`
Called when the HMG object instance is deactivated. Deletes `tEvents[uGuid]` if set. Does not clear the
table entry afterward (leaves a stale/deleted event handle in `tEvents[uGuid]` rather than setting it to
`nil`).

## Events
- `Event.WeaponEvent` — the only `Event.*` reference in this file. Filtered on `{"Human", "Drop", uGuid}`;
  fires `Object.Remove(uGuid)` directly as the callback (no intermediate handler function in this file).

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the lifecycle of the event listener.
- This module does not have any public API functions other than the two engine lifecycle hooks.
- `OnDeactivate` does not null out `tEvents[uGuid]` after deleting the event — harmless in practice since
  `OnActivate` always overwrites it on the next activation, but worth knowing if you're auditing for leaks.