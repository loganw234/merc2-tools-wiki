---
title: Init
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: none
tags: [init, sound]
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
- Listens for `Event.TimerRelative` to trigger a sound cue after 1 second of activation.
- Listens for `OnActivate` to start the material animation and set up the timer event.
- Listens for `OnDeactivate` to stop the material animation, stop the sound, delete the timer event, and clean up the `tEvents` table entry.

## Notes for modders
- Ensure that `Init()` is called once during module initialization to set up the global `tEvents` table.
- Use `OnActivate` and `OnDeactivate` appropriately to manage the lifecycle of the material animation and sound cue.
- Be aware that the timer event (`Event.TimerRelative`) is used to delay the sound cue, so modifying this timing may affect gameplay behavior.