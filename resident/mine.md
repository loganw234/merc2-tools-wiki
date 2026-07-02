---
title: Mine
parent: World Objects & Props
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [mine, proximity]
---

# Mine

*Module: mine.lua*

## Overview
The `Mine` module represents a mine object in the game. It handles the activation, deactivation, and explosion of mines. When activated, it plays an animation and sets up a proximity trigger for human targets. Upon death, it schedules an explosion with different delays based on whether the target is human or a vehicle.

## Inheritance
- Inherits from: none — base/utility module
- Imports: `none`

## Instance pattern
This module does not follow the per-instance object pattern (keyed by `uGuid`). It manages global state for mine objects, such as event handlers and filters.

## Functions
### `Init()`
Initializes global variables and sets up object filters for human and vehicle targets. This function is called once when the module is loaded.

### `Deinit()`
Cleans up global variables by setting them to `nil`. This function is called when the module is unloaded.

### `OnActivate(uGuid, uOwner, nArg)`
Called when a mine object is activated. It plays an animation and sets up a proximity trigger if `nArg` is 2 (indicating a human-proximity kill mine).

### `OnDeactivate(uGuid, nArg)`
Called when a mine object is deactivated. It stops the animation and deletes the associated event handler.

### `OnDeath(uGuid)`
Called when a mine object dies. It plays a sound cue and schedules an explosion with different delays based on whether the target is human or a vehicle.

### `Explode(uGuid, x, y, z, sType)`
Handles the explosion of the mine. It stops the sound cue and spawns the appropriate explosion type based on the target type (`human`, `veh`, or other).

## Events
- Listens for `Event.ObjectProximity` to trigger a human-proximity kill.
- Listens for `Event.TimerRelative` to schedule the explosion after death.

## Notes for modders
- Ensure that `Init` and `Deinit` are called appropriately to manage global state.
- Use `OnActivate`, `OnDeactivate`, and `OnDeath` to control the lifecycle of mine objects.
- Customize the proximity trigger radius and explosion delays by modifying the corresponding constants in the module.
- Be aware that network synchronization may affect multiplayer behavior.