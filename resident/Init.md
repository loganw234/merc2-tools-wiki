---
title: Init
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [init, sound]
verified: true
verified_note: corrected Events section — OnActivate/OnDeactivate are lifecycle callbacks, not Event.* subscriptions; only Event.TimerRelative is a real event reference in this file
---

# Init

*Module: Init.lua*

## Overview
The `Init` module is responsible for initializing a global table to manage events and handling the activation and deactivation of world objects. It specifically manages a timer that triggers a sound cue when an object is activated.

## Inheritance
- Inherits from: none — base/utility module
- Imports: none

## Instance pattern
This is a stateless manager/utility module. It does not track any per-instance state but uses a global table `tEvents` to manage event handles associated with world objects.

## Functions
### `Init()`
Initializes the global `tEvents` table if it hasn't been initialized yet. This function ensures that there's a table available to store event handles for different world object instances.

### `OnActivate(uGuid, args)`
Called when a world object instance is activated. It plays a material animation on the object and sets up a timer event that triggers a sound cue after 1 second.

### `OnDeactivate(uGuid, args)`
Called when a world object instance is deactivated. It stops the material animation playing on the object, stops any associated sound, deletes the timer event, and clears the entry in the `tEvents` table for this object.

## Events
- Fires `Event.TimerRelative` (in `OnActivate`) to schedule `Sound.CueSound` one second after activation.
- `OnActivate` and `OnDeactivate` are engine-invoked lifecycle callbacks, not `Event.*` subscriptions —
  they are the entry/exit points the engine calls directly on world-object activate/deactivate, not
  something this module registers via `Event.Create`.

## Notes for modders
- Ensure that `Init()` is called once during module initialization to set up the global `tEvents` table.
- Use `OnActivate` and `OnDeactivate` appropriately to manage the lifecycle of the material animation and sound cue.
- Be aware that the timer event (`Event.TimerRelative`) is used to delay the sound cue, so modifying this timing may affect gameplay behavior.