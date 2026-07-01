---
title: VehicleBlippable
parent: Vehicles
grand_parent: Resident Modules
nav_order: 1
inherits: OrientedBlippable
tags: [vehicle, blip]
---

# VehicleBlippable

*Module: vehicleblippable.lua*

## Overview
The `VehicleBlippable` module is responsible for managing radar and off-screen world markers for vehicles. It handles the blip color based on the driver's relation to the PMC faction, ensuring that the vehicle's blip accurately reflects its status (ally, neutral, enemy, empty, or PMC). This module also listens for driver enter/exit events and faction attitude changes to update the blip accordingly.

## Inheritance
- Inherits from: `OrientedBlippable`
- Imports: `MrxUtil`, `MrxFactionManager`

## Instance pattern
This is a per-instance object module (keyed by `uGuid`). It tracks the following key fields:
- `DriverEnter`: Event handle for driver enter events.
- `DriverExit`: Event handle for driver exit events.
- `Attitude`: Event handle for faction attitude change events.
- `tColorAlly`, `tColorNeutral`, `tColorEnemy`, `tColorEmpty`, `tColorPmc`: Color tables for different blip states.

## Functions
### `OnActivate(uGuid, uRuntimeOwner, iArg)`
Called when the vehicle instance is activated. It sets up an event to call `Start` once the object leaves hibernation.

### `Start(uGuid, uRuntimeOwner, iArg)`
Checks if the vehicle is alive and creates a new per-instance table for the vehicle using the module's prototype.

### `Create(oPrototype, uGuid, uRuntimeOwner)`
Creates a new per-instance table for the vehicle. It sets up event listeners for driver enter/exit events and faction attitude changes, and initializes the blip color based on the current state.

### `Delete(self)`
Tears down the per-instance table by clearing any active blips and calling the base class's `Delete`.

### `SetBlipped(oSelf, uVehicle)`
Updates the vehicle's blip color based on the driver's relation to the PMC faction. It also clears the blip if a player is controlling the vehicle.

## Events
- Listens for `Event.ObjectHibernation` to call `Start` when the object leaves hibernation.
- Listens for `Event.ObjectInSeat` (`DriverEnter`, `DriverExit`) to update the blip color on driver changes.
- Listens for faction attitude change events to recolor the blip based on updated relations.

## Notes for modders
- Ensure that `OnActivate` and `OnDeactivate` are called appropriately to manage blip lifecycle.
- Customize blip colors by modifying the `tColorAlly`, `tColorNeutral`, `tColorEnemy`, `tColorEmpty`, and `tColorPmc` fields.
- Be aware that faction attitude changes will automatically recolor the blips, so ensure that these events are properly handled if custom behavior is needed.