---
title: ProximityMine
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mine, proximity]
verified: true
verified_note: corrects the Instance pattern section -- confirmed via source as a bare module-level uEvent[uGuid] bookkeeping table (no Create/setmetatable/tInstance factory), not the Inheritable rich-instance pattern
---

# ProximityMine

*Module: proximitymine.lua*

## Overview
The `ProximityMine` module is responsible for handling the behavior of proximity mines in the game. When a human player enters a 6-meter radius around the mine, it triggers an event that removes the mine and spawns upward-firing ordnance (`Grenade MG Projectile`) at the mine's location.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `none`

## Instance pattern
**Not the `Inheritable`/rich-instance pattern, and not a class-factory either** — confirmed from source: a
plain module-level table, `uEvent[uGuid]`, set up once via `Init()` alongside a single shared `uFilter`
(both true singleton/module-level fields, not per-instance), with no `Create`/`setmetatable`/rich-instance
factory anywhere. Each activated mine gets one event handle entry in `uEvent`, not a full instance object
with inherited methods. It tracks the following key fields:
- `uEvent`: A table to store event handles for each instance.
- `uFilter`: A single shared object filter used to detect human players, set up once in `Init()` — not per-instance.

## Functions
### `Init()`
Initializes the module by creating an event handle table and setting up an object filter to detect humans.

### `Deinit()`
Cleans up the module by clearing the event handle table and object filter.

### `OnActivate(uGuid, nArg)`
Called when the proximity mine instance is activated. It sets up a proximity event that triggers when a human player enters a 6-meter radius around the mine.

### `OnDeactivate(uGuid)`
Called when the proximity mine instance is deactivated. It deletes the associated proximity event and clears its handle.

### `Triggered(uGuid, tListOfObjects)`
A callback function triggered when the proximity event detects a human player within range. It schedules a timer to call the `Popup` function after a short delay (0.001 seconds).

### `Popup(uGuid)`
Removes the proximity mine instance and spawns upward-firing ordnance (`Grenade MG Projectile`) at the mine's location.

## Events
- Listens for `Event.ObjectProximity` to detect when a human player enters a 6-meter radius around the mine.
- Listens for `Event.TimerRelative` to schedule the `Popup` function after a short delay.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage the proximity mine's lifecycle.
- Customize the trigger radius or ordnance behavior by modifying the code in the `Triggered` and `Popup` functions.
- Be aware of the network synchronization settings if using this module in multiplayer scenarios.