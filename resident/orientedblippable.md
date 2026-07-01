---
title: OrientedBlippable
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [blip, radar]
---

# OrientedBlippable

*Module: orientedblippable.lua*

## Overview
The `OrientedBlippable` module extends the functionality of the `Blippable` module by adding support for oriented blips, which rotate based on the object's orientation. It is used for objects that need to be visually represented with a rotating radar objective.

## Inheritance
- Inherits from: `Blippable`
- Imports: `none`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `bRotate`: Indicates whether the blip should rotate.
- `bOriented`: Indicates whether the blip is oriented.
- `TimerEvent`: Handle for the persistent timer event used to flash the blip.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It logs a debug message and sets up an event to call `Awake` once the object leaves hibernation.

### `TimerCallback(oSelf)`
A helper function that adds an objective with flashing enabled. This is called by the persistent timer event.

### `SetBlipped(oSelf)`
Adds a radar objective and marker for the object, setting it as oriented. If flashing is enabled and no timer event is already set, it creates a persistent timer event to flash the blip every 0.05 seconds.

### `ClearBlipped(oSelf)`
Removes the radar objective and marker for the object. It also deletes any associated timer event to stop the flashing.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Uses a persistent timer event (`Event.TimerRelative`) to flash the blip every 0.05 seconds if enabled.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage blip lifecycle.
- Use `SetBlipped` and `ClearBlipped` to control the visibility of radar objectives.
- Customize blip properties by setting fields like `tColor`, `nWidth`, and `sTexture`.
- Be aware that network synchronization (`bNetSync`) may affect multiplayer behavior.