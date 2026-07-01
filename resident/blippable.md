---
title: Blippable
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Inheritable
tags: [blip, radar]
---

# Blippable

*Module: blippable.lua*

## Overview
The `Blippable` module is responsible for adding and removing radar objectives and off-screen world markers for game objects. It provides functionality to set and clear blips, as well as manage their properties such as color, size, and texture.

## Inheritance
- Inherits from: `Inheritable`
- Imports: `MrxUtil`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `bActive`: Indicates whether the blip is currently active.
- `tColor`: The default color of the radar objective.
- `tFlash`: The flash color of the radar objective.
- `nWidth` and `nHeight`: Dimensions of the radar objective.
- `sName`: Name of the radar objective.
- `sTexture`: Texture used for the radar objective.
- `bSticky`: Whether the blip is sticky on the radar.
- `bRotate`: Whether the blip should rotate.
- `bOriented`: Whether the blip is oriented.
- `nSortOrder`: Sort order of the blip.
- `bNetSync`: Whether network synchronization is enabled for the blip.
- `tMarker`: Configuration for the off-screen marker.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the object instance is activated. It logs a debug message and sets up an event to call `Awake` once the object leaves hibernation.

### `Awake(uGuid, iArg)`
Creates a new per-instance table for the object using the module's prototype.

### `Delete(self)`
Tears down the per-instance table by clearing any active blips and calling the base class's `Delete`.

### `SetBlipped(self)`
Adds a radar objective and marker for the object. Sets `bActive` to true.

### `ClearBlipped(self)`
Removes the radar objective and marker for the object. Clears `bActive`.

### `AddObjective(self, bFlash)`
Adds a radar objective and an off-screen world marker for the object. Configures the blip's properties based on the instance's fields and network synchronization settings.

### `RemoveObjective(self)`
Removes the radar objective and marker for the object. Cleans up any associated network events.

## Events
- Listens for `Event.ObjectHibernation` to call `Awake` when the object leaves hibernation.
- Listens for custom event `HideMarker` to remove objectives for hidden objects.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage blip lifecycle.
- Use `SetBlipped` and `ClearBlipped` to control the visibility of radar objectives.
- Customize blip properties by setting fields like `tColor`, `nWidth`, and `sTexture`.
- Be aware that network synchronization (`bNetSync`) may affect multiplayer behavior.