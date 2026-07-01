---
title: EnemyBlippable
parent: Core Engine & Utilities
grand_parent: Resident Modules
nav_order: 1
inherits: Blippable
tags: [enemy, blip]
---

# EnemyBlippable

*Module: enemyblippable.lua*

## Overview
The `EnemyBlippable` module extends the functionality of the `Blippable` module to manage radar objectives and off-screen world markers specifically for enemy vehicles. It determines the blip color based on the relationship between the vehicle's driver and the PMC faction, ensuring that enemy vehicles are clearly marked on the radar.

## Inheritance
- Inherits from: `Blippable`
- Imports: `MrxUtil`, `MrxFactionManager`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `tColor`: The color of the radar objective.
- `bHostile`: Indicates whether the vehicle is hostile to the PMC faction.
- `DriverEnter`: Event handle for when a driver enters the vehicle.
- `DriverExit`: Event handle for when a driver exits the vehicle.
- `Attitude`: Persistent attitude change event handle.

## Functions
### `Create(oPrototype, uGuid, iArg)`
Called when the object instance is activated. It sets up event listeners for driver entry and exit, creates an attitude change event to update blip colors based on faction relations, and initializes the blip color if a driver is present.

### `Delete(self)`
Tears down the per-instance table by deleting any persistent events (`DriverEnter`, `Attitude`, `DriverExit`) and calling the base class's `Delete`.

### `PickColor(self, uGuid)`
Determines the appropriate blip color based on the relationship between the vehicle's driver and the PMC faction. It updates the blip color and marker color accordingly. If the vehicle is controlled by a player or has no driver, it clears the blip.

## Events
- Listens for `Event.ObjectInSeat` to call `PickColor` when a driver enters or exits the vehicle.
- Listens for custom event `HideMarker` to remove objectives for hidden objects.
- Listens for persistent attitude change events to update blip colors based on faction relations.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage blip lifecycle.
- Customize blip properties by setting fields like `tColor`.
- Be aware that network synchronization (`bNetSync`) may affect multiplayer behavior.
- The module uses predefined color tables (`tColorAlly`, `tColorNeutral`, `tColorEnemy`, `tColorEmpty`, `tColorPmc`) to determine blip colors based on faction relations.